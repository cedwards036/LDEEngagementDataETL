declare
    @EISDegreeLevelID INT = 838,
    @JHEDID INT = 463;

with URM as (
    select distinct HopkinsId,
                    MAX(case
                            when p.IsInternational = 'Y' and c.IsPermanentUSResident = 'N' then 'Unknown or N/A'
                            else
                                (case
                                     when eth.EthnicityType = 'Hispanic' then 'URM'
                                     when eth.EthnicityType = 'NonHispanic' or eth.EthnicityType is null then
                                         (case
                                              when race.RaceType in ('White', 'Asian', 'Caucasian', 'Asian American')
                                                  then 'Not URM'
                                              when race.RaceType in ('Unknown', 'Other') or race.RaceType is null
                                                  then 'Unknown or N/A'
                                              else 'URM'
                                             end)
                                     else 'Unknown or N/A'
                                    end)
                        end) as URMStatus
    from CMN_Persons p
             left join CMN_PersonsCitizenshipInfo c on p.CMN_PersonsID = c.CMN_PersonsID
             left join CMN_PersonsEthnicity eth on eth.CMN_PersonsID = p.CMN_PersonsID
             left join CMN_PersonsRace race on race.CMN_PersonsID = p.CMN_PersonsID
    group by HopkinsId
),
     Students as (
         select distinct s.CMN_PersonsID,
                         s.CMN_StudentsID,
                         t.StartDate as StudentStartDate
         from CMN_Students s
                  left join CMN_Terms t on t.CMN_TermsID = s.CMN_TermsID
     ),
     Enrollments as (
         select distinct se.CMN_PersonsID,
                         se.CMN_TermsID as EnrollmentTermID,
                         et.StartDate   as EnrollmentTermStartDate
         from SSS_StudentEnrollments se
                  left join CMN_Terms et on et.CMN_TermsID = se.CMN_TermsID
                  left join CMN_Persons p on p.CMN_PersonsID = se.CMN_PersonsID
         where se.IsConfirmed = 'Y'
           and et.Name not like '%intersession%'
     ),
     TermCounts as (
         select s.CMN_StudentsID,
                COUNT(distinct e.EnrollmentTermID) as EnrolledTermCount
         from Students s
                  left join Enrollments e
                            on (e.CMN_PersonsID = s.CMN_PersonsID) and (e.EnrollmentTermStartDate >= s.StudentStartDate)
                  left join SSS_StudentsInstance si on si.CMN_StudentsID = s.CMN_StudentsID
         where EnrollmentTermID is not null
           and si.IsPrimary = 'Y'
         group by s.CMN_StudentsID
     )


select distinct p.HopkinsId,
                CMN_PersonsMisc.AttributeValue  AS jhed,
                s.CMN_StudentsID,
                (case
                     when p.IsInternational = 'Y' and c.IsPermanentUSResident = 'N' then 'Not U.S. Citizen'
                     else 'U.S. Citizen or Permanant Resident'
                    end)                        as Citizenship,
                URM.URMStatus,
                p.Gender,
                (case
                     when s.TypeName = 'PTE' then 'EP'
                     when s.TypeName = 'ASEN - Grad' then 'Full-Time'
                    end)                        as StudentType,
                ssp.DegreeName,
                ssp.MajorName,
                (case
                     when sim.AttributeValue = '65-Post-Masters Certificate' then 'Post-Masters Certificate'
                     when sim.AttributeValue = '50-Post-baccalaureate certificate' then 'Post-Baccalaureate Certificate'
                     when sim.AttributeValue = '60-Masters' then 'Masters'
                    end)                        as EducationLevel,
                s.TypeName                      as SISTypeName,
                s.SubTypeName                   as SISSubTypeName,
                ssp.AcademicProgramName         as SISAcademicProgramName,
                stat.Name                       as SISStatusName,
                ISNULL(tc.EnrolledTermCount, 0) as EnrolledTermCount
from CMN_Persons p
         left join SSS_StudentsInstance si on si.CMN_PersonsID = p.CMN_PersonsID
         left join CMN_PersonsCitizenshipInfo c on p.CMN_PersonsID = c.CMN_PersonsID
         left join URM on URM.HopkinsId = p.HopkinsId
         left join CMN_Students s on s.CMN_StudentsID = si.CMN_StudentsID
         left join SSS_StudentStudyPrograms ssp on ssp.SSS_StudentsInstanceID = si.SSS_StudentsInstanceID
         left join SSS_StudentsInstanceMisc sim ON sim.SSS_StudentsInstanceID = si.SSS_StudentsInstanceID
    and sim.SYS_MiscInfoTablesDetailsID = @EISDegreeLevelID
         left join CMN_StudInstanceStatuses sis on sis.CMN_StudentsID = si.CMN_StudentsID
         left join CMN_Statuses stat on stat.CMN_StatusesID = sis.CMN_StatusesID
         left join TermCounts tc on tc.CMN_StudentsID = si.CMN_StudentsID
         left join CMN_PersonsMisc
                   on CMN_PersonsMisc.CMN_PersonsID = SI.CMN_PersonsID
                       and CMN_PersonsMisc.SYS_MiscInfoTablesDetailsID = @JHEDID
         inner join JHU_SSS_SIStoHandShakeStaging hs on hs.Identifier1 = p.Identifier1
where (s.TypeName = 'PTE' or (s.TypeName = 'ASEN - Grad' and ssp.AcademicProgramName like 'EN %'))
  and s.SubTypeName not like '%Non-Degree%'
  and ssp.MajorStatusName = 'Active'
  and ssp.IsPrimary = 'Y'
  and si.IsPrimary = 'Y'
  and not sim.AttributeValue = '81-Doctorate (research and scholarship)'
  and sis.IsCurrent = 'Y'
  and stat.Name in
      ('GR Non-Resident', 'PE Special Student', 'Current', 'GR New Instance', 'PE Admit Full', 'GR Current',
       'Leave of Absence',
       'GR Leave of Absence', 'GR No Reg-Reason', 'PE Admit Provisional', 'PE Admit Conditional')
order by HopkinsId

select distinct p.Identifier1 as hopkins_id,
                'minor'       as wgs_affiliation_type
from SSS_StudentMinors m
         join SSS_StudentStudyPrograms ssp on ssp.SSS_StudentStudyProgramsID = m.SSS_StudentStudyProgramsID
         join SSS_StudentsInstance si on ssp.SSS_StudentsInstanceID = si.SSS_StudentsInstanceID
         join CMN_Students s on s.CMN_StudentsID = si.CMN_StudentsID
         join CMN_Persons p on p.CMN_PersonsID = si.CMN_PersonsID
where MinorName = 'Studies of Women, Gender & Sexuality'
  and MinorStatusName = 'Active'
declare
@term varchar(63) = 'Spring 2021';

with minor_students as (
    select distinct p.Identifier1 as hopkins_id,
                    'minor'       as wgs_affiliation_type
    from SSS_StudentMinors m
             join SSS_StudentStudyPrograms ssp on ssp.SSS_StudentStudyProgramsID = m.SSS_StudentStudyProgramsID
             join SSS_StudentsInstance si on ssp.SSS_StudentsInstanceID = si.SSS_StudentsInstanceID
             join CMN_Students s on s.CMN_StudentsID = si.CMN_StudentsID
             join CMN_Persons p on p.CMN_PersonsID = si.CMN_PersonsID
    where MinorName = 'Studies of Women, Gender & Sexuality'
      and MinorStatusName = 'Active'
)

select p.Identifier1 as hopkins_id,
       'enrollment'  as wgs_affiliation_type
from SSS_StudentEnrollments se
         join SSS_CourseDepartments cd on cd.SSS_CourseCatalogID = se.SSS_CourseCatalogID
         join CMN_Departments d on d.CMN_DepartmentsID = cd.CMN_DepartmentsID
         join CMN_Persons p on p.CMN_PersonsID = se.CMN_PersonsID
         join CMN_Terms t on t.CMN_TermsID = se.CMN_TermsID
         left join minor_students ms on ms.hopkins_id = p.Identifier1
where t.WebName = @term
  and d.Name = 'AS Study of Women, Gender, & Sexuality'
  and se.IsConfirmed = 'Y'
  and se.IsWaitListed = 'N'
  and ms.wgs_affiliation_type is null --if a student is in the minor, that takes precedence as the affiliation type
union
select *
from minor_students
order by hopkins_id
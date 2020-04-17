select
	CMN_PersonsID as cmn_persons_id,
	handshake.Identifier1 as hopkins_id,
	email_address,
	substring(auth_identifier, 0, (patindex('%@johnshopkins.edu', auth_identifier))) AS jhed,
	(case when preferred_name = '' THEN handshake.first_name else preferred_name end) as first_name,
	handshake.first_name as legal_first_name,
	preferred_name,
	middle_name,
	last_name,
	school_year_name as school_year,
	ethnicity,
	(case
		when ethnicity = 'White/Caucasian' then 'FALSE'
		when ethnicity = 'Asian/Asian American' then 'FALSE'
		when ethnicity = '' then ''
		else 'TRUE'
	end) as 'is_urm',
	[primary_education:major_names] as majors,
	[primary_education:college_name] as primary_college,
	[primary_education:start_date] as education_start_date,
	[primary_education:end_date] as education_end_date,
	work_authorization_name as visa_status,
	(case
		when work_authorization_name = 'U.S. Citizen' then 'U.S. Citizen or Permanant Resident'
		when work_authorization_name = 'Permanent U.S. Resident' then 'U.S. Citizen or Permanant Resident'
		when work_authorization_name = '' then ''
		else 'Not U.S. Citizen'
	end) as citizenship,
	gender,
	home_location,
	system_label_names as system_labels,
	athlete as is_athlete,
	first_generation as is_first_generation,
	veteran as is_veteran,
	work_study_eligible,
	pell.is_pell_eligible
from JHU_SSS_SIStoHandShakeStaging as handshake

--add pell proxy data
left join (
	select
		p.Identifier1,
		(case when attribute_value = 'Y' then 'TRUE' else 'FALSE' end) as is_pell_eligible
	from JHU_SSS_ASEN_Starfish_UserAttributes s
	left join cmn_persons p on s.user_integration_id = p.Identifier1
	where attribute_key = 'IS_PELL_ELIGIBLE'
) as pell on pell.Identifier1 = handshake.Identifier1

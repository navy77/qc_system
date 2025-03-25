# mssql 
database = qc_system
table = qc_data
#script 
CREATE TABLE qc_data (
    register datetime,
    occurred datetime,
    spec_id varchar(50),
    part_no varchar(20),
    job_tag varchar(20),
    process varchar(20),
    rev varchar(3),
    item_no varchar(3),
    item_check varchar(10),
    spec_nominal float,
    tolerance_max float,
    tolerance_min float,
    emp_id varchar(20),
    equipment_no varchar(20)
);

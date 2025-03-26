# mssql 
database = qc_system
table = qc_data
#script 
CREATE TABLE measure_tb (
    register datetime,
    occurred datetime,
    spec_id varchar(30),
    part_no varchar(30),
    rev varchar(3),
    process varchar(10),
    item_no varchar(3),
    item_name varchar(10),
    spec_nominal float,
    tolerance_max float,
    tolerance_min float,
    value float,
    job_id varchar(50),
    emp_id varchar(20),
    equipment_no varchar(20)
);


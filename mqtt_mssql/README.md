pip install -r requirements.txt

# mssql 
database = qc_system
table = master_spec
#script 
CREATE TABLE master_spec (
    spec_id varchar(10),
    part_no varchar(10),
    rev int,
    process varchar(10),
    item_no int,
    item_check varchar(10),
    spec_nominal float,
    tolerance_max float,
    tolerance_min float,
    method int,
    point int,
    register datatime
);

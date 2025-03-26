pip install -r requirements.txt

# mssql 
database = qc_system
table = master_spec
#script 
CREATE TABLE master_spec (
    spec_id varchar(30),
    part_no varchar(30),
    rev varchar(3),
    process varchar(10),
    item_no varchar(3),
    item_check varchar(10),
    spec_nominal float,
    tolerance_max float,
    tolerance_min float,
    method int,
    point int,
    register datetime
    PRIMARY KEY (spec_id)
);

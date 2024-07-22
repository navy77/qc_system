pip install -r requirements.txt

# mssql 
database = qc_demo
table = spec_tb
#script 
CREATE TABLE spec_tb (
    spec_id varchar(10),
    spec_name varchar(50),
    point int,
    method int,
    spec float,
	spec_min float,
	spec_max float,
);

# mssql 
## create measure_tb
create table measure_tb (
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
## create master_spec_tb
create table master_spec_tb (
    spec_id varchar(30),
    part_no varchar(30),
    rev varchar(3),
    process varchar(10),
    item_no varchar(3),
    item_name varchar(10),
    spec_nominal float,
    tolerance_max float,
    tolerance_min float,
    method int,
    point int,
    register datetime
    PRIMARY KEY (spec_id)
);
## create measure_log_tb
create table measure_log_tb (
	registered datetime,
	status varchar(50),
	process varchar(50),
	message varchar(MAX),
	error varchar(MAX)
);

## mqtt request
{ "spec_id":"AAA_GD_1_1" }
## mqtt return
[
  {
    "spec_id": "AAA_GD_1_1",
    "part_no": "AAA",
    "rev": "1",
    "process": "GD",
    "item_no": "1",
    "item_name": "RWD",
    "spec_nominal": 0,
    "tolerance_max": 0.005,
    "tolerance_min": -0.005,
    "method": 1,
    "point": 1
  }
]
## mqtt publish
  {
    "spec_id": "AAA_GD_1_1",
    "part_no": "AAA",
    "rev": "1",
    "process": "GD",
    "item_no": "1",
    "item_name": "RWD",
    "spec_nominal": 0,
    "tolerance_max": 0.005,
    "tolerance_min": -0.005,
    "method":1,
    "point":1,
    "raw_value": [0.001],
    "value":0.001,
    "value_min": 0.001,
    "value_max": 0.001,
    "job_id":"job-001",
    "emp_id":"abcd",
    "equipment_no":"eq01"
  }

  ## script run
version 1.0.0
docker compose build --no-cache
docker compose up -d
IF DB_ID('qc_system') IS NULL
	CREATE DATABASE qc_system;
GO

USE qc_system;
GO
# create table master spec
CREATE TABLE master_spec (
	spec_id VARCHAR(50) PRIMARY KEY, 
	part_no VARCHAR(50),    
    rev INT,
	process VARCHAR(50),   
	item_no INT,
	item_check VARCHAR(100),
	spec_nominal DECIMAL(10, 3),
	tolerance_max DECIMAL(10, 3),
	tolerance_min DECIMAL(10, 3),
	method INT,
	point INT,                
	register DATETIME
);
# create table data
CREATE TABLE data (
	spec_id VARCHAR(50), 
	part_no VARCHAR(50),    
	job_tag VARCHAR(50),
	process VARCHAR(50),   
	item_no INT,
	item_check VARCHAR(100),
	equipment_no VARCHAR(10),
	emp_id VARCHAR(10),
	spec_nominal DECIMAL(10, 3),
	tolerance_max DECIMAL(10, 3),
	tolerance_min DECIMAL(10, 3),
    judge VARCHAR(2),
	fnl_data DECIMAL(10, 3),
	time DATETIME
);

CREATE TABLE log_data (
	registered_at DATETIME,
	status VARCHAR(50),
	process VARCHAR(50),
	message VARCHAR(MAX),
	error VARCHAR(MAX)
)


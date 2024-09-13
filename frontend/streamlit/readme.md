IF DB_ID('qc_system') IS NULL
	CREATE DATABASE qc_system;
GO

USE qc_system;
GO

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

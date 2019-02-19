CREATE DATABASE indeed;

USE indeed
go

CREATE TABLE companies(
	cmp_Name varchar(50) PRIMARY KEY,
	cmp_Industry varchar(50),
	cmp_Sector varchar(50),
	cmp_Headquarters varchar(50),
	cmp_Founded int,
	cmp_Notes varchar(60)
);

CREATE TABLE scores(
	scr_Company varchar(50) FOREIGN KEY REFERENCES companies(cmp_Name),
	scr_Date date,
	scr_Culture decimal(10,1),
	scr_JobSecurityAndAdvancement decimal(10,1), 
	scr_Management decimal(10,1),
	scr_PayAndBenefits decimal(10,1),
	scr_WorkLifeBalance decimal(10,1),
	scr_Overall decimal(10,1),
	scr_JobCount int,
	scr_ReviewCount int,
	scr_SalaryCount int
);

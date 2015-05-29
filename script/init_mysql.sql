#create database smweb and user;
CREATE DATABASE IF NOT EXISTS 'smweb' DEFAULT CHARACTER SET `utf8` COLLATE `utf8_unicode_ci`;
GRANT ALL PRIVILEGES ON smweb.* TO sysops@'192.168.%' IDENTIFIED BY '123456' with grant option;

#create Rackinfo table;
set names 'utf8';
CREATE TABLE Rackinfo(
id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
ip VARCHAR(16) NOT NULL,
hostname VARCHAR(40) NOT NULL,
system VARCHAR(20) NOT NULL,
cpu VARCHAR(20) NOT NULL,
cpu_num INT NOT NULL,
memory VARCHAR(20) NOT NULL,
idrac_ip VARCHAR(16) NOT NULL,
project VARCHAR(20) NOT NULL,
rack VARCHAR(16) NOT NULL);

#create Userinfo table;
set names 'utf8';
CREATE TABLE Userinfo(
id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
Email VARCHAR(50) NOT NULL,
password VARCHAR(50) NOT NULL,
remarks VARCHAR(20),
name varchar(20));


#create Deployinfo table;
set names 'utf8';
CREATE TABLE Deployinfo(
id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
item VARCHAR(30) NOT NULL,
hostname VARCHAR(50) NOT NULL,
ipaddress VARCHAR(50) NOT NULL,
s_dir VARCHAR(100) NOT NULL,
d_dir VARCHAR(100) NOT NULL,
execlude VARCHAR(150));

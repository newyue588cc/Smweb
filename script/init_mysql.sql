#create database sysops and user;
CREATE DATABASE IF NOT EXISTS 'sysops' DEFAULT CHARACTER SET `utf8` COLLATE `utf8_unicode_ci`;
GRANT ALL PRIVILEGES ON sysops.* TO sysops@'10.40.%' IDENTIFIED BY '071013071083' with grant option;

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

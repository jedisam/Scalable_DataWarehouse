-- create database if not exists traffic_db;
-- use traffic_db;

create table if not exists vehicles
(
track_id int primary key,
vehicle_type varchar(500) NOT null,
traveled_d varchar(500) NOT null,
avg_speed float NOT null,
lat float NOT null,
lon float NOT null,
speed float NOT null,
loan_acc float NOT null,
lat_acc float NOT null,
record_time date NOT null
);
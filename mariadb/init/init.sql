CREATE DATABASE IF NOT EXISTS legrow;


CREATE TABLE IF NOT EXISTS legrow.data
(
	id int auto_increment,
	date timestamp default CURRENT_TIMESTAMP() not null,
	moist_data int null,
	temp_data float null,
	constraint data2_pk
		primary key (id)
);

SHOW WARNINGS;

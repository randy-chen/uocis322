
/*  Need more comments about the tables
*/

/*  Added a numeric primary key as usernames can have a mix of letters and numbers, 
	so having them as primary keys would make keeping track of the users more difficult. 
	The numeric pk helps us organize the users better. Both the username and password
	fields have a maximum length of 16 characters, which is in accordance with the specs. 
*/
CREATE TABLE users (
	user_pk         serial primary key,
	username        varchar(16), 
	password        varchar(16),
	role            text
);

CREATE TABLE assets (
	asset_pk         serial primary key,
	asset_tag        varchar(16),
	description      text,
	status           text
);

CREATE TABLE facilities (
	facility_pk      serial primary key,
	fcode            varchar(6),
	common_name      varchar(32),
	location         text
);

CREATE TABLE asset_history (
	asset_fk         integer references assets(asset_pk) not null,
	facility_fk      integer references facilities(facility_pk),
	arrive_dt        timestamp, 
	depart_dt        timestamp
);

/* The tables created by the statements below will be used for a future assignment. */
CREATE TABLE in_transit ();

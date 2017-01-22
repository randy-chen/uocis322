

CREATE TABLE products (
	product_pk       serial primary key,
	vendor           text,
	description      text,
	alt_description  text
);

CREATE TABLE assets (
	asset_pk         serial primary key,
	product_fk       integer references products(product_pk),
	asset_tag        text,
	description      text,
	alt_description  text
);

CREATE TABLE vehicles (
	vehicle_pk       serial primary key,
	asset_fk         integer references assets(asset_pk) not null
);

CREATE TABLE facilities (
	facility_pk      serial primary key,
	fcode            text,
	common_name      text,
	location         text
);

CREATE TABLE asset_at (
	asset_fk         integer references assets(asset_pk) not null,
	facility_fk      integer references facilities(facility_pk) not null,
	arrive_dt        timestamp, 
	depart_dt        timestamp
);

CREATE TABLE convoys (
	convoy_pk        serial primary key,
	request          text,
	source_fk        integer not null,
	dest_fk          integer not null,
	arrive_dt        timestamp, 
	depart_dt        timestamp	
);

CREATE TABLE used_by (
	vehicle_fk       integer not null,
	convoy_fk        integer not null
);

CREATE TABLE asset_on (
	asset_fk         integer not null,
	convoy_fk        integer not null,
	asset_tag        text,
	load_dt          timestamp, 
	unload_dt        timestamp	
);



CREATE TABLE users (
	user_pk         serial primary key,
	username        text,
	active          boolean
);

CREATE TABLE roles (
	role_pk        serial primary key,
	title          text
);

CREATE TABLE user_is (
	user_fk         integer references users(user_pk) not null,
	role_fk         integer references roles(role_pk) not null
);

CREATE TABLE user_supports (
	user_fk         integer not null,
	facility_fk     integer not null
);




CREATE TABLE levels (
	level_pk         serial primary key,
	abbrv            text,
	comment          text
);

CREATE TABLE compartments (
	compartment_pk   serial primary key,
	abbrv            text,
	comment          text
);

CREATE TABLE security_tags (
	tag_pk           serial primary key,
	level_fk         integer not null,
	compartment_fk   integer not null,
	user_fk          integer,
	product_fk       integer,
	asset_fk         integer
);


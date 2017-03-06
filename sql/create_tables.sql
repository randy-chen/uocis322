
/*  Since there aren't that many roles, they can be easilty kept track of as part of the users table.
	also makes role selection when creating a new user easier to implement.
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
	role            text,
	active			boolean
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
/* Really, this table is more like 'asset history'. It keeps track of where an asset has been as well
   when it arrived and was disposed. This table allows us to map assets to facilities with foreign keys.
*/
CREATE TABLE asset_at (
	asset_fk         integer references assets(asset_pk),
	facility_fk      integer references facilities(facility_pk),
	arrival          timestamp, 
	disposal         timestamp
);

/* I decided to use one big table to handle all the information of a transfer request and 
   times in transit and the load times and unload times. It seemed unnecessary to have 
   separate tables keep track of an asset in motion and the requests behind putting that 
   asset in motion.	This way all information is easily visible in one table, letting 
   the user track transfer requests as well as transit.
 */
CREATE TABLE transfers (
	req_id           serial primary key,
	requester        varchar(16),
	tf_asset         varchar(16),
	req_dt           timestamp,
	src_fac          varchar(6),
	load_dt          timestamp,
	tf_status        text,
	des_fac          varchar(6),
	unload_dt        timestamp,
	approver         varchar(16),
	aprv_dt          timestamp
);

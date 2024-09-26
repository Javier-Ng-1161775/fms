-- Can drop the schema in PythonAnywhere SQL, but can't recreate it (have to use Databases page).
-- Instead, this query drops the tables and then recreates and populates them.

DROP TABLE IF EXISTS stock;
DROP TABLE IF EXISTS mobs;
DROP TABLE IF EXISTS paddocks;

CREATE TABLE paddocks (
	id int NOT NULL AUTO_INCREMENT,
	name varchar(50) NOT NULL,
	area float(2) not null,
    dm_per_ha float(2) not null,
	total_dm float(2) default null,
	PRIMARY KEY (id)
);

INSERT INTO paddocks VALUES
	(1, "Stream 1", 1.22, 1500, 1.22*1500),
	(4, "Rear 1", 1.23, 2300, 1.23*2300),
	(2, "Rear 2", 1.15, 1900, 1.15*1900),
	(12, "Barn", 0.95, 1750, 0.95*1750)
; 

CREATE TABLE mobs (
	id int NOT NULL AUTO_INCREMENT,
	name varchar(50) DEFAULT NULL,
	paddock_id int not null,
	PRIMARY KEY (id),
    UNIQUE INDEX paddock_idx (paddock_id),	-- Ensures that paddock_id is unique
	CONSTRAINT fk_paddock
		FOREIGN KEY (paddock_id)
		REFERENCES paddocks(id)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
);

INSERT INTO mobs VALUES
	(1,"Mob 1", 4),
	(7,"Mob 2", 1),
	(2,"Mob 3", 2)
; 

CREATE TABLE stock (
	id int NOT NULL AUTO_INCREMENT,
    mob_id int default null,
	dob date NOT NULL,
	weight float(2) not null,
	PRIMARY KEY (id),
	CONSTRAINT fk_mob
		FOREIGN KEY (mob_id)
		REFERENCES mobs(id)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
	);

INSERT INTO stock VALUES
	(1001, 1, '2022-07-25', 586.3),
	(1002, 2, '2023-08-22', 311.2),
	(1003, 7, '2023-09-17', 293),
	(1004, 1, '2022-08-16', 570.9),
	(1005, 2, '2023-11-01', 261.5),
	(1006, 7, '2023-09-26', 286.7),
	(1007, 1, '2022-08-24', 565.3),
	(1008, 7, '2023-09-03', 302.8),
	(1009, 7, '2023-09-24', 288.1),
	(1010, 1, '2022-09-09', 554.1),
	(1011, 2, '2023-08-07', 321.7),
	(1012, 2, '2023-08-13', 317.5),
	(1013, 1, '2022-09-14', 550.6),
	(1014, 7, '2023-09-20', 290.9),
	(1015, 7, '2023-09-10', 297.9),
	(1016, 1, '2022-10-30', 518.4),
	(1017, 2, '2023-07-16', 337.1),
	(1018, 2, '2023-07-15', 337.8),
	(1019, 7, '2023-10-06', 279.7),
	(1020, 1, '2022-08-27', 563.2),
	(1021, 7, '2023-09-10', 297.9),
	(1022, 1, '2022-09-30', 539.4),
	(1023, 2, '2023-07-15', 337.8),
	(1024, 1, '2022-08-24', 565.3),
	(1025, 1, '2022-09-03', 558.3),
	(1026, 7, '2023-09-24', 288.1);
    
    
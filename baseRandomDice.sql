--
-- Fichier généré par SQLiteStudio v3.2.1 sur lun. nov. 16 11:16:33 2020
--
-- Encodage texte utilisé : System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table : dice
DROP TABLE IF EXISTS dice;
CREATE TABLE dice (
	dice_id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	value INTEGER NOT NULL, 
	owner VARCHAR(50) NOT NULL, 
	date_created DATETIME, 
	PRIMARY KEY (dice_id)
);
INSERT INTO dice (dice_id, name, value, owner, date_created) VALUES (1, '1er dé olivier', 2, 'olivier', '2020-11-15 12:11:23.767189');
INSERT INTO dice (dice_id, name, value, owner, date_created) VALUES (2, '2eme dé olivier', 3, 'olivier', '2020-11-15 12:11:47.886569');
INSERT INTO dice (dice_id, name, value, owner, date_created) VALUES (3, '3eme dé olivier', 5, 'olivier', '2020-11-15 12:11:52.765848');
INSERT INTO dice (dice_id, name, value, owner, date_created) VALUES (4, '4eme dé olivier', 8, 'olivier', '2020-11-15 12:11:57.070094');
INSERT INTO dice (dice_id, name, value, owner, date_created) VALUES (5, '5eme dé olivier', 13, 'olivier', '2020-11-15 12:12:01.969374');

-- Table : dice_group
DROP TABLE IF EXISTS dice_group;
CREATE TABLE dice_group (
	group_id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	owner VARCHAR(50) NOT NULL, 
	last_result INTEGER, 
	dice_count INTEGER, 
	date_created DATETIME, 
	PRIMARY KEY (group_id)
);
INSERT INTO dice_group (group_id, name, owner, last_result, dice_count, date_created) VALUES (1, '1er lancé olivier', 'olivier', 3, 1, '2020-11-15 12:12:08.555751');
INSERT INTO dice_group (group_id, name, owner, last_result, dice_count, date_created) VALUES (2, '2eme lancé olivier', 'olivier', NULL, NULL, '2020-11-15 12:12:11.860940');

-- Table : dice_historic
DROP TABLE IF EXISTS dice_historic;
CREATE TABLE dice_historic (
	dice_historic_id INTEGER NOT NULL, 
	value INTEGER, 
	dice_id INTEGER NOT NULL, 
	roll_historic_id INTEGER NOT NULL, 
	date_created DATETIME, 
	PRIMARY KEY (dice_historic_id), 
	FOREIGN KEY(dice_id) REFERENCES dice (dice_id), 
	FOREIGN KEY(roll_historic_id) REFERENCES roll_historic (roll_historic_id)
);
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (1, 3, 4, 1, '2020-11-15 12:13:15.700591');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (2, 1, 5, 1, '2020-11-15 12:13:15.703591');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (3, 5, 3, 1, '2020-11-15 12:13:15.704591');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (4, 7, 4, 2, '2020-11-15 12:19:59.257673');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (5, 2, 5, 2, '2020-11-15 12:19:59.261674');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (6, 5, 3, 2, '2020-11-15 12:19:59.266674');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (7, 1, 1, 2, '2020-11-15 12:19:59.268674');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (8, 1, 2, 2, '2020-11-15 12:19:59.271674');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (9, 8, 4, 3, '2020-11-15 12:20:00.131723');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (10, 11, 5, 3, '2020-11-15 12:20:00.136724');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (11, 5, 3, 3, '2020-11-15 12:20:00.138724');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (12, 1, 1, 3, '2020-11-15 12:20:00.139724');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (13, 3, 2, 3, '2020-11-15 12:20:00.141724');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (14, 7, 4, 4, '2020-11-15 12:20:00.995773');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (15, 11, 5, 4, '2020-11-15 12:20:01.000773');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (16, 4, 3, 4, '2020-11-15 12:20:01.004773');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (17, 2, 1, 4, '2020-11-15 12:20:01.006773');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (18, 1, 2, 4, '2020-11-15 12:20:01.011774');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (19, 2, 4, 5, '2020-11-15 12:20:25.143154');
INSERT INTO dice_historic (dice_historic_id, value, dice_id, roll_historic_id, date_created) VALUES (20, 3, 4, 6, '2020-11-15 12:20:25.955200');

-- Table : junction_dice_group
DROP TABLE IF EXISTS junction_dice_group;
CREATE TABLE junction_dice_group (
	junction_dice_group_id INTEGER NOT NULL, 
	dice_id INTEGER NOT NULL, 
	group_id INTEGER NOT NULL, 
	PRIMARY KEY (junction_dice_group_id), 
	FOREIGN KEY(dice_id) REFERENCES dice (dice_id), 
	FOREIGN KEY(group_id) REFERENCES dice_group (group_id)
);
INSERT INTO junction_dice_group (junction_dice_group_id, dice_id, group_id) VALUES (1, 4, 1);

-- Table : roll_historic
DROP TABLE IF EXISTS roll_historic;
CREATE TABLE roll_historic (
	roll_historic_id INTEGER NOT NULL, 
	dice_group_id INTEGER NOT NULL, 
	date_created DATETIME, 
	PRIMARY KEY (roll_historic_id), 
	FOREIGN KEY(dice_group_id) REFERENCES dice_group (group_id)
);
INSERT INTO roll_historic (roll_historic_id, dice_group_id, date_created) VALUES (1, 1, '2020-11-15 12:13:15.546582');
INSERT INTO roll_historic (roll_historic_id, dice_group_id, date_created) VALUES (2, 1, '2020-11-15 12:19:59.148667');
INSERT INTO roll_historic (roll_historic_id, dice_group_id, date_created) VALUES (3, 1, '2020-11-15 12:19:59.945713');
INSERT INTO roll_historic (roll_historic_id, dice_group_id, date_created) VALUES (4, 1, '2020-11-15 12:20:00.840764');
INSERT INTO roll_historic (roll_historic_id, dice_group_id, date_created) VALUES (5, 1, '2020-11-15 12:20:24.989145');
INSERT INTO roll_historic (roll_historic_id, dice_group_id, date_created) VALUES (6, 1, '2020-11-15 12:20:25.799191');

-- Table : user
DROP TABLE IF EXISTS user;
CREATE TABLE user (
	login VARCHAR(200) NOT NULL, 
	password VARCHAR(200) NOT NULL, 
	PRIMARY KEY (login)
);
INSERT INTO user (login, password) VALUES ('olivier', 'pbkdf2:sha256:150000$VHKf9yaS$bd365044e6598375e627636923d27eb264348c244f07a5f5edd42e5ec75a8a4b');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;

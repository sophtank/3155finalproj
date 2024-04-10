CREATE DATABASE finalProject; --run me first!

DROP DATABASE finalProject; --run me if you mess up

DROP TABLE IF EXISTS users; --run the rest of the code now

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50),
    password VARCHAR(50) NOT NULL, --may need to change the length once we decide hashing length, for now store in plaintext
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (username)
);

DROP TABLE IF EXISTS vehicle;

CREATE TABLE IF NOT EXISTS vehicle (
    vehicle_id UUID,    -- this is just a basic vehicle
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year CHAR(4) NOT NULL,
    PRIMARY KEY (vehicle_id)
);

DROP TABLE IF EXISTS drive;

CREATE TABLE IF NOT EXISTS drive (
  drive_id UUID,
    vehicle_id UUID NOT NULL, --assigns a vehicle to the drive
    milage FLOAT NOT NULL,
    duration INT NOT NULL,  --integer in minutes
    title VARCHAR(200) NOT NULL,
    caption VARCHAR(500) NOT NULL,
    photo VARCHAR(500) NOT NULL, --link
    date TIMESTAMP NOT NULL,    --timestamp for when the drive is added to database
    username VARCHAR(50) NOT NULL, --assigns a drive to a user
    PRIMARY KEY (drive_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id),
    FOREIGN KEY (username) REFERENCES users(username)
);

DROP TABLE IF EXISTS tags;

CREATE TABLE IF NOT EXISTS tags (
    drive_id UUID,
    commute BOOL,   --for all of these, true = tagged, false or null = not tagged
    near_death_experience BOOL,
    carpool BOOL,
    mostly_highway BOOL,
    mostly_backroads BOOL,
    PRIMARY KEY (drive_id)
    FOREIGN KEY (drive_id) REFERENCES drive(drive_id) 
    
);

DROP TABLE IF EXISTS likes;

CREATE TABLE IF NOT EXISTS likes (
  drive_id UUID, --the drive that user liked
  username VARCHAR(50), --the user that liked it
  PRIMARY KEY (drive_id,username),
  FOREIGN KEY (drive_id) REFERENCES drive(drive_id),
  FOREIGN KEY (username) REFERENCES users(username)
);

DROP TABLE IF EXISTS comments;

CREATE TABLE IF NOT EXISTS comments (
    drive_id UUID, --the drive that is commented
    username VARCHAR(50), --the user that commented
    comment VARCHAR(200) NOT NULL,
    date TIMESTAMP NOT NULL, --when the comment was left
    PRIMARY KEY (drive_id,username),
    FOREIGN KEY (drive_id) REFERENCES drive(drive_id),
    FOREIGN KEY (username) REFERENCES users(username)
);

DROP TABLE IF EXISTS user_vehicle;

CREATE TABLE IF NOT EXISTS user_vehicle (
    username VARCHAR(50), --attributes a vehicle to a user
    vehicle_id UUID,
    color VARCHAR(20) NOT NULL,
    PRIMARY KEY (username, vehicle_id),
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id)
);

DROP TABLE IF EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics (
    username VARCHAR(50),
    time_logged_in INT, --total minutes logged in
    sign_in_count INT, --number of sign-ins
    PRIMARY KEY (username)
);

-- insert fake data :)
INSERT INTO users VALUES
                      ('asico', '123', 'Ashleigh', 'Sico'),
                      ('stanker', '123', 'Sophie', 'Tanker'),
                      ('ccuartas', '123', 'Christopher', 'Cuartas'),
                      ('svasire4', '123', 'Sandeep', 'Vasireddy'),
                      ('skiser18', '123', 'Sean', 'Kiser'),
                      ('mwilki31', '123', 'Matt', 'Wilkinson');

INSERT INTO vehicle VALUES
                        ('6a6a459f-4986-4f23-b9f5-a8ec1923ef6d', 'Honda', 'Pilot','2010'),
                        ('ffa2b0b9-efd5-4dc9-b947-d9a25af99692', 'Toyota', 'RAV4', '2015'),
                        ('6bc88650-535b-4c44-9a7a-11ebe27bab83', 'Honda', 'Civic', '2018'),
                        ('cebef27b-8de6-42c5-bbc9-a2e8158ab3ae', 'Ford', 'F-150', '2016'),
                        ('da4ad3d4-2d51-47bd-927f-ba9a2812ae4f', 'Chevrolet', 'Silverado', '2023'),
                        ('338763f1-cdd4-43e7-9c69-8f248df1abbf', 'Nissan', 'Leaf', '2024'),
                        ('4c964948-caad-4fcd-b917-52af70367ca5', 'Volkswagen', 'Beetle', '2020');

INSERT INTO drive VALUES
                      ('8574e1d5-7369-4f23-8c5f-0f53d8977303', '6a6a459f-4986-4f23-b9f5-a8ec1923ef6d', 20.4, 40, 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(), 'asico'),
                      ('3f16c4e4-e8d0-4175-84f3-53ee91923ec1', '6a6a459f-4986-4f23-b9f5-a8ec1923ef6d', 19.7, 39, 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(), 'asico'),
                      ('5c971fbf-7210-4f9e-8358-4e6d54defc88', 'ffa2b0b9-efd5-4dc9-b947-d9a25af99692', 10.4, 23, 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(), 'stanker'),
                      ('457fdf98-de29-421b-8ab6-fbea9d780cc2', 'cebef27b-8de6-42c5-bbc9-a2e8158ab3ae', 22.2, 58, 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(), 'svasire4'),
                      ('5282a1ac-b818-4cac-b3f3-5fca6732cd15', 'cebef27b-8de6-42c5-bbc9-a2e8158ab3ae', 12.7, 36, 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(), 'svasire4'),
                      ('1dad8038-ac60-42b3-80f1-ff10d0762778', '6bc88650-535b-4c44-9a7a-11ebe27bab83', 37.5, 58, 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(), 'ccuartas'),
                      ('bb6fcd45-d54d-404f-89a7-f01e60fb0bf3', 'ffa2b0b9-efd5-4dc9-b947-d9a25af99692', 15.6, 26, 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(), 'ccuartas'),
                      ('e5aec1d5-4a8a-4478-b2f0-e573244a6b4b', 'da4ad3d4-2d51-47bd-927f-ba9a2812ae4f', 55.2, 115, 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(),'skiser18'),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', '4c964948-caad-4fcd-b917-52af70367ca5', 32.1, 42, 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(),  'mwilki31');

INSERT INTO user_vehicle VALUES
                      ('asico', '6a6a459f-4986-4f23-b9f5-a8ec1923ef6d', 'blue'),
                      ('stanker', 'ffa2b0b9-efd5-4dc9-b947-d9a25af99692', 'silver'),
                      ('ccuartas', '6bc88650-535b-4c44-9a7a-11ebe27bab83', 'black'),
                      ('ccuartas', 'ffa2b0b9-efd5-4dc9-b947-d9a25af99692', 'blue'),
                      ('svasire4','da4ad3d4-2d51-47bd-927f-ba9a2812ae4f', 'red'),
                      ('skiser18', 'cebef27b-8de6-42c5-bbc9-a2e8158ab3ae', 'white'),
                      ('skiser18', '6a6a459f-4986-4f23-b9f5-a8ec1923ef6d', 'black'),
                      ('mwilki31', '338763f1-cdd4-43e7-9c69-8f248df1abbf', 'red'),
                      ('mwilki31', '4c964948-caad-4fcd-b917-52af70367ca5', 'yellow');

INSERT INTO tags VALUES
                     ('8574e1d5-7369-4f23-8c5f-0f53d8977303', TRUE, FALSE, FALSE, TRUE, FALSE),
                     ('3f16c4e4-e8d0-4175-84f3-53ee91923ec1', TRUE, TRUE, FALSE, TRUE, FALSE),
                     ('5c971fbf-7210-4f9e-8358-4e6d54defc88', FALSE, FALSE, FALSE, FALSE, TRUE),
                     ('457fdf98-de29-421b-8ab6-fbea9d780cc2', FALSE, TRUE, TRUE, FALSE, FALSE),
                     ('5282a1ac-b818-4cac-b3f3-5fca6732cd15', FALSE, FALSE, FALSE, FALSE, FALSE),
                     ('1dad8038-ac60-42b3-80f1-ff10d0762778', FALSE, TRUE, FALSE, FALSE, TRUE),
                     ('bb6fcd45-d54d-404f-89a7-f01e60fb0bf3', TRUE, TRUE, TRUE, TRUE, FALSE),
                     ('e5aec1d5-4a8a-4478-b2f0-e573244a6b4b', TRUE, TRUE, FALSE, FALSE, FALSE),
                     ('b6581a62-a5ac-4ec7-a043-006724940583', FALSE, FALSE, FALSE, FALSE, FALSE);

INSERT INTO likes VALUES
                      ('8574e1d5-7369-4f23-8c5f-0f53d8977303', 'svasire4'),
                      ('8574e1d5-7369-4f23-8c5f-0f53d8977303', 'stanker'),
                      ('8574e1d5-7369-4f23-8c5f-0f53d8977303', 'ccuartas'),
                      ('3f16c4e4-e8d0-4175-84f3-53ee91923ec1', 'asico'),
                      ('3f16c4e4-e8d0-4175-84f3-53ee91923ec1', 'skiser18'),
                      ('5c971fbf-7210-4f9e-8358-4e6d54defc88', 'asico'),
                      ('5c971fbf-7210-4f9e-8358-4e6d54defc88', 'svasire4'),
                      ('5c971fbf-7210-4f9e-8358-4e6d54defc88', 'stanker'),
                      ('5c971fbf-7210-4f9e-8358-4e6d54defc88', 'mwilki31'),
                      ('5282a1ac-b818-4cac-b3f3-5fca6732cd15', 'ccuartas'),
                      ('5282a1ac-b818-4cac-b3f3-5fca6732cd15', 'svasire4'),
                      ('1dad8038-ac60-42b3-80f1-ff10d0762778', 'stanker'),
                      ('bb6fcd45-d54d-404f-89a7-f01e60fb0bf3', 'svasire4'),
                      ('bb6fcd45-d54d-404f-89a7-f01e60fb0bf3', 'ccuartas'),
                      ('bb6fcd45-d54d-404f-89a7-f01e60fb0bf3', 'skiser18'),
                      ('bb6fcd45-d54d-404f-89a7-f01e60fb0bf3', 'asico'),
                      ('e5aec1d5-4a8a-4478-b2f0-e573244a6b4b', 'ccuartas'),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'asico'),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'ccuartas'),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'mwilki31'),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'stanker'),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'svasire4'),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'skiser18');

INSERT INTO comments VALUES
                      ('8574e1d5-7369-4f23-8c5f-0f53d8977303', 'svasire4', 'looks like fun!', NOW()),
                      ('3f16c4e4-e8d0-4175-84f3-53ee91923ec1', 'asico', 'looks like fun!', NOW()),
                      ('3f16c4e4-e8d0-4175-84f3-53ee91923ec1', 'skiser18', 'looks like fun!', NOW()),
                      ('5c971fbf-7210-4f9e-8358-4e6d54defc88', 'asico', 'looks like fun!', NOW()),
                      ('5c971fbf-7210-4f9e-8358-4e6d54defc88', 'stanker', 'looks like fun!', NOW()),
                      ('1dad8038-ac60-42b3-80f1-ff10d0762778', 'stanker', 'looks like fun!', NOW()),
                      ('bb6fcd45-d54d-404f-89a7-f01e60fb0bf3', 'ccuartas', 'looks like fun!', NOW()),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'asico', 'looks like fun!', NOW()),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'ccuartas', 'looks like fun!', NOW()),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'mwilki31', 'looks like fun!', NOW()),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', 'stanker', 'looks like fun!', NOW());

INSERT INTO analytics VALUES
                     ('asico', 43, 2),
                     ('stanker', 37, 4),
                     ('ccuartas', 56, 3),
                     ('svasire4', 26, 2),
                     ('skiser18', 17, 1),
                     ('mwilki31', 127, 9);
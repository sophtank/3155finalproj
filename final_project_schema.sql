CREATE DATABASE finalProject; --run me first!

DROP DATABASE finalProject; --run me if you mess up

DROP TABLE IF EXISTS users; --run the rest of the code now

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50),
    password VARCHAR(255) NOT NULL, --may need to change the length once we decide hashing length, for now store in plaintext
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (username)
);

DROP TABLE IF EXISTS vehicle;

CREATE TABLE IF NOT EXISTS vehicle (
    vehicle_id UUID,    -- this is just a basic vehicle
    username VARCHAR(50) NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year CHAR(4) NOT NULL,
    color VARCHAR(20) NOT NULL,
    PRIMARY KEY (vehicle_id),
    FOREIGN KEY(username) REFERENCES users(username)
);

DROP TABLE IF EXISTS drive;

drop table drive cascade; -- Use this To delete the drive table, then create the table below
drop table likes, comments, tags; --Then Run this, and add all the tables back and then insert the values after drive

CREATE TABLE IF NOT EXISTS drive (
    drive_id UUID,
    vehicle_id UUID NOT NULL, --assigns a vehicle to the drive
    mileage FLOAT NOT NULL,
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
    comment_id UUID,
    drive_id UUID, --the drive that is commented
    username VARCHAR(50), --the user that commented
    comment VARCHAR(200) NOT NULL,
    date TIMESTAMP NOT NULL, --when the comment was left
    PRIMARY KEY (comment_id),
    FOREIGN KEY (drive_id) REFERENCES drive(drive_id),
    FOREIGN KEY (username) REFERENCES users(username)
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
                      ('asico', '$2b$12$tXaxFFvBbPJw0xDCeshGdOdqlPE1q1xILKocy4qvoWPtm4yGeo7Ke', 'Ashleigh', 'Sico'),
                      ('stanker', '$2b$12$ZA/TDf3hN9XjZYguPpZCUefOCeyMEHaeMQ9eShaAN86UjA7ojUaMy', 'Sophie', 'Tanker'),
                      ('ccuartas', '$2b$12$0RYdGy8J.nNuI4E3bsx7XuFxvasX4lpg.8NEak0uvo5qs4hWIr4EK', 'Christopher', 'Cuartas'),
                      ('svasire4', '$2b$12$xLgFYaD3I2ovbIDObpTOSuEhCi2ZDVZ8iMZPEDHPLadrXaT4G/uUO', 'Sandeep', 'Vasireddy'),
                      ('skiser18', '$2b$12$4N60BrbUkTaXpc5KG9fwL.gxoDM5ucZh7zv3Cf7ejmsDgKB9h9mEG', 'Sean', 'Kiser'),
                      ('mwilki31', '$2b$12$V6RcoyTt0bjPhskvcDoPBuydBcbvwcmW28Izr46wT1t.iIldl9XM6', 'Matt', 'Wilkinson');

INSERT INTO vehicle VALUES
                        ('6a6a459f-4986-4f23-b9f5-a8ec1923ef6d','asico', 'Honda', 'Pilot','2010', 'blue'),
                        ('6a6a459f-4986-4f23-b9f5-a8ec1923ee5c','skiser18', 'Honda', 'Pilot','2010', 'black'),
                        ('ffa2b0b9-efd5-4dc9-b947-d9a25af99692', 'stanker', 'Toyota', 'RAV4', '2015', 'silver'),
                        ('ffa2b0ca-efd5-4dc9-b947-d9a25af99692', 'ccuartas', 'Toyota', 'RAV4', '2015', 'blue'),
                        ('6bc88650-535b-4c44-9a7a-11ebe27bab83', 'ccuartas', 'Honda', 'Civic', '2018', 'black'),
                        ('cebef27b-8de6-42c5-bbc9-a2e8158ab3ae','skiser18', 'Ford', 'F-150', '2016', 'white'),
                        ('da4ad3d4-2d51-47bd-927f-ba9a2812ae4f','svasire4', 'Chevrolet', 'Silverado', '2023', 'red'),
                        ('338763f1-cdd4-43e7-9c69-8f248df1abbf','mwilki31', 'Nissan', 'Leaf', '2024', 'red'),
                        ('4c964948-caad-4fcd-b917-52af70367ca5', 'mwilki31', 'Volkswagen', 'Beetle', '2020', 'yellow');

INSERT INTO drive VALUES
                      ('8574e1d5-7369-4f23-8c5f-0f53d8977303', '6a6a459f-4986-4f23-b9f5-a8ec1923ef6d', 20.4, 40, 'my drive!', 'a great drive!', 'https://images.pexels.com/photos/386025/pexels-photo-386025.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', NOW(), 'asico'),
                      ('3f16c4e4-e8d0-4175-84f3-53ee91923ec1', '6a6a459f-4986-4f23-b9f5-a8ec1923ef6d', 19.7, 39, 'my drive!', 'a great drive!', 'https://wallpapercave.com/wp/wp8030431.jpg', NOW(), 'asico'),
                      ('5c971fbf-7210-4f9e-8358-4e6d54defc88', 'ffa2b0b9-efd5-4dc9-b947-d9a25af99692', 10.4, 23,  'my drive!','a great drive!', 'https://images.pexels.com/photos/1592384/pexels-photo-1592384.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', NOW(), 'stanker'),
                      ('457fdf98-de29-421b-8ab6-fbea9d780cc2', 'cebef27b-8de6-42c5-bbc9-a2e8158ab3ae', 22.2, 58, 'my drive!', 'a great drive!', 'https://images.pexels.com/photos/116675/pexels-photo-116675.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', NOW(), 'svasire4'),
                      ('5282a1ac-b818-4cac-b3f3-5fca6732cd15', 'cebef27b-8de6-42c5-bbc9-a2e8158ab3ae', 12.7, 36, 'my drive!', 'a great drive!', 'https://images.pexels.com/photos/707046/pexels-photo-707046.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', NOW(), 'svasire4'),
                      ('1dad8038-ac60-42b3-80f1-ff10d0762778', '6bc88650-535b-4c44-9a7a-11ebe27bab83', 37.5, 58, 'my drive!', 'a great drive!', 'https://images.pexels.com/photos/3593922/pexels-photo-3593922.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', NOW(), 'ccuartas'),
                      ('bb6fcd45-d54d-404f-89a7-f01e60fb0bf3', 'ffa2b0ca-efd5-4dc9-b947-d9a25af99692', 15.6, 26, 'my drive!', 'a great drive!', 'https://images.pexels.com/photos/3311574/pexels-photo-3311574.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', NOW(), 'ccuartas'),
                      ('e5aec1d5-4a8a-4478-b2f0-e573244a6b4b', 'da4ad3d4-2d51-47bd-927f-ba9a2812ae4f', 55.2, 115, 'my drive!', 'a great drive!', 'https://images.pexels.com/photos/1638459/pexels-photo-1638459.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', NOW(),'skiser18'),
                      ('b6581a62-a5ac-4ec7-a043-006724940583', '4c964948-caad-4fcd-b917-52af70367ca5', 32.1, 42, 'my drive!', 'a great drive!', 'https://img.freepik.com/free-photo/luxurious-car-parked-highway-with-illuminated-headlight-sunset_181624-60607.jpg', NOW(),  'mwilki31');

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
                      ('c0456910-f652-4d6f-a4e0-6d41dd618bad','8574e1d5-7369-4f23-8c5f-0f53d8977303', 'svasire4', 'looks like fun!', NOW()),
                      ('a2b1d86c-289d-403e-a8cd-9476fb264aef','3f16c4e4-e8d0-4175-84f3-53ee91923ec1', 'asico', 'looks like fun!', NOW()),
                      ('87b4d955-fbc0-4b84-bd56-df5553a7efd9', '3f16c4e4-e8d0-4175-84f3-53ee91923ec1', 'skiser18', 'looks like fun!', NOW()),
                      ('91885b33-0971-466b-a3f5-8d3bb876847a', '5c971fbf-7210-4f9e-8358-4e6d54defc88', 'asico', 'looks like fun!', NOW()),
                      ('3dc74e73-cbd6-4741-b704-9ee53c7e668f', '5c971fbf-7210-4f9e-8358-4e6d54defc88', 'stanker', 'looks like fun!', NOW()),
                      ('96f3e2a5-6504-4c7c-9aac-2056099d5865', '1dad8038-ac60-42b3-80f1-ff10d0762778', 'stanker', 'looks like fun!', NOW()),
                      ('3b97c197-e1a9-46ff-8fdf-91bc0f477c1c', 'bb6fcd45-d54d-404f-89a7-f01e60fb0bf3', 'ccuartas', 'looks like fun!', NOW()),
                      ('6b290b81-826a-49d0-b700-4ee5919b41db', 'b6581a62-a5ac-4ec7-a043-006724940583', 'asico', 'looks like fun!', NOW()),
                      ('cfcf4387-2c07-4c94-9910-54bbc26dbe6a', 'b6581a62-a5ac-4ec7-a043-006724940583', 'ccuartas', 'looks like fun!', NOW()),
                      ('398daf19-3192-4e84-be2f-4c24699861dc', 'b6581a62-a5ac-4ec7-a043-006724940583', 'mwilki31', 'looks like fun!', NOW()),
                      ('b61a1dd5-5dfa-4cca-9153-d4a4ecebdcb5', 'b6581a62-a5ac-4ec7-a043-006724940583', 'stanker', 'looks like fun!', NOW());

INSERT INTO analytics VALUES
                     ('asico', 43, 2),
                     ('stanker', 37, 4),
                     ('ccuartas', 56, 3),
                     ('svasire4', 26, 2),
                     ('skiser18', 17, 1),
                     ('mwilki31', 127, 9);
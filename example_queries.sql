-- user info
SELECT users.first_name AS "First Name",
        users.last_name AS "Last Name",
        vehicle.make AS "Vehicle Make",
        vehicle.model AS "Vehicle Model",
        vehicle.year AS "Vehicle Year",
        user_vehicle.color AS "Vehicle Color"
FROM users JOIN user_vehicle
ON users.username = user_vehicle.username
JOIN vehicle
on user_vehicle.vehicle_id = vehicle.vehicle_id;

-- drive info
SELECT users.first_name AS "First Name",
       users.last_name AS "Last Name",
       drive.date AS "Date",
       drive.milage AS "Milage",
       vehicle.make AS "Vehicle Make",
       vehicle.model AS "Vehicle Model"
FROM users JOIN drive
ON users.username = drive.username
JOIN vehicle ON drive.vehicle_id = vehicle.vehicle_id;


-- who likes Sophie's drive?
SELECT users.first_name AS "First Name",
       users.last_name AS "Last Name"
FROM users
JOIN likes
ON users.username = likes.username
WHERE likes.drive_id = '5c971fbf-7210-4f9e-8358-4e6d54defc88';

-- Who commented on Sophie's drive?
SELECT users.first_name AS "First Name",
       users.last_name AS "Last Name",
       comments.comment AS "Comment"
FROM users
JOIN comments
ON users.username = comments.username
WHERE comments.drive_id = '5c971fbf-7210-4f9e-8358-4e6d54defc88';

-- what tags did Sophie use?
SELECT tags.commute, tags.near_death_experience, tags.carpool, tags.mostly_backroads, tags.mostly_highway
FROM tags
WHERE drive_id = '5c971fbf-7210-4f9e-8358-4e6d54defc88';
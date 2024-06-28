-- Prepares the MySQL server for this project
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Creates a user 'hbnb_dev' with specified password 'hbnb_dev_pwd' for local access
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grants all privileges on the database 'hbnb_dev_db' to the user 'hbnb_dev'
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost';
-- Grants SELECT privileges on the performance schema to the user 'hbnb_dev' for monitoring
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';
-- Flushes privileges to apply changes immediately
FLUSH PRIVILEGES;

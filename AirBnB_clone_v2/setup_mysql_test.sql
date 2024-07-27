-- Prepares the MySQL server for this project
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- Creates a user 'hbnb_test' with specified password 'hbnb_test_pwd' for local access
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Grants all privileges on the database 'hbnb_test_db' to the user 'hbnb_test'
GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO 'hbnb_test'@'localhost';
-- Grants SELECT privileges on the performance schema to the user 'hbnb_test' for monitoring
GRANT SELECT ON `performance_schema`.* TO 'hbnb_test'@'localhost';
-- Flushes privileges to apply changes immediately
FLUSH PRIVILEGES;

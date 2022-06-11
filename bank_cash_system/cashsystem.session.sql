--@block
CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    login VARCHAR(6) NOT NULL UNIQUE,
    pin INT NOT NULL,
    password VARCHAR(10) NOT NULL,
    balance INT
);
--@block
INSERT INTO users (name, login, pin, password, balance)
VALUES ('Marie', 'mar123', 1234, 'marie1999', 1000),
    ('Mark', 'mar321', 4321, 'mark1988', 15000),
    ('Christine', 'ch1234', 2345, 'christie12', 25000);
--@block 
ALTER TABLE users
ADD blocked VARCHAR(5) NOT NULL DEFAULT 'False';
--@block
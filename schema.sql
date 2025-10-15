CREATE DATABASE IF NOT EXISTS ad_dashboard;
USE ad_dashboard;

CREATE TABLE IF NOT EXISTS campaigns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    channel VARCHAR(50),
    budget DECIMAL(10,2),
    impressions INT,
    clicks INT,
    conversions INT
);

INSERT INTO campaigns (name, channel, budget, impressions, clicks, conversions) VALUES
('Diwali Sale', 'Google Ads', 5000.00, 10000, 450, 50),
('New Year Blast', 'Meta Ads', 3000.00, 7000, 300, 30);
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE USER 'crawler_user'@'%' IDENTIFIED BY 'daniella';

GRANT ALL PRIVILEGES ON drogasil.* TO 'crawler_user'@'%';

FLUSH PRIVILEGES;
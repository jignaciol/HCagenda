SELECT role, level FROM roles;

INSERT into roles values ('user', 50);

SELECT * FROM users;

INSERT INTO users(
            username, role, hash, email_addr, "desc", creation_date, last_login)
VALUES ('admin', 'admin', 'cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=', 'admin@localhost.local', 'admin test user', '2012-10-28 20:50:26.286723', '2016-04-12 15:15:50.064919');



update users set email_addr = 'jignaciol@gmail.com' where username = 'jignaciol@gmail.com';
update users set "desc" = 'admin test user' where username = 'jignaciol@gmail.com';
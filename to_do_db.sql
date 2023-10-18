CREATE DATABASE TO_DO
GO

USE TO_DO
GO

CREATE TABLE Items(
ItemID int IDENTITY(1,1) NOT NULL PRIMARY KEY,
Title nvarchar(50) NOT NULL,
Content nvarchar(100) NOT NULL,
Priority int NOT NULL CHECK (Priority > 0 and Priority < 6));
GO

INSERT INTO Items(
Title, Content, Priority)
VALUES
	('New Title 1', 'New Content 1', 1),
	('New Title 2', 'New Content 2', 2),
	('New Title 3', 'New Content 3', 3),
	('New Title 4', 'New Content 4', 4),
	('New Title 5', 'New Content 5', 5);
GO

SELECT * FROM Items
GO
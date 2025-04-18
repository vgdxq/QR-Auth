-- Створення бази даних
CREATE DATABASE AuthDB;
GO

-- Використання бази даних
USE AuthDB;
GO

-- Створення таблиці QRTokens
CREATE TABLE QRTokens (
    Token NVARCHAR(36) NOT NULL,
    UserID NVARCHAR(50) NOT NULL,
    CreatedAt DATETIME NOT NULL
);
GO

-- Додавання унікального обмеження на UserID
ALTER TABLE QRTokens
ADD CONSTRAINT UK_QRTokens_UserID UNIQUE (UserID);
GO

--Вивід таблиці
SELECT * FROM QRTokens;
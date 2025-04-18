-- ��������� ���� �����
CREATE DATABASE AuthDB;
GO

-- ������������ ���� �����
USE AuthDB;
GO

-- ��������� ������� QRTokens
CREATE TABLE QRTokens (
    Token NVARCHAR(36) NOT NULL,
    UserID NVARCHAR(50) NOT NULL,
    CreatedAt DATETIME NOT NULL
);
GO

-- ��������� ���������� ��������� �� UserID
ALTER TABLE QRTokens
ADD CONSTRAINT UK_QRTokens_UserID UNIQUE (UserID);
GO

--���� �������
SELECT * FROM QRTokens;
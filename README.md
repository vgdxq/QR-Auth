# QR Authentication Project

Flask-додаток для генерації QR-кодів для автентифікації користувачів через токени, які зберігаються в базі даних SQL Server.

## Вимоги

1. **Python 3.8+**.
2. **SQL Server** (наприклад, SQL Server Express) із SQL Server Management Studio (SSMS) для керування базою даних.
3. **ODBC Driver 17 for SQL Server** ( [офіційного сайту Microsoft](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)).
4. Браузер (Google Chrome, Firefox тощо).
5. Сканер QR-кодів (наприклад, Google Lens або програма на телефоні).

## Установка

### 1. Налаштування SQL Server
1. Встановіть SQL Server, якщо ще не встановлено (наприклад, SQL Server Express).
2. Встановіть ODBC Driver 17 for SQL Server.
3. Відкрийте SQL Server Management Studio (SSMS).
4. Виконайте скрипт із файлу `database_setup.sql`, щоб створити базу даних `AuthDB` і таблицю `QRTokens`.
5. Переконайтеся, що SQL Server запущений, і запам’ятайте ім’я сервера (наприклад, `CHOTA-TAM\SQLEXPRESS`).

### 2. Налаштування Python
1. Створіть віртуальне середовище (опціонально, але рекомендується):
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   
### 3. Підключення серверу
1. Замініть VGDXQ\\SQLEXPRESS на ім’я вашого SQL Server. Щоб знайти ім’я сервера:
2. У SSMS виконайте запит: SELECT @@SERVERNAME;
3. Або перевірте в налаштуваннях SQL Server Configuration Manager.

### 4. Запуск додатка
1. У терміналі, перебуваючи в теці проекту, виконайте: python app.py
2. У консолі має з’явитися повідомлення: Database connection successful Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
3. Відкрийте браузер і перейдіть за адресою: http://127.0.0.1:5000

### 5. Тестування
1. На головній сторінці введіть User ID (наприклад, zxc12) і натисніть "Отримати QR-код".
2. Проскануйте QR-код за допомогою телефону.
3. Скопіюйте токен із QR-коду, вставте його в поле "Введіть токен" і натисніть "Перевірити токен".
4. У разі успіху ви побачите повідомлення: ✅ Успішна автентифікація! Користувач: <user_id>.
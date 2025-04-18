# QR Authentication Project

Flask application for generating QR codes for user authentication via tokens stored in a SQL Server database.

## Requirements

1. **Python 3.8+**.
2. **SQL Server** (for example, SQL Server Express) with SQL Server Management Studio (SSMS) to manage the database.
3. **ODBC Driver 17 for SQL Server** (from the Microsoft website (https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)).
4. Browser (Google Chrome, Firefox, etc.).
5. A QR code scanner (for example, Google Lens or an app on your phone).

## Installing

### 1. Setting up SQL Server
1. Install SQL Server, if not already installed (for example, SQL Server Express).
2. Install the ODBC Driver 17 for SQL Server.
3. Open SQL Server Management Studio (SSMS).
4. Run the script from the `database_setup.sql` file to create the `AuthDB` database and the `QRTokens` table.
5. Make sure that SQL Server is running and remember the server name (for example, `CHOTA-TAM\SQLEXPRESS`).

### 2. Setting up Python
1. Create a virtual environment (optional, but recommended):
   ```bash
 python -m venv venv
 source venv/bin/activate # On Windows: venv\Scripts\activate
   
### 3. Connecting the server
1. Replace VGDXQ\\SQLEXPRESS with the name of your SQL Server. To find the server name:
2. In SSMS, run the query: SELECT @@SERVERNAME;
3. Or check in the SQL Server Configuration Manager settings.

### 4. Running the application
1. In the terminal, in the project folder, run: python app.py
2. A message should appear in the console: Database connection successful Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
3. Open a browser and go to the following address: http://127.0.0.1:5000

### 5. Testing
1. On the main page, enter the User ID (for example, zxc12) and click ‘Get QR code’.
2. Scan the QR code with your phone.
3. Copy the token from the QR code, paste it into the ‘Enter token’ field and click ‘Verify token’.
4. If successful, you will see a notification: ✅ Successful authentication! User: <user_id>.

Translated with DeepL.com (free version)

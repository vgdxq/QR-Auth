from flask import Flask, jsonify, request, send_file, render_template_string
import qrcode
import uuid
import io
import time
import pyodbc
from datetime import datetime, timedelta

app = Flask(__name__)

# З'єднання з SQL Server
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=VGDXQ\\SQLEXPRESS;"
    "Database=AuthDB;"
    "Trusted_Connection=yes;"
)

# Перевірка підключення до бази даних
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("Database connection successful")
except pyodbc.Error as e:
    print(f"Database connection failed: {e}")
    exit(1)

TOKEN_EXPIRY = 60
last_request = {}  # Для захисту від швидких повторних запитів

# 📄 HTML-шаблон
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>QR Авторизація</title>
    <style>
        body { font-family: sans-serif; padding: 40px; background: #f9f9f9; }
        input, button { padding: 10px; font-size: 16px; margin: 5px; }
        img { margin-top: 20px; border: 1px solid #ccc; display: none; }
        #status { margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <h2>Генерація QR-коду для автентифікації</h2>
    <input type="text" id="user_id" placeholder="Введіть User ID">
    <button onclick="generateQR()">Отримати QR-код</button>
    <br>
    <img id="qr_image" src="" alt="QR Code"/>
    <div id="status"></div>

    <h3>Введіть токен з QR-коду</h3>
    <input type="text" id="token_input" placeholder="Введіть токен (наприклад, 0669ce27-...)">
    <button onclick="verifyToken()">Перевірити токен</button>
    <div id="auth_status"></div>

    <script>
        function generateQR() {
            const userId = document.getElementById('user_id').value;
            if (!userId) {
                alert('Введіть User ID!');
                return;
            }

            const button = document.querySelector('button');
            button.disabled = true; // Блокувати кнопку

            console.log(`Fetching QR for user: ${userId}`);
            fetch(`/generate_qr/${userId}`)
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.blob();
                })
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    document.getElementById('qr_image').src = url;
                    document.getElementById('qr_image').style.display = 'block';
                    document.getElementById('status').innerText = 'Скануйте QR-код для отримання токена';
                })
                .catch(err => {
                    console.error('Error:', err);
                    document.getElementById('status').innerText = 'Помилка при отриманні QR-коду';
                })
                .finally(() => {
                    button.disabled = false; // Розблокувати кнопку
                });
        }

        function verifyToken() {
            const token = document.getElementById('token_input').value;
            if (!token) {
                alert('Введіть токен!');
                return;
            }

            fetch('/verify_token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: token })
            })
            .then(response => response.json())
            .then(data => {
                const authStatus = document.getElementById('auth_status');
                if (data.status === 'success') {
                    authStatus.innerText = `✅ Успішна автентифікація! Користувач: ${data.user_id}`;
                } else {
                    authStatus.innerText = `❌ ${data.message}`;
                }
            })
            .catch(err => {
                console.error('Помилка:', err);
                document.getElementById('auth_status').innerText = 'Помилка при перевірці токена';
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    print("Accessing index page")
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate_qr/<user_id>', methods=['GET'])
def generate_qr(user_id):
    # Захист від швидких повторних запитів
    current_time = time.time()
    if user_id in last_request and current_time - last_request[user_id] < 2:
        print(f"Ignoring rapid request for user {user_id}")
        cursor.execute("SELECT Token FROM QRTokens WHERE UserID = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            token = row[0]
            qr = qrcode.make(token)
            buf = io.BytesIO()
            qr.save(buf, format='PNG')
            buf.seek(0)
            response = send_file(buf, mimetype='image/png')
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
            return response
        else:
            return jsonify({'status': 'error', 'message': 'No token found'}), 404

    last_request[user_id] = current_time

    # Очистити старі токени
    cursor.execute("DELETE FROM QRTokens WHERE UserID = ? OR CreatedAt < ?",
                   (user_id, datetime.now() - timedelta(seconds=TOKEN_EXPIRY)))
    conn.commit()

    # Генерація нового токена
    token = str(uuid.uuid4())
    created_at = datetime.now()
    print(f"Generated token for user {user_id}: {token}")

    # Збереження токена
    try:
        cursor.execute("INSERT INTO QRTokens (Token, UserID, CreatedAt) VALUES (?, ?, ?)",
                       token, user_id, created_at)
        conn.commit()
    except pyodbc.IntegrityError:
        print(f"Token already exists for user {user_id}, returning existing token")
        cursor.execute("SELECT Token FROM QRTokens WHERE UserID = ?", (user_id,))
        token = cursor.fetchone()[0]

    # Створення QR-коду
    print(f"QR code content: {token}")
    qr = qrcode.make(token)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    buf.seek(0)

    response = send_file(buf, mimetype='image/png')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    return response

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({'status': 'error', 'message': 'Token is required'}), 400

    cursor.execute("SELECT UserID, CreatedAt FROM QRTokens WHERE Token = ?", token)
    row = cursor.fetchone()

    if not row:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

    user_id, created_at = row
    if datetime.now() - created_at > timedelta(seconds=TOKEN_EXPIRY):
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401

    return jsonify({'status': 'success', 'user_id': user_id})

@app.route('/verify_token', methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({'status': 'error', 'message': 'Токен не вказано'}), 400

    cursor.execute("SELECT UserID, CreatedAt FROM QRTokens WHERE Token = ?", token)
    row = cursor.fetchone()

    if not row:
        return jsonify({'status': 'error', 'message': 'Недійсний токен'}), 401

    user_id, created_at = row
    if datetime.now() - created_at > timedelta(seconds=TOKEN_EXPIRY):
        return jsonify({'status': 'error', 'message': 'Токен прострочений'}), 401

    # Видалити токен після успішної автентифікації
    cursor.execute("DELETE FROM QRTokens WHERE Token = ?", token)
    conn.commit()

    return jsonify({'status': 'success', 'user_id': user_id})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
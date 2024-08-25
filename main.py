from flask import Flask, request, render_template_string, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Koneksi ke MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # ganti dengan host MySQL Anda
        user='root',       # ganti dengan user MySQL Anda
        password='',       # ganti dengan password MySQL Anda
        database='percobaan_sql'  # ganti dengan nama database Anda
    )
    return connection

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        pesan = request.form['pesan']

        # Simpan data ke database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO pesan (name, pesan) VALUES (%s, %s)', (name, pesan))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('index'))

    # Mengambil data dari database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT name, pesan FROM pesan ORDER BY id DESC LIMIT 5')
    records = cursor.fetchall()
    cursor.close()
    connection.close()

    # HTML Template
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Form Input</title>
        <style>
            body {
                display: flex;
                background-color: rgb(90, 90, 90);
                align-items: center;
                justify-content: center;
                font-family: Arial, sans-serif;
            }

            .container {
                padding: 30px;
                border-radius: 10px;
                background-color: rgb(235, 234, 234);
                text-align: center;
            }

            .container h1 {
                color: green;
            }

            .container label {
                display: block;
                text-align: left;
                margin-bottom: 5px;
                font-weight: bold;
            }

            .container input[type="text"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }

            .container button {
                width: 100%;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }

            .container button:hover {
                background-color: #45a049;
            }

            .container ul {
                padding-top: 20px;
                text-align: left;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Percobaan SQL</h1>
            <form method="post">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required><br>
                <label for="pesan">Pesan:</label>
                <input type="text" id="pesan" name="pesan" required><br>
                <button type="submit">Submit</button>
            </form>

            <ul>
                {% for name, pesan in records %}
                <li><strong>{{ name }}</strong><br>{{ pesan }}</li><br>
                {% endfor %}
            </ul>
        </div>

    </body>
    </html>
    '''

    return render_template_string(html, records=records)

if __name__ == '__main__':
    app.run(debug=True)

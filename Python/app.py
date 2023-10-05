from flask import Flask, render_template, request, redirect, url_for, session, Response, make_response
from flask_session import Session
import sqlite3
from functools import wraps

app = Flask(__name__)

# Función para crear la conexión a la base de datos y la tabla si no existe
def conexion():
    connection = None
    try:
        connection = sqlite3.connect("publicaciones.db")

        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS tb_publicaciones (
        id INTEGER PRIMARY KEY,
        comentario TEXT,
        archivo BLOB,
        tipo TEXT
        )
    ''')
        connection.commit()
        return connection  # Devolver la conexión creada
    except sqlite3.Error as e:
       
        #print("Conexión a la base de datos 'RedSocial.db y tabla 'tb_usuarios' creadas exitosamente o ya existentes")
        raise e
conexion()

@app.route('/')
def index():
    return render_template('index.html')

#--------------------Comentarios-------------------------
@app.route('/publicaciones')
def listar_publicaciones():
    conn = sqlite3.connect('publicaciones.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_publicaciones")
    items = cursor.fetchall()
    conn.close()
    return render_template('comentarios.html', items=items)

@app.route('/upload', methods=['POST'])
def upload():
    comentario = request.form['comentario']
    archivo = request.files['archivo']
    datos = archivo.read()
    tipo = archivo.mimetype

    conn = sqlite3.connect('publicaciones.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tb_publicaciones (comentario, archivo, tipo) VALUES (?, ?, ?)",
                   (comentario, datos, tipo))
    conn.commit()
    conn.close()

    return redirect(url_for('listar_publicaciones'))

@app.route('/media/<int:item_id>')
def get_media(item_id):
    conn = sqlite3.connect('publicaciones.db')
    cursor = conn.cursor()
    cursor.execute("SELECT archivo, tipo FROM tb_publicaciones WHERE id = ?", (item_id,))
    archivo, tipo = cursor.fetchone()
    conn.close()

    return archivo, {'Content-Type': tipo}

@app.route('/especificaciones')
def especificaciones():
    return render_template('especificaciones.html')

@app.route('/reparaciones')
def reparaciones():
    return render_template('reparaciones.html')

@app.route('/software')
def software():
    return render_template('software.html')

if __name__ == '__main__':
    app.run(port=5500, debug=True)
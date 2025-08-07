import os
import sqlite3

DB_FILE = "inventario.db"

def crear_base_si_no_existe():
    if not os.path.exists(DB_FILE):
        print("Creando base de datos...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE productos (
                codigo TEXT PRIMARY KEY,
                nombre TEXT,
                precio REAL,
                stock INTEGER,
                descripcion TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE boletas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                total REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE detalle_boleta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_boleta INTEGER,
                codigo_producto TEXT,
                nombre TEXT,
                cantidad INTEGER,
                precio_unitario REAL,
                FOREIGN KEY (id_boleta) REFERENCES boletas(id)
            )
        ''')
        conn.commit()
        conn.close()
        print("Base de datos creada.")
    else:
        print("Base de datos ya existe.")

# Llamar esta función antes de abrir el menú
crear_base_si_no_existe()

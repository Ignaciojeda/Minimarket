import sqlite3

# Conectar o crear archivo de base de datos
conn = sqlite3.connect("minimarket.db")
cursor = conn.cursor()

# Tabla de productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    codigo_barras TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL,
    descripcion TEXT
)
""")

# Tabla de ventas
cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    total REAL NOT NULL
)
""")

# Detalles de cada venta
cursor.execute("""
CREATE TABLE IF NOT EXISTS detalle_venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER,
    codigo_barras TEXT,
    cantidad INTEGER,
    subtotal REAL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (codigo_barras) REFERENCES productos(codigo_barras)
)
""")

conn.commit()
conn.close()

print("Base de datos creada exitosamente.")

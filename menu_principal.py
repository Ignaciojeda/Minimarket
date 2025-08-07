import tkinter as tk
import subprocess
import os

# Ruta base donde están los otros scripts
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))

def abrir_script(nombre_archivo):
    ruta_completa = os.path.join(RUTA_BASE, nombre_archivo)
    subprocess.Popen(["python", ruta_completa])

# GUI
root = tk.Tk()
root.title("Minimarket - Menú Principal")
root.geometry("800x600")

tk.Label(root, text="MINIMARKET BRECAS", font=("Arial", 20, "bold")).pack(pady=20)

# Sección de productos
tk.Label(root, text="Gestión de Productos", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="🆕 Ingreso de productos", width=30, height=2,
          command=lambda: abrir_script("ingreso_productos.py")).pack(pady=5)

tk.Button(root, text="✏️ Modificar producto / stock", width=30, height=2,
          command=lambda: abrir_script("modificar_producto.py")).pack(pady=5)

tk.Button(root, text="🗑️ Ver / eliminar productos por stock", width=30, height=2,
          command=lambda: abrir_script("gestion_productos.py")).pack(pady=5)

# Sección de ventas
tk.Label(root, text="Ventas", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="🛒 Realizar venta", width=30, height=2,
          command=lambda: abrir_script("realizar_venta.py")).pack(pady=5)

tk.Button(root, text="🧾 Ver boletas (filtro por fecha/precio)", width=30, height=2,
          command=lambda: abrir_script("ver_boletas.py")).pack(pady=5)

# Consulta
tk.Label(root, text="Consultas", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="🔍 Consulta de precio", width=30, height=2,
          command=lambda: abrir_script("consulta_precio.py")).pack(pady=5)

# Salir
tk.Button(root, text="❌ Salir", width=30, height=2, command=root.quit).pack(pady=30)

root.mainloop()

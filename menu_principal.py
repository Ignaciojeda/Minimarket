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
root.geometry("400x400")

tk.Label(root, text="MINIMARKET BRECAS", font=("Arial", 16)).pack(pady=20)

btn1 = tk.Button(root, text="🆕 Ingreso de productos", width=30, height=2,
                 command=lambda: abrir_script("ingreso_productos.py"))
btn1.pack(pady=5)

btn2 = tk.Button(root, text="✏️ Modificar producto / stock", width=30, height=2,
                 command=lambda: abrir_script("modificar_producto.py"))
btn2.pack(pady=5)

btn3 = tk.Button(root, text="🛒 Realizar venta", width=30, height=2,
                 command=lambda: abrir_script("realizar_venta.py"))
btn3.pack(pady=5)

btn4 = tk.Button(root, text="🔍 Consulta de precio", width=30, height=2,
                 command=lambda: abrir_script("consulta_precio.py"))
btn4.pack(pady=5)

btn_salir = tk.Button(root, text="❌ Salir", width=30, height=2, command=root.quit)
btn_salir.pack(pady=20)

root.mainloop()

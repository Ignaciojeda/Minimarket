import sqlite3
import tkinter as tk
from tkinter import messagebox


def consultar_precio(event=None):
    codigo = entry_codigo.get()
    
    if not codigo:
        return

    conn = sqlite3.connect("minimarket.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio FROM productos WHERE codigo_barras = ?", (codigo,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nombre, precio = resultado
        label_resultado.config(
            text=f"Producto: {nombre}\nPrecio: ${precio:.0f}",
            fg="green"
        )
    else:
        label_resultado.config(text="Producto no encontrado.", fg="red")

    entry_codigo.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Consulta de Precio")
# Tamaño ventana
root.geometry("800x600")

tk.Label(root, text="Escanea el código de barras").pack(pady=10)

entry_codigo = tk.Entry(root, font=('Arial', 18), width=25)
entry_codigo.pack(pady=5)
entry_codigo.focus()
entry_codigo.bind("<Return>", consultar_precio)

label_resultado = tk.Label(root, text="", font=('Arial', 16))
label_resultado.pack(pady=20)

root.mainloop()

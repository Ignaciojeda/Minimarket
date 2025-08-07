import sqlite3
import tkinter as tk
from tkinter import messagebox

# Función para guardar un producto
def guardar_producto():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    descripcion = entry_descripcion.get()

    if not codigo or not nombre or not precio or not stock:
        messagebox.showwarning("Campos incompletos", "Por favor llena todos los campos obligatorios.")
        return

    try:
        conn = sqlite3.connect("minimarket.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (codigo_barras, nombre, precio, stock, descripcion)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo, nombre, float(precio), int(stock), descripcion))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Producto guardado correctamente.")
        entry_codigo.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_stock.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Ya existe un producto con ese código de barras.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Crear ventana
root = tk.Tk()
root.title("Ingreso de Productos")

# Campos de entrada
tk.Label(root, text="Código de Barras *").grid(row=0, column=0, sticky="e")
entry_codigo = tk.Entry(root)
entry_codigo.grid(row=0, column=1)

tk.Label(root, text="Nombre *").grid(row=1, column=0, sticky="e")
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=1, column=1)

tk.Label(root, text="Precio *").grid(row=2, column=0, sticky="e")
entry_precio = tk.Entry(root)
entry_precio.grid(row=2, column=1)

tk.Label(root, text="Stock *").grid(row=3, column=0, sticky="e")
entry_stock = tk.Entry(root)
entry_stock.grid(row=3, column=1)

tk.Label(root, text="Descripción").grid(row=4, column=0, sticky="e")
entry_descripcion = tk.Entry(root)
entry_descripcion.grid(row=4, column=1)

# Botón para guardar
btn_guardar = tk.Button(root, text="Guardar Producto", command=guardar_producto)
btn_guardar.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()

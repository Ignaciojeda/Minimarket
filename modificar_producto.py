import sqlite3
import tkinter as tk
from tkinter import messagebox

def buscar_producto():
    codigo = entry_codigo.get()
    if not codigo:
        messagebox.showwarning("Atención", "Ingresa un código de barras.")
        return

    conn = sqlite3.connect("minimarket.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio, stock FROM productos WHERE codigo_barras = ?", (codigo,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nombre, precio, stock = resultado
        entry_nombre.config(state="normal")
        entry_precio.config(state="normal")
        entry_stock.config(state="normal")
        entry_nombre.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_stock.delete(0, tk.END)
        entry_nombre.insert(0, nombre)
        entry_precio.insert(0, str(precio))
        entry_stock.insert(0, str(stock))
        entry_nombre.config(state="disabled")
        btn_guardar.config(state="normal")
    else:
        messagebox.showerror("Error", "Producto no encontrado.")
        limpiar_campos()

def guardar_cambios():
    codigo = entry_codigo.get()
    nuevo_precio = entry_precio.get()
    nuevo_stock = entry_stock.get()

    try:
        conn = sqlite3.connect("minimarket.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos
            SET precio = ?, stock = ?
            WHERE codigo_barras = ?
        """, (float(nuevo_precio), int(nuevo_stock), codigo))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def limpiar_campos():
    entry_nombre.config(state="normal")
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)
    entry_nombre.config(state="disabled")
    btn_guardar.config(state="disabled")

# GUI
root = tk.Tk()
root.title("Modificar Producto")

tk.Label(root, text="Código de Barras:").grid(row=0, column=0, padx=5, pady=5)
entry_codigo = tk.Entry(root)
entry_codigo.grid(row=0, column=1)
entry_codigo.bind("<Return>", lambda e: buscar_producto())

tk.Label(root, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(root, state="disabled")
entry_nombre.grid(row=1, column=1)

tk.Label(root, text="Precio:").grid(row=2, column=0, padx=5, pady=5)
entry_precio = tk.Entry(root)
entry_precio.grid(row=2, column=1)

tk.Label(root, text="Stock:").grid(row=3, column=0, padx=5, pady=5)
entry_stock = tk.Entry(root)
entry_stock.grid(row=3, column=1)

btn_guardar = tk.Button(root, text="Guardar Cambios", command=guardar_cambios, state="disabled")
btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

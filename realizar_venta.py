import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Variables globales
carrito = []

# Función para buscar producto por código de barras
def agregar_producto(event=None):
    codigo = entry_codigo.get()
    if not codigo:
        return
    
    conn = sqlite3.connect("minimarket.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio, stock FROM productos WHERE codigo_barras = ?", (codigo,))
    producto = cursor.fetchone()
    conn.close()

    if producto:
        nombre, precio, stock = producto
        if stock <= 0:
            messagebox.showwarning("Sin stock", f"No hay stock disponible para '{nombre}'")
            return

        # Buscar si ya está en el carrito
        for item in carrito:
            if item["codigo"] == codigo:
                if item["cantidad"] < stock:
                    item["cantidad"] += 1
                    item["subtotal"] = item["cantidad"] * item["precio"]
                else:
                    messagebox.showinfo("Límite", "No hay más stock disponible.")
                break
        else:
            carrito.append({
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "cantidad": 1,
                "subtotal": precio
            })

        actualizar_tabla()
        entry_codigo.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Producto no encontrado.")

# Actualizar tabla del carrito
def actualizar_tabla():
    for row in tabla_carrito.get_children():
        tabla_carrito.delete(row)
    
    total = 0
    for item in carrito:
        tabla_carrito.insert("", "end", values=(item["codigo"], item["nombre"], item["cantidad"], f"${item['precio']:.0f}", f"${item['subtotal']:.0f}"))
        total += item["subtotal"]

    label_total.config(text=f"Total: ${total:.0f}")

# Finalizar venta
def finalizar_venta():
    if not carrito:
        messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")
        return

    total = sum(item["subtotal"] for item in carrito)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("minimarket.db")
    cursor = conn.cursor()

    try:
        # Insertar en tabla ventas
        cursor.execute("INSERT INTO ventas (fecha, total) VALUES (?, ?)", (fecha, total))
        venta_id = cursor.lastrowid

        # Insertar en detalle_venta y actualizar stock
        for item in carrito:
            cursor.execute("""
                INSERT INTO detalle_venta (venta_id, codigo_barras, cantidad, subtotal)
                VALUES (?, ?, ?, ?)
            """, (venta_id, item["codigo"], item["cantidad"], item["subtotal"]))

            # Actualizar stock
            cursor.execute("""
                UPDATE productos
                SET stock = stock - ?
                WHERE codigo_barras = ?
            """, (item["cantidad"], item["codigo"]))

        conn.commit()
        conn.close()

        carrito.clear()
        actualizar_tabla()
        messagebox.showinfo("Venta realizada", "La venta se ha registrado con éxito.")

    except Exception as e:
        conn.rollback()
        conn.close()
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# GUI
root = tk.Tk()
root.title("Realizar Venta")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Escanea el producto:").grid(row=0, column=0, padx=5)
entry_codigo = tk.Entry(frame_top, font=('Arial', 16), width=25)
entry_codigo.grid(row=0, column=1)
entry_codigo.focus()
entry_codigo.bind("<Return>", agregar_producto)

# Tabla del carrito
cols = ("Código", "Producto", "Cantidad", "Precio", "Subtotal")
tabla_carrito = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tabla_carrito.heading(col, text=col)
tabla_carrito.pack(padx=10, pady=10)

label_total = tk.Label(root, text="Total: $0", font=("Arial", 16))
label_total.pack(pady=10)

btn_finalizar = tk.Button(root, text="Finalizar Venta", font=("Arial", 14), command=finalizar_venta)
btn_finalizar.pack(pady=5)

root.mainloop()

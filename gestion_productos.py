import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_PATH = "minimarket.db"  # corregí que antes usabas "inventario.db" al eliminar, unifiqué

def obtener_productos(filtrar_stock=None):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    query = "SELECT * FROM productos"
    params = []

    if filtrar_stock is not None:
        query += " WHERE stock <= ?"
        params.append(filtrar_stock)

    query += " ORDER BY stock ASC"  # ordenar por stock ascendente

    cursor.execute(query, params)
    productos = cursor.fetchall()
    conexion.close()
    return productos

def eliminar_producto(id_producto):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()
    conexion.close()

def cargar_productos_en_tabla(filtrar_stock=None):
    # Limpiar tabla
    for item in tree.get_children():
        tree.delete(item)

    productos = obtener_productos(filtrar_stock)

    for producto in productos:
        # Asumiendo que producto es (id, algo, nombre, precio, stock, descripcion)
        tree.insert("", tk.END, values=(producto[0], producto[2], producto[3], producto[4], producto[5]))

def on_eliminar():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Atención", "Selecciona un producto para eliminar.")
        return

    # Confirmar eliminación
    respuesta = messagebox.askyesno("Confirmar", "¿Seguro quieres eliminar el producto seleccionado?")
    if not respuesta:
        return

    id_producto = tree.item(selected_item)["values"][0]
    eliminar_producto(id_producto)
    messagebox.showinfo("Éxito", f"Producto con ID {id_producto} eliminado.")
    cargar_productos_en_tabla(entry_stock.get() or None)

def on_filtrar():
    filtro = entry_stock.get()
    if filtro:
        try:
            filtro_num = int(filtro)
        except ValueError:
            messagebox.showerror("Error", "El filtro de stock debe ser un número entero.")
            return
    else:
        filtro_num = None

    cargar_productos_en_tabla(filtro_num)

# Configuración ventana principal
root = tk.Tk()
root.title("Inventario de Productos")

# Filtro stock
frame_filtro = tk.Frame(root)
frame_filtro.pack(padx=10, pady=5, fill="x")

tk.Label(frame_filtro, text="Mostrar productos con stock <= ").pack(side=tk.LEFT)
entry_stock = tk.Entry(frame_filtro, width=10)
entry_stock.pack(side=tk.LEFT, padx=5)
btn_filtrar = tk.Button(frame_filtro, text="Filtrar", command=on_filtrar)
btn_filtrar.pack(side=tk.LEFT)

# Tabla productos
columns = ("ID", "Nombre", "Precio", "Stock", "Descripción")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, minwidth=50, width=120, anchor=tk.W)

tree.pack(padx=10, pady=10, fill="both", expand=True)

# Botón eliminar
btn_eliminar = tk.Button(root, text="Eliminar producto seleccionado", command=on_eliminar)
btn_eliminar.pack(pady=5)

# Carga inicial sin filtro
cargar_productos_en_tabla()

root.mainloop()

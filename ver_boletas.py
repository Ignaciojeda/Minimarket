import sqlite3
import tkinter as tk
from tkinter import messagebox

def ver_boletas(filtro_precio=None, filtro_fecha=None):
    conexion = sqlite3.connect("minimarket.db")
    cursor = conexion.cursor()

    query = "SELECT * FROM boletas WHERE 1=1"
    params = []

    if filtro_precio is not None:
        query += " AND total >= ?"
        params.append(filtro_precio)

    if filtro_fecha is not None and filtro_fecha.strip() != "":
        query += " AND fecha = ?"
        params.append(filtro_fecha)

    cursor.execute(query, params)
    boletas = cursor.fetchall()

    resultados = ""

    for boleta in boletas:
        resultados += f"\nBoleta ID: {boleta[0]}, Fecha: {boleta[1]}, Total: ${boleta[2]:.2f}\n"
        cursor.execute("SELECT producto_id, cantidad, subtotal FROM detalle_boleta WHERE boleta_id = ?", (boleta[0],))
        detalles = cursor.fetchall()
        for detalle in detalles:
            resultados += f"   Producto ID: {detalle[0]}, Cantidad: {detalle[1]}, Subtotal: ${detalle[2]:.2f}\n"

    conexion.close()
    return resultados

def mostrar_boletas():
    try:
        precio = entry_precio.get()
        fecha = entry_fecha.get()

        # Validar precio: si está vacío, usar None, sino convertir a float
        filtro_precio = float(precio) if precio else None
        filtro_fecha = fecha if fecha else None

        resultado = ver_boletas(filtro_precio, filtro_fecha)
        text_resultados.delete(1.0, tk.END)
        if resultado.strip() == "":
            text_resultados.insert(tk.END, "No se encontraron boletas con esos filtros.")
        else:
            text_resultados.insert(tk.END, resultado)
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número válido.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Consulta de Boletas")

# Etiquetas y entradas para filtros
tk.Label(root, text="Precio mínimo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_precio = tk.Entry(root)
entry_precio.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_fecha = tk.Entry(root)
entry_fecha.grid(row=1, column=1, padx=5, pady=5)

# Botón para ejecutar la búsqueda
btn_mostrar = tk.Button(root, text="Mostrar Boletas", command=mostrar_boletas)
btn_mostrar.grid(row=2, column=0, columnspan=2, pady=10)

# Área de texto para mostrar resultados
text_resultados = tk.Text(root, width=60, height=20)
text_resultados.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

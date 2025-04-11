import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

 
conn = mysql.connector.connect(
    host="localhost",         
    user="root",        
    password="", 
    database="agendacontactos"  
)
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS contactos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        telefono VARCHAR(20) NOT NULL,
        correo VARCHAR(100) NOT NULL
    )
''')
conn.commit()



def cargar_contactos():
    for item in tabla.get_children():
        tabla.delete(item)
    cursor.execute('SELECT * FROM contactos')
    for row in cursor.fetchall():
        tabla.insert("", "end", values=row)

def agregar_contacto():
    nombre = entrada_nombre.get()
    telefono = entrada_telefono.get()
    correo = entrada_correo.get()

    if nombre and telefono and correo:
        cursor.execute('INSERT INTO contactos (nombre, telefono, correo) VALUES (%s, %s, %s)', (nombre, telefono, correo))
        conn.commit()
        cargar_contactos()
        entrada_nombre.delete(0, tk.END)
        entrada_telefono.delete(0, tk.END)
        entrada_correo.delete(0, tk.END)
    else:
        messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")

def eliminar_contacto():
    seleccionado = tabla.selection()
    if seleccionado:
        item = tabla.item(seleccionado)
        id_contacto = item["values"][0]
        cursor.execute('DELETE FROM contactos WHERE id = %s', (id_contacto,))
        conn.commit()
        cargar_contactos()
    else:
        messagebox.showwarning("Selecciona un contacto", "Primero selecciona un contacto para eliminar.")

def editar_contacto():
    seleccionado = tabla.selection()
    if seleccionado:
        item = tabla.item(seleccionado)
        id_contacto = item["values"][0]
        nombre = entrada_nombre.get()
        telefono = entrada_telefono.get()
        correo = entrada_correo.get()

        if nombre and telefono and correo:
            cursor.execute('UPDATE contactos SET nombre = %s, telefono = %s, correo = %s WHERE id = %s',
                           (nombre, telefono, correo, id_contacto))
            conn.commit()
            cargar_contactos()
            entrada_nombre.delete(0, tk.END)
            entrada_telefono.delete(0, tk.END)
            entrada_correo.delete(0, tk.END)
        else:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos para editar.")
    else:
        messagebox.showwarning("Selecciona un contacto", "Selecciona un contacto para editar.")

def buscar_contacto(event=None):
    busqueda = entrada_busqueda.get()
    for item in tabla.get_children():
        tabla.delete(item)
    cursor.execute("SELECT * FROM contactos WHERE nombre LIKE %s OR telefono LIKE %s OR correo LIKE %s",
                   (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"))
    for row in cursor.fetchall():
        tabla.insert("", "end", values=row)

def llenar_campos(event):
    seleccionado = tabla.selection()
    if seleccionado:
        item = tabla.item(seleccionado)
        entrada_nombre.delete(0, tk.END)
        entrada_telefono.delete(0, tk.END)
        entrada_correo.delete(0, tk.END)

        entrada_nombre.insert(0, item["values"][1])
        entrada_telefono.insert(0, item["values"][2])
        entrada_correo.insert(0, item["values"][3])



ventana = tk.Tk()
ventana.title("Agenda de Contactos con HeidiSQL (MySQL)")


tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
entrada_nombre = tk.Entry(ventana)
entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(ventana, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5)
entrada_telefono = tk.Entry(ventana)
entrada_telefono.grid(row=1, column=1, padx=5, pady=5)

tk.Label(ventana, text="Correo:").grid(row=2, column=0, padx=5, pady=5)
entrada_correo = tk.Entry(ventana)
entrada_correo.grid(row=2, column=1, padx=5, pady=5)


tk.Button(ventana, text="Agregar", command=agregar_contacto).grid(row=0, column=2, padx=5, pady=5)
tk.Button(ventana, text="Editar", command=editar_contacto).grid(row=1, column=2, padx=5, pady=5)
tk.Button(ventana, text="Eliminar", command=eliminar_contacto).grid(row=2, column=2, padx=5, pady=5)


tk.Label(ventana, text="Buscar:").grid(row=3, column=0, padx=5, pady=5)
entrada_busqueda = tk.Entry(ventana)
entrada_busqueda.grid(row=3, column=1, padx=5, pady=5)
entrada_busqueda.bind("<KeyRelease>", buscar_contacto)

columnas = ("ID", "Nombre", "Teléfono", "Correo")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
for col in columnas:
    tabla.heading(col, text=col)
tabla.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
tabla.bind("<<TreeviewSelect>>", llenar_campos)


cargar_contactos()


ventana.mainloop()

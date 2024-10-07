import tkinter as tk, tkinter.ttk as ttk
import sqlite3    
con = sqlite3.connect('contra.db')
cur = con.cursor()

id_map = {}

def insertar():
    usuario = usu.get()
    contraseña = contra.get()
    descripcion = desc.get()
    cur.execute("Insert INTO contraseñas (usuario,contraseña,descripcion) values (?,?,?)",( usuario, contraseña, descripcion ))
    con.commit()
    actulist()

def actulist():
    lista.delete(0, tk.END)
    id_map.clear()
    cur.execute("SELECT id_contra, usuario, contraseña, descripcion FROM contraseñas")
    con.commit()
    for i, row in enumerate(cur.fetchall()):
        lista.insert(tk.END, f"Usuario: {row[1]}, Contraseña: {row[2]}, Descripción: {row[3]}")
        id_map[i] = row[0]  # Mapea el índice de la lista al id de la base de datos

def borrar():
    select = lista.curselection()
    if select:
        index = select[0]
        item_id = id_map[index]
        cur.execute("DELETE FROM contraseñas WHERE id_contra=?", (item_id,))
        con.commit()
        actulist()

def modificar():
    usuario = usu.get()
    contraseña = contra.get()
    descripcion = desc.get()
    select = lista.curselection()
    if select:
        page = select[0]
        id = id_map[page]
        con.execute("UPDATE contraseñas SET usuario=?, contraseña=?, descripcion=? where id_contra =?", (usuario, contraseña, descripcion, id))
    actulist()


def inicio():

    def igual():
        ventana2.destroy()
        ventana.deiconify()

    ventana2 = tk.Tk()
    ventana2.title('gestor de contraseñas')
    ventana2.geometry('400x300')

    etiqueta = tk.Label(ventana2, text='ingrese su nombre:')
    etiqueta.pack()

    nombre = ttk.Entry(ventana2, width=30)
    nombre.pack()

    etiqueta2 = tk.Label(ventana2, text='ingrese su contraseña:')
    etiqueta2.pack()

    contraseña = ttk.Entry(ventana2, width=30)
    contraseña.pack()

    ingresar = ttk.Button(ventana2, text="comprobar", command=igual)
    ingresar.pack()

    ventana2.mainloop()

#ventana de la aplicacion
ventana = tk.Tk()
ventana.title("Gestor de contraseñas")
ventana.geometry("599x300")

ventana.withdraw()

#frame text
texto = ttk.Frame(ventana)
texto.pack(side='left', fill='both', padx=5, pady=5)

#escribir contraseñas
label_contra = ttk.Label(texto, text="Ingrese una usuario:")
label_contra.pack(anchor='w', padx=5, pady=5)
usu = ttk.Entry(texto)
usu.pack(anchor='w',padx=5, pady=5)
label_contra = ttk.Label(texto, text="Ingrese su contraseña:")
label_contra.pack( anchor='w', padx=5, pady=5)
contra = ttk.Entry(texto)
contra.pack(anchor='w', padx=5, pady=5)
label_contra = ttk.Label(texto, text="Ingrese una Descripcion:")
label_contra.pack(anchor='w', padx=5, pady=5)
desc = ttk.Entry(texto)
desc.pack(anchor='w',padx=5, pady=5)
divlist = ttk.Frame(ventana)
divlist.pack(side='left', fill='both', expand=True, padx=5, pady=5)

# Lista de contraseñas
lista = tk.Listbox(divlist)
lista.pack(fill='both', expand=True, padx=0.5, pady=0.5)

#frame botones
divbotones = ttk.Frame(ventana)
divbotones.pack(side='right', fill='both', padx=10, pady=5)

#botones de accion
boton = ttk.Button(divbotones, text="Insertar", command= insertar)
boton.pack(anchor='e', padx=10, pady=5)
boton = ttk.Button(divbotones, text="Borrar", command= borrar)
boton.pack(anchor='e', padx=10, pady=5)
boton = ttk.Button(divbotones, text="Modificar", command= modificar)
boton.pack(anchor='e', padx=10, pady=5)

#mostrar la lista
actulist()

inicio()
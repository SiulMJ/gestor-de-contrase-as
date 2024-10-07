import tkinter as tk, tkinter.ttk as ttk
import sqlite3    
con = sqlite3.connect('contra.db')
cur = con.cursor()

id_map = {}

def insertar():
    pagina = pag.get()
    contraseña = contra.get()
    descripcion = desc.get()
    cur.execute("Insert INTO contraseñas (pagina,contraseña,descripcion) values (?,?,?)",( pagina, contraseña, descripcion ))
    con.commit()
    actulist()

def actulist():
    lista.delete(0, tk.END)
    id_map.clear()
    cur.execute("SELECT id_contraseñas, pagina, contraseña, descripcion FROM contraseñas")
    con.commit()
    for i, row in enumerate(cur.fetchall()):
        lista.insert(tk.END, f"Usuario: {row[1]}, Contraseña: {row[2]}, Descripción: {row[3]}")
        id_map[i] = row[0]

def registrar(ev):
    registro = tk.Toplevel()
    registro.geometry("400x200")
    registro.title("registrar")
    reg = ttk.Frame(registro, padding="20")
    reg.pack(expand=True)
    tk.Label(reg, text='ingrese su nombre:').grid(row=0, column=0, pady=10, sticky="w")
    nombre = ttk.Entry(reg, width=30)
    nombre.grid(row=0, column=1, pady=10)

    tk.Label(reg, text='ingrese su contraseña: ').grid(row=1, column=0, pady=10, sticky="w")
    contraseña = ttk.Entry(reg, width=30, show="*")
    contraseña.grid(row=1, column=1, pady=10)

    ttk.Button(reg, text="registrar", command="#").grid(row=2, column=0, columnspan=2, pady=20)


def borrar():
    select = lista.curselection()
    if select:
        index = select[0]
        item_id = id_map[index]
        cur.execute("DELETE FROM contraseñas WHERE id_contraseñas=?", (item_id,))
        con.commit()
        actulist()

def modificar():
    pagina = pagina.get()
    contraseña = contra.get()
    descripcion = desc.get()
    select = lista.curselection()
    if select:
        page = select[0]
        id = id_map[page]
        con.execute("UPDATE contraseñas SET pagina=?, contraseña=?, descripcion=? where id_contraseñas =?", (pagina, contraseña, descripcion, id))
    actulist()

def cerrar():
    ventana.quit()

def inicio():

    def igual():
        ventana2.destroy()
        ventana.deiconify()
        

    ventana2 = tk.Tk()
    ventana2.title('gestor de contraseñas')
    ventana2.geometry('400x300')
    login = ttk.Frame(ventana2, padding="20")
    login.pack(expand=True)
    ventana2.protocol("WM_DELETE_WINDOW", cerrar)

    tk.Label(login, text='ingrese su nombre:').grid(row=0, column=0, pady=10, sticky="w")
    nombre = ttk.Entry(login, width=30)
    nombre.grid(row=0, column=1, pady=10)

    tk.Label(login, text='ingrese su contraseña: ').grid(row=1, column=0, pady=10, sticky="w")
    contraseña = ttk.Entry(login, width=30, show="*")
    contraseña.grid(row=1, column=1, pady=10)

    ttk.Button(login, text="comprobar", command=igual).grid(row=2, column=0, columnspan=2, pady=20)
    
    etiqueta = ttk.Label(login, text='¿Notienes usuario?')
    etiqueta.grid(row=3, column=0, columnspan=2, pady=20)
    etiqueta.bind('<Button-1>', registrar)


    
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
label_contra = ttk.Label(texto, text="Ingrese una pagina:")
label_contra.pack(anchor='w', padx=5, pady=5)
pag = ttk.Entry(texto)
pag.pack(anchor='w',padx=5, pady=5)
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

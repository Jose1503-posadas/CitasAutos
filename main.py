import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
from vPub import VentanaUsuario

class Modelo:
    def __init__(self):
        #Conexiones a la base de datos
        self.conn = sqlite3.connect("database.db")
        self.conn_log = sqlite3.connect("login.db")
        #Métodos para crear las tablas
        self.crearTablaUsuarios()
        self.crearTablaLogin()

    # Crear tabla de usuarios
    def crearTablaUsuarios(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombreUsuario TEXT UNIQUE,
                            password TEXT,
                            avatar TEXT)''')
        #Confirma transaccion
        self.conn.commit()
    
    # Crear tabla de login
    def crearTablaLogin(self):
        cursor = self.conn_log.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS login (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombreUsuario TEXT,
                            FechaHora TEXT)''')
        self.conn_log.commit()

    def validarLogin(self, nombreUsuario, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombreUsuario=? AND password=?", (nombreUsuario, password))
        user = cursor.fetchone()
        if user:
            # Accede a los elementos de la tupla por índices numéricos
            nombreUsuario = user[1]  # El segundo elemento contiene el nombre de usuario
            avatar = user[3]          # El cuarto elemento contiene el avatar
            return {'nombreUsuario': nombreUsuario, 'avatar': avatar}
        else:
            #Si no se encuentra regresa none
            return None

    #Inserta nuevo usuario en la BD, tabla usuarios
    def registroUsuarioBD(self, nombreUsuario, password, avatar):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombreUsuario, password, avatar) VALUES (?, ?, ?)", (nombreUsuario, password, avatar))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    #registrar el inicio de sesión de un usuario en una base de datos
    def login(self, nombreUsuario):
        FechaHora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.conn_log.cursor()
        cursor.execute("INSERT INTO login (nombreUsuario, FechaHora) VALUES (?, ?)", (nombreUsuario, FechaHora))
        self.conn_log.commit()

#Subclase de la principal, da funcioanlidades para ventanas 
class Vista(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        #Comunicacion con el controlador
        self.controlador = controlador
        self.title("Micro-X")
        self.geometry("400x250")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.login_tab = ttk.Frame(self.notebook)
        self.register_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.login_tab, text="Iniciar Sesión")
        self.notebook.add(self.register_tab, text="Registrarse")

        self.controlador.mostrarLogin(self.login_tab)
        self.controlador.mostrarRegistro(self.register_tab)

    #Metodo para mostrar y ocultar ventana
    def mostrarUsuario(self, user):
        self.login_tab.pack_forget()  # Oculta la pestaña de inicio de sesión
        self.controlador.mostrarUsuario(user)  # Muestra la ventana de usuario



class Controlador:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = Vista(self)

    def mostrarLogin(self, tab):
        VentanaLogin(tab, self)

    def mostrarRegistro(self, tab):
        VentanaRegistro(tab, self)

    def mostrarUsuario(self, user):
        self.ventana_usuario = VentanaUsuario(user)
        
    def registroInicioSesion(self, username):
        self.modelo.login(username)


class VentanaLogin:
    #Metodo constructor 
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.username_label = ttk.Label(parent, text="Usuario:")
        self.username_label.pack()
        self.username_entry = ttk.Entry(parent)
        self.username_entry.pack()

        self.password_label = ttk.Label(parent, text="Contraseña:")
        self.password_label.pack()
        self.password_entry = ttk.Entry(parent, show="*")
        self.password_entry.pack()

        self.login_button = ttk.Button(parent, text="Iniciar Sesión", command=self.InicioSesion)
        self.login_button.pack()

    #Metodo cuando hace clic en boton "INICIO DE SESION"
    def InicioSesion(self):
        nombreUsuario = self.username_entry.get()
        password = self.password_entry.get()
        #Llama a metodo validarLogin()
        user = self.controlador.modelo.validarLogin(nombreUsuario, password)

        if user:
            messagebox.showinfo("Inicio de Sesión", "Sesión iniciada exitosamente")
            self.controlador.registroInicioSesion(nombreUsuario)
            self.controlador.mostrarUsuario(user)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


class VentanaRegistro:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.username_label = ttk.Label(parent, text="Usuario:")
        self.username_label.pack()
        self.username_entry = ttk.Entry(parent)
        self.username_entry.pack()

        self.password_label = ttk.Label(parent, text="Contraseña:")
        self.password_label.pack()
        self.password_entry = ttk.Entry(parent, show="*")
        self.password_entry.pack()

        self.avatar_label = ttk.Label(parent, text="Selecciona una imagen\n")
        self.avatar_label.pack()

        self.avatar_path = tk.StringVar()
        self.avatar_button = ttk.Button(parent, text="Seleccionar", command=self.eligeAvatar)
        self.avatar_button.pack()

        self.registrar_button = ttk.Button(parent, text="Registrarse", command=self.registrarUsuario)
        self.registrar_button.pack()
    
    #Metodo para cuando el usuario elige "SELECCIONA IMAGEN"
    def eligeAvatar(self):
        ruta_imagen = filedialog.askopenfilename()
        if ruta_imagen:
            self.avatar_path.set(ruta_imagen)

    #Clic en boton de "REGISTRO"
    def registrarUsuario(self):
        nombreUsuario = self.username_entry.get()
        password = self.password_entry.get()
        avatar = self.avatar_path.get()

        #Llama al metodo de registroBD para registrarlo en la BD
        registrado = self.controlador.modelo.registroUsuarioBD(nombreUsuario, password, avatar)

        if registrado:
            messagebox.showinfo("Registro", "Usuario registrado exitosamente")
        else:
            messagebox.showerror("Error", "El usuario ya existe en la base de datos.")


if __name__ == "__main__":
    controlador = Controlador()
    controlador.vista.mainloop()

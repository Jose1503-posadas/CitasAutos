import sqlite3
from tkinter import ttk, Tk
from PIL import Image, ImageTk
from tkinter import messagebox

# Importar la clase Publicacion o MiPublicacion según sea necesario
from misPublicaciones import miPublicacion
# o from nombre_de_tu_archivo import MiPublicacion

class Perfil:
    def __init__(self, ventana_usuario, nombre_usuario, avatar):
        self.ventana_usuario = ventana_usuario
        self.nombre_usuario = nombre_usuario
        self.avatar = avatar
        self.publicaciones_usuario = []  
        self.frame_perfil = None

    def cargar_publicaciones_usuario(self):
        conn = sqlite3.connect("publicaciones.db")
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, hora_fecha, contenido, imagen FROM publicaciones WHERE usuario = ? ORDER BY hora_fecha DESC", (self.nombre_usuario,))
        self.publicaciones_usuario = cursor.fetchall()
        conn.close()

    def mostrar_perfil(self):
        if self.frame_perfil:
            self.frame_perfil.destroy()

        self.frame_perfil = ttk.Frame(self.ventana_usuario.container)
        self.frame_perfil.pack()

        self.cargar_publicaciones_usuario()

        try:
            avatar_image = Image.open(self.avatar)
            avatar_image = avatar_image.resize((50, 50))  
            avatar_photo = ImageTk.PhotoImage(avatar_image)

            contenedor_avatar_nombre = ttk.Frame(self.frame_perfil)
            contenedor_avatar_nombre.pack(side="top", pady=20)  

            avatar_label = ttk.Label(contenedor_avatar_nombre, image=avatar_photo)
            avatar_label.image = avatar_photo
            avatar_label.pack(side="left", padx=(50, 10))  

            nombre_label = ttk.Label(contenedor_avatar_nombre, text=f"{self.nombre_usuario}", font=('Arial', 12, 'bold'))
            nombre_label.pack(side="left", padx=(10, 140))  

        except FileNotFoundError:
            error_label = ttk.Label(self.frame_perfil, text="Error: No se encontró la imagen.")
            error_label.pack()

        # Crear una instancia de la clase Publicacion o MiPublicacion según necesites
        publicacion_viewer = miPublicacion(self.frame_perfil)
        # o publicacion_viewer = MiPublicacion(self.frame_perfil)

        # Mostrar las publicaciones en el perfil
        for publicacion in self.publicaciones_usuario:
            publicacion_viewer.mostrar_publicacion(publicacion)

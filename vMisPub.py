import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk

class PublicacionBuilder:
    def __init__(self):
        self.usuario = ""
        self.fecha = ""
        self.contenido = ""
        self.imagen_path = ""
    
    def with_usuario(self, usuario):
        self.usuario = usuario
        return self
    
    def with_fecha(self, fecha):
        self.fecha = fecha
        return self
    
    def with_contenido(self, contenido):
        self.contenido = contenido
        return self
    
    def with_imagen_path(self, imagen_path):
        self.imagen_path = imagen_path
        return self
    
    def build(self):
        return (self.usuario, self.fecha, self.contenido, self.imagen_path)

class Perfil:
    def __init__(self, ventana_usuario, nombre_usuario, avatar):
        self.ventana_usuario = ventana_usuario
        self.nombre_usuario = nombre_usuario
        self.avatar = avatar
        self.publicaciones_usuario = []  # Lista para almacenar las publicaciones del usuario
        self.frame_perfil = None

    def cargar_publicaciones_usuario(self):
        # Conectar a la base de datos y obtener las publicaciones del usuario
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

        # Cargar las publicaciones del usuario desde la base de datos
        self.cargar_publicaciones_usuario()

        # Mostrar el avatar y el nombre del usuario
        try:
            avatar_image = Image.open(self.avatar)
            avatar_image = avatar_image.resize((50, 50))  # Redimensionar la imagen
            avatar_photo = ImageTk.PhotoImage(avatar_image)

            avatar_label = ttk.Label(self.frame_perfil, image=avatar_photo)
            avatar_label.image = avatar_photo  # Mantener una referencia
            avatar_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

            nombre_label = ttk.Label(self.frame_perfil, text=f"{self.nombre_usuario}", font=('Arial', 12, 'bold'))
            nombre_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        except FileNotFoundError:
            error_label = ttk.Label(self.frame_perfil, text="Error: No se encontró la imagen.")
            error_label.pack()

        # Mostrar las publicaciones del usuario actual
        row_index = 1
        for publicacion in self.publicaciones_usuario:
            self.mostrar_publicacion(publicacion, row_index)
            row_index += 1

    def mostrar_publicacion(self, publicacion, row_index):
        usuario, fecha, contenido, imagen_path = publicacion

        # Crear un marco para la publicación con fondo violeta
        frame_publicacion = ttk.Frame(self.frame_perfil, style="Custom.TFrame")
        frame_publicacion.grid(row=row_index, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Establecer el estilo para el fondo violeta del contenedor
        s = ttk.Style()
        s.configure("Custom.TFrame", background="dark violet")

        # Etiqueta para el nombre de usuario
        nombre_label = ttk.Label(frame_publicacion, text=usuario, font=("Arial", 16, "bold"), background="dark violet", foreground="white")
        nombre_label.grid(row=0, column=0, sticky="w")

        # Etiqueta para la fecha (solo la parte de la fecha)
        fecha_solo = fecha.split()[1]  # Extraer solo la parte de la fecha
        fecha_label = ttk.Label(frame_publicacion, text=f"Fecha: {fecha_solo}", background="dark violet", foreground="white")
        fecha_label.grid(row=1, column=0, sticky="w")

        # Etiqueta para el contenido
        contenido_label = ttk.Label(frame_publicacion, text=f"Contenido: {contenido}", background="dark violet", foreground="white", wraplength=500)
        contenido_label.grid(row=2, column=0, sticky="w")

        # Etiqueta para la imagen si está presente
        if imagen_path:
            imagen_content = Image.open(imagen_path)
            imagen_content = imagen_content.resize((200, 200), Image.BILINEAR)
            imagen_tk = ImageTk.PhotoImage(imagen_content)
            imagen_label = ttk.Label(frame_publicacion, image=imagen_tk, background="dark violet")
            imagen_label.image = imagen_tk
            imagen_label.grid(row=3, column=0, columnspan=2, sticky="w")

import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk

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
            # Cargar la imagen del avatar
            avatar_image = Image.open(self.avatar)
            avatar_image = avatar_image.resize((50, 50))  # Redimensionar la imagen
            avatar_photo = ImageTk.PhotoImage(avatar_image)

            contenedor_avatar_nombre = ttk.Frame(self.frame_perfil)
            contenedor_avatar_nombre.pack(side="top", pady=20)  # Empaqueta el contenedor en la parte superior con un relleno vertical de 20 píxeles

            avatar_label = ttk.Label(contenedor_avatar_nombre, image=avatar_photo)
            avatar_label.image = avatar_photo
            avatar_label.pack(side="left", padx=(50, 10))  # Ajusta el relleno horizontal

            nombre_label = ttk.Label(contenedor_avatar_nombre, text=f"{self.nombre_usuario}", font=('Arial', 12, 'bold'))
            nombre_label.pack(side="left", padx=(10, 140))  # Ajusta el relleno horizontal



        except FileNotFoundError:
            error_label = ttk.Label(self.frame_perfil, text="Error: No se encontró la imagen.")
            error_label.pack()


        # Mostrar las publicaciones del usuario actual
        for publicacion in self.publicaciones_usuario:
            self.mostrar_publicacion(publicacion)

    def mostrar_publicacion(self, publicacion):
        usuario, fecha, contenido, imagen_path = publicacion

        # Crear un marco para la publicación con fondo violeta
        frame_publicacion = ttk.Frame(self.frame_perfil, style="Custom.TFrame")
        frame_publicacion.pack(padx=10, pady=10, fill="both")

        # Establecer el estilo para el fondo violeta del contenedor
        s = ttk.Style()
        s.configure("Custom.TFrame", background="dark violet")

        # Etiqueta para el nombre de usuario
        nombre_label = ttk.Label(frame_publicacion, text=usuario, font=("Arial", 16, "bold"), background="dark violet", foreground="white")
        nombre_label.pack(anchor="w")

        # Etiqueta para la fecha (solo la parte de la fecha)
        fecha_solo = fecha.split()[1]  # Extraer solo la parte de la fecha
        fecha_label = ttk.Label(frame_publicacion, text=f"Fecha: {fecha_solo}", background="dark violet", foreground="white")
        fecha_label.pack(anchor="w")

        # Etiqueta para el contenido
        contenido_label = ttk.Label(frame_publicacion, text=f"Contenido: {contenido}", background="dark violet", foreground="white", wraplength=500)
        contenido_label.pack(anchor="w")

        # Etiqueta para la imagen si está presente
        if imagen_path:
            imagen_content = Image.open(imagen_path)
            imagen_content = imagen_content.resize((200, 200), Image.BILINEAR)
            imagen_tk = ImageTk.PhotoImage(imagen_content)
            imagen_label = ttk.Label(frame_publicacion, image=imagen_tk, background="dark violet")
            imagen_label.image = imagen_tk
            imagen_label.pack(anchor="w")

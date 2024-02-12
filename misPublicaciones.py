import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

COLOR_FONDO_CONTENEDOR = "dark violet"

class miPublicacion:
    def __init__(self, container):
        self.container = container

    def actualizar_publicaciones(self):
        # Limpiar las publicaciones anteriores
        for widget in self.container.winfo_children():
            widget.destroy()

        # Conectar a la base de datos y obtener las publicaciones
        conn = sqlite3.connect("publicaciones.db")
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, hora_fecha, contenido, imagen FROM publicaciones ORDER BY hora_fecha DESC",(self.nombre_usuario,))  # Seleccionar solo las columnas necesarias
        publicaciones = cursor.fetchall()
        conn.close()

        # Mostrar las publicaciones en la ventana
        for publicacion in publicaciones:
            self.mostrar_publicacion(publicacion)

    def mostrar_publicacion(self, publicacion):
        usuario, fecha, contenido, imagen_path = publicacion

        # Crear un marco para la publicación
        frame_publicacion = ttk.Frame(self.container, style="Custom.TFrame")
        frame_publicacion.pack(pady=20, padx=20, fill="both")

        # Establecer el estilo para el fondo
        s = ttk.Style()
        s.configure("Custom.TFrame", background=COLOR_FONDO_CONTENEDOR)

        # Etiqueta para el nombre de usuario
        nombre_label = tk.Label(frame_publicacion, text=usuario, font=("Arial", 20, "bold"), bg=COLOR_FONDO_CONTENEDOR, fg="white")
        nombre_label.pack(fill="x")  # Hacer que la etiqueta se expanda horizontalmente

        # Etiqueta para la fecha (solo la parte de la fecha)
        fecha_solo = fecha.split()[1]  # Extraer solo la parte de la fecha
        tk.Label(frame_publicacion, text=f"Fecha: {fecha_solo}", bg=COLOR_FONDO_CONTENEDOR, fg="white").pack(fill="x")
        
        # Etiqueta para el contenido
        tk.Label(frame_publicacion, text=f"Contenido: {contenido}", bg=COLOR_FONDO_CONTENEDOR, fg="white").pack(fill="x")
        
        # Etiqueta para la imagen si está presente
        if imagen_path:
            imagenContent = Image.open(imagen_path)
            imagenContent = imagenContent.resize((200, 200), Image.BILINEAR)
            imagen_tk = ImageTk.PhotoImage(imagenContent)
            imagen_label = tk.Label(frame_publicacion, image=imagen_tk, bg=COLOR_FONDO_CONTENEDOR, fg="white")
            imagen_label.image = imagen_tk
            imagen_label.pack(fill="both", expand=True)  # Hacer que la imagen se expanda horizontal y verticalmente

        # Botones para eliminar y editar la publicación
        boton_eliminar = tk.Button(frame_publicacion, text="Eliminar", command=lambda: self.eliminar_publicacion(usuario, fecha, contenido))
        boton_eliminar.pack(side="left", padx=(30, 10), pady=10)

        boton_editar = tk.Button(frame_publicacion, text="Editar", command=lambda: self.editar_publicacion(usuario, fecha, contenido, imagen_path))
        boton_editar.pack(side="left", padx=(100, 10), pady=10)

    def eliminar_publicacion(self, usuario, fecha, contenido):
        pass

    def editar_publicacion(self, usuario, fecha, contenido, imagen_path):
        # Aquí puedes implementar la lógica para editar la publicación
        pass

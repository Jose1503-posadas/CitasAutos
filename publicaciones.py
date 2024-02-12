import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

COLOR_FONDO_CONTENEDOR = "dark violet"

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

class PublicacionDirector:
    def construir_publicacion(self, builder, usuario, fecha, contenido, imagen_path=""):
        return builder.with_usuario(usuario) \
                      .with_fecha(fecha) \
                      .with_contenido(contenido) \
                      .with_imagen_path(imagen_path) \
                      .build()

class Publicacion:
    def __init__(self, container):
        self.container = container
        self.ventana_agrandada = None  # Para almacenar la ventana agrandada

    def actualizar_publicaciones(self):
        # Limpiar las publicaciones anteriores
        for widget in self.container.winfo_children():
            widget.destroy()

        # Conectar a la base de datos y obtener las publicaciones
        conn = sqlite3.connect("publicaciones.db")
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, hora_fecha, contenido, imagen FROM publicaciones ORDER BY hora_fecha DESC")  # Seleccionar solo las columnas necesarias
        publicaciones = cursor.fetchall()
        conn.close()

        # Mostrar las publicaciones en la ventana
        for publicacion in publicaciones:
            self.mostrar_publicacion(publicacion)

    def mostrar_publicacion(self, publicacion):
        usuario, fecha, contenido, imagen_path = publicacion

        # Crear un marco para la publicación con fondo violeta
        frame_publicacion = ttk.Frame(self.container, style="Custom.TFrame")
        frame_publicacion.pack(pady=20, padx=90, fill="x")

        # Establecer el estilo para el fondo violeta del contenedor
        s = ttk.Style()
        s.configure("Custom.TFrame", background=COLOR_FONDO_CONTENEDOR)

        # Etiqueta para el nombre de usuario
        nombre_label = tk.Label(frame_publicacion, text=usuario, font=("Arial", 20, "bold"), bg=COLOR_FONDO_CONTENEDOR, fg="white")
        nombre_label.grid(row=0, column=0, sticky="w")

        # Etiqueta para la fecha (solo la parte de la fecha)
        fecha_solo = fecha.split()[1]  # Extraer solo la parte de la fecha
        tk.Label(frame_publicacion, text=f"Fecha: {fecha_solo}", bg=COLOR_FONDO_CONTENEDOR, fg="white").grid(row=1, column=0, sticky="w")
        
        # Etiqueta para el contenido
        tk.Label(frame_publicacion, text=f"Contenido: {contenido}", bg=COLOR_FONDO_CONTENEDOR, fg="white").grid(row=2, column=0, sticky="w")
        
        # Etiqueta para la imagen si está presente
        if imagen_path:
            imagenContent = Image.open(imagen_path)
            imagenContent = imagenContent.resize((200, 200), Image.BILINEAR)
            imagen_tk = ImageTk.PhotoImage(imagenContent)
            imagen_label = tk.Label(frame_publicacion, image=imagen_tk, bg=COLOR_FONDO_CONTENEDOR, fg="white")
            imagen_label.image = imagen_tk
            imagen_label.grid(row=3, column=0, columnspan=2)
        
        # Botón para agrandar
        boton_agrandar = tk.Button(frame_publicacion, text="Agrandar", command=lambda pub=publicacion: self.abrir_ventana_agrandada(pub))
        boton_agrandar.grid(row=4, column=0, columnspan=2, sticky="we", padx=5, pady=5)

    def abrir_ventana_agrandada(self, publicacion):
        # Cerrar la ventana agrandada si ya está abierta
        if self.ventana_agrandada:
            self.ventana_agrandada.destroy()

        # Crear una nueva ventana
        self.ventana_agrandada = tk.Toplevel()
        self.ventana_agrandada.title("vPubDetalle")
        self.ventana_agrandada.geometry("400x300")
        
        # Mostrar el contenido de la publicación en la ventana agrandada
        usuario, fecha, contenido, imagen_path = publicacion
        tk.Label(self.ventana_agrandada, text=f"Usuario: {usuario}").pack()
        fecha_solo = fecha.split()[1]
        tk.Label(self.ventana_agrandada, text=f"Fecha: {fecha_solo}").pack()
        tk.Label(self.ventana_agrandada, text=f"Contenido: {contenido}").pack()
        if imagen_path:
            imagenContent = Image.open(imagen_path)
            imagenContent = imagenContent.resize((200, 200), Image.BILINEAR)
            imagen_tk = ImageTk.PhotoImage(imagenContent)
            imagen_label = tk.Label(self.ventana_agrandada, image=imagen_tk)
            imagen_label.image = imagen_tk
            imagen_label.pack()


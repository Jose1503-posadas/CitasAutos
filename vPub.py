import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from vMisPub import Perfil
from VnuevaPub import VentanaNuevoPost
from publicaciones import Publicacion

class VentanaUsuario(tk.Toplevel):
    def __init__(self, user):
        super().__init__()
        self.title("vPub")
        self.geometry("400x400")
        self.perfil = Perfil(self, user['nombreUsuario'], user['avatar'])

        # Marco para los botones fijos
        self.frame_botones = ttk.Frame(self)
        self.frame_botones.pack(side="top", fill="x")

        # Botones
        self.btn_nuevo_post = ttk.Button(self.frame_botones, text="Nuevo Post", command=self.mostrar_nuevo_post)
        self.btn_perfil = ttk.Button(self.frame_botones, text="Perfil", command=self.mostrar_perfil)
        self.btn_nuevo_post.pack(side="left", padx=(20, 10), pady=5)
        self.btn_perfil.pack(side="left", padx=(140, 5), pady=5)

        # Configurar el Canvas y el Scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Contenedor para los elementos
        self.container = ttk.Frame(self.canvas)
        self.canvas.create_window((60, 60), window=self.container, anchor="nw")

        # Ajustar tamaño del canvas al contenedor
        self.container.bind("<Configure>", self.on_frame_configure)

        # Inicializar el gestor de publicaciones
        self.publicacion_manager = Publicacion(self.container)

        # Mostrar las publicaciones iniciales
        self.actualizar_publicaciones()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def mostrar_nuevo_post(self):
        ventana_nuevo_post = VentanaNuevoPost(self, {'nombre': self.perfil.nombre_usuario})
        ventana_nuevo_post.grab_set()  # Bloquea la interacción con otras ventanas
        ventana_nuevo_post.wait_window()  # Espera hasta que se cierre la ventana nueva post

        # Llama a la función para actualizar las publicaciones cuando se publique un nuevo post
        self.actualizar_publicaciones()

    def actualizar_publicaciones(self):
        self.publicacion_manager.actualizar_publicaciones()

    """ def mostrar_perfil(self):
        self.perfil.mostrar_perfil()"""
    def mostrar_perfil(self):
        # Limpiar el contenedor principal
        for widget in self.container.winfo_children():
            widget.destroy()

        # Crear el frame del perfil dentro del contenedor principal
        self.frame_perfil = ttk.Frame(self.container)
        self.frame_perfil.pack(fill="both", expand=True)

        # Mostrar el perfil en el nuevo frame
        self.perfil.mostrar_perfil()

        # Agregar un botón para regresar a la página principal
        btn_regresar = ttk.Button(self.frame_perfil, text="Regresar", command=self.regresar_pagina_principal)
        btn_regresar.pack(side="bottom", pady=10)

    def regresar_pagina_principal(self):
        # Destruir el frame del perfil
        self.frame_perfil.destroy()
        # Volver a mostrar las publicaciones
        self.actualizar_publicaciones()


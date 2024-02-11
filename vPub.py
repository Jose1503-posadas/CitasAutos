import tkinter as tk
from tkinter import ttk
from vMisPub import Perfil
from VnuevaPub import VentanaNuevoPost

class VentanaUsuario(tk.Toplevel):
    def __init__(self, user):
        super().__init__()
        self.title("Micro-X")
        self.geometry("400x400")

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
        self.canvas.create_window((0, 0), window=self.container, anchor="nw")

        # Ajustar tamaño del canvas al contenedor
        self.container.bind("<Configure>", self.on_frame_configure)

        # Inicializar el gestor de publicaciones
        self.perfil = Perfil(self, user['nombreUsuario'], user['avatar'])

    def on_frame_configure(self, event):
        """Configurar el tamaño del canvas."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    """def mostrar_nuevo_post(self):
        self.perfil.mostrar_nuevo_post()"""
    def mostrar_nuevo_post(self):
        ventana_nuevo_post = VentanaNuevoPost.obtener_instancia({'nombre': self.perfil.nombre_usuario})
        ventana_nuevo_post.grab_set()  # Bloquea la interacción con otras ventanas


    def mostrar_perfil(self):
        self.perfil.mostrar_perfil(

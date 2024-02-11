import tkinter as tk
from tkinter import ttk

"""patron singleton"""
class VentanaNuevoPost(tk.Toplevel):
    _instance = None  # Instancia única para el singleton

    @classmethod
    def obtener_instancia(cls, usuario):
        if cls._instance is None:
            cls._instance = cls(usuario)
        return cls._instance

    def __init__(self, usuario):
        super().__init__()
        self.title("Nuevo Post")
        self.geometry("400x300")

        self.usuario = usuario

        # Mostrar foto y nombre de usuario
        self.frame_usuario = ttk.Frame(self)
        self.frame_usuario.pack(pady=10)
        self.lbl_nombre = ttk.Label(self.frame_usuario, text=f"Usuario: {self.usuario['nombre']}")
        self.lbl_nombre.pack()
        # Aquí puedes mostrar la foto del usuario si tienes esa funcionalidad

        # Campo de texto para el post
        self.entry_post = ttk.Entry(self, width=50)
        self.entry_post.pack(pady=10)

        # Botones
        self.frame_botones = ttk.Frame(self)
        self.frame_botones.pack(pady=5)
        self.btn_cancelar = ttk.Button(self.frame_botones, text="Cancelar", command=self.destroy)
        self.btn_cancelar.pack(side="left", padx=10)
        self.btn_publicar = ttk.Button(self.frame_botones, text="Publicar", command=self.publicar)
        self.btn_publicar.pack(side="left")

    def publicar(self):
        texto_post = self.entry_post.get()
        # Publicar el post utilizando el patrón de diseño singleton
        publicacion = Publicacion.obtener_instancia()
        publicacion.agregar_post(self.usuario['nombreUsuario'], texto_post)
        self.destroy()

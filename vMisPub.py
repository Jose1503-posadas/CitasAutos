from tkinter import ttk
from PIL import Image, ImageTk

class Perfil:
    def __init__(self, ventana_usuario, nombre_usuario, avatar):
        self.ventana_usuario = ventana_usuario
        self.nombre_usuario = nombre_usuario
        self.avatar = avatar
        self.frame_perfil = None

    def mostrar_perfil(self):
        if self.frame_perfil:
            self.frame_perfil.destroy()

        self.frame_perfil = ttk.Frame(self.ventana_usuario.container)
        self.frame_perfil.pack()

        nombre_label = ttk.Label(self.frame_perfil, text=f"Usuario: {self.nombre_usuario}")
        nombre_label.pack()

        # Redimensionar la imagen del avatar
        try:
            avatar_image = Image.open(self.avatar)
            avatar_image = avatar_image.resize((50, 50))  # Redimensionar la imagen
            avatar_photo = ImageTk.PhotoImage(avatar_image)

            avatar_label = ttk.Label(self.frame_perfil, image=avatar_photo)
            avatar_label.image = avatar_photo  # Mantener una referencia
            avatar_label.pack()
        except FileNotFoundError:
            error_label = ttk.Label(self.frame_perfil, text="Error: No se encontró la imagen.")
            error_label.pack()

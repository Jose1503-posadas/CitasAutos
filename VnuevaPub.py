import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

class PublicacionStrategy:
    def publicar(self, usuario, texto, imagen_path):
        raise NotImplementedError("Subclases deben implementar el método 'publicar'.")

class PublicacionSimple(PublicacionStrategy):
    def publicar(self, usuario, texto, imagen_path):
        hora_fecha_actual = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
        conn = sqlite3.connect("publicaciones.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS publicaciones (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT,
                            hora_fecha TEXT,
                            contenido TEXT,
                            imagen TEXT,
                            estado int
                        )''')
        cursor.execute("INSERT INTO publicaciones (usuario, hora_fecha, contenido, imagen, estado) VALUES (?, ?, ?, ?,?)",
                       (usuario['nombre'], hora_fecha_actual, texto, imagen_path, '0'))
        conn.commit()
        conn.close()

class VentanaNuevoPost(tk.Toplevel):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.title("VnuevaPub")
        self.geometry("400x350")

        self.usuario = usuario
        self.estrategia_publicacion = PublicacionSimple()  # Estrategia por defecto

        self.avatar_path = tk.StringVar()

        self.lbl_post = ttk.Label(self, text="Escribe tu publicación:")
        self.lbl_post.pack(pady=10)

        self.entry_post = tk.Text(self, width=30, height=3)
        self.entry_post.pack()

        self.btn_adjuntar_imagen = ttk.Button(self, text="Adjuntar Imagen", command=self.cargar_avatar)
        self.btn_adjuntar_imagen.pack(pady=5)

        self.lbl_avatar = ttk.Label(self)
        self.lbl_avatar.pack()

        self.frame_botones = ttk.Frame(self)
        self.frame_botones.pack(pady=5)

        self.btn_cancelar = ttk.Button(self.frame_botones, text="Cancelar", command=self.destroy)
        self.btn_cancelar.pack(side="left", padx=10)

        self.btn_publicar = ttk.Button(self.frame_botones, text="Publicar", command=self.publicar)
        self.btn_publicar.pack(side="left")

    def cargar_avatar(self):
        ruta_imagen = filedialog.askopenfilename()
        if ruta_imagen:
            self.avatar_path.set(ruta_imagen)
            self.mostrar_avatar()

    def mostrar_avatar(self):
        ruta_imagen = self.avatar_path.get()
        if ruta_imagen:
            avatar_image = Image.open(ruta_imagen)
            avatar_image = avatar_image.resize((50, 50))
            self.avatar_photo = ImageTk.PhotoImage(avatar_image)
            self.lbl_avatar.config(image=self.avatar_photo)
            self.lbl_avatar.image = self.avatar_photo

    def publicar(self):
        texto_post = self.entry_post.get("1.0", tk.END)
        self.estrategia_publicacion.publicar(self.usuario, texto_post, self.avatar_path.get())
        self.destroy()

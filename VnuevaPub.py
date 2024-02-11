import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

class VentanaNuevoPost(tk.Toplevel):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.title("VnuevaPub")
        self.geometry("400x350")

        self.usuario = usuario
        self.avatar_path = tk.StringVar()

        # Etiqueta para el texto del post
        self.lbl_post = ttk.Label(self, text="Escribe tu publicación:")
        self.lbl_post.pack(pady=10)

        # Campo de texto para el post
        self.entry_post = tk.Text(self, width=30, height=3)  # Ajusta el height según tu preferencia
        self.entry_post.pack()

        # Botón para adjuntar imagen
        self.btn_adjuntar_imagen = ttk.Button(self, text="Adjuntar Imagen", command=self.cargar_avatar)
        self.btn_adjuntar_imagen.pack(pady=5)

        # Etiqueta para mostrar la imagen seleccionada
        self.lbl_avatar = ttk.Label(self)
        self.lbl_avatar.pack()

        # Botones de Publicar y Cancelar
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
        texto_post = self.entry_post.get("1.0", tk.END)  # Obtener el contenido del Text widget
        
        # Obtener la hora y la fecha actual
        hora_fecha_actual = datetime.now().strftime("%H:%M:%S %Y-%m-%d")

        # Conectar a la base de datos
        conn = sqlite3.connect("publicaciones.db")
        cursor = conn.cursor()

        # Crear la tabla si no existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS publicaciones (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT,
                            hora_fecha TEXT,
                            contenido TEXT,
                            imagen TEXT
                        )''')

        # Insertar los datos en la tabla
        cursor.execute("INSERT INTO publicaciones (usuario, hora_fecha, contenido, imagen) VALUES (?, ?, ?, ?)",
                       (self.usuario['nombre'], hora_fecha_actual, texto_post, self.avatar_path.get()))

        # Guardar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        # Cerrar la ventana después de publicar
        self.destroy()

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    VentanaNuevoPost(root, {'nombre': 'Usuario de Ejemplo'})
    root.mainloop()

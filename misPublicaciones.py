import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

COLOR_FONDO_CONTENEDOR = "dark violet"

class miPublicacion:
    def __init__(self, container, observer):  # Agrega observer como parámetro
        self.container = container
        self.observer = observer  # Guarda observer como un atributo

    def actualizar_publicaciones(self):
        # Limpiar las publicaciones anteriores
        for widget in self.container.winfo_children():
            widget.destroy()

        # Conectar a la base de datos y obtener las publicaciones
        conn = sqlite3.connect("publicaciones.db")
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, hora_fecha, contenido, imagen FROM publicaciones WHERE usuario = ? AND estado = 0 ORDER BY hora_fecha DESC",(self.nombre_usuario,))       
        publicaciones = cursor.fetchall()
        conn.close()

        # Mostrar las publicaciones en la ventana
        for publicacion in publicaciones:
            self.mostrar_publicacion(publicacion)

    def mostrar_publicacion(self, publicacion, observer):  # Agrega observer como parámetro
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
        boton_eliminar = tk.Button(frame_publicacion, text="Eliminar", command=lambda: self.VentanaEmergenteConfirmacion(observer, usuario, fecha, contenido))
        boton_eliminar.pack(side="left", padx=(30, 10), pady=10)
        

        boton_editar = tk.Button(frame_publicacion, text="Editar", command=lambda: self.VentanaEditarPublicacion(observer,usuario, fecha, contenido))
        boton_editar.pack(side="left", padx=(100, 10), pady=10)

    class VentanaEmergenteConfirmacion(tk.Toplevel):
        def __init__(self, observer, usuario, fecha, contenido):
            super().__init__()
            self.observer = observer
            self.usuario = usuario
            self.fecha = fecha
            self.contenido = contenido
            
            self.title("Confirmar Eliminación")
            self.geometry("300x100")
            
            label_confirmacion = tk.Label(self, text="¿Estás seguro que quieres eliminar esta publicación?")
            label_confirmacion.pack(pady=10)

            boton_confirmar = tk.Button(self, text="Confirmar", command=self.eliminar_publicacion)
            boton_confirmar.pack(side="left", padx=10)

            boton_cancelar = tk.Button(self, text="Cancelar", command=self.destroy)
            boton_cancelar.pack(side="left", padx=10)

        def eliminar_publicacion(self):
            # Función para cambiar el estado de la publicación a 1 en la base de datos
            conn = sqlite3.connect("publicaciones.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE publicaciones SET estado = 1 WHERE usuario = ? AND hora_fecha = ? AND contenido = ?", (self.usuario, self.fecha, self.contenido))
            conn.commit()
            conn.close()
            # Notificar al observador sobre la eliminación
            self.observer.actualizar_publicaciones()
            self.destroy()
    class VentanaEditarPublicacion(tk.Toplevel):
        def __init__(self, observer, usuario, fecha, contenido):
            super().__init__()
            self.observer = observer
            self.usuario = usuario
            self.fecha = fecha
            self.contenido = contenido
            self.title("Editar Publicación")
            self.geometry("400x200")

            # Etiqueta y cuadro de texto para editar el contenido
            tk.Label(self, text="Editar Contenido:").pack()
            self.texto_editar = tk.Text(self, height=5, width=40)
            self.texto_editar.insert(tk.END, contenido)
            self.texto_editar.pack()

            # Botones para guardar y cancelar los cambios
            boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_edicion)
            boton_guardar.pack(side="left", padx=5, pady=5)

            boton_cancelar = tk.Button(self, text="Cancelar", command=self.destroy)
            boton_cancelar.pack(side="left", padx=5, pady=5)

        def guardar_edicion(self):
            nuevo_contenido = self.texto_editar.get("1.0", "end-1c")
            conn = sqlite3.connect("publicaciones.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE publicaciones SET contenido = ? WHERE usuario = ? AND hora_fecha = ?", (nuevo_contenido, self.usuario, self.fecha))
            conn.commit()
            conn.close()
            self.observer.actualizar_publicaciones()
            self.destroy()

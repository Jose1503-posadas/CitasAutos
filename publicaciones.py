import tkinter as tk
from PIL import Image, ImageTk

COLOR_FONDO_CONTENEDOR = "dark violet"

class Publicacion:
    def __init__(self, nombre_usuario, avatar, fecha, contenido, imagen):
        self.nombre_usuario = nombre_usuario
        self.avatar = avatar
        self.fecha = fecha
        self.contenido = contenido
        self.imagen = imagen

class PublicacionBuilder:
    def __init__(self):
        self.nombre_usuario = None
        self.avatar = None
        self.fecha = None
        self.contenido = None
        self.imagen = None

    def with_usuario(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario
        return self

    def with_avatar(self, avatar):
        self.avatar = avatar
        return self

    def with_fecha(self, fecha):
        self.fecha = fecha
        return self

    def with_contenido(self, contenido):
        self.contenido = contenido
        return self
    
    def with_imagen(self, imagen):
        self.imagen = imagen
        return self
    
    def build(self):
        return Publicacion(self.nombre_usuario, self.avatar, self.fecha, self.contenido, self.imagen)

class InterfazPublicacion:
    def __init__(self):
        self.publicacion = None

    def crear_publicacion(self):
        builder = PublicacionBuilder()
        self.publicacion = builder.build()
        
    def crear_interfaz_grafica(self):
        root = tk.Tk()
        contenedor = tk.LabelFrame(root, padx=10, pady=10, borderwidth=2, relief="groove", bg=COLOR_FONDO_CONTENEDOR, fg="white")
        contenedor.pack(padx=10, pady=25)

        if self.publicacion.avatar:
            imagen = Image.open(self.publicacion.avatar)
            imagen = imagen.resize((50, 50), Image.BILINEAR)
            imagen_tk = ImageTk.PhotoImage(imagen)
            imagen_label = tk.Label(contenedor, image=imagen_tk, bg=COLOR_FONDO_CONTENEDOR, fg="white")
            imagen_label.image = imagen_tk
            imagen_label.grid(row=0, column=0, sticky="w")
            nombre_label = tk.Label(contenedor, text=self.publicacion.nombre_usuario, font=("Arial", 20, "bold"), bg=COLOR_FONDO_CONTENEDOR, fg="white")
            nombre_label.grid(row=0, column=1, sticky="w")
        else:
            nombre_label = tk.Label(contenedor, text=self.publicacion.nombre_usuario, font=("Arial", 20, "bold"), bg=COLOR_FONDO_CONTENEDOR, fg="white")
            nombre_label.grid(row=0, column=0, columnspan=2, sticky="w")

        tk.Label(contenedor, text=f"Fecha: {self.publicacion.fecha}", bg=COLOR_FONDO_CONTENEDOR, fg="white").grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Label(contenedor, text=f"Contenido: {self.publicacion.contenido}", bg=COLOR_FONDO_CONTENEDOR, fg="white").grid(row=2, column=0, columnspan=2, sticky="w")

        if self.publicacion.imagen:
            imagenContent = Image.open(self.publicacion.imagen)
            imagenContent = imagenContent.resize((200, 200), Image.BILINEAR)
            imagen_tk = ImageTk.PhotoImage(imagenContent)
            imagen_label = tk.Label(contenedor, image=imagen_tk, bg=COLOR_FONDO_CONTENEDOR, fg="white")
            imagen_label.image = imagen_tk
            imagen_label.grid(row=3, column=0, columnspan=2)

        boton_agrandar = tk.Button(contenedor, text="Agrandar", command=self.abrir_ventana_agrandada)
        boton_agrandar.grid(row=4, column=0, columnspan=2, sticky="we", padx=5, pady=5)

        root.mainloop()

    def abrir_ventana_agrandada(self):
        ventana_agrandada = tk.Toplevel()
        ventana_agrandada.title("Publicación")

        contenedor_agrandado = tk.LabelFrame(ventana_agrandada, padx=10, pady=10, borderwidth=2, relief="groove", bg=COLOR_FONDO_CONTENEDOR, fg="white")
        contenedor_agrandado.pack(padx=10, pady=25)

        tk.Label(contenedor_agrandado, text=f"Nombre de usuario: {self.publicacion.nombre_usuario}", bg=COLOR_FONDO_CONTENEDOR, fg="white").grid(row=0, column=0, columnspan=2, sticky="w")
        tk.Label(contenedor_agrandado, text=f"Fecha: {self.publicacion.fecha}", bg=COLOR_FONDO_CONTENEDOR, fg="white").grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Label(contenedor_agrandado, text=f"Contenido: {self.publicacion.contenido}", bg=COLOR_FONDO_CONTENEDOR, fg="white").grid(row=2, column=0, columnspan=2, sticky="w")

        if self.publicacion.imagen:
            imagen_content_agrandada = Image.open(self.publicacion.imagen)
            imagen_content_agrandada = imagen_content_agrandada.resize((400, 400), Image.BILINEAR)
            imagen_tk_agrandada = ImageTk.PhotoImage(imagen_content_agrandada)

            imagen_label_agrandada = tk.Label(contenedor_agrandado, image=imagen_tk_agrandada, bg=COLOR_FONDO_CONTENEDOR, fg="white")
            imagen_label_agrandada.image = imagen_tk_agrandada
            imagen_label_agrandada.grid(row=3, column=0, columnspan=2)

# Crear una instancia de PublicacionBuilder con los valores deseados
builder = PublicacionBuilder().with_usuario("Usuario1") \
                               .with_avatar("/Users/joseposadas/Desktop/uam/MiniX-1/imagenes/imagen3.jpg") \
                               .with_fecha("2024-02-11") \
                               .with_contenido("Este es el contenido de la publicación") \
                               .with_imagen("/Users/joseposadas/Desktop/uam/MiniX-1/imagenes/imagen4.jpg")

# Construir la publicación con los valores proporcionados
publicacion = builder.build()

# Crear una instancia de InterfazPublicacion y establecer la publicación
interfaz_publicacion = InterfazPublicacion()
interfaz_publicacion.publicacion = publicacion

# Crear la interfaz gráfica
interfaz_publicacion.crear_interfaz_grafica()


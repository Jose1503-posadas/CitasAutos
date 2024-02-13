import tkinter as tk
from tkinter import ttk, messagebox
from main import Modelo, VentanaLogin, Controlador
from unittest.mock import Mock, patch

def test_validarLogin():
    modelo = Modelo()
    nombreUsuario ="moni"
    password = "1234"
    avatar ="C:/Users/moni/Desktop/MiniXFinal/imagenes/imagen2.jpg"
    
    resultado = modelo.validarLogin(nombreUsuario, password)
    assert resultado['nombreUsuario'] == nombreUsuario
    assert resultado['avatar'] == avatar

def test_registroUsuarioBD():
    modelo = Modelo()
    nombreUsuario ="nombre"
    password = "0123"
    avatar ="C:/Users/moni/Desktop/MiniXFinal/imagenes/imagen2.jpg"
    assert modelo.registroUsuarioBD(nombreUsuario, password, avatar) is True

def test_login():
    modelo = Modelo()
    nombre_usuario_prueba = "usuario1"
    modelo.login(nombre_usuario_prueba)
    # Verificar si se insertaron correctamente en la base de datos
    cursor = modelo.conn_log.cursor()
    cursor.execute("SELECT * FROM login WHERE nombreUsuario=?", (nombre_usuario_prueba,))
    resultado = cursor.fetchone()
    # Verificar si se encontró el registro en la base de datos
    assert resultado is not None






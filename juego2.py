import tkinter as tk
from tkinter import messagebox
import random
import pygame  # Importamos la librería pygame para manejar música

# Inicializar pygame para usar la música
pygame.mixer.init()

# Funciones para generar las secuencias
def secuencia_doble():
    return [2, 4, 8, 16, '?']

def secuencia_fibonacci():
    return [0, 1, 1, 2, 3, 5, '?']

def secuencia_potencias():
    return [2**0, 2**1, 2**2, 2**3, '?']

def secuencia_aritmetica():
    return [3, 6, 9, 12, '?']

def secuencia_cubos():
    return [1**3, 2**3, 3**3, 4**3, '?']

def secuencia_pares():
    return [2, 4, 6, 8, '?']

# Función para generar la sugerencia
def generar_sugerencia(secuencia_tipo):
    if secuencia_tipo == "Doble":
        return "Pista: Cada número es el doble del anterior."
    elif secuencia_tipo == "Fibonacci":
        return "Pista: Es la secuencia de Fibonacci."
    elif secuencia_tipo == "Potencias":
        return "Pista: Potencias de 2."
    elif secuencia_tipo == "Aritmética":
        return "Pista: Incremento de 3 en cada paso."
    elif secuencia_tipo == "Cubos":
        return "Pista: Cubos de los números enteros."
    elif secuencia_tipo == "Pares":
        return "Pista: Números pares."

# Función para seleccionar una secuencia aleatoria que no se haya repetido
def seleccionar_secuencia_aleatoria():
    secuencias = [secuencia_doble, secuencia_fibonacci, secuencia_potencias, secuencia_aritmetica, secuencia_cubos, secuencia_pares]
    
    # Si ya se han mostrado todas las secuencias, reiniciar el historial
    if len(secuencias_usadas) == len(secuencias):
        secuencias_usadas.clear()

    # Seleccionar una secuencia aleatoria que no haya sido usada
    secuencia = random.choice([s for s in secuencias if s not in secuencias_usadas])
    secuencias_usadas.append(secuencia)
    return secuencia()

# Función para actualizar la secuencia mostrada
def actualizar_secuencia():
    secuencia = seleccionar_secuencia_aleatoria()

    # Actualizar el label con la secuencia
    label_secuencia.config(text=f"Secuencia: {', '.join(map(str, secuencia))}")

    # Actualizar la pista
    label_sugerencia.config(text=generar_sugerencia(secuencia_tipo.get()))

    # Actualizar la respuesta correcta para la secuencia actual
    actualizar_respuesta_correcta(secuencia)

# Lógica para actualizar la respuesta correcta basada en la secuencia
def actualizar_respuesta_correcta(secuencia):
    global respuesta_correcta
    if secuencia == secuencia_doble():
        respuesta_correcta = 32
    elif secuencia == secuencia_fibonacci():
        respuesta_correcta = 8
    elif secuencia == secuencia_potencias():
        respuesta_correcta = 16
    elif secuencia == secuencia_aritmetica():
        respuesta_correcta = 15
    elif secuencia == secuencia_cubos():
        respuesta_correcta = 125
    elif secuencia == secuencia_pares():
        respuesta_correcta = 10

# Lógica para verificar la respuesta
def verificar_respuesta():
    global puntuacion, aciertos
    try:
        respuesta_jugador = int(entry_respuesta.get())
        if respuesta_jugador == respuesta_correcta:
            puntuacion += 1
            aciertos += 1  # Aumentamos el contador de aciertos

            # Mostrar el mensaje de respuesta correcta
            messagebox.showinfo("¡Aceraste!", f"¡La respuesta es correcta! Puntuación: {puntuacion}")
            actualizar_secuencia()  # Cambiar la secuencia al acertar
            actualizar_puntaje()    # Actualizar el puntaje
            verificar_punto_extra()  # Verificar si se debe dar un punto extra

        else:
            messagebox.showerror("Incorrecto", "La respuesta es incorrecta.")
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa un número válido.")

# Función para verificar si se otorga un punto extra
def verificar_punto_extra():
    global puntuacion, aciertos
    # Verificar si el jugador tiene 3 aciertos
    if aciertos >= 3:  
        puntuacion += 1  # Otorgar un punto extra
        aciertos = 0  # Reiniciar el contador de aciertos
        mostrar_punto_extra()  # Mostrar el mensaje de punto extra
        animar_lluvia_estrellas()  # Ejecutar la animación de lluvia de estrellas
    actualizar_puntaje()

# Función para mostrar el mensaje de punto extra
def mostrar_punto_extra():
    punto_extra_label.config(text="¡Tienes un punto extra por acertar 3 veces! 🎉", font=("Helvetica", 14, "bold"), fg="green")
    punto_extra_label.pack(pady=10)

# Función para actualizar el cuadro de puntaje
def actualizar_puntaje():
    label_puntaje.config(text=f"Puntaje: {puntuacion}")

# Función para mostrar el juego y ocultar la portada
def iniciar_juego():
    # Ocultar la portada
    portada_frame.pack_forget()

    # Mostrar la ventana principal del juego
    juego_frame.pack(padx=10, pady=10)

    # Reproducir la música de fondo
    pygame.mixer.music.load("musica_de_fondo.mp3")  # Asegúrate de que el archivo esté en la misma carpeta
    pygame.mixer.music.play(-1)  # Reproducir en bucle

# Función para animar la lluvia de estrellas
def animar_lluvia_estrellas():
    canvas = tk.Canvas(juego_frame, width=600, height=400, bg='black')  # Fondo oscuro para las estrellas
    canvas.pack()

    colores = ["white", "yellow", "lightblue", "silver"]
    estrellas = []
    
    for _ in range(50):  # Genera 50 estrellas
        x = random.randint(0, 600)
        y = random.randint(0, 400)
        color = random.choice(colores)
        size = random.randint(5, 15)
        estrella = canvas.create_text(x, y, text="*", font=("Helvetica", size), fill=color)
        estrellas.append(estrella)

    def mover_estrellas():
        for estrella in estrellas:
            # Hacer que las estrellas se muevan de arriba a abajo
            canvas.move(estrella, 0, random.randint(1, 3))  # Movimiento vertical
            # Reaparecer estrellas que salen de la pantalla
            coords = canvas.coords(estrella)
            if coords[1] > 400:
                canvas.coords(estrella, random.randint(0, 600), 0)  # Reseteamos las estrellas al tope
        root.after(50, mover_estrellas)  # Mueve las estrellas cada 50 milisegundos

    mover_estrellas()

# Interfaz Gráfica con Tkinter
root = tk.Tk()
root.title("Juego de Secuencias Numéricas")
root.geometry("600x500")
root.config(bg="#e0f7fa")  # Fondo azul claro para la ventana principal

# Variables para la puntuación y los aciertos
puntuacion = 0
aciertos = 0  # Contador de aciertos
secuencias_usadas = []  # Historial de secuencias usadas

# Crear un frame para la portada con borde azul
portada_frame = tk.Frame(root, bg="#e0ffff", bd=5, relief="solid", padx=20, pady=20)

# Mensaje de bienvenida en la portada
label_bienvenida = tk.Label(portada_frame, text="¡Bienvenido al Juego de Secuencias Numéricas!", font=("Helvetica", 16, "bold"), bg="#e0ffff", fg="#2e8b57")
label_bienvenida.pack(pady=20)

# Botón Siguiente
button_siguiente = tk.Button(portada_frame, text="Siguiente", font=("Helvetica", 14), fg="white", bg="#2e8b57", command=iniciar_juego)
button_siguiente.pack(pady=20)

# Mostrar la portada
portada_frame.pack(padx=10, pady=10)

# Crear un frame para el juego (oculto al principio)
juego_frame = tk.Frame(root, bg="white")

# Instrucciones
label_instrucciones = tk.Label(juego_frame, text="Elige un tipo de secuencia y adivina el número faltante.", font=("Helvetica", 12), bg="white", fg="#8b0000")
label_instrucciones.pack(pady=10)

# Cuadro que dice "Elija" antes de las opciones de secuencia
label_elija = tk.Label(juego_frame, text="Elija una secuencia:", font=("Helvetica", 12), bg="white", fg="#8b0000")
label_elija.pack(pady=5)

# Selección del tipo de secuencia
secuencia_tipo = tk.StringVar()
secuencia_tipo.set("Doble")

opciones_secuencia = ["Doble", "Fibonacci", "Potencias", "Aritmética", "Cubos", "Pares"]
menu_secuencia = tk.OptionMenu(juego_frame, secuencia_tipo, *opciones_secuencia, command=lambda x: actualizar_secuencia())
menu_secuencia.pack(pady=10)

# Mostrar la secuencia con el número faltante
label_secuencia = tk.Label(juego_frame, text="Secuencia: 2, 4, 8, ?", font=("Helvetica", 12), bg="white")
label_secuencia.pack(pady=10)

# Campo de entrada para la respuesta
label_respuesta = tk.Label(juego_frame, text="Ingresa tu respuesta:", font=("Helvetica", 12), bg="white")
label_respuesta.pack(pady=5)
entry_respuesta = tk.Entry(juego_frame, font=("Helvetica", 12))
entry_respuesta.pack(pady=10)

# Pista de la secuencia
label_sugerencia = tk.Label(juego_frame, text="", font=("Helvetica", 10), fg="blue", bg="white")
label_sugerencia.pack(pady=10)

# Botón para verificar la respuesta
button_verificar = tk.Button(juego_frame, text="Verificar Respuesta", font=("Helvetica", 12), fg="white", bg="#4682b4", command=verificar_respuesta)
button_verificar.pack(pady=20)

# Cuadro de puntaje
label_puntaje = tk.Label(juego_frame, text="Puntaje: 0", font=("Helvetica", 12), bg="white", fg="#4682b4")
label_puntaje.pack(pady=5)

# Label para mostrar el punto extra
punto_extra_label = tk.Label(juego_frame, bg="white")

# Cerrar la ventana
button_salir = tk.Button(juego_frame, text="Salir", font=("Helvetica", 12), fg="white", bg="#b22222", command=root.quit)
button_salir.pack(pady=10)

# Iniciar la interfaz gráfica
root.mainloop()

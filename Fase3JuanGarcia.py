import tkinter as tk

from tkinter import messagebox

def verificar_contrasena(event=None):
    """
    Verifica si la contraseña ingresada en el campo de texto es correcta.
    El parametro 'event' es para permitir la vinculación con eventos de teclado.
    """
    intentos_restantes = int(label_intentos.cget("text").split()[-1])
    
    if entry_contrasena.get() == "Caja":
        messagebox.showinfo("Acceso Concedido", "Contraseña correcta. Bienvenido.", parent=ventana)
        ventana.destroy() # Cierra la ventana de login
        ## abrir_ventana_registro() # Llama a la función que crea la nueva ventana
    else:
        intentos_restantes -= 1
        if intentos_restantes > 0:
            messagebox.showwarning("Acceso Denegado", f"Contraseña incorrecta. Le quedan {intentos_restantes} intentos.", parent=ventana)
            label_intentos.config(text=f"Intentos restantes: {intentos_restantes}")
            entry_contrasena.delete(0, tk.END) # Limpia el campo de contraseña
        else:
            messagebox.showerror("Acceso Bloqueado", "Ha superado el número de intentos permitidos.", parent=ventana)
            ventana.destroy() # Cierra la aplicación

def acerca_de(event=None):
    titulo = "Acerca de"
    mensaje = (
        "Programa: Estructura de datos\n"
        "Estudiante: Juan Pablo Garcia\n"
        "Número de grupo colaborativo: 301305A_2201"
    )
    messagebox.showinfo(titulo, mensaje, parent=ventana)


# --- Configuración de la Ventana Principal (Login) ---
ventana = tk.Tk()
ventana.title("Login - Compensandote")
ventana.geometry("540x220") # Aumentamos la altura para asegurar que los botones sean visibles
ventana.resizable(False, False)

# --- Barra superior con el botón "Acerca de" ---
# En lugar de un menú (que en macOS se va a la barra superior de la pantalla),
# creamos un Frame para simular una barra dentro de la ventana.
frame_menu = tk.Frame(ventana, relief="raised", bd=1)
frame_menu.pack(side="top", fill="x")
# Añadimos un botón con apariencia plana (flat) para que parezca un texto de menú.
tk.Button(frame_menu, text="Acerca de...", command=acerca_de, relief="flat").pack(side="left")

# --- Creación de Widgets ---
tk.Label(ventana, text="Ingrese la contraseña de acceso:").pack(pady=10)

# Este es el campo de entrada para la contraseña. La opción show="*" oculta el texto.
entry_contrasena = tk.Entry(ventana, show="*", font=("Helvetica", 12), width=25)
entry_contrasena.pack(pady=5)
# Vinculamos la tecla "Enter" (Return) al campo de contraseña para llamar a la función de verificación.
entry_contrasena.bind('<Return>', verificar_contrasena)

label_intentos = tk.Label(ventana, text="Intentos restantes: 3")
label_intentos.pack(pady=5)

# --- Contenedor para los botones ---
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Ingresar", command=verificar_contrasena, font=("Helvetica", 12)).grid(row=0, column=0, padx=10) # Columna 0
tk.Button(frame_botones, text="Salir", command=ventana.destroy, font=("Helvetica", 12)).grid(row=0, column=1, padx=10) # Columna 1

# Iniciar el bucle de eventos para que la ventana aparezca y sea interactiva
ventana.mainloop()
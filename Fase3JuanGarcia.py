import tkinter as tk

from tkinter import messagebox
from tkinter import ttk # Importar ttk para el Combobox

def abrir_control_afiliados():
    registro = tk.Tk()
    registro.title("Caja Compensandote - Control de Afiliados")
    registro.geometry("1000x600")
    registro.resizable(False, False)

    def tarifa_ingreso_empleado(ingreso):
        #Calcula la tarifa de afiliación basada en el ingreso mensual.
        tarifa = 0
        if 1000000 <= ingreso <= 2000000:
            tarifa = 45000
        elif 2000001 <= ingreso <= 3000000:
            tarifa = 60000
        elif 3000001 <= ingreso <= 4000000:
            tarifa = 75000
        elif 4000001 <= ingreso <= 5000000:
            tarifa = 90000
        elif ingreso > 5000000:
            tarifa = 150000
        return tarifa
    
    def tarifa_ingreso_independiente(ingreso):
        #Calcula la tarifa de afiliación basada en el ingreso mensual.
        tarifa = 0
        if 1000000 <= ingreso <= 2000000:
            tarifa = 10000
        elif 2000001 <= ingreso <= 3000000:
            tarifa = 20000
        elif 3000001 <= ingreso <= 4000000:
            tarifa = 30000
        elif 4000001 <= ingreso <= 5000000:
            tarifa = 40000
        elif ingreso > 5000000:
            tarifa = 80000
        return tarifa
    
    def tarifa_extra(servicio, ingreso):
        #Calcula la tarifa de afiliación basada en el ingreso mensual.
        tarifa = 0
        if servicio == "Subsidio de desempleo":
            tarifa = 0
        elif servicio == "Ingreso a parque":
            tarifa = 2500
        elif servicio == "Curso de formacion":
            tarifa = 7500
        elif servicio == "Paquete de viaje":
            tarifa = 10000
        elif servicio == "Medicina preventiva":
            tarifa = ingreso * 0.10 # 10% del ingreso
        return tarifa

    # --- Funciones de Validación ---
    def validar_solo_numeros(P):
        return P == "" or P.isdigit()
    vcmd_num = (registro.register(validar_solo_numeros), '%P')

    def validar_solo_letras(P):
        return all(c.isalpha() or c.isspace() for c in P)
    vcmd_alpha = (registro.register(validar_solo_letras), '%P')

    # --- Datos para el Formulario ---
    documentos_identidad = ["CC", "CE", "NUIP", "PAS"]
    servicios = [
        "Subsidio de desempleo",
        "Ingreso a parque",
        "Curso de formacion",
        "Paquete de viaje",
        "Medicina preventiva"
        ]

    # --- Función Principal de Cálculo ---
    def calcular_tarifa_final():
        try:
            # 1. Obtener todos los valores del formulario
            num_id = widgets["numero_identificacion"].get()
            nombre = widgets["nombre_completo"].get()
            ingreso_str = widgets["ingresos_actuales"].get()
            modalidad = modalidad_empleo_var.get()
            servicio = widgets["servicio_deseado"].get()

            # 2. Validar que los campos no estén vacíos
            if not all([num_id, nombre, ingreso_str, modalidad, servicio]):
                messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos.", parent=registro)
                return

            ingreso = float(ingreso_str)
            tarifa_base = 0

            # 3. Calcular tarifa base según la modalidad
            if modalidad == "Empleado":
                tarifa_base = tarifa_ingreso_empleado(ingreso)
            elif modalidad == "Independiente":
                tarifa_base = tarifa_ingreso_independiente(ingreso)

            # 4. Calcular tarifa extra según el servicio
            t_extra = tarifa_extra(servicio, ingreso)

            # 5. Calcular total y actualizar la etiqueta de resultado
            total = tarifa_base + t_extra
            resultado_var.set(f"Tarifa Total de Afiliación: ${total:,.2f}")

        except ValueError:
            messagebox.showerror("Error de Datos", "El campo 'Ingresos Actuales' debe ser un número válido.", parent=registro)

    # --- Configuración de la Interfaz Gráfica (UI) ---
    frame_formulario = tk.Frame(registro, padx=15, pady=15)
    frame_formulario.pack(fill="both", expand=True)
    frame_formulario.columnconfigure(1, weight=1)

    widgets = {}
    labels_texto = ["Tipo de Identificación:", "Número de Identificación:", "Nombre Completo:", "Ingresos Actuales:", "Modalidad de Empleo:", "Servicio Deseado:"]

    for i, texto in enumerate(labels_texto):
        tk.Label(frame_formulario, text=texto, font=("Helvetica", 12)).grid(row=i, column=0, padx=5, pady=8, sticky="w")

    # --- Creación de Widgets del Formulario ---
    widgets["tipo_identificacion"] = ttk.Combobox(frame_formulario, values=documentos_identidad, font=("Helvetica", 12), state="readonly")
    widgets["numero_identificacion"] = tk.Entry(frame_formulario, font=("Helvetica", 12), validate="key", validatecommand=vcmd_num)
    widgets["nombre_completo"] = tk.Entry(frame_formulario, font=("Helvetica", 12), validate="key", validatecommand=vcmd_alpha)
    widgets["ingresos_actuales"] = tk.Entry(frame_formulario, font=("Helvetica", 12), validate="key", validatecommand=vcmd_num)

    modalidad_empleo_var = tk.StringVar(value="Empleado")
    frame_modalidad = tk.Frame(frame_formulario)
    tk.Radiobutton(frame_modalidad, text="Empleado", variable=modalidad_empleo_var, value="Empleado", font=("Helvetica", 11)).pack(side="left")
    tk.Radiobutton(frame_modalidad, text="Independiente", variable=modalidad_empleo_var, value="Independiente", font=("Helvetica", 11)).pack(side="left", padx=10)

    widgets["servicio_deseado"] = ttk.Combobox(frame_formulario, values=servicios, font=("Helvetica", 12), state="readonly")

    # --- Posicionamiento de Widgets en la Rejilla ---
    widgets["tipo_identificacion"].grid(row=0, column=1, padx=5, pady=8, sticky="ew")
    widgets["numero_identificacion"].grid(row=1, column=1, padx=5, pady=8, sticky="ew")
    widgets["nombre_completo"].grid(row=2, column=1, padx=5, pady=8, sticky="ew")
    widgets["ingresos_actuales"].grid(row=3, column=1, padx=5, pady=8, sticky="ew")
    frame_modalidad.grid(row=4, column=1, padx=5, pady=8, sticky="w")
    widgets["servicio_deseado"].grid(row=5, column=1, padx=5, pady=8, sticky="ew")

    # --- Botón de Acción y Etiqueta de Resultado ---
    tk.Button(frame_formulario, text="Calcular Tarifa de Afiliación", command=calcular_tarifa_final, font=("Helvetica", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=20)

    resultado_var = tk.StringVar()
    tk.Label(frame_formulario, textvariable=resultado_var, font=("Helvetica", 14, "bold"), fg="blue").grid(row=7, column=0, columnspan=2, pady=10)

def verificar_contrasena(event=None):
    """
    Verifica si la contraseña ingresada en el campo de texto es correcta.
    El parametro 'event' es para permitir la vinculación con eventos de teclado.
    """
    intentos_restantes = int(label_intentos.cget("text").split()[-1])
    
    if entry_contrasena.get() == "Caja":
        messagebox.showinfo("Acceso Concedido", "Contraseña correcta. Bienvenido.", parent=ventana)
        ventana.destroy() # Cierra la ventana de login
        abrir_control_afiliados()
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
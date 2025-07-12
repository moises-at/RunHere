import tkinter as tk
from tkinter import messagebox
import winreg
import os

def agregar_al_registro(nombre_app, ruta_exe):
    """
    Agrega la aplicación al menú contextual del explorador de Windows
    en HKEY_CLASSES_ROOT\Directory\Background\shell.
    """
    
    # Ruta base en el registro para el menú contextual de carpeta
    base_ruta = r"Directory\Background\shell"
    
    try:
        # Abrir o crear la clave principal en HKEY_CLASSES_ROOT
        try:
            # Intentar abrir la clave con permisos de escritura
            key_shell = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, base_ruta, 0, winreg.KEY_WRITE)
        except FileNotFoundError:
            # Si la clave no existe, crearla.
            key_shell = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, base_ruta)

        # Crear la clave para la aplicación (nombre_app) dentro de 'shell'
        key_app = winreg.CreateKey(key_shell, nombre_app)
        
        # Modificar el valor predeterminado (Default) de la clave de la aplicación
        # para mostrar "Abrir con [Nombre de la aplicación]" en el menú contextual.
        nombre_menu = f"Abrir con {nombre_app}"
        winreg.SetValue(key_app, None, winreg.REG_SZ, nombre_menu)
        
        # Crear o modificar la clave 'Icon' y establecer la ruta del icono (la ruta del exe)
        # Esto es opcional, pero añade un icono al menú contextual.
        try:
            winreg.SetValueEx(key_app, "Icon", 0, winreg.REG_SZ, ruta_exe)
        except Exception as e:
            print(f"Error al establecer el icono: {e}")

        # Crear la subclave 'command' para especificar la acción a realizar
        key_command = winreg.CreateKey(key_app, "command")
        
        # Modificar el valor predeterminado de 'command' para ejecutar el .exe
        # "%V" se usa para pasar el directorio actual al comando.
        # Es importante usar comillas alrededor de la ruta para manejar espacios.
        comando = f'"{ruta_exe}" "%V"'
        winreg.SetValue(key_command, None, winreg.REG_SZ, comando)
        
        # Cerrar las claves abiertas
        winreg.CloseKey(key_command)
        winreg.CloseKey(key_app)
        winreg.CloseKey(key_shell)
        
        messagebox.showinfo("Éxito", f"Se ha agregado '{nombre_app}' al menú contextual del explorador.")
    
    except PermissionError:
        messagebox.showerror("Error de Permisos", "Necesitas ejecutar este script como Administrador para modificar el registro.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

# --- Interfaz Gráfica (Tkinter) ---

def ejecutar_script():
    """
    Función que se ejecuta al presionar el botón 'Aceptar'.
    Recupera los datos de la GUI y llama a la función de modificación del registro.
    """
    nombre_app = entry_nombre.get().strip()
    ruta_exe = entry_ruta.get().strip()
    
    if not nombre_app or not ruta_exe:
        messagebox.showwarning("Campos Requeridos", "Por favor, ingresa el nombre de la aplicación y la ruta del ejecutable.")
        return
    
    if not os.path.exists(ruta_exe):
        messagebox.showwarning("Ruta Inválida", "La ruta del archivo EXE no existe.")
        return

    # Llamar a la función principal para agregar al registro
    agregar_al_registro(nombre_app, ruta_exe)
    
    # Cerrar la ventana después de completar la acción
    root.destroy()

# Configurar la ventana principal
root = tk.Tk()
root.title("RunHere")
root.geometry("450x150")
root.resizable(True, True)

# Crear y posicionar los elementos de la GUI

# Nombre de la aplicación
tk.Label(root, text="Nombre del programa:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_nombre = tk.Entry(root, width=40)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

# Ruta del archivo EXE
tk.Label(root, text="Ruta del programa:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_ruta = tk.Entry(root, width=40)
entry_ruta.grid(row=1, column=1, padx=10, pady=10)

# Botón para ejecutar
btn_aceptar = tk.Button(root, text="Aceptar", command=ejecutar_script)
btn_aceptar.grid(row=2, column=1, pady=20)

# Botón para salir
btn_salir = tk.Button(root, text="Salir", command=root.quit)
btn_salir.grid(row=2, column=0, pady=20)

# Iniciar el bucle de la GUI
root.mainloop()

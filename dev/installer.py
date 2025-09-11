import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import requests
import zipfile
import io
import threading
import webbrowser
import sys

# ---------------- Configuración de descarga ----------------
GITHUB_USER = "GuzmanMD"
GITHUB_REPO = "ModsInstaller"

# ---------------- Funciones generales ----------------
def seleccionar_mods_final(mods_dir, ventana_padre):
    mods_disponibles = [f for f in os.listdir(mods_dir) if f.endswith(".dll") or f.endswith(".mod")]
    if not mods_disponibles:
        messagebox.showinfo("Info", "No se encontraron mods en la carpeta.")
        return

    ventana_mods = tk.Toplevel(ventana_padre)
    ventana_mods.title("Selecciona los mods a mantener")
    ventana_mods.geometry("400x600")
    ventana_mods.configure(bg="#2c2f33")
    ventana_mods.protocol("WM_DELETE_WINDOW", cerrar_todo)  # Forzar cierre

    tk.Label(ventana_mods, text="Selecciona los mods a mantener",
             font=("Arial", 12, "bold"), bg="#2c2f33", fg="white").pack(pady=10)

    vars_mods = {}
    for mod in mods_disponibles:
        var = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(ventana_mods, text=mod, variable=var,
                             bg="#2c2f33", fg="white", selectcolor="#7289da",
                             font=("Arial", 10))
        chk.pack(anchor="w", padx=20)
        vars_mods[mod] = var

    def aplicar_seleccion():
        for mod, var in vars_mods.items():
            if not var.get():
                try:
                    os.remove(os.path.join(mods_dir, mod))
                except:
                    pass
        ventana_mods.destroy()
        messagebox.showinfo("Éxito", f"Mods seleccionados mantenidos en:\n{mods_dir}")

    tk.Button(ventana_mods, text="Aplicar selección",
              bg="#7289da", fg="white", font=("Arial", 12, "bold"),
              relief="raised", bd=3, command=aplicar_seleccion).pack(pady=20)


def descargar_mods(mods_dir, api_subcarpeta, ventana, barra_progreso):
    try:
        # Construye la lista de zips según la carpeta del juego
        zips = [f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/raw/main/{api_subcarpeta}/mods{i}.zip" for i in range(1, 6)]
        total_zips = len(zips)
        zips_descargados = 0

        for url in zips:
            print(f"Descargando {url}...")
            try:
                r = requests.get(url)
                r.raise_for_status()
            except:
                print(f"No se pudo descargar {url}, se omite.")
                continue

            archivo_bytes = io.BytesIO(r.content)

            try:
                with zipfile.ZipFile(archivo_bytes) as zip_ref:
                    zip_ref.extractall(mods_dir)
                print(f"{url} descomprimido correctamente.")
            except zipfile.BadZipFile:
                print(f"{url} no es un zip válido, se omite.")
                continue

            zips_descargados += 1
            barra_progreso['value'] = int(zips_descargados / total_zips * 100)
            ventana.update_idletasks()

        seleccionar_mods_final(mods_dir, ventana)

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error:\n{e}")


def abrir_github(url=f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"):
    webbrowser.open(url)


# ---------------- Función para cerrar toda la app ----------------
def cerrar_todo(event=None):
    try:
        root.destroy()
    except:
        pass
    sys.exit(0)


# ---------------- Función para abrir ventana de un juego ----------------
def abrir_ventana_juego(nombre_juego, api_subcarpeta="mods"):
    ventana = tk.Toplevel()
    ventana.title(f"Instalador de Mods - {nombre_juego}")
    ventana.geometry("500x750")
    ventana.configure(bg="#2c2f33")
    ventana.protocol("WM_DELETE_WINDOW", cerrar_todo)  # Forzar cierre

    frame_seleccion = tk.Frame(ventana, bg="#2c2f33")
    frame_seleccion.pack(fill="both", expand=True)

    titulo = tk.Label(frame_seleccion, text=f"Instalar mods en {nombre_juego}", 
                      font=("Arial", 14, "bold"), bg="#2c2f33", fg="white")
    titulo.pack(pady=20)

    barra_progreso = ttk.Progressbar(frame_seleccion, orient="horizontal", length=300, mode="determinate")
    barra_progreso.pack(pady=10)

    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory(title=f"Selecciona la carpeta de {nombre_juego}")
        if carpeta:
            mods_dir = os.path.join(carpeta, "BepInEx", "plugins")
            if not os.path.exists(mods_dir):
                messagebox.showerror("Error", f"No se encontró la carpeta BepInEx/Plugins en el directorio:\n{carpeta}")
                return
            hilo = threading.Thread(target=descargar_mods, args=(mods_dir, api_subcarpeta, ventana, barra_progreso))
            hilo.start()

    boton_carpeta = tk.Button(frame_seleccion, text=f"Seleccionar carpeta de {nombre_juego}", 
                              bg="#7289da", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3,
                              command=seleccionar_carpeta)
    boton_carpeta.pack(pady=10)

    boton_github = tk.Button(frame_seleccion, text="GitHub", 
                             bg="#7289da", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=1,
                             command=lambda: abrir_github(f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"))
    boton_github.pack(pady=10)

    def cambiar_juego():
        ventana.destroy()
        abrir_menu_juegos()

    boton_cambiar = tk.Button(frame_seleccion, text="Cambiar juego",
                              bg="#7289da", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3,
                              command=cambiar_juego)
    boton_cambiar.pack(pady=10)

    def on_enter(e):
        e.widget['bg'] = "#99aab5"
    def on_leave(e):
        e.widget['bg'] = "#7289da"

    boton_carpeta.bind("<Enter>", on_enter)
    boton_carpeta.bind("<Leave>", on_leave)
    boton_github.bind("<Enter>", on_enter)
    boton_github.bind("<Leave>", on_leave)
    boton_cambiar.bind("<Enter>", on_enter)
    boton_cambiar.bind("<Leave>", on_leave)


# ---------------- Menú de selección de juego ----------------
def abrir_menu_juegos():
    ventana_menu = tk.Toplevel()
    ventana_menu.title("Selecciona un Juego")
    ventana_menu.geometry("400x300")
    ventana_menu.configure(bg="#2c2f33")
    ventana_menu.protocol("WM_DELETE_WINDOW", cerrar_todo)  # Forzar cierre

    tk.Label(ventana_menu, text="Selecciona el juego", 
             font=("Arial", 14, "bold"), bg="#2c2f33", fg="white").pack(pady=20)

    juegos = [("Lethal Company", "mods_lethal"), ("REPO", "mods_repo"), ("Phasmo", "mods_phasmo")]

    for nombre, carpeta_api in juegos:
        tk.Button(ventana_menu, text=nombre, bg="#7289da", fg="white", font=("Arial", 12, "bold"),
                  relief="raised", bd=3, command=lambda n=nombre, c=carpeta_api: [ventana_menu.destroy(), abrir_ventana_juego(n, c)]).pack(pady=5)


# ---------------- Ejecutar ----------------
root = tk.Tk()
root.withdraw()  # Ocultamos la ventana principal
root.protocol("WM_DELETE_WINDOW", cerrar_todo)  # Forzar cierre
abrir_menu_juegos()
root.mainloop()


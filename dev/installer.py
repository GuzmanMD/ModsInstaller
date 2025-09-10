import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import requests
import zipfile
import io
import threading
import webbrowser

# ---------------- Configuración de descarga ----------------
GITHUB_USER = "GuzmanMD"
GITHUB_REPO = "ModsInstaller"
CARPETA_MODS = "mods"

# ---------------- Funciones generales ----------------
def descargar_mods(mods_dir, api_url, ventana, barra_progreso):
    cancelar_descarga = False
    try:
        r = requests.get(api_url)
        r.raise_for_status()
        archivos = r.json()

        zip_file = None
        for f in archivos:
            if f["name"].endswith(".zip"):
                zip_file = f["download_url"]
                break

        if not zip_file:
            messagebox.showerror("Error", "No se encontró ningún archivo .zip en la carpeta /mods del repo")
            return

        r = requests.get(zip_file, stream=True)
        r.raise_for_status()

        archivo_bytes = io.BytesIO()
        total = int(r.headers.get('content-length', 0))
        descargado = 0
        chunk_size = 8192

        for chunk in r.iter_content(chunk_size=chunk_size):
            archivo_bytes.write(chunk)
            descargado += len(chunk)
            progreso = int(descargado / total * 100) if total else 0
            barra_progreso['value'] = progreso
            ventana.update_idletasks()

        archivo_bytes.seek(0)
        with zipfile.ZipFile(archivo_bytes) as zip_ref:
            zip_ref.extractall(mods_dir)

        messagebox.showinfo("Éxito", f"Mods instalados en:\n{mods_dir}")

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error:\n{e}")

def abrir_github(url="https://github.com/GuzmanMD/ModsInstaller"):
    webbrowser.open(url)

# ---------------- Función para abrir ventana de un juego ----------------
def abrir_ventana_juego(nombre_juego, api_subcarpeta="mods"):
    ventana = tk.Toplevel()
    ventana.title(f"Instalador de Mods - {nombre_juego}")
    ventana.geometry("500x450")
    ventana.configure(bg="#2c2f33")

    # ---------------- Frame de selección de carpeta ---------------- #
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
            mods_dir = os.path.join(carpeta, "mods")
            if not os.path.exists(mods_dir):
                messagebox.showerror("Error", f"No se encontró la carpeta 'mods' en:\n{carpeta}")
                return
            hilo = threading.Thread(target=descargar_mods, args=(mods_dir, f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{api_subcarpeta}", ventana, barra_progreso))
            hilo.start()

    boton_carpeta = tk.Button(frame_seleccion, text=f"Seleccionar carpeta de {nombre_juego}", 
                              bg="#7289da", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3,
                              command=seleccionar_carpeta)
    boton_carpeta.pack(pady=10)

    boton_github = tk.Button(frame_seleccion, text="GitHub", 
                             bg="#7289da", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=1,
                             command=lambda: abrir_github(f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"))
    boton_github.pack(pady=10)

    # ---------------- Botón cambiar juego ---------------- #
    def cambiar_juego():
        ventana.destroy()
        abrir_menu_juegos()

    boton_cambiar = tk.Button(frame_seleccion, text="Cambiar juego",
                              bg="#7289da", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3,
                              command=cambiar_juego)
    boton_cambiar.pack(pady=10)

    # Efecto hover
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

    tk.Label(ventana_menu, text="Selecciona el juego", 
             font=("Arial", 14, "bold"), bg="#2c2f33", fg="white").pack(pady=20)

    juegos = [("Lethal Company", "mods_lethal"), ("REPO", "mods_repo"), ("Phasmo", "mods_phasmo")]

    for nombre, carpeta_api in juegos:
        tk.Button(ventana_menu, text=nombre, bg="#7289da", fg="white", font=("Arial", 12, "bold"),
                  relief="raised", bd=3, command=lambda n=nombre, c=carpeta_api: [ventana_menu.destroy(), abrir_ventana_juego(n, c)]).pack(pady=5)

# ---------------- Ejecutar ----------------
root = tk.Tk()
root.withdraw()  # Ocultamos la ventana principal

abrir_menu_juegos()
root.mainloop()

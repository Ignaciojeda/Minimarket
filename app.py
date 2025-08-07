import main  # tu main.py con la función para crear la base
import subprocess
import os
import sys

def main_app():
    # 1. Crear base si no existe
    main.crear_base_si_no_existe()

    # 2. Ejecutar menu_principal.py con el mismo intérprete Python
    ruta_menu = os.path.join(os.path.dirname(os.path.abspath(__file__)), "menu_principal.py")
    # Si quieres que el menu_principal se ejecute en el mismo proceso, podrías importarlo y llamarlo.
    # Pero como usas subprocess, se mantiene igual:
    subprocess.Popen([sys.executable, ruta_menu])

if __name__ == "__main__":
    main_app()

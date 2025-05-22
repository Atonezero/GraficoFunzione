import PyInstaller.__main__
import os
import sys

# Ottieni il percorso della directory corrente
current_dir = os.path.dirname(os.path.abspath(__file__))

# Configura i parametri per PyInstaller
PyInstaller.__main__.run([
    os.path.join(current_dir, 'src', 'main.py'),  # Il file principale con percorso completo
    '--name=GraficoFunzione',  # Nome dell'eseguibile
    '--onefile',  # Crea un singolo file eseguibile
    '--windowed',  # Non mostrare la console
    '--clean',  # Pulisci la cache prima di buildare
    '--noconfirm',  # Non chiedere conferma
    '--debug=all',  # Abilita il debug
    f'--workpath={os.path.join(current_dir, "build")}',  # Directory di lavoro
    f'--distpath={os.path.join(current_dir, "dist")}',  # Directory di output
    '--hidden-import=PIL._tkinter_finder',  # Import nascosti necessari
    '--hidden-import=matplotlib',
    '--hidden-import=numpy',
    '--hidden-import=sympy',
    '--hidden-import=sv_ttk',
    '--hidden-import=pywinstyles',
    '--collect-all=matplotlib',  # Raccogli tutte le dipendenze di matplotlib
    '--collect-all=numpy',  # Raccogli tutte le dipendenze di numpy
    '--collect-all=PIL',  # Raccogli tutte le dipendenze di PIL
    '--collect-all=sympy',  # Raccogli tutte le dipendenze di sympy
    '--collect-all=sv_ttk',  # Raccogli tutte le dipendenze di sv_ttk
    '--collect-all=pywinstyles',  # Raccogli tutte le dipendenze di pywinstyles
]) 
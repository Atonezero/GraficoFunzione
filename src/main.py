import tkinter as tk
from view import GraficoView

def main():
    root = tk.Tk()
    app = GraficoView(root)
    root.mainloop()

if __name__ == "__main__":
    main() 

#TODO:
# - Cambiare il font dei label interni
# - Spostare a sinistra il pulsante disegna grafico
# - Impostare dimensione varibile ma fissa della finestra
# - Aggiungere spaziatura nel lim h->0
# - Provare il tutto in WSL e con tema light
# - Provare a esportarlo come .exe
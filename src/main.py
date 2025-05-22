import tkinter as tk
from view import GraficoView

def main():
    root = tk.Tk()
    app = GraficoView(root)
    root.mainloop()

if __name__ == "__main__":
    main() 

#TODO:
# - Cambiare il font dei label interni in Roboto
# - Spostare a sinistra il pulsante disegna grafico
# - Provare il tutto in WSL e con tema light(con uno switch in alto a destra)
# - Provare a esportarlo come .exe
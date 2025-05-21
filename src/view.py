import tkinter as tk
from tkinter import ttk
import sv_ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import FunzioneFrazionaria, calcola_asintoto_obliquo
import pywinstyles, sys
import numpy as np
from sympy import Symbol, Eq, solve, sympify, diff, limit, oo
from sympy.printing.latex import latex
from PIL import Image, ImageTk
import io

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()
    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

def render_math_to_image(math_text, fontsize=16):
    fig = plt.figure(figsize=(5, 1))
    fig.text(0.5, 0.5, math_text, fontsize=fontsize, ha='center', va='center')
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

class GraficoView:
    def __init__(self, root,):
        self.root = root
        self.root.title("Grafico Funzione Frazionaria")
        sv_ttk.set_theme("dark")
        apply_theme_to_titlebar(root)
        
        # Frame principale
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.configure(style="Dark.TFrame")
        
        # Input frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Inserisci la funzione", padding="5", style="Dark.TLabelframe")
        self.input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Numeratore
        ttk.Label(self.input_frame, text="Numeratore:").grid(row=0, column=0, sticky=tk.W)
        self.num_entry = ttk.Entry(self.input_frame, width=30)
        self.num_entry.grid(row=0, column=1, padx=5)
        self.num_entry.insert(0, "x**2 - 25")
        
        # Denominatore
        ttk.Label(self.input_frame, text="Denominatore:").grid(row=1, column=0, sticky=tk.W)
        self.den_entry = ttk.Entry(self.input_frame, width=30)
        self.den_entry.grid(row=1, column=1, padx=5, pady=5)
        self.den_entry.insert(0, "x + 2")
        
        # Range frame
        self.range_frame = ttk.LabelFrame(self.main_frame, text="Range del grafico", padding="5", style="Dark.TLabelframe")
        self.range_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # X min
        ttk.Label(self.range_frame, text="X min:").grid(row=0, column=0, sticky=tk.W)
        self.xmin_entry = ttk.Entry(self.range_frame, width=10)
        self.xmin_entry.grid(row=0, column=1, padx=5)
        self.xmin_entry.insert(0, "-10")
        
        # X max
        ttk.Label(self.range_frame, text="X max:").grid(row=0, column=2, sticky=tk.W)
        self.xmax_entry = ttk.Entry(self.range_frame, width=10)
        self.xmax_entry.grid(row=0, column=3, padx=5)
        self.xmax_entry.insert(0, "10")
        
        # Y min
        ttk.Label(self.range_frame, text="Y min:").grid(row=1, column=0, sticky=tk.W)
        self.ymin_entry = ttk.Entry(self.range_frame, width=10)
        self.ymin_entry.grid(row=1, column=1, padx=5)
        self.ymin_entry.insert(0, "-20")
        
        # Y max
        ttk.Label(self.range_frame, text="Y max:").grid(row=1, column=2, sticky=tk.W)
        self.ymax_entry = ttk.Entry(self.range_frame, width=10)
        self.ymax_entry.grid(row=1, column=3, padx=5)
        self.ymax_entry.insert(0, "20")
        
        # Pulsante per disegnare
        self.draw_button = ttk.Button(self.main_frame, text="Disegna Grafico", command=self.disegna_grafico)
        self.draw_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame per il grafico
        self.graph_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.graph_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Creazione della figura matplotlib
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Stili personalizzati per dark mode
        style = ttk.Style()
        style.configure("Dark.TFrame", background="#222222")
        style.configure("Dark.TLabelframe", background="#222222", foreground="white")
        style.configure("Dark.TLabelframe.Label", background="#222222", foreground="white", font=('TkDefaultFont', 14)) 
        
        
        # Frame per le formule matematiche
        self.formule_frame = ttk.LabelFrame(self.main_frame, text="Calcolo della derivata", padding="5", style="Dark.TLabelframe")
        self.formule_frame.grid(row=0, column=2, rowspan=4, sticky=(tk.N, tk.E, tk.S), padx=2)
        
        # Frame per contenere le immagini delle formule
        self.formule_container = ttk.Frame(self.formule_frame, style="Dark.TFrame")
        self.formule_container.pack(fill=tk.BOTH, expand=True)
        
        # Labels per le formule
        self.funzione_img_label = ttk.Label(self.formule_container, style="Dark.TLabel")
        self.funzione_img_label.pack(anchor=tk.W, pady=(5,10))
        
        self.rapporto_img_label = ttk.Label(self.formule_container, style="Dark.TLabel")
        self.rapporto_img_label.pack(anchor=tk.W, pady=(5,10))
        
        self.limite_img_label = ttk.Label(self.formule_container, style="Dark.TLabel")
        self.limite_img_label.pack(anchor=tk.W, pady=(5,10))
        
        self.derivata_img_label = ttk.Label(self.formule_container, style="Dark.TLabel")
        self.derivata_img_label.pack(anchor=tk.W, pady=(5,10))
        
        # Blocca il ridimensionamento della finestra
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.root.minsize(width + 400, height)
        self.root.maxsize(width + 400, height)
        self.root.geometry(f"{width + 475}x{height}")
        
    def on_resize(self, event):
        self.canvas.draw()
        
    def disegna_grafico(self):
        try:
            # Ottieni i valori dagli entry
            numeratore = self.num_entry.get()
            denominatore = self.den_entry.get()
            try:
                x_min = float(self.xmin_entry.get())
                x_max = float(self.xmax_entry.get())
                y_min = float(self.ymin_entry.get())
                y_max = float(self.ymax_entry.get())
            except ValueError:
                tk.messagebox.showerror("Errore", "I valori di X min, X max, Y min e Y max devono essere numerici.")
                return
            if x_min >= x_max:
                tk.messagebox.showerror("Errore", "X min deve essere strettamente minore di X max.")
                return
            if y_min >= y_max:
                tk.messagebox.showerror("Errore", "Y min deve essere strettamente minore di Y max.")
                return
                
            # Crea l'istanza della funzione
            funzione = FunzioneFrazionaria(numeratore, denominatore)
            
            # Ottieni i punti per il grafico
            x, y = funzione.get_dominio(x_min, x_max)
            
            # Pulisci il grafico precedente
            self.ax.clear()
            
            # Imposta sfondo e colori scuri
            self.fig.patch.set_facecolor('#222222')
            self.ax.set_facecolor('#222222')
            self.ax.tick_params(colors='white')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.title.set_color('white')
            
            # Disegna il nuovo grafico
            self.ax.plot(x, y, color='white')
            self.ax.grid(True, color='#444444')
            self.ax.axhline(y=0, color='#888888', linestyle='-', alpha=0.3)
            self.ax.axvline(x=0, color='#888888', linestyle='-', alpha=0.3)
            
            # Imposta i limiti degli assi
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_ylim(y_min, y_max)
            
            # Calcola e disegna gli asintoti verticali
            asintoti = funzione.calcola_campo_esistenza()
            for asintoto in asintoti:
                if asintoto.is_real:
                    self.ax.axvline(x=float(asintoto), color='red', linestyle='-', alpha=0.5)
            
            # Calcola e disegna l'asintoto obliquo
            asintoto_obliquo = calcola_asintoto_obliquo(numeratore, denominatore)
            if asintoto_obliquo is not None:
                m, q = asintoto_obliquo
                x_vals = np.linspace(x_min, x_max, 500)
                y_vals = m * x_vals + q
                self.ax.plot(x_vals, y_vals, color='hotpink', linestyle='--', linewidth=2, label='Asintoto obliquo')
            
            # Calcola e disegna gli zeri della funzione
            zeri = funzione.calcola_zeri()
            for zero in zeri:
                if zero.is_real:
                    self.ax.axvline(x=float(zero), color='green', linestyle='--', alpha=0.5)
            
            # Calcola e applica il segno della funzione
            intervalli_segno = funzione.calcola_segno()
            for a, b, segno in intervalli_segno:
                if not np.isfinite(a):
                    a = x[0]
                if not np.isfinite(b):
                    b = x[-1]
                if segno > 0:
                    self.ax.axvspan(a, b, ymin=0, ymax=0.5, color='gray', alpha=0.3, hatch='///', zorder=0)
                else:
                    self.ax.axvspan(a, b, ymin=0.5, ymax=1, color='gray', alpha=0.3, hatch='///', zorder=0)
            
            # Calcolo simbolico della funzione e della sua derivata
            x_sym = Symbol('x')
            h_sym = Symbol('h')
            num_sym = sympify(numeratore)
            den_sym = sympify(denominatore)
            f_sym = num_sym / den_sym
            
            # Calcola il rapporto incrementale
            f_x_plus_h = f_sym.subs(x_sym, x_sym + h_sym)
            rapporto_incrementale = (f_x_plus_h - f_sym) / h_sym
            
            # Calcola il limite del rapporto incrementale
            f_prime = diff(f_sym, x_sym)
            lim_rapporto = limit(rapporto_incrementale, h_sym, 0)
            
            # Genera le formule in LaTeX
            funzione_tex = r"$f(x) = " + latex(f_sym) + r"$"
            rapporto_tex = r"$\frac{f(x+h) - f(x)}{h} = " + latex(rapporto_incrementale) + r"$"
            limite_tex = r"$\lim_{h \to 0} \frac{f(x+h) - f(x)}{h} = " + latex(lim_rapporto) + r"$"
            derivata_tex = r"$f'(x) = " + latex(f_prime) + r"$"
            
            # Renderizza le formule
            self.funzione_img = ImageTk.PhotoImage(render_math_to_image(funzione_tex))
            self.rapporto_img = ImageTk.PhotoImage(render_math_to_image(rapporto_tex))
            self.limite_img = ImageTk.PhotoImage(render_math_to_image(limite_tex))
            self.derivata_img = ImageTk.PhotoImage(render_math_to_image(derivata_tex))
            
            # Aggiorna le labels con le immagini
            self.funzione_img_label.configure(image=self.funzione_img)
            self.rapporto_img_label.configure(image=self.rapporto_img)
            self.limite_img_label.configure(image=self.limite_img)
            self.derivata_img_label.configure(image=self.derivata_img)
            
            # Aggiorna il canvas
            self.canvas.draw()
            
        except Exception as e:
            tk.messagebox.showerror("Errore", str(e))

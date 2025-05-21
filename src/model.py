import numpy as np
from sympy import Symbol, solve, Eq, sympify, limit, oo

class FunzioneFrazionaria:
    def __init__(self, numeratore, denominatore):
        """
        Inizializza una funzione fratta
        :param numeratore: stringa rappresentante il numeratore
        :param denominatore: stringa rappresentante il denominatore
        """
        self.numeratore = numeratore
        self.denominatore = denominatore

    def calcola_valori(self, x):
        """
        Calcola i valori della funzione per un array di x
        :param x: array di valori x
        :return: array di valori y
        """
        try:
            # Valuta il numeratore e il denominatore
            num = eval(self.numeratore, {"x": x, "np": np})
            den = eval(self.denominatore, {"x": x, "np": np})
            
            # Gestisce la divisione per zero
            y = np.divide(num, den, out=np.zeros_like(num), where=den!=0)
            return y
        except Exception as e:
            raise ValueError(f"Errore nel calcolo della funzione: {str(e)}")

    def get_dominio(self, x_min, x_max, punti=1000):
        """
        Genera i punti x e y per il grafico
        :param x_min: valore minimo di x
        :param x_max: valore massimo di x
        :param punti: numero di punti da generare
        :return: tuple (x, y)
        """
        x = np.linspace(x_min, x_max, punti)
        y = self.calcola_valori(x)
        return x, y

    def calcola_campo_esistenza(self):
        """
        Calcola il campo di esistenza della funzione, ponendo il denominatore a zero.
        :return: lista di punti di asintoto verticale
        """
        x = Symbol('x')
        den = sympify(self.denominatore)
        asintoti = solve(Eq(den, 0), x)
        return asintoti

    def calcola_zeri(self):
        """
        Calcola gli zeri della funzione, ponendo il numeratore a zero.
        :return: lista di zeri della funzione
        """
        x = Symbol('x')
        num = sympify(self.numeratore)
        zeri = solve(Eq(num, 0), x)
        return zeri

    def calcola_segno(self):
        """
        Calcola il segno della funzione, ponendo a sistema denominatore > 0 e numeratore > 0.
        :return: lista di intervalli di segno
        """
        x = Symbol('x')
        num = sympify(self.numeratore)
        den = sympify(self.denominatore)
        num_zeri = solve(Eq(num, 0), x)
        den_zeri = solve(Eq(den, 0), x)
        punti_critici = sorted([float(p) for p in num_zeri + den_zeri if p.is_real])
        intervalli = []
        # Aggiungi estremi per coprire tutto il dominio
        estremi = [float('-inf')] + punti_critici + [float('inf')]
        for i in range(len(estremi) - 1):
            x_test = estremi[i] + 1e-3 if estremi[i] != float('-inf') else estremi[i+1] - 1
            try:
                val = num.subs(x, x_test) / den.subs(x, x_test)
                segno = 1 if val > 0 else -1
                intervalli.append((estremi[i], estremi[i+1], segno))
            except Exception:
                continue
        return intervalli 

def calcola_asintoto_obliquo(numeratore, denominatore):
    x = Symbol('x')
    num = sympify(numeratore)
    den = sympify(denominatore)
    f = num / den
    # Calcola il coefficiente angolare m
    try:
        m = limit(f / x, x, oo)
    except Exception:
        m = None
    # Se m esiste, non è infinito e non è zero
    if m is not None and m != 0 and m.is_finite:
        try:
            q = limit(f - m * x, x, oo)
        except Exception:
            q = None
        if q is not None and q.is_finite:
            return float(m), float(q)
    return None 
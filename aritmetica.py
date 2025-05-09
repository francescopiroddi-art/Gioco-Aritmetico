# Gioco Aritmetico - Interfaccia grafica con Tkinter
# Copyright (C) 2025 Francesco Piroddi
#
# Questo programma è software libero: puoi ridistribuirlo e/o modificarlo
# secondo i termini della Licenza Pubblica Generica GNU pubblicata
# dalla Free Software Foundation, versione 3 della licenza o (a tua scelta)
# una versione successiva.
#
# Questo programma è distribuito nella speranza che possa essere utile,
# ma SENZA ALCUNA GARANZIA; senza neppure la garanzia implicita di
# COMMERCIABILITÀ o di IDONEITÀ PER UN PARTICOLARE SCOPO. Vedi la
# Licenza Pubblica Generica GNU per maggiori dettagli.
#
# Dovresti aver ricevuto una copia della Licenza Pubblica Generica GNU
# insieme a questo programma. In caso contrario, vedi <https://www.gnu.org/licenses/>.

import tkinter as tk
import random
import time
from tkinter import messagebox

class GiocoAritmetico:
    def __init__(self, root):
        self.root = root
        self.root.title("Gioco Aritmetico")
        self.punteggio = 0
        self.livello = 1
        self.punteggio_massimo = 0
        self.in_gioco = False

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()

        self.label_operazione = tk.Label(self.frame, text="", font=("Arial", 18))
        self.label_operazione.pack()

        self.entry_risposta = tk.Entry(self.frame, font=("Arial", 16))
        self.entry_risposta.pack()
        self.entry_risposta.bind("<Return>", self.verifica_risposta)

        self.label_info = tk.Label(self.frame, text="Punteggio: 0 | Livello: 1 | Record: 0", font=("Arial", 12))
        self.label_info.pack(pady=10)

        self.label_timer = tk.Label(self.frame, text="Tempo: 0.0 sec", font=("Arial", 12))
        self.label_timer.pack()

        self.btn_start = tk.Button(self.frame, text="Start", command=self.start_game, bg="green", fg="white")
        self.btn_start.pack(side="left", padx=10)

        self.btn_stop = tk.Button(self.frame, text="Stop", command=self.stop_game, bg="red", fg="white")
        self.btn_stop.pack(side="right", padx=10)

        self.operazione_corrente = None
        self.tempo_inizio = None
        self.aggiorna_timer_id = None

    def start_game(self):
        if self.in_gioco:
            return
        self.in_gioco = True
        self.punteggio = 0
        self.livello = 1
        self.tempo_inizio = time.time()
        self.mostra_nuova_operazione()
        self.aggiorna_timer()

    def stop_game(self):
        if self.aggiorna_timer_id:
            self.root.after_cancel(self.aggiorna_timer_id)
        self.in_gioco = False
        self.label_operazione.config(text="Gioco fermato.")
        self.entry_risposta.delete(0, tk.END)

    def genera_operazione(self):
        op = random.choice(['+', '-', '*', '/'])
        if op == '/':
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
        else:
            a = random.randint(1, 100)
            b = random.randint(1, 100)
        return a, b, op

    def calcola_risultato(self, a, b, op):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a // b

    def mostra_nuova_operazione(self):
        self.operazione_corrente = self.genera_operazione()
        a, b, op = self.operazione_corrente
        self.label_operazione.config(text=f"Quanto fa {a} {op} {b}?")
        self.entry_risposta.delete(0, tk.END)
        self.entry_risposta.focus()

    def verifica_risposta(self, event):
        if not self.in_gioco:
            return
        try:
            risposta = int(self.entry_risposta.get())
            a, b, op = self.operazione_corrente
            risultato_corretto = self.calcola_risultato(a, b, op)

            if risposta == risultato_corretto:
                self.punteggio += risultato_corretto

            if self.punteggio >= 1000:
                tempo_trascorso = time.time() - self.tempo_inizio
                messagebox.showinfo("Livello completato!",
                    f"Hai completato il livello {self.livello} in {tempo_trascorso:.2f} secondi!")
                self.punteggio *= 10
                self.livello += 1
                self.tempo_inizio = time.time()

            if self.punteggio > self.punteggio_massimo:
                self.punteggio_massimo = self.punteggio

            self.aggiorna_info()
            self.mostra_nuova_operazione()

        except ValueError:
            messagebox.showwarning("Errore", "Inserisci un numero valido.")
            self.entry_risposta.delete(0, tk.END)

    def aggiorna_info(self):
        self.label_info.config(
            text=f"Punteggio: {self.punteggio} | Livello: {self.livello} | Record: {self.punteggio_massimo}"
        )

    def aggiorna_timer(self):
        if self.in_gioco:
            tempo_attuale = time.time() - self.tempo_inizio
            self.label_timer.config(text=f"Tempo: {tempo_attuale:.1f} sec")
            self.aggiorna_timer_id = self.root.after(100, self.aggiorna_timer)

# Avvia la finestra
if __name__ == "__main__":
    root = tk.Tk()
    app = GiocoAritmetico(root)
    root.mainloop()

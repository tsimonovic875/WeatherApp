import tkinter as tk
import json,requests

API_KEY = "06c921750b9a82d8f5d1294e1586276f"


class AplikacijaVremena:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacija za prognozu vremena")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1e293b")
        self.glavni_okvir = tk.Frame(root, bg="#1e293b")
        self.glavni_okvir.pack(fill="both", expand=True)
        
        self.okvir1 = tk.Frame(self.glavni_okvir, bg="#1e293b")
        self.okvir1.pack(side="left", fill="both", expand=True)

        naslov = tk.Label(
            self.okvir1,
            text="Prognoza vremena",
            font=("Segoe UI", 28, "bold"),
            bg="#1e293b",
            fg="white"
        )
        naslov.pack(pady=15)
        
        self.unos_grad = tk.Entry(
            self.okvir1,
            font=("Segoe UI", 18),
            justify="center"
        )
        self.unos_grad.pack(pady=10)

        okvir_za_dugmad = tk.Frame(self.okvir1, bg="#1e293b")
        okvir_za_dugmad.pack()

        tk.Button(
            okvir_za_dugmad,
            text="Pretraži"
        ).pack(side="left", padx=5)

        tk.Button(
            okvir_za_dugmad,
            text="Moja lokacija",
            command=self.detektuj_lokaciju
        ).pack(side="left", padx=5)

        tk.Button(
            okvir_za_dugmad,
            text="⭐ Dodaj"
        ).pack(side="left", padx=5)

        self.label_ikona = tk.Label(
            self.okvir1,
            text="☀️",
            font=("Segoe UI Emoji", 70),
            bg="#1e293b"
        )
        self.label_ikona.pack()
    def detektuj_lokaciju(self):
        try:
            podaci = requests.get("https://ipinfo.io/json").json()
            grad = podaci["city"]
            print(grad)
        except:
            print("Nema pristup")
root = tk.Tk()
app = AplikacijaVremena(root)
root.mainloop()

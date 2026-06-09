import tkinter as tk
import json,requests
from tkinter import messagebox

API_KEY = "06c921750b9a82d8f5d1294e1586276f"

ikonice_vremena = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Snow": "❄️",
    "Thunderstorm": "⛈️",
    "Drizzle": "🌦️",
    "Mist": "🌫️"
}

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
        self.label_info = tk.Label(
            self.okvir1,
            text="",
            font=("Segoe UI", 14),
            bg="#1e293b",
            fg="white",
            justify="left"
        )
        self.label_info.pack(pady=10)
        self.label_vrijeme = tk.Label(
            self.okvir1,
            text="",
            font=("Segoe UI", 22, "bold"),
            bg="#1e293b",
            fg="white"
        )
        self.label_vrijeme.pack()
    def trenutno_vrijeme(self):

        grad = self.unos_grad.get().strip()
        if not grad:
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={grad}&appid={API_KEY}&units=metric"

        try:
            podaci = requests.get(url).json()

            vrijeme = podaci["weather"][0]["main"]
            temp = round(podaci["main"]["temp"])
            vlaznost = podaci["main"]["humidity"]
            pritisak = podaci["main"]["pressure"]
            vjetar = podaci["wind"]["speed"]

            self.vremenska_zona = podaci["timezone"]

            self.label_ikona.config(text=ikonice_vremena.get(vrijeme, "🌍"))
            self.label_vrijeme.config(text=f"{grad} • {temp}°C")

            self.label_info.config(
                text=f"Vrijeme: {vrijeme}\nVlažnost: {vlaznost}%\nPritisak: {pritisak} hPa\nVjetar: {vjetar} m/s"
            )

 

        except Exception as e:
            messagebox.showerror("Greška", str(e))
            
    def detektuj_lokaciju(self):
        try:
            podaci = requests.get("https://ipinfo.io/json").json()
            grad = podaci["city"]

            self.unos_grad.delete(0, tk.END)
            self.unos_grad.insert(0, grad)

            self.trenutno_vrijeme()

        except:
            messagebox.showerror("Greška", "Ne mogu lokaciju.")
root = tk.Tk()
app = AplikacijaVremena(root)
root.mainloop()

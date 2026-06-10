import tkinter as tk
import json,requests
from tkinter import messagebox
from datetime import datetime, timedelta
import os
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
        self.vremenska_zona=0
        self.omiljeni_gradovi = self.ucitaj_gradove()

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
            text="Pretraži",
            command=self.trenutno_vrijeme
        ).pack(side="left", padx=5)

        tk.Button(
            okvir_za_dugmad,
            text="Moja lokacija",
            command=self.detektuj_lokaciju
        ).pack(side="left", padx=5)

        tk.Button(
            okvir_za_dugmad,
            text="⭐ Dodaj",
            command=self.dodaj_u_omiljene
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

        self.label_sat = tk.Label(
            self.okvir1,
            text="",
            font=("Segoe UI", 18),
            bg="#1e293b",
            fg="#38bdf8"
        )
        self.label_sat.pack()
        self.label_prognoza = tk.Label(
            self.okvir1,
            text="",
            font=("Consolas", 12),
            bg="#1e293b",
            fg="white",
            justify="left"
        )
        self.label_prognoza.pack(pady=20)

        self.sidebar = tk.Frame(self.glavni_okvir, bg="#0f172a", width=220)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar,
            text="⭐ Omiljeni",
            bg="#0f172a",
            fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        self.lista_gradova = tk.Listbox(
            self.sidebar,
            font=("Segoe UI", 11),
            bg="#1e293b",
            fg="white",
            selectbackground="#38bdf8",
            height=18
        )
        self.lista_gradova.pack(padx=10, pady=5, fill="both", expand=True)
        self.osvjezi_listu()

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

            self.trenutno_sati()
            lat = podaci["coord"]["lat"]
            lon = podaci["coord"]["lon"]
            self.duza_prognoza(lat, lon)
        except Exception as e:
            messagebox.showerror("Greška", str(e))
    def dodaj_u_omiljene(self):
        grad = self.unos_grad.get().strip()
        if not grad:
            return

        if grad not in self.omiljeni_gradovi:
            self.omiljeni_gradovi.append(grad)
            self.sacuvaj_gradove()
            self.osvjezi_listu()
    def osvjezi_listu(self):
        self.lista_gradova.delete(0, tk.END)
        for g in self.omiljeni_gradovi:
            self.lista_gradova.insert(tk.END, g)
    def sacuvaj_gradove(self):
        with open("omiljeni_gradovi.json", "w", encoding="utf-8") as f:
            json.dump(self.omiljeni_gradovi, f, ensure_ascii=False)

    def ucitaj_gradove(self):
        if os.path.exists("omiljeni_gradovi.json"):
            with open("omiljeni_gradovi.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    def detektuj_lokaciju(self):
        try:
            podaci = requests.get("https://ipinfo.io/json").json()
            grad = podaci["city"]

            self.unos_grad.delete(0, tk.END)
            self.unos_grad.insert(0, grad)

            self.trenutno_vrijeme()
            
            loc = podaci["loc"].split(",")
            lat = float(loc[0])
            lon = float(loc[1])
            self.duza_prognoza(lat, lon)
        except:
            messagebox.showerror("Greška", "Nema lokacije.")
    def duza_prognoza(self, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

        podaci = requests.get(url).json()

        if "list" not in podaci:
            self.label_prognoza.config(text="Greška prognoze")
            return

        tekst=""

        for i in range(0, min(len(podaci["list"]), 40), 8):
            s = podaci["list"][i]
            datum = s["dt_txt"].split(" ")[0]
            temp = round(s["main"]["temp"])
            vr = s["weather"][0]["main"]
            tekst += f"{datum}  {vr}  {temp}°C\n"

        self.label_prognoza.config(text=tekst)
    def trenutno_sati(self):
        lokalno = datetime.utcnow() + timedelta(seconds=self.vremenska_zona)
        self.label_sat.config(text=lokalno.strftime("%H:%M:%S"))
        self.root.after(1000, self.trenutno_sati)
root = tk.Tk()
app = AplikacijaVremena(root)
root.mainloop()

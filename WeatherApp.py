import tkinter as tk

API_KEY = "06c921750b9a82d8f5d1294e1586276f"

class AplikacijaVremena:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacija za prognozu vremena")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1e293b")


root = tk.Tk()
app = AplikacijaVremena(root)
root.mainloop()


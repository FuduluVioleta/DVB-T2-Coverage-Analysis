import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

FISIER_CSV = "masuratori.csv"
FISIER_GPS = "gps_curent.txt"
FISIER_RSSI = "semnal_curent.txt"


def creeaza_csv_daca_nu_exista():
    if not os.path.exists(FISIER_CSV):
        with open(FISIER_CSV, "w", newline="", encoding="utf-8") as fisier:
            writer = csv.writer(fisier)
            writer.writerow([
                "id_punct",
                "data_ora_salvare",
                "latitudine",
                "longitudine",
                "frecventa_mhz",
                "canal",
                "mediu",
                "inaltime_receptie_m",
                "rssi_db",
                "timestamp_gps",
                "timestamp_rssi",
                "mod_rssi",
                "observatii"
            ])


def citeste_gps_din_fisier():
    try:
        with open(FISIER_GPS, "r", encoding="utf-8") as fisier:
            linie = fisier.readline().strip()

        parti = linie.split(",")

        if len(parti) >= 3:
            timestamp = parti[0].strip()
            lat = parti[1].strip()
            lon = parti[2].strip()

            float(lat)
            float(lon)

            entry_latitudine.config(state="normal")
            entry_longitudine.config(state="normal")

            entry_latitudine.delete(0, tk.END)
            entry_latitudine.insert(0, lat)

            entry_longitudine.delete(0, tk.END)
            entry_longitudine.insert(0, lon)

            entry_latitudine.config(state="readonly")
            entry_longitudine.config(state="readonly")

            label_status_gps.config(text=f"GPS actualizat: {timestamp}")
            label_timestamp_gps.config(text=timestamp)

    except Exception:
        label_status_gps.config(text="GPS indisponibil")

    fereastra.after(1000, citeste_gps_din_fisier)


def citeste_rssi_din_fisier():
    if var_mod_rssi.get() == "manual":
        fereastra.after(1000, citeste_rssi_din_fisier)
        return

    try:
        with open(FISIER_RSSI, "r", encoding="utf-8") as fisier:
            linie = fisier.readline().strip()

        parti = linie.split(",")

        if len(parti) >= 2:
            timestamp = parti[0].strip()
            rssi = parti[1].strip()

            float(rssi)

            entry_rssi.delete(0, tk.END)
            entry_rssi.insert(0, rssi)

            label_status_rssi.config(text=f"RSSI actualizat: {timestamp}")
            label_timestamp_rssi.config(text=timestamp)

    except Exception:
        label_status_rssi.config(text="RSSI automat indisponibil")

    fereastra.after(1000, citeste_rssi_din_fisier)


def salveaza_punct():
    id_punct = entry_id_punct.get().strip()
    latitudine = entry_latitudine.get().strip()
    longitudine = entry_longitudine.get().strip()
    frecventa = entry_frecventa.get().strip()
    canal = entry_canal.get().strip()
    mediu = var_mediu.get()
    inaltime = entry_inaltime.get().strip()
    rssi = entry_rssi.get().strip()
    observatii = entry_observatii.get().strip()
    timestamp_gps = label_timestamp_gps.cget("text")
    timestamp_rssi = label_timestamp_rssi.cget("text")
    mod_rssi = var_mod_rssi.get()

    if id_punct == "":
        messagebox.showerror("Eroare", "Completează ID-ul punctului.")
        return

    if latitudine == "" or longitudine == "":
        messagebox.showerror("Eroare", "Nu există coordonate GPS valide.")
        return

    if frecventa == "":
        messagebox.showerror("Eroare", "Completează frecvența.")
        return

    if canal == "":
        messagebox.showerror("Eroare", "Completează canalul.")
        return

    if inaltime == "":
        messagebox.showerror("Eroare", "Completează înălțimea de recepție.")
        return

    if rssi == "":
        messagebox.showerror("Eroare", "Nu există valoare RSSI.")
        return

    try:
        float(latitudine)
        float(longitudine)
        float(frecventa)
        float(inaltime)
        float(rssi)
    except ValueError:
        messagebox.showerror("Eroare", "Coordonatele, frecvența, înălțimea și RSSI trebuie să fie numere.")
        return

    data_ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FISIER_CSV, "a", newline="", encoding="utf-8") as fisier:
        writer = csv.writer(fisier)
        writer.writerow([
            id_punct,
            data_ora,
            latitudine,
            longitudine,
            frecventa,
            canal,
            mediu,
            inaltime,
            rssi,
            timestamp_gps,
            timestamp_rssi,
            mod_rssi,
            observatii
        ])

    messagebox.showinfo("Succes", "Punctul a fost salvat în CSV.")
    pregateste_punct_nou()


def pregateste_punct_nou():
    entry_rssi.delete(0, tk.END)
    entry_observatii.delete(0, tk.END)

    try:
        id_curent = int(entry_id_punct.get())
        entry_id_punct.delete(0, tk.END)
        entry_id_punct.insert(0, str(id_curent + 1))
    except ValueError:
        pass


def reseteaza_tot():
    entry_id_punct.delete(0, tk.END)
    entry_id_punct.insert(0, "1")

    entry_frecventa.delete(0, tk.END)
    entry_canal.delete(0, tk.END)
    entry_inaltime.delete(0, tk.END)
    entry_rssi.delete(0, tk.END)
    entry_observatii.delete(0, tk.END)

    var_mediu.set("urban")
    var_mod_rssi.set("automat")


def schimba_mod_rssi():
    if var_mod_rssi.get() == "manual":
        label_status_rssi.config(text="RSSI introdus manual")
    else:
        label_status_rssi.config(text="RSSI automat activ")


creeaza_csv_daca_nu_exista()

fereastra = tk.Tk()
fereastra.title("Aplicație colectare date SDR/GPS")
fereastra.geometry("850x620")
fereastra.configure(bg="#f2f4f7")

stil = ttk.Style()
stil.theme_use("clam")
stil.configure("TFrame", background="#f2f4f7")
stil.configure("TLabel", background="#f2f4f7", font=("Arial", 10))
stil.configure("Titlu.TLabel", background="#f2f4f7", font=("Arial", 15, "bold"))
stil.configure("TButton", font=("Arial", 10), padding=6)

frame_principal = ttk.Frame(fereastra, padding=15)
frame_principal.pack(fill="both", expand=True)

ttk.Label(
    frame_principal,
    text="Aplicație colectare date SDR/GPS",
    style="Titlu.TLabel"
).pack(pady=(0, 10))

frame_date = ttk.LabelFrame(frame_principal, text="Date punct de măsurare", padding=12)
frame_date.pack(fill="x", pady=8)

ttk.Label(frame_date, text="ID punct").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_id_punct = ttk.Entry(frame_date, width=25)
entry_id_punct.grid(row=0, column=1, padx=5, pady=5)
entry_id_punct.insert(0, "1")

ttk.Label(frame_date, text="Latitudine GPS").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_latitudine = ttk.Entry(frame_date, width=25, state="readonly")
entry_latitudine.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_date, text="Longitudine GPS").grid(row=1, column=2, sticky="w", padx=5, pady=5)
entry_longitudine = ttk.Entry(frame_date, width=25, state="readonly")
entry_longitudine.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(frame_date, text="Frecvență [MHz]").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_frecventa = ttk.Entry(frame_date, width=25)
entry_frecventa.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_date, text="Canal").grid(row=2, column=2, sticky="w", padx=5, pady=5)
entry_canal = ttk.Entry(frame_date, width=25)
entry_canal.grid(row=2, column=3, padx=5, pady=5)

ttk.Label(frame_date, text="Mediu").grid(row=3, column=0, sticky="w", padx=5, pady=5)
var_mediu = tk.StringVar(value="urban")
combo_mediu = ttk.Combobox(
    frame_date,
    textvariable=var_mediu,
    values=["urban", "rural"],
    state="readonly",
    width=22
)
combo_mediu.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame_date, text="Înălțime recepție [m]").grid(row=3, column=2, sticky="w", padx=5, pady=5)
entry_inaltime = ttk.Entry(frame_date, width=25)
entry_inaltime.grid(row=3, column=3, padx=5, pady=5)

label_status_gps = ttk.Label(frame_date, text="GPS indisponibil")
label_status_gps.grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=5)

label_timestamp_gps = ttk.Label(frame_date, text="-")
label_timestamp_gps.grid(row=4, column=3, sticky="e", padx=5, pady=5)

frame_semnal = ttk.LabelFrame(frame_principal, text="Nivel semnal", padding=12)
frame_semnal.pack(fill="x", pady=8)

ttk.Label(frame_semnal, text="Mod RSSI").grid(row=0, column=0, sticky="w", padx=5, pady=5)
var_mod_rssi = tk.StringVar(value="automat")

radio_auto = ttk.Radiobutton(
    frame_semnal,
    text="Automat din GNU Radio",
    variable=var_mod_rssi,
    value="automat",
    command=schimba_mod_rssi
)
radio_auto.grid(row=0, column=1, sticky="w", padx=5, pady=5)

radio_manual = ttk.Radiobutton(
    frame_semnal,
    text="Manual",
    variable=var_mod_rssi,
    value="manual",
    command=schimba_mod_rssi
)
radio_manual.grid(row=0, column=2, sticky="w", padx=5, pady=5)

ttk.Label(frame_semnal, text="RSSI [dB / dBm]").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_rssi = ttk.Entry(frame_semnal, width=25)
entry_rssi.grid(row=1, column=1, padx=5, pady=5)

label_status_rssi = ttk.Label(frame_semnal, text="RSSI automat activ")
label_status_rssi.grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5)

label_timestamp_rssi = ttk.Label(frame_semnal, text="-")
label_timestamp_rssi.grid(row=2, column=3, sticky="e", padx=5, pady=5)

frame_observatii = ttk.LabelFrame(frame_principal, text="Observații", padding=12)
frame_observatii.pack(fill="x", pady=8)

entry_observatii = ttk.Entry(frame_observatii, width=100)
entry_observatii.pack(fill="x", padx=5, pady=5)

frame_butoane = ttk.Frame(frame_principal)
frame_butoane.pack(pady=15)

buton_salveaza = ttk.Button(frame_butoane, text="Salvează punct", command=salveaza_punct)
buton_salveaza.grid(row=0, column=0, padx=10)

buton_reseteaza = ttk.Button(frame_butoane, text="Resetează tot", command=reseteaza_tot)
buton_reseteaza.grid(row=0, column=1, padx=10)

citeste_gps_din_fisier()
citeste_rssi_din_fisier()

fereastra.mainloop()
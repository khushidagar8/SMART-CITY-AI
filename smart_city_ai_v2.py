
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import random
import csv

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================
# SMART CITY AI - VERSION 2.0
# Advanced Analytics and Management System
# ==========================================

root = tk.Tk()
root.title("SMART CITY AI | Advanced Analytics")
root.geometry("1350x820")
root.minsize(1050, 700)
root.configure(bg="#0B1120")

BG = "#0B1120"
PANEL = "#151F32"
CARD = "#1C2940"
BLUE = "#3285F5"
CYAN = "#21C7D9"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"
GREEN = "#22C55E"
ORANGE = "#F59E0B"
RED = "#EF4444"

# SIMULATED CITY DATA

zones = [
    "Sector 15",
    "Central Market",
    "Railway Road",
    "Industrial Area",
    "City Centre",
    "Main Highway"
]

traffic = [random.randint(20, 95) for _ in zones]
pollution = [random.randint(40, 250) for _ in zones]
vehicles = [random.randint(100, 900) for _ in zones]

incidents = []


# MAIN HEADER

header = tk.Frame(root, bg=PANEL, height=75)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="SMART CITY AI",
    font=("Arial", 23, "bold"),
    bg=PANEL,
    fg=CYAN
).pack(side="left", padx=25)

tk.Label(
    header,
    text="ADVANCED CITY INTELLIGENCE SYSTEM",
    font=("Arial", 10),
    bg=PANEL,
    fg=MUTED
).pack(side="left")

clock = tk.Label(
    header,
    bg=PANEL,
    fg=WHITE,
    font=("Arial", 11, "bold")
)
clock.pack(side="right", padx=25)


def update_clock():
    clock.config(
        text=datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
    )
    root.after(1000, update_clock)


# MAIN LAYOUT

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True)

sidebar = tk.Frame(main, bg=PANEL, width=225)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = tk.Frame(main, bg=BG)
content.pack(
    side="left",
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


def heading(title, subtitle):
    tk.Label(
        content,
        text=title,
        bg=BG,
        fg=WHITE,
        font=("Arial", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        content,
        text=subtitle,
        bg=BG,
        fg=MUTED,
        font=("Arial", 10)
    ).pack(anchor="w", pady=(5, 20))


def make_card(parent, title, value, color):
    card = tk.Frame(
        parent,
        bg=CARD,
        padx=16,
        pady=15
    )
    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=6
    )

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=MUTED,
        font=("Arial", 10)
    ).pack(anchor="w")

    tk.Label(
        card,
        text=value,
        bg=CARD,
        fg=color,
        font=("Arial", 23, "bold")
    ).pack(anchor="w", pady=9)


def create_chart(parent, title, values, color, ylabel):
    fig = Figure(figsize=(7, 3.1), dpi=90)
    fig.patch.set_facecolor(CARD)

    ax = fig.add_subplot(111)
    ax.set_facecolor(CARD)

    bars = ax.bar(
        zones,
        values,
        color=color,
        width=0.55
    )

    ax.set_title(
        title,
        color=WHITE,
        fontsize=12,
        pad=15
    )

    ax.set_ylabel(ylabel, color=MUTED)
    ax.tick_params(axis="x", labelrotation=18, colors=WHITE)
    ax.tick_params(axis="y", colors=WHITE)

    for spine in ax.spines.values():
        spine.set_color("#34445E")

    ax.grid(
        axis="y",
        alpha=0.2,
        linestyle="--"
    )

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(int(bar.get_height())),
            ha="center",
            va="bottom",
            color=WHITE,
            fontsize=8
        )

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# DASHBOARD

def show_dashboard():
    clear_content()

    heading(
        "Smart City Dashboard",
        "Central intelligence and monitoring overview"
    )

    stats = tk.Frame(content, bg=BG)
    stats.pack(fill="x")

    avg_traffic = sum(traffic) // len(traffic)
    avg_pollution = sum(pollution) // len(pollution)

    make_card(stats, "Average Traffic", str(avg_traffic) + "%", BLUE)
    make_card(stats, "Average AQI", str(avg_pollution), ORANGE)
    make_card(stats, "Total Vehicles", str(sum(vehicles)), CYAN)
    make_card(stats, "Incidents", str(len(incidents)), RED)

    charts = tk.Frame(content, bg=BG)
    charts.pack(fill="both", expand=True, pady=20)

    left = tk.Frame(charts, bg=CARD, padx=10, pady=10)
    left.pack(side="left", fill="both", expand=True, padx=5)

    right = tk.Frame(charts, bg=CARD, padx=10, pady=10)
    right.pack(side="left", fill="both", expand=True, padx=5)

    create_chart(
        left,
        "Traffic Density by Zone",
        traffic,
        "#3285F5",
        "Traffic %"
    )

    create_chart(
        right,
        "Pollution Levels by Zone",
        pollution,
        "#F59E0B",
        "AQI"
    )


# TRAFFIC ANALYTICS

def show_traffic():
    clear_content()

    heading(
        "Traffic Intelligence",
        "Zone-wise traffic density and risk classification"
    )

    table = ttk.Treeview(
        content,
        columns=("zone", "vehicles", "density", "risk"),
        show="headings",
        height=7
    )

    for col, title in [
        ("zone", "City Zone"),
        ("vehicles", "Vehicles"),
        ("density", "Density"),
        ("risk", "Risk Level")
    ]:
        table.heading(col, text=title)
        table.column(col, anchor="center", width=160)

    for i, zone in enumerate(zones):
        if traffic[i] >= 75:
            risk = "HIGH"
        elif traffic[i] >= 45:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        table.insert(
            "",
            "end",
            values=(
                zone,
                vehicles[i],
                str(traffic[i]) + "%",
                risk
            )
        )

    table.pack(fill="x", pady=10)

    chart_frame = tk.Frame(content, bg=CARD, padx=10, pady=10)
    chart_frame.pack(fill="both", expand=True, pady=10)

    create_chart(
        chart_frame,
        "Traffic Density Analysis",
        traffic,
        "#3285F5",
        "Density %"
    )

    def refresh():
        for i in range(len(zones)):
            traffic[i] = random.randint(20, 95)
            vehicles[i] = random.randint(100, 900)
        show_traffic()

    tk.Button(
        content,
        text="REFRESH TRAFFIC DATA",
        command=refresh,
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        padx=18,
        pady=10
    ).pack(anchor="w", pady=5)


# POLLUTION ANALYTICS

def show_pollution():
    clear_content()

    heading(
        "Pollution Intelligence",
        "Air quality analysis and zone comparison"
    )

    avg = sum(pollution) // len(pollution)

    stats = tk.Frame(content, bg=BG)
    stats.pack(fill="x")

    if avg <= 50:
        category = "Good"
        color = GREEN
    elif avg <= 100:
        category = "Satisfactory"
        color = GREEN
    elif avg <= 200:
        category = "Moderate"
        color = ORANGE
    else:
        category = "Poor"
        color = RED

    make_card(stats, "Average AQI", str(avg), color)
    make_card(stats, "Zones Monitored", str(len(zones)), CYAN)
    make_card(stats, "Highest AQI", str(max(pollution)), RED)

    chart = tk.Frame(content, bg=CARD, padx=15, pady=15)
    chart.pack(fill="both", expand=True, pady=20)

    create_chart(
        chart,
        "Air Quality Comparison",
        pollution,
        "#F59E0B",
        "AQI"
    )

    tk.Label(
        content,
        text="Overall Demo Category: " + category,
        bg=BG,
        fg=color,
        font=("Arial", 14, "bold")
    ).pack(anchor="w")


# AI RECOMMENDATIONS

def show_ai():
    clear_content()

    heading(
        "AI Recommendation Engine",
        "Rule-based analysis of simulated city data"
    )

    result = tk.Frame(content, bg=CARD, padx=20, pady=20)
    result.pack(fill="both", expand=True)

    recommendations = []

    for i, zone in enumerate(zones):

        if traffic[i] >= 75:
            recommendations.append(
                zone + ": High traffic detected. "
                "Review traffic signal timing and congestion management."
            )

        if pollution[i] > 150:
            recommendations.append(
                zone + ": Elevated demo AQI. "
                "Review air-quality monitoring and local pollution sources."
            )

    if not recommendations:
        recommendations.append(
            "No high-risk conditions detected in the current demo dataset."
        )

    for number, item in enumerate(recommendations, 1):
        tk.Label(
            result,
            text=str(number) + ". " + item,
            bg=CARD,
            fg=CYAN,
            font=("Arial", 11),
            wraplength=850,
            justify="left"
        ).pack(anchor="w", pady=12)

    tk.Label(
        content,
        text="Recommendations use predefined rules, not a trained ML model.",
        bg=BG,
        fg=MUTED
    ).pack(anchor="w", pady=10)


# EMERGENCY CENTER

def show_emergency():
    clear_content()

    heading(
        "Emergency Management",
        "Register and review simulated city incidents"
    )

    tk.Label(
        content,
        text="Incident Location",
        bg=BG,
        fg=WHITE
    ).pack(anchor="w")

    location = tk.Entry(
        content,
        bg=CARD,
        fg=WHITE,
        insertbackground=WHITE,
        font=("Arial", 12)
    )
    location.pack(fill="x", pady=8)

    tk.Label(
        content,
        text="Incident Type",
        bg=BG,
        fg=WHITE
    ).pack(anchor="w")

    kind = ttk.Combobox(
        content,
        values=["Fire", "Medical", "Road Accident", "Other"],
        state="readonly"
    )
    kind.set("Fire")
    kind.pack(fill="x", pady=8)

    def register():
        place = location.get().strip()

        if not place:
            messagebox.showwarning(
                "Required",
                "Enter an incident location."
            )
            return

        incidents.append({
            "location": place,
            "type": kind.get(),
            "time": datetime.now().strftime("%d-%m-%Y %H:%M")
        })

        messagebox.showinfo(
            "Registered",
            "Demo incident registered successfully."
        )

        location.delete(0, tk.END)

    tk.Button(
        content,
        text="REGISTER INCIDENT",
        bg=RED,
        fg=WHITE,
        relief="flat",
        padx=20,
        pady=12,
        command=register
    ).pack(anchor="w", pady=12)

    table = ttk.Treeview(
        content,
        columns=("location", "type", "time"),
        show="headings"
    )

    for col, title in [
        ("location", "Location"),
        ("type", "Incident"),
        ("time", "Registration Time")
    ]:
        table.heading(col, text=title)
        table.column(col, anchor="center", width=200)

    for item in incidents:
        table.insert(
            "",
            "end",
            values=(
                item["location"],
                item["type"],
                item["time"]
            )
        )

    table.pack(fill="both", expand=True, pady=15)


# CITY ZONE ANALYSIS

def show_zones():
    clear_content()

    heading(
        "City Zone Analysis",
        "Comparative performance of monitored city zones"
    )

    for i, zone in enumerate(zones):
        frame = tk.Frame(content, bg=CARD, padx=15, pady=12)
        frame.pack(fill="x", pady=5)

        tk.Label(
            frame,
            text=zone,
            bg=CARD,
            fg=WHITE,
            font=("Arial", 11, "bold")
        ).pack(side="left")

        tk.Label(
            frame,
            text=f"Traffic: {traffic[i]}%   |   AQI: {pollution[i]}",
            bg=CARD,
            fg=CYAN,
            font=("Arial", 10)
        ).pack(side="right")


# CSV REPORT

def export_report():
    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="smart_city_report.csv"
    )

    if not path:
        return

    try:
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Zone",
                "Traffic Density",
                "Vehicles",
                "AQI"
            ])

            for i, zone in enumerate(zones):
                writer.writerow([
                    zone,
                    traffic[i],
                    vehicles[i],
                    pollution[i]
                ])

            writer.writerow([])
            writer.writerow(["Registered Incidents"])

            writer.writerow(["Location", "Type", "Time"])

            for item in incidents:
                writer.writerow([
                    item["location"],
                    item["type"],
                    item["time"]
                ])

        messagebox.showinfo(
            "Success",
            "City report exported successfully!"
        )

    except Exception as error:
        messagebox.showerror("Export Error", str(error))


# NAVIGATION

tk.Label(
    sidebar,
    text="CONTROL CENTER",
    bg=PANEL,
    fg=MUTED,
    font=("Arial", 10, "bold")
).pack(pady=25)

menu = [
    ("Dashboard", show_dashboard),
    ("Traffic Analytics", show_traffic),
    ("Pollution Monitor", show_pollution),
    ("AI Recommendations", show_ai),
    ("Emergency Center", show_emergency),
    ("City Zone Analysis", show_zones),
    ("Export CSV Report", export_report)
]

for name, function in menu:
    tk.Button(
        sidebar,
        text="  " + name,
        command=function,
        bg=PANEL,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        relief="flat",
        anchor="w",
        font=("Arial", 10),
        padx=15,
        pady=15,
        cursor="hand2"
    ).pack(fill="x", padx=8, pady=3)

tk.Label(
    sidebar,
    text="SMART CITY AI\nADVANCED VERSION 2.0",
    bg=PANEL,
    fg=CYAN,
    font=("Arial", 9, "bold"),
    justify="center"
).pack(side="bottom", pady=25)

update_clock()
show_dashboard()

root.mainloop()

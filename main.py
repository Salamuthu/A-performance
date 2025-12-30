from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Scale, Radiobutton, StringVar, Label
from tkinter.ttk import Combobox
import pandas as pd
import ml
import ai_coach
import threading
from tkinter import scrolledtext

# ---------------- PATHS ----------------
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# ---------------- INITIALIZE MODELS ----------------
injury_model, perf_model = ml.train_models()


# ---------------- UI HELPERS ----------------
def draw_rounded_rect(canvas, x, y, w, h, radius, color):
    """Draws a rounded rectangle on the canvas for entry backgrounds."""
    canvas.create_oval(x, y, x + radius * 2, y + radius * 2, fill=color, outline=color)
    canvas.create_oval(x + w - radius * 2, y, x + w, y + radius * 2, fill=color, outline=color)
    canvas.create_oval(x, y + h - radius * 2, x + radius * 2, y + h, fill=color, outline=color)
    canvas.create_oval(x + w - radius * 2, y + h - radius * 2, x + w, y + h, fill=color, outline=color)
    canvas.create_rectangle(x + radius, y, x + w - radius, y + h, fill=color, outline=color)
    canvas.create_rectangle(x, y + radius, x + w, y + h - radius, fill=color, outline=color)


def handle_predict():
    try:
        level_str = athlete_dropdown.get()
        if not level_str:
            feedback_text.config(text="Status: Please select athlete level!", fg="red")
            return

        data = {
            "age": int(entry_2.get()),
            "training_hours_per_day": training_hrs.get(),
            "training_days_per_week": training_days.get(),
            "sleep_hours": sleep_hrs.get(),
            "rest_days_per_week": rest_days.get(),
            "previous_injury": 1 if injury_var.get() == "Yes" else 0,
            "athlete_level": level_map[level_str]
        }

        input_df = pd.DataFrame([data])
        res_injury = injury_model.predict(input_df)[0]
        res_perf = perf_model.predict(input_df)[0]

        risk_label.config(text=f"Injury Risk: {res_injury}")
        perf_label.config(text=f"Performance: {res_perf}")

        feedback_text.config(text="AI Coach is generating advice...", fg="black")

        def run_ai():
            advice = ai_coach.get_ai_advice(data, res_injury, res_perf)
            ai_display.configure(state='normal')
            ai_display.delete('1.0', 'end')
            ai_display.insert('1.0', advice)
            ai_display.configure(state='disabled')
            feedback_text.config(text="Status: Complete", fg="green")

        threading.Thread(target=run_ai).start()

    except ValueError:
        feedback_text.config(text="Status: Please enter a valid Age!", fg="red")


# ---------------- WINDOW SETUP ----------------
window = Tk()
window.title("AI Athlete Coach")
window.geometry("1200x750")
window.resizable(False, False)

canvas = Canvas(window, width=1200, height=750, highlightthickness=0)
canvas.pack(fill="both", expand=True)


# ---------------- GRADIENT ----------------
def draw_custom_gradient(canvas, width, height):
    stop_y = int(height * 0.35)
    r1, g1, b1 = canvas.winfo_rgb("#FFFFFF")
    r2, g2, b2 = canvas.winfo_rgb("#ADD914")
    for y in range(stop_y):
        canvas.create_line(0, y, width, y, fill="#FFFFFF")
    gradient_height = height - stop_y
    for i in range(gradient_height):
        nr = int(r1 + (r2 - r1) * i / gradient_height)
        ng = int(g1 + (g2 - g1) * i / gradient_height)
        nb = int(b1 + (b2 - b1) * i / gradient_height)
        color = f"#{nr // 256:02x}{ng // 256:02x}{nb // 256:02x}"
        canvas.create_line(0, stop_y + i, width, stop_y + i, fill=color)


draw_custom_gradient(canvas, 1200, 750)

# ---------------- UI ELEMENTS ----------------
image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(600, 90, image=image_1)


# Labels
def create_text(x, y, txt, font=("Inter Bold", 16)):
    canvas.create_text(x, y, anchor="nw", text=txt, fill="#000000", font=font)


create_text(75, 171, "Name:")
create_text(75, 249, "Age:")
create_text(76, 330, "Training hrs/day:")
create_text(76, 400, "Training days/week:")
create_text(75, 470, "Sleep hours:")
create_text(75, 540, "Rest Days:")
create_text(76, 610, "Previous injury:")
create_text(75, 680, "Athlete level:")

# --- Rounded Backgrounds for Entries ---
draw_rounded_rect(canvas, 80, 201, 366, 46, 10, "#D9EFA3")  # Name Entry
draw_rounded_rect(canvas, 80, 278, 145, 46, 10, "#D9EFA3")  # Age Entry

entry_1 = Entry(window, bd=0, font=("Inter", 14), bg="white", highlightthickness=0)
entry_1.place(x=90, y=206, width=346, height=36)

entry_2 = Entry(window, bd=0, font=("Inter", 14), bg="white", highlightthickness=0)
entry_2.place(x=90, y=283, width=125, height=36)

# --- Themed Sliders ---
slider_style = {"bg": "white", "troughcolor": "#D9EFA3", "activebackground": "#ADD914",
                "highlightthickness": 0, "orient": "horizontal", "length": 250}

training_hrs = Scale(window, from_=1, to=12, **slider_style)
training_hrs.place(x=80, y=360)

training_days = Scale(window, from_=1, to=7, **slider_style)
training_days.place(x=80, y=430)

sleep_hrs = Scale(window, from_=1, to=12, **slider_style)
sleep_hrs.place(x=80, y=500)

rest_days = Scale(window, from_=1, to=7, **slider_style)
rest_days.place(x=80, y=570)

# --- Injury Radio ---
injury_var = StringVar(value="No")
Radiobutton(window, text="Yes", variable=injury_var, value="Yes", bg="#ADD914", activebackground="#ADD914",
            font=("Inter", 12)).place(x=80, y=640)
Radiobutton(window, text="No", variable=injury_var, value="No", bg="#ADD914", activebackground="#ADD914",
            font=("Inter", 12)).place(x=150, y=640)

# --- Dropdown ---
level_map = {"Beginner": 0, "Intermediate": 1, "Professional": 2}
athlete_dropdown = Combobox(window, values=list(level_map.keys()), state="readonly", font=("Inter", 12))
athlete_dropdown.place(x=86, y=705, width=217, height=41)

# --- AI Feedback Appearance ---
# We use a color that matches the bottom of your gradient (#ADD914) to make it "blend in"
ai_display = scrolledtext.ScrolledText(
    window,
    font=("Inter", 11),
    wrap='word',
    bg="#D9EFA3",  # Matches the mid-gradient color
    fg="#000000",
    bd=0,  # No border
    padx=10, pady=10,
    highlightthickness=1,
    highlightbackground="#FFFFFF"  # Subtle white edge
)
ai_display.place(x=745, y=410, width=400, height=280)
ai_display.insert('1.0', "AI Coach feedback will appear here...")
ai_display.configure(state='disabled')

# Result Displays
canvas.create_text(744, 350, anchor="nw", text="AI COACH FEEDBACK", fill="#000000", font=("Impact", 26))

risk_label = Label(window, text="Injury Risk: --", font=("Inter Bold", 18), bg="white", fg="#D9534F")
risk_label.place(x=745, y=205)

perf_label = Label(window, text="Performance: --", font=("Inter Bold", 18), bg="white", fg="#5CB85C")
perf_label.place(x=745, y=266)

feedback_text = Label(window, text="", font=("Inter", 10), bg="#ADD914")  # Blends with bottom
feedback_text.place(x=745, y=700)

# Predict Button
button_img = PhotoImage(file=relative_to_assets("button_1.png"))
Button(window, image=button_img, borderwidth=0, command=handle_predict, bg="#ADD914", activebackground="#ADD914",
       cursor="hand2").place(x=379, y=680)

window.mainloop()
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Scale, Radiobutton, StringVar, Label
from tkinter.ttk import Combobox
import pandas as pd
import ml  # Import our training script

# ---------------- PATHS ----------------
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\lap.lk\Desktop\Aperformance\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# ---------------- INITIALIZE MODELS ----------------
# Train models once when the script starts
injury_model, perf_model = ml.train_models()

# ---------------- FUNCTIONS ----------------
def handle_predict():
    try:
        # Validate selection
        level_str = athlete_dropdown.get()
        if not level_str:
            feedback_text.config(text="Status: Please select athlete level!")
            return

        # 1. Collect and Format Data (Keys must match ml.py features)
        data = {
            "age": int(entry_2.get()),
            "training_hours_per_day": training_hrs.get(),
            "training_days_per_week": training_days.get(),
            "sleep_hours": sleep_hrs.get(),
            "rest_days_per_week": rest_days.get(),
            "previous_injury": 1 if injury_var.get() == "Yes" else 0,
            "athlete_level": level_map[level_str]
        }

        # 2. Convert to DataFrame for Prediction
        input_df = pd.DataFrame([data])

        # 3. Perform Prediction
        res_injury = injury_model.predict(input_df)[0]
        res_perf = perf_model.predict(input_df)[0]

        # 4. Update UI
        risk_label.config(text=f"Injury Risk: {res_injury}")
        perf_label.config(text=f"Performance: {res_perf}")
        feedback_text.config(text="AI COACH: Analysis Complete.")

    except ValueError:
        feedback_text.config(text="Status: Please enter a valid Age!")
    except Exception as e:
        feedback_text.config(text=f"Error: {str(e)}")

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
        color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
        canvas.create_line(0, stop_y + i, width, stop_y + i, fill=color)

# ---------------- WINDOW SETUP ----------------
window = Tk()
window.title("AI Athlete Coach")
window.geometry("1200x750")
window.resizable(False, False)

canvas = Canvas(window, width=1200, height=750, highlightthickness=0)
canvas.pack(fill="both", expand=True)
draw_custom_gradient(canvas, 1200, 750)

# ---------------- UI ELEMENTS ----------------
image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(600, 90, image=image_1)

# Labels
def create_text(x, y, txt):
    canvas.create_text(x, y, anchor="nw", text=txt, fill="#000000", font=("Inter Bold", 18))

create_text(75, 171, "Name:")
create_text(75, 249, "Age:")
create_text(76, 330, "Training hrs/day:")
create_text(76, 400, "Training days/week:")
create_text(75, 470, "Sleep hours:")
create_text(75, 540, "Rest Days:")
create_text(76, 610, "Previous injury:")
create_text(75, 680, "Athlete level:")

# Entry/Inputs
entry_1 = Entry(window, bd=0, font=("Inter", 14))
entry_1.place(x=85, y=206, width=356, height=41)

entry_2 = Entry(window, bd=0, font=("Inter", 14))
entry_2.place(x=86, y=283, width=135, height=41)

# Sliders
training_hrs = Scale(window, from_=1, to=12, orient="horizontal", length=200, bg="#FFFFFF")
training_hrs.place(x=80, y=360)

training_days = Scale(window, from_=1, to=7, orient="horizontal", length=200, bg="#FFFFFF")
training_days.place(x=80, y=430)

sleep_hrs = Scale(window, from_=1, to=12, orient="horizontal", length=200, bg="#FFFFFF")
sleep_hrs.place(x=80, y=500)

rest_days = Scale(window, from_=1, to=7, orient="horizontal", length=200, bg="#FFFFFF")
rest_days.place(x=80, y=570)

# Injury Radio
injury_var = StringVar(value="No")
Radiobutton(window, text="Yes", variable=injury_var, value="Yes", bg="#ADD914").place(x=80, y=640)
Radiobutton(window, text="No", variable=injury_var, value="No", bg="#ADD914").place(x=150, y=640)

# Dropdown
level_map = {"Beginner": 0, "Intermediate": 1, "Professional": 2}
athlete_dropdown = Combobox(window, values=list(level_map.keys()), state="readonly", font=("Inter", 12))
athlete_dropdown.place(x=86, y=705, width=217, height=41)

# Result Displays
canvas.create_text(744, 350, anchor="nw", text="AI COACH FEEDBACK", fill="#000000", font=("Impact", 26))

risk_label = Label(window, text="Injury Risk: --", font=("Inter Bold", 18), bg="#FFFFFF", fg="red")
risk_label.place(x=745, y=205)

perf_label = Label(window, text="Performance: --", font=("Inter Bold", 18), bg="#FFFFFF", fg="green")
perf_label.place(x=745, y=266)

feedback_text = Label(window, text="Status: Ready", font=("Inter", 12), bg="#FFFFFF")
feedback_text.place(x=745, y=410)

# Predict Button
button_img = PhotoImage(file=relative_to_assets("button_1.png"))
Button(window, image=button_img, borderwidth=0, command=handle_predict, bg="#ADD914").place(x=379, y=680)

window.mainloop()
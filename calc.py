#############################################
# Simple Macro Calculator by William Tucker #
#############################################

import tkinter as tk
from tkinter import messagebox


def calculate_macros():
    try:
        # Mode selection
        if mode.get() == 'manual':
            bmr = float(bmr_entry.get())
        else:
            weight_kg = float(weight_entry.get()) * 0.453592
            height_cm = float(feet_entry.get()) * 30.48 + \
                float(inches_entry.get()) * 2.54
            if gender_entry.get().lower() == 'm':
                bmr = 88.362 + (13.397 * weight_kg) + (4.799 *
                                                       height_cm) - (5.677 * int(age_entry.get()))
            else:
                bmr = 447.593 + (9.247 * weight_kg) + (3.098 *
                                                       height_cm) - (4.330 * int(age_entry.get()))

        # Exercise calories
        exercise_calories = float(exercise_calories_entry.get())

        # Adjust total calories based on the goal
        if goal.get() == 'fat_loss':
            total_calories = bmr * 0.8  # 20% deficit for example
        elif goal.get() == 'muscle_gain':
            total_calories = bmr * 1.2  # 20% surplus for example
        else:
            total_calories = bmr  # Maintenance

        # Macro calculations (example percentages)
        protein = total_calories * 0.15 / 4
        carbs = total_calories * 0.55 / 4
        fats = total_calories * 0.30 / 9

        # Update table with results
        results['total_calories'].config(text=f"{total_calories:.2f}")
        results['protein'].config(text=f"{protein:.2f}")
        results['carbs'].config(text=f"{carbs:.2f}")
        results['fats'].config(text=f"{fats:.2f}")
    except ValueError:
        messagebox.showerror(
            "Input Error", "Please ensure all fields are filled with valid numbers.")


def clear_form():
    for entry in [age_entry, weight_entry, feet_entry, inches_entry, gender_entry, bmr_entry, exercise_calories_entry]:
        entry.delete(0, tk.END)


def update_mode():
    if mode.get() == 'manual':
        for widget in auto_widgets:
            widget.grid_remove()
        bmr_entry.grid()
    else:
        for widget in auto_widgets:
            widget.grid()
        bmr_entry.grid_remove()


# Create the main window
root = tk.Tk()
root.title("Macro Intake Calculator by billski")

# Variable to store the mode (auto or manual BMR calculation)
mode = tk.StringVar(value='auto')

# Radio buttons to choose mode
auto_mode_rb = tk.Radiobutton(
    root, text="Auto Calculate BMR", variable=mode, value='auto', command=update_mode)
auto_mode_rb.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

manual_mode_rb = tk.Radiobutton(
    root, text="Manual BMR Entry", variable=mode, value='manual', command=update_mode)
manual_mode_rb.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Auto BMR Calculation Widgets
auto_widgets = []
labels = ["Age", "Weight (lbs)", "Height (feet)",
          "Height (inches)", "Gender (M/F)"]
entries = []

for i, label in enumerate(labels):
    lbl = tk.Label(root, text=label)
    lbl.grid(row=i+2, column=0, padx=10, pady=10, sticky="e")
    entry = tk.Entry(root)
    entry.grid(row=i+2, column=1, padx=10, pady=10, sticky="w")
    auto_widgets.extend([lbl, entry])
    entries.append(entry)

age_entry, weight_entry, feet_entry, inches_entry, gender_entry = entries

# Manual BMR Entry Widget
bmr_entry = tk.Entry(root)
bmr_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")
tk.Label(root, text="BMR").grid(row=7, column=0, padx=10, pady=10, sticky="e")

# Exercise Calories Burned Entry
exercise_calories_entry = tk.Entry(root)
exercise_calories_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")
tk.Label(root, text="Exercise Calories Burned").grid(
    row=8, column=0, padx=10, pady=10, sticky="e")

# Goal selection using radio buttons
goal = tk.StringVar(value='maintenance')
goals_frame = tk.LabelFrame(root, text="Goal")
goals_frame.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

tk.Radiobutton(goals_frame, text="Fat Loss", variable=goal,
               value='fat_loss').pack(side=tk.LEFT)
tk.Radiobutton(goals_frame, text="Maintenance", variable=goal,
               value='maintenance').pack(side=tk.LEFT)
tk.Radiobutton(goals_frame, text="Muscle Gain", variable=goal,
               value='muscle_gain').pack(side=tk.LEFT)

# Table for results
results_frame = tk.LabelFrame(root, text="Results")
results_frame.grid(row=10, column=0, columnspan=2,
                   padx=10, pady=10, sticky="ew")

# Labels for table headers
headers = ["Total Calories", "Protein (g)", "Carbs (g)", "Fats (g)"]
for i, header in enumerate(headers):
    tk.Label(results_frame, text=header).grid(row=0, column=i, padx=10, pady=5)

# Dictionary to hold result labels
results = {}

# Labels for table data
for i, header in enumerate(headers):
    key = header.lower().replace(' (g)', '').replace(' ', '_')
    result_label = tk.Label(results_frame, text="")
    result_label.grid(row=1, column=i, padx=10, pady=5)
    results[key] = result_label

# Buttons
calculate_button = tk.Button(
    root, text="Calculate Macros", command=calculate_macros)
calculate_button.grid(row=11, column=0, padx=10, pady=10, sticky="e")

clear_button = tk.Button(root, text="Clear Form", command=clear_form)
clear_button.grid(row=11, column=1, padx=10, pady=10, sticky="w")

# Initialize the form based on the default mode
update_mode()

# Start the GUI event loop
root.mainloop()

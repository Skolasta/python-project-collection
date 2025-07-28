import tkinter as tk
from tkinter import messagebox

# --- FUNCTIONS ---
def calculate_bmi():
    """
    Gets weight and height from entry fields, calculates the BMI,
    and updates the result label. Includes error handling for invalid input.
    """
    try:
        # Get values from the entry widgets
        weight_str = weight_entry.get()
        height_str = height_entry.get()

        # Check if the fields are empty
        if not weight_str or not height_str:
            result_label.config(text="Please enter both weight and height.")
            return

        # Convert strings to numbers
        weight_in_kg = float(weight_str)
        height_in_cm = float(height_str)
        
        # Ensure height is a positive number to avoid division by zero
        if height_in_cm <= 0:
            result_label.config(text="Height must be a positive number.")
            return

        # Convert height from cm to meters for the formula
        height_in_m = height_in_cm / 100
        
        # Calculate BMI: BMI = weight (kg) / [height (m)]^2
        bmi_value = weight_in_kg / (height_in_m ** 2)

        # Determine the BMI category
        if bmi_value < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi_value < 25:
            category = "Normal weight"
        elif 25 <= bmi_value < 30:
            category = "Overweight"
        elif 30 <= bmi_value < 35:
            category = "Obesity (Class I)"
        elif 35 <= bmi_value < 40:
            category = "Obesity (Class II)"
        else:
            category = "Obesity (Class III)"
        
        # Update the result label with the calculated BMI and category
        result_label.config(text=f"Your BMI is: {bmi_value:.2f}\n({category})")

    except ValueError:
        # Handle cases where the input is not a valid number
        result_label.config(text="Invalid input. Please enter numbers only.")
    except Exception as e:
        # Handle any other unexpected errors
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        result_label.config(text="An error occurred.")


# --- UI SETUP ---
# Create the main window
window = tk.Tk()
window.title("BMI Calculator")
window.config(padx=20, pady=20) # Add padding around the whole window
window.minsize(width=300, height=250)

# Weight Label and Entry
weight_label = tk.Label(text="Enter your weight (kg)", font=("Arial", 12))
weight_label.pack(pady=(0, 5)) # Add padding below

weight_entry = tk.Entry(width=25)
weight_entry.pack(pady=(0, 15)) # Add padding below

# Height Label and Entry
height_label = tk.Label(text="Enter your height (cm)", font=("Arial", 12))
height_label.pack(pady=(0, 5)) # Add padding below

height_entry = tk.Entry(width=25)
height_entry.pack(pady=(0, 20)) # Add padding below

# Calculate Button
calculate_button = tk.Button(text="Calculate BMI", command=calculate_bmi, font=("Arial", 12, "bold"))
calculate_button.pack()

# Result Label
result_label = tk.Label(text="", font=("Arial", 14), justify="center")
result_label.pack(pady=20)

# Start the main event loop
window.mainloop()

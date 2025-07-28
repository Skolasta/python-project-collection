import requests
import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.title("Weather App") # Create the main window
root.geometry("150x150") # Set the size of the window

city_label = tk.Label(root, text="City:") # Create a label for the city entry
city_label.pack()

city_entry = tk.Entry(root) # Create an entry widget for the city input
city_entry.pack()

fetch_button = tk.Button(root, text="Fetch Weather",width=13) # Create a button to fetch the weather
# The button will call the fetch_weather function when clicked
fetch_button.pack()

clear_button = tk.Button(root, text="Clear", command=lambda: (weather_label.config(text=""), city_entry.delete(0, tk.END)),width=13)  # Create a button to clear the weather label and city entry
clear_button.pack()

weather_label = tk.Label(root, text="") # Create a label to display the weather information
weather_label.pack()

def fetch_weather():
    city = city_entry.get() # Get the city name from the entry widget
    # Add your API key here
    api_key = ""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric" # Construct the API URL with the city name and API key
    
    try:
        response = requests.get(url) # Make a GET request to the OpenWeather API
        data = response.json() # Parse the JSON response
        temperature = data["main"]["temp"] # Extract the temperature from the response
        weather = data["weather"][0]["description"] # Extract the weather description from the response
        weather_label.config(text=f"Temperature: {temperature}°C\nWeather: {weather}") # Update the weather label with the temperature and weather description
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data") # Show an error message if there is an issue with the API request

fetch_button.config(command=fetch_weather) # Set the command for the fetch button to call the fetch_weather function

# Start the GUI main loop
root.mainloop()
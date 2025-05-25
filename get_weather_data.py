import tkinter as tk
from tkinter import ttk, messagebox
import requests
from io import BytesIO
from PIL import Image, ImageTk
import platform
import sys

# Replace with your own OpenWeatherMap API key
API_KEY = "e897b6c5abdfa238bccea4476a17552d"

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # DPI awareness for better scaling (Windows)
        if sys.platform == "win32":
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass

        self.title("Weather App")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = min(int(screen_width * 0.9), 500)
        window_height = min(int(screen_height * 0.85), 800)
        self.geometry(f"{window_width}x{window_height}")
        self.configure(bg='#1e1e3c')

        try:
            bg_image_path = "background.jpg"
            self.bg_image = Image.open(bg_image_path)
            self.bg_image = self.bg_image.resize((window_width, window_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Warning: Background image load failed: {e}")

        # Fonts
        if platform.system() == "Darwin":
            base_font = ("Helvetica Neue", 16)
            title_font = ("Helvetica Neue", 28, "bold")
            large_font = ("Helvetica Neue", 26, "bold")
            medium_font = ("Helvetica Neue", 20, "italic")
            small_font = ("Helvetica Neue", 14, "bold")
        elif platform.system() == "Windows":
            base_font = ("Segoe UI", 12)
            title_font = ("Segoe UI", 24, "bold")
            large_font = ("Segoe UI", 32, "bold")
            medium_font = ("Segoe UI", 18, "italic")
            small_font = ("Segoe UI", 12, "bold")
        else:
            base_font = ("Ubuntu", 12)
            title_font = ("Ubuntu", 24, "bold")
            large_font = ("Ubuntu", 32, "bold")
            medium_font = ("Ubuntu", 18, "italic")
            small_font = ("Ubuntu", 12, "bold")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton',
                        background='#8a2be2', foreground='white',
                        font=base_font,
                        padding=10)
        style.map('TButton',
                  background=[('active', '#6f21cc')])

        heading = tk.Label(self, text="Weather App", font=title_font,
                           fg="#c8a2ff", bg='#1e1e3c', anchor="center")
        heading.grid(row=0, column=0, columnspan=2, pady=(30, 20), sticky="ew")

        self.city_var = tk.StringVar()
        self.last_city = ""
        self.refresh_interval = 600_000  # 10 minutes

        city_entry = tk.Entry(self, textvariable=self.city_var, font=base_font,
                              justify='center', bd=4, relief='ridge')
        city_entry.grid(row=1, column=0, columnspan=2, pady=10, padx=30, sticky="ew")
        city_entry.focus()

        get_weather_btn = ttk.Button(self, text="Get Weather", command=self.get_weather)
        get_weather_btn.grid(row=2, column=0, columnspan=2, pady=15, padx=80, sticky="ew")

        self.info_frame = tk.Frame(self, bg='#1e1e3c')
        self.info_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew", padx=20)

        self.icon_label = tk.Label(self.info_frame, bg='#1e1e3c')
        self.icon_label.pack(pady=10)

        self.temp_label = tk.Label(self.info_frame, bg='#1e1e3c', fg='#b09aff',
                                   font=large_font)
        self.temp_label.pack()

        self.desc_label = tk.Label(self.info_frame, bg='#1e1e3c', fg='#d3bcff',
                                   font=medium_font)
        self.desc_label.pack()

        self.location_label = tk.Label(self.info_frame, bg='#1e1e3c', fg='#c2a6ff',
                                       font=small_font)
        self.location_label.pack(pady=(10, 0))

        self.status_label = tk.Label(self, bg='#1e1e3c', fg='#f06a6a', font=small_font)
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.after(self.refresh_interval, self.auto_refresh)

    def get_weather(self, auto=False):
        city = self.city_var.get().strip() or self.last_city
        if not city:
            if not auto:
                messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        self.last_city = city
        if not auto:
            self.status_label.config(text="Loading weather...")
            self.clear_weather()

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.display_weather(data, show_popup=not auto)
            self.status_label.config(text="")
        except requests.exceptions.HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else None
            if status_code == 404:
                self.status_label.config(text="City not found. Please check spelling.")
            else:
                self.status_label.config(text=f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException:
            self.status_label.config(text="Failed to retrieve data. Check your connection.")
        except Exception:
            self.status_label.config(text="An unexpected error occurred.")

    def display_weather(self, data, show_popup=True):
        temp = round(data["main"]["temp"])
        description = data["weather"][0]["description"].capitalize()
        location = f"{data['name']}, {data['sys']['country']}"
        icon_code = data["weather"][0]["icon"]

        self.temp_label.config(text=f"{temp}°C")
        self.desc_label.config(text=description)
        self.location_label.config(text=location)

        # Load icon
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"
        try:
            img_data = requests.get(icon_url, timeout=5).content
            img = Image.open(BytesIO(img_data))
            img = img.resize((150, 150), Image.LANCZOS)
            self.weather_icon = ImageTk.PhotoImage(img)
            self.icon_label.config(image=self.weather_icon)
        except:
            self.icon_label.config(image=None)
            self.weather_icon = None

        if show_popup:
            emoji = self.weather_emoji(description)
            self.show_weather_popup(temp, description, location, emoji)

    def show_weather_popup(self, temp, description, location, emoji):
        popup = tk.Toplevel(self)
        popup.title("Current Weather")
        popup.configure(bg='#29294d')
        popup.geometry("300x200")
        popup.resizable(False, False)

        label1 = tk.Label(popup, text=f"{emoji} {temp}°C", font=("Helvetica", 24, "bold"), fg="white", bg='#29294d')
        label1.pack(pady=10)

        label2 = tk.Label(popup, text=description, font=("Helvetica", 16), fg="#b6b6ff", bg='#29294d')
        label2.pack()

        label3 = tk.Label(popup, text=location, font=("Helvetica", 14), fg="#d6d6ff", bg='#29294d')
        label3.pack(pady=10)

        ok_btn = ttk.Button(popup, text="OK", command=popup.destroy)
        ok_btn.pack(pady=10)

    def weather_emoji(self, description):
        d = description.lower()
        if "cloud" in d:
            return "☁️"
        elif "rain" in d:
            return "🌧️"
        elif "sun" in d or "clear" in d:
            return "☀️"
        elif "snow" in d:
            return "❄️"
        elif "storm" in d:
            return "🌩️"
        elif "fog" in d or "mist" in d:
            return "🌫️"
        else:
            return "🌈"

    def clear_weather(self):
        self.temp_label.config(text='')
        self.desc_label.config(text='')
        self.location_label.config(text='')
        self.icon_label.config(image=None)
        self.weather_icon = None

    def auto_refresh(self):
        self.get_weather(auto=True)
        self.after(self.refresh_interval, self.auto_refresh)


if __name__ == "__main__":
   
    app = WeatherApp()
    app.mainloop()

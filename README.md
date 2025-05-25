# A-Basic-Weather-App-with-GUI-in-Python

🔧 Libraries Used
tkinter: For GUI
ttk: Styled widgets
messagebox: Alert dialogs
requests: HTTP API calls
PIL.Image: Handle images (e.g., icons and background)
platform/sys: Platform-specific adjustments (like fonts or DPI)

🚀 Class: WeatherApp
__init__ (Constructor)
This method initializes the GUI and sets up the layout.
1. DPI Awareness for Windows: Improves visual scaling on high-DPI screens (Windows only).
2. Window Setup: Sets title, size (max 500x800), and background color.
3. Background Image: Loads and resizes a background image to fill the app window.
4. Fonts Based on OS: Different fonts are applied based on the operating system (macOS, Windows, Linux).
5. Styling Buttons: Customizes button colors, font, and hover effect.
6. Widgets:
•Title Label
•City input box
•“Get Weather” button
•Weather info frame (icon, temperature, description, location)
•Status label (for errors or loading)
7. Auto-refresh Timer: Refreshes weather data every 10 minutes (600,000 ms) using after().

🧠 get_weather(auto=False)
Called when:
•User clicks the "Get Weather" button
•Timer triggers auto_refresh

What it does:
•Gets the city name from input.
•Builds API URL and makes request.
•If successful → shows weather.
•On failure → shows error message.
•Saves last city for auto-refresh.

🌦️ display_weather(data, show_popup=True)
Parses the weather JSON data:
•Extracts temperature, condition, city, country, and icon.
•Displays in main frame.
•Optionally shows popup window if show_popup=True.

📦 show_weather_popup(...)
Creates a separate Toplevel popup window showing:
•Emoji + Temperature
•Description
•Location

😄 weather_emoji(description)
Returns a relevant emoji based on the weather description like:
•☀️ Clear
•☁️ Cloudy
•🌧️ Rain
•❄️ Snow
•🌈 Default

🧹 clear_weather()
Resets weather display fields (used before re-fetching).

🔁 auto_refresh()
Automatically fetches the last known city’s weather every 10 minutes

🏁 Main Block
Runs the app if the script is executed directly.

💡 Summary
| Feature              | Description                                     |
| -------------------- | ----------------------------------------------- |
| Weather API          | Uses OpenWeatherMap API to fetch real-time data |
| City Input           | Text input field for entering a city            |
| Responsive Layout    | Scales to screen size                           |
| Platform-aware fonts | Different fonts for Mac, Windows, Linux         |
| Auto-refresh         | Every 10 minutes                                |
| Popup Display        | Weather appears in a themed popup               |
| Emojis               | Weather icons as emojis                         |
| Background Image     | Optional background aesthetic                   |
| Error Handling       | Friendly messages for common issues             |



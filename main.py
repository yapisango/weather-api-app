import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QPushButton, QLabel,
                             QLineEdit, QVBoxLayout)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter Cuty name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.imoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.imoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.imoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.imoji_label.setObjectName("imoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
                           QLabel, QPushButton{
                               font-family: calibri;
                            }
                            QLabel#city_label{
                                font-size: 40px;
                                font-family: italic;
                            }
                            QLineEdit#city_input{
                                font-size: 40px;
                            }
                            QPushButton#get_weather_button{
                                font-size: 30px;
                                font-weight: bold;
                            }
                            QLabel#temperature_label{
                                font-size: 75px
                            }
                            QLabel#imoji_label{
                                font-size: 100px;
                                font-family: Segoe UI imoji;
                            }
                            QLabel#description_label{
                                font-size: 50px;
                            }
                            """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "3154ae89e9ace537755ce82674fdb1ed"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
            else:
                print(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_errort("Unauthorized\nInvalid Api key")
                case 403:
                    self.display_error("Forbiddent\nAccess is denied")
                case 404:
                    self.display_error("Not found\nCity not found")
                case 500:
                    self.display_error("Internal server\nPlease try again later")
                case 502:
                    self.display_error("Bad gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailablw\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        try:
            # Extract temperature (convert from Kelvin to Celsius)
            temp_kelvin = data["main"]["temp"]
            temp_celsius = round(temp_kelvin - 273.15)

            # Extract weather description
            description = data["weather"][0]["description"].capitalize()

            # Choose emoji based on weather condition
            weather_main = data["weather"][0]["main"]
            emoji_map = {
                "Clear": "☀️",
                "Clouds": "☁️",
                "Rain": "🌧️",
                "Drizzle": "🌦️",
                "Thunderstorm": "⛈️",
                "Snow": "❄️",
                "Mist": "🌫️",
                "Haze": "🌁"
            }
            emoji = emoji_map.get(weather_main, "🌡️")

            # Update labels
            self.temperature_label.setText(f"{temp_celsius}°C")
            self.imoji_label.setText(emoji)
            self.description_label.setText(description)

        except Exception as e:
            self.display_error(f"Error parsing data:\n{e}")


def main():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

"""
Kate Yurmanovych
Lesson 6 Homework

1) Создать консольную программу-парсер, с выводом прогноза погоды. Дать
возможность пользователю получить прогноз погоды в его локации ( по
умолчанию) и в выбраной локации, на определенную пользователем дату.
Можно реализовать, как консольную программу, так и веб страницу.
Используемые инструменты: requests, beautifulsoup, остальное по желанию.
На выбор можно спарсить страницу, либо же использовать какой-либо API.

I'm using https://openweathermap.org/ API.
The forecast is up to 5 future days, as further days are in the paid subscription.
Note, I could've used "forecast" request for "today" as well, but since "forecast" returns
json for 5 days, it would have increased the parsing time. So I decided to write more code but save up some
program working time.
"""

from datetime import datetime
import requests
import json


class Weather:

    def __init__(self, def_city: str, def_country: str):
        self._api_key = "e95a51412c5c6d5443b73d8584e5e1d6"      # my working API key
        self._def_city = def_city
        self._def_country = def_country
        self._city = None
        self._country = None
        self._location_id = None
        self._date = None
        self._url_today = "http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}"
        self._url_forecast = "http://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}"

    def define_location(self):
        while True:
            is_def_location = input("Get weather for your default location? Y/N")
            if is_def_location == "y" or is_def_location == "Y":
                self._city = self._def_city
                self._country = self._def_country
                break
            elif is_def_location == "n" or is_def_location == "N":
                self._city = input("Enter city: ")
                self._country = input("Enter country in the format 'XX' (e.g. US): ")
                break
            else:
                print("Incorrect choice. Please press either Y or N ")
                continue

    def define_date(self):
        is_date = input("Show weather forecast for today? Y/N ")
        if is_date == "y" or is_date == "Y":
            self._date = datetime.now()
        else:
            print("You can get a 5 future day forecast")
            date = input('Enter date in the exact format “dd/mm/YYYY”, not more than 5 days ahead: ')
            try:
                date = datetime.strptime(date, '%d/%m/%Y')
            except (TypeError, ValueError):
                print('\nException: Incorrect date format, should be string “dd/mm/YYYY”. \n The date will be set to '
                      'today.')
                self._date = datetime.now()
            else:
                time_delta = date - datetime.now()
                if time_delta.days < 0 or time_delta.days > 5:
                    print("You entered data which is either in the past or more than 5 days in the future. Your date "
                          "will be set to today.")
                    self._date = datetime.now()
                else:
                    self._date = datetime.now() + time_delta

    def get_weather(self):
        self.define_location()
        self.define_date()

        #  today's weather
        if self._date == datetime.now():
            r = requests.get(self._url_today.format(self._city, self._country, self._api_key))
            if r.status_code != 200:
                print(f"Incorrect data input.\n Status code: {r.status_code}, response text: {r.text}")
            else:
                weather_data = json.loads(r.text)
                print("City: ", weather_data["name"])
                print("Weather: ", weather_data["weather"][0]["description"])
                print("Temperature: ", weather_data["main"]["temp"])

        # forecast up to 5th day ahead
        else:
            r = requests.get(self._url_forecast.format(self._city, self._country, self._api_key))
            if r.status_code != 200:
                print(f"Incorrect data input.\n Status code: {r.status_code}, response text: {r.text}")
            else:
                weather_data = json.loads(r.text)
                print("City: ", weather_data["city"]["name"])
                for day in weather_data["list"]:
                    date_forecast = day["dt_txt"]
                    if date_forecast[:10] == self._date.strftime('%Y-%m-%d')[:10]:
                        print("Date: ", day["dt_txt"])
                        print("Weather:", day["weather"][0]["description"])
                        print("Temperature: ", day["main"]["temp"])
                        break


if __name__ == "__main__":
    my_weather = Weather("Kyiv", "UA")
    my_weather.get_weather()

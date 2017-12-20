#!/usr/bin/python3

import socket
import tkinter as tk
import requests
from urllib.request import urlopen
from urllib.error import URLError
from PIL import Image, ImageTk
from io import BytesIO


class InterfaceSetup:
    """Class to train and plot Mean square error and Absolute error variations LMS algorithm"""

    def __init__(self, root, master, statusbar):
        self.master = master
        self.root = root
        self.status_bar = statusbar

        # Variables
        self.latitude = None
        self.longitude = None
        self.weather_info_response = None
        self.weather_icon_response = tk.PhotoImage('')

        self.weather_frame = tk.Frame(self.master, bg='yellow')
        self.weather_frame.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.weather_frame.rowconfigure(10, weight=1)
        self.weather_frame.columnconfigure(3, weight=1)

        # Latitude label
        self.latitude_label = tk.Label(self.weather_frame, text="Enter Latitude", justify="left", bg='yellow')
        self.latitude_label.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10, pady=10)

        self.latitude_textbox = tk.Entry(self.weather_frame, justify="left")
        self.latitude_textbox.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10, pady=10)

        # Longitude label
        self.longitude_label = tk.Label(self.weather_frame, text="Enter Longitude", justify="left", bg='yellow')
        self.longitude_label.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10, pady=10)

        # https://www.tutorialspoint.com/python/tk_entry.htm
        self.longitude_textbox = tk.Entry(self.weather_frame, justify="left")
        self.longitude_textbox.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10, pady=10)

        # Submit button
        self.submit_button = tk.Button(self.weather_frame, text="Submit", justify="center", command=self.submit_function)
        self.submit_button.grid(row=2, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=20, pady=10)

        # Clear button
        self.clear_button = tk.Button(self.weather_frame, text="Clear", justify="center", command=self.clear)
        self.clear_button.grid(row=2, column=1, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=20, pady=10)

        # Refresh button
        self.refresh_button = tk.Button(self.weather_frame, text="Refresh", justify="center", command=self.refresh, width=12)
        self.refresh_button.grid(row=2, column=2, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=20, pady=10)

        # Results label
        self.results_label = tk.Label(self.weather_frame, text="Weather Information", justify="left", bg='yellow')
        self.results_label.grid(row=3, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10, pady=5)

        # Temperature label
        self.temperature_label = tk.Label(self.weather_frame, text="Temperature", justify="left", bg='yellow')
        self.temperature_label.grid(row=4, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                 pady=10)

        self.temperature_textbox = tk.Entry(self.weather_frame, justify="left")
        self.temperature_textbox.grid(row=4, column=1, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                   pady=10)
        # Temperature trend label
        self.temperature_trend_label = tk.Label(self.weather_frame, text="Temperature Trend", justify="left", bg='yellow')
        self.temperature_trend_label.grid(row=5, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                 pady=10)

        self.temperature_trend_textbox = tk.Entry(self.weather_frame, justify="left")
        self.temperature_trend_textbox.grid(row=5, column=1, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                   pady=10)
        # Wind speed label
        self.wind_speed_label = tk.Label(self.weather_frame, text="Wind Speed", justify="left", bg='yellow')
        self.wind_speed_label.grid(row=6, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                 pady=10)

        self.wind_speed_textbox = tk.Entry(self.weather_frame, justify="left")
        self.wind_speed_textbox.grid(row=6, column=1, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                   pady=10)
        # Wind direction label
        self.wind_direction_label = tk.Label(self.weather_frame, text="Wind Direction", justify="left", bg='yellow')
        self.wind_direction_label.grid(row=7, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                 pady=10)

        self.wind_direction_textbox = tk.Entry(self.weather_frame, justify="left")
        self.wind_direction_textbox.grid(row=7, column=1, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                   pady=10)
        # Short forecast label
        self.short_forecast_label = tk.Label(self.weather_frame, text="Short Forecast", justify="left", bg='yellow')
        self.short_forecast_label.grid(row=8, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                 pady=10)

        self.short_forecast_textbox = tk.Entry(self.weather_frame, justify="left")
        self.short_forecast_textbox.grid(row=8, column=1, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=1, columnspan=1, padx=10,
                                   pady=10)

        self.forecast_image = None

        # https://www.tutorialspoint.com/python/tk_message.htm
        # self.weather_information_message_set = tk.StringVar()
        # self.weather_information_message = tk.Message(self.weather_frame, relief='solid', bg='white', textvariable=self.weather_information_message_set)
        # self.weather_information_message.config(anchor='w')
        # self.weather_information_message.grid(row=4, column=0, sticky=tk.N + tk.E + tk.S + tk.W, rowspan=2, columnspan=2, padx=10, pady=5)

        # self.figure = pyplot.figure()

        # Print window size
        print("Window size:", self.master.winfo_width(), self.master.winfo_height())

    def submit_function(self):
        # Clear previous results -->From second submit onwards
        self.temperature_textbox.delete(0, 'end')
        self.temperature_trend_textbox.delete(0, 'end')
        self.wind_speed_textbox.delete(0, 'end')
        self.wind_direction_textbox.delete(0, 'end')
        self.short_forecast_textbox.delete(0, 'end')
        self.forecast_image = ''

        self.status_bar.set("Webservice called")

        self.latitude = self.latitude_textbox.get()
        self.longitude = self.longitude_textbox.get()

        try:
            socket_obj = SocketConnection(self.latitude, self.longitude)
            self.weather_info_response = socket_obj.weather_info_request()

            # Set results
            self.temperature_textbox.insert('end', str(self.weather_info_response['temperature']) + ' F')
            self.temperature_trend_textbox.insert('end', self.weather_info_response['temperatureTrend'])
            self.wind_speed_textbox.insert('end', self.weather_info_response['windSpeed'])
            self.wind_direction_textbox.insert('end', self.weather_info_response['windDirection'])
            self.short_forecast_textbox.insert('end', self.weather_info_response['shortForecast'])

            print(self.weather_info_response)

            self.weather_icon_response = socket_obj.weather_icon_request()

            # https://stackoverflow.com/questions/27599311/tkinter-photoimage-doesnt-not-support-png-image (HCLivess ans)
            image = ImageTk.PhotoImage(self.weather_icon_response, height=86, width=86)
            self.forecast_image = tk.Label(self.weather_frame, image=image, width=86, height=86)
            self.forecast_image.grid(row=9, column=2, rowspan=1, columnspan=1)
            self.forecast_image = image

            # self.forecast_image_textbox.image_create('end', image=image)

            # pyplot.imshow(self.weather_icon_response)
            # pyplot.show()

        except TypeError:
            self.status_bar.set("Latitude and Longitude values are not entered")

    def clear(self):
        # http://effbot.org/tkinterbook/entry.htm
        self.latitude_textbox.delete(0, 'end')
        self.longitude_textbox.delete(0, 'end')
        self.temperature_textbox.delete(0, 'end')
        self.temperature_trend_textbox.delete(0, 'end')
        self.wind_speed_textbox.delete(0, 'end')
        self.wind_direction_textbox.delete(0, 'end')
        self.short_forecast_textbox.delete(0, 'end')
        self.forecast_image = ''

        self.status_bar.set("All fields cleared")

    def refresh(self):
        self.status_bar.set("Refresh data in progress....")

        # Clear current results
        self.temperature_textbox.delete(0, 'end')
        self.temperature_trend_textbox.delete(0, 'end')
        self.wind_speed_textbox.delete(0, 'end')
        self.wind_direction_textbox.delete(0, 'end')
        self.short_forecast_textbox.delete(0, 'end')
        self.forecast_image = ''

        # Fetch latest update --> Uncomment the below statement to get new details
        # self.latitude = self.latitude_textbox.get()
        # self.longitude = self.longitude_textbox.get()

        # Use previous values to refresh data
        socket_obj = SocketConnection(self.latitude, self.longitude)

        try:
            self.weather_info_response = socket_obj.weather_info_request()
            # Set results
            self.temperature_textbox.insert('end', str(self.weather_info_response['temperature']) + ' F')
            self.temperature_trend_textbox.insert('end', self.weather_info_response['temperatureTrend'])
            self.wind_speed_textbox.insert('end', self.weather_info_response['windSpeed'])
            self.wind_direction_textbox.insert('end', self.weather_info_response['windDirection'])
            self.short_forecast_textbox.insert('end', self.weather_info_response['shortForecast'])

            print(self.weather_info_response)

            self.weather_icon_response = socket_obj.weather_icon_request()

            # https://stackoverflow.com/questions/27599311/tkinter-photoimage-doesnt-not-support-png-image (HCLivess ans)
            image = ImageTk.PhotoImage(self.weather_icon_response, height=86, width=86)

            self.forecast_image = tk.Label(self.weather_frame, image=image, width=86, height=86)
            self.forecast_image.grid(row=9, column=2, rowspan=1, columnspan=1)
            self.forecast_image = image

            self.status_bar.set("Refreshing data completed")
        except TypeError:
            self.status_bar.set("Latitude and Longitude values are not entered")


class SocketConnection(object):
    def __init__(self, latitude, longitude):
        self.base_url = " https://api.weather.gov/points/"
        self.extended_url = None
        self.json_response = None
        self.latitude = latitude
        self.longitude = longitude
        self.weather_dict = {'temperature': None, 'temperatureTrend': None, 'windSpeed': None, 'windDirection': None, 'icon': None, 'shortForecast': None}

    def weather_info_request(self):
        self.extended_url = self.base_url + self.latitude + ',' + self.longitude + "/forecast/"
        print(self.extended_url)

        # request = Request(self.extended_url)

        # Working
        try:
            response = requests.get(self.extended_url)
        except ConnectionError:
            print("Connection to the server failed")
            response = None

        try:
            self.json_response = response.json()
        except ValueError:
            print("JSON cannot be parsed")
            self.json_response = None

        try:
            self.weather_dict['temperature'] = self.json_response["properties"]["periods"][0]['temperature']
            self.weather_dict['temperatureTrend'] = self.json_response["properties"]["periods"][0]['temperatureTrend']
            self.weather_dict['windSpeed'] = self.json_response["properties"]["periods"][0]['windSpeed']
            self.weather_dict['windDirection'] = self.json_response["properties"]["periods"][0]['windDirection']
            self.weather_dict['icon'] = self.json_response["properties"]["periods"][0]['icon']
            self.weather_dict['shortForecast'] = self.json_response["properties"]["periods"][0]['shortForecast']

            return self.weather_dict
        except KeyError:
            print("Values are not entered correctly")

    def weather_icon_request(self):
        # https://stackoverflow.com/questions/31064981/python3-error-initial-value-must-be-str-or-none

        try:
            response = urlopen(self.weather_dict['icon']).read()
            image = Image.open(BytesIO(response))

            return image
        except URLError:
            # https://docs.python.org/3/library/urllib.request.html
            print("Host doesn't handle the specified URL")
            return None
        except AttributeError:
            print("Values are none")
        except IOError:
            print("Image cannot be read or not found on server")
            return None

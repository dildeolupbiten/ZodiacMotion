#!/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

import os
import re
import sys
import ssl
import tkinter as tk

from time import time, sleep
from threading import Thread
from subprocess import Popen
from webbrowser import open_new
from platform import architecture
from math import cos, sin, radians
from urllib.request import urlopen
from tkinter.ttk import Progressbar
from tkinter.messagebox import showinfo
from datetime import (datetime as dt, timedelta as td)

try:
    from dateutil import tz
except ModuleNotFoundError:
    os.system("pip3 install python-dateutil")
    from dateutil import tz
try:
    from pytz import timezone
except ModuleNotFoundError:
    os.system("pip3 install pytz")
    from pytz import timezone
try:
    from timezonefinder import TimezoneFinder
except ModuleNotFoundError:
    os.system("pip3 install timezonefinder")
    from timezonefinder import TimezoneFinder


def select_module(
        name: str = "",
        file: list = [],
        path: str = ""
):
    if os.name == "posix":
        os.system(f"pip3 install {name}")
    elif os.name == "nt":
        if sys.version_info.minor == 6:
            if architecture()[0] == "32bit":
                new_path = os.path.join(path, file[0])
                os.system(f"pip3 install {new_path}")
            elif architecture()[0] == "64bit":
                new_path = os.path.join(path, file[1])
                os.system(f"pip3 install {new_path}")
        elif sys.version_info.minor == 7:
            if architecture()[0] == "32bit":
                new_path = os.path.join(path, file[2])
                os.system(f"pip3 install {new_path}")
            elif architecture()[0] == "64bit":
                new_path = os.path.join(path, file[3])
                os.system(f"pip3 install {new_path}")
        elif sys.version_info.minor == 8:
            if architecture()[0] == "32bit":
                new_path = os.path.join(path, file[4])
                os.system(f"pip3 install {new_path}")
            elif architecture()[0] == "64bit":
                new_path = os.path.join(path, file[5])
                os.system(f"pip3 install {new_path}")


PATH = os.path.join(os.getcwd(), "Eph", "Whl")

try:
    import swisseph as swe
except ModuleNotFoundError:
    select_module(
        name="pyswisseph",
        file=[i for i in os.listdir(PATH) if "pyswisseph" in i],
        path=PATH
    )
    import swisseph as swe

swe.set_ephe_path(os.path.join(os.getcwd(), "Eph"))

SIGNS = {
    "Aries": {
        "symbol": "\u2648",
        "color": "#FF0000"
    },
    "Taurus": {
        "symbol": "\u2649",
        "color": "#00FF00"
    },
    "Gemini": {
        "symbol": "\u264A",
        "color": "#FFFF00"
    },
    "Cancer": {
        "symbol": "\u264B",
        "color": "#0000FF"
    },
    "Leo": {
        "symbol": "\u264C",
        "color": "#FF0000"
    },
    "Virgo": {
        "symbol": "\u264D",
        "color": "#00FF00"
    },
    "Libra": {
        "symbol": "\u264E",
        "color": "#FFFF00"
    },
    "Scorpio": {
        "symbol": "\u264F",
        "color": "#0000FF"
    },
    "Sagittarius": {
        "symbol": "\u2650",
        "color": "#FF0000"
    },
    "Capricorn": {
        "symbol": "\u2651",
        "color": "#00FF00"
    },
    "Aquarius": {
        "symbol": "\u2652",
        "color": "#FFFF00"
    },
    "Pisces": {
        "symbol": "\u2653",
        "color": "#0000FF"
    }
}

PLANETS = {
    "Sun": {
        "number": swe.SUN,
        "symbol": "\u2299"
    },
    "Moon": {
        "number": swe.MOON,
        "symbol": "\u263E"
    },
    "Mercury": {
        "number": swe.MERCURY,
        "symbol": "\u263F"
    },
    "Venus": {
        "number": swe.VENUS,
        "symbol": "\u2640"
    },
    "Mars": {
        "number": swe.MARS,
        "symbol": "\u2642"
    },
    "Jupiter": {
        "number": swe.JUPITER,
        "symbol": "\u2643"
    },
    "Saturn": {
        "number": swe.SATURN,
        "symbol": "\u2644"
    },
    "Uranus": {
        "number": swe.URANUS,
        "symbol": "\u2645"
    },
    "Neptune": {
        "number": swe.NEPTUNE,
        "symbol": "\u2646"
    },
    "Pluto": {
        "number": swe.PLUTO,
        "symbol": "\u2647"
    },
    "True": {
        "number": swe.TRUE_NODE,
        "symbol": "\u260A"
    },
    "Asc": {
        "number": None,
        "symbol": "Asc"
    },
    "MC": {
        "number": None,
        "symbol": "MC"
    }
}

ASPECTS = {
    "Conjunction": {
        "degree": 0,
        "orb": "10\u00b0 0\' 0\"",
    },
    "Semi-Sextile": {
        "degree": 30,
        "orb": "3\u00b0 0\' 0\"",
    },
    "Semi-Square": {
        "degree": 45,
        "orb": "3\u00b0 0\' 0\"",
    },
    "Sextile": {
        "degree": 60,
        "orb": "6\u00b0 0\' 0\"",
    },
    "Quintile": {
        "degree": 72,
        "orb": "2\u00b0 0\' 0\"",
    },
    "Square": {
        "degree": 90,
        "orb": "10\u00b0 0\' 0\"",
    },
    "Trine": {
        "degree": 120,
        "orb": "10\u00b0 0\' 0\"",
    },
    "Sesquiquadrate": {
        "degree": 135,
        "orb": "3\u00b0 0\' 0\"",
    },
    "BiQuintile": {
        "degree": 144,
        "orb": "2\u00b0 0\' 0\"",
    },
    "Quincunx": {
        "degree": 150,
        "orb": "3\u00b0 0\' 0\"",
    },
    "Opposite": {
        "degree": 180,
        "orb": "10\u00b0 0\' 0\"",
    }
}

HOUSE_SYSTEMS = {
    "Placidus": "P",
    "Koch": "K",
    "Porphyrius": "O",
    "Regiomontanus": "R",
    "Campanus": "C",
    "Equal": "E",
    "Whole Signs": "W"
}

HSYS = "P"


def convert_degree(degree: float = 0):
    for i in range(12):
        if i * 30 <= degree < (i + 1) * 30:
            return degree - (30 * i), [*SIGNS][i]


def reverse_convert_degree(degree: float = 0, sign: str = ""):
    return degree + 30 * [*SIGNS].index(sign)


def dms_to_dd(dms: str = ""):
    dms = dms.replace(" ", "")
    dms = dms.replace("\u00b0", " ").replace("\'", " ").replace("\"", " ")
    degree = int(dms.split(" ")[0])
    minute = float(dms.split(" ")[1]) / 60
    second = float(dms.split(" ")[2]) / 3600
    return degree + minute + second


class Zodiac:
    def __init__(
            self,
            year: int = 0,
            month: int = 0,
            day: int = 0,
            hour: int = 0,
            minute: int = 0,
            second: int = 0,
            lat: float = .0,
            lon: float = .0,
            hsys: str = ""
    ):
        self.LOCAL_YEAR = year
        self.LOCAL_MONTH = month
        self.LOCAL_DAY = day
        self.LOCAL_HOUR = hour
        self.LOCAL_MINUTE = minute
        self.LOCAL_SECOND = second
        self.LAT = lat
        self.LON = lon
        self.HSYS = hsys
        self.UTC_YEAR = self.local_to_utc()["year"]
        self.UTC_MONTH = self.local_to_utc()["month"]
        self.UTC_DAY = self.local_to_utc()["day"]
        self.UTC_HOUR = self.local_to_utc()["hour"]
        self.UTC_MINUTE = self.local_to_utc()["minute"]
        self.UTC_SECOND = self.local_to_utc()["second"]
        self.JD = self.julday()

    def julday(self):
        t_given = dt.strptime(
            f"{self.UTC_YEAR}.{self.UTC_MONTH}.{self.UTC_DAY}",
            "%Y.%m.%d"
        )
        t_limit = dt.strptime("1582.10.15", "%Y.%m.%d")
        if (t_limit - t_given).days > 0:
            calendar = swe.JUL_CAL
        else:
            calendar = swe.GREG_CAL
        jd = swe.julday(
            self.UTC_YEAR,
            self.UTC_MONTH,
            self.UTC_DAY,
            self.UTC_HOUR
            + (self.UTC_MINUTE / 60)
            + (self.UTC_SECOND / 3600),
            calendar
        )
        deltat = swe.deltat(jd)
        return round(jd + deltat, 6)

    def local_to_utc(self):
        local_zone = tz.gettz(
            str(
                timezone(
                    TimezoneFinder().timezone_at(
                        lat=self.LAT, lng=self.LON
                    )
                )
            )
        )
        utc_zone = tz.gettz("UTC")
        global_time = dt.strptime(
            f"{self.LOCAL_YEAR}-{self.LOCAL_MONTH}-{self.LOCAL_DAY} "
            f"{self.LOCAL_HOUR}:{self.LOCAL_MINUTE}:{self.LOCAL_SECOND}",
            "%Y-%m-%d %H:%M:%S"
        )
        local_time = global_time.replace(tzinfo=local_zone)
        utc_time = local_time.astimezone(utc_zone)
        return {
            "year": utc_time.year,
            "month": utc_time.month,
            "day": utc_time.day,
            "hour": utc_time.hour,
            "minute": utc_time.minute,
            "second": utc_time.second
        }

    def planet_pos(self, planet: int = 0):
        calc = convert_degree(
            degree=swe.calc_ut(self.JD, planet)[0]
        )
        return calc[1], reverse_convert_degree(calc[0], calc[1])

    def house_pos(self):
        house = []
        asc = 0
        degree = []
        for i, j in enumerate(swe.houses(
                self.JD, self.LAT, self.LON,
                bytes(self.HSYS.encode("utf-8")))[0]):
            if i == 0:
                asc += j
            degree.append(j)
            house.append((
                f"{i + 1}",
                j,
                f"{convert_degree(j)[1]}"))
        return house, asc, degree

    def patterns(self):
        planet_positions = []
        house_positions = []
        sign_positions = []
        for i in range(12):
            house = [
                int(self.house_pos()[0][i][0]),
                self.house_pos()[0][i][-1],
                float(self.house_pos()[0][i][1]),
            ]
            house_positions.append(house)
        hp = [j[-1] for j in house_positions]
        for key, value in PLANETS.items():
            if key in ["Asc", "MC"]:
                continue
            planet = self.planet_pos(planet=value["number"])
            house = 0
            for i in range(12):
                if i != 11:
                    if hp[i] < planet[1] < hp[i + 1]:
                        house = i + 1
                        break
                    elif hp[i] < planet[1] > hp[i + 1] \
                            and hp[i] - hp[i + 1] > 240:
                        house = i + 1
                        break
                    elif hp[i] > planet[1] < hp[i + 1] \
                            and hp[i] - hp[i + 1] > 240:
                        house = i + 1
                        break
                else:
                    if hp[i] < planet[1] < hp[0]:
                        house = i + 1
                        break
                    elif hp[i] < planet[1] > hp[0] \
                            and hp[i] - hp[0] > 240:
                        house = i + 1
                        break
                    elif hp[i] > planet[1] < hp[0] \
                            and hp[i] - hp[0] > 240:
                        house = i + 1
                        break
            planet_info = [
                key,
                planet[0],
                planet[1],
                f"H{house}"
            ]
            planet_positions.append(planet_info)
        asc = house_positions[0] + ["H1"]
        asc[0] = "Asc"
        mc = house_positions[9] + ["H10"]
        mc[0] = "MC"
        planet_positions.extend([asc, mc])
        asc = convert_degree(house_positions[0][-1])
        for i in range(1, 13):
            degree = 180 + (30 * i) - asc[0]
            if degree >= 360:
                degree -= 360
            try:
                sign_positions.append(
                    [
                        [*SIGNS][[*SIGNS].index(asc[-1]) + i],
                        degree
                    ]
                )
            except IndexError:
                sign_positions.append(
                    [
                        [*SIGNS][[*SIGNS].index(asc[-1]) + i - 12],
                        degree
                    ]
                )
        return planet_positions, house_positions, sign_positions


class Canvas(tk.Canvas):
    def __init__(self, zodiac: Zodiac = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False
        self.zodiac = zodiac
        self.objects = {}
        self.aspect_objects = {}
        self.count = -1
        self.new_asc = ""
        self.old_asc = ""
        self["width"] = self.master.winfo_screenwidth()
        self["height"] = self.master.winfo_screenheight()
        self.planet_positions = zodiac[0]
        self.house_positions = zodiac[1]
        self.sign_positions = zodiac[2]
        self.house_pos = [i[-1] for i in self.house_positions]
        self.sign_pos = [i[-1] for i in self.sign_positions]
        self.signs = [i[0] for i in self.sign_positions]
        self.signs = [self.signs[-1]] + self.signs[:-1]
        self.pack()
        self.midpoint_of_houses = []
        self.draw_oval_object()
        self.draw_houses()
        self.draw_signs()
        self.draw_house_numbers()
        self.draw_sign_symbols()
        self.draw_planets()
        self.draw_aspects()

    def draw_oval_object(self, x: int = 400, y: int = 300):
        self.oval_object(x=x, y=y, r=260, dash=False)
        self.oval_object(x=x, y=y, r=210, dash=False)
        self.oval_object(x=x, y=y, r=165)
        self.oval_object(x=x, y=y, r=60, dash=False)

    @staticmethod
    def line_components(degree: float = .0, r: int = 0):
        x, y = 400, 300
        x += (r * cos(radians(degree)))
        y -= (r * sin(radians(degree)))
        return x, y

    def coordinates(self, degree: float = .0, r1: int = 0, r2: int = 0):
        x1, y1 = self.line_components(degree=degree, r=r1)
        x2, y2 = self.line_components(degree=degree, r=r2)
        return x1, y1, x2, y2

    def oval_object(
            self,
            x: float = .0,
            y: float = .0,
            r: int = 0,
            dash: bool = True
    ):
        if dash:
            dash = (1, 10)
            self.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                fill="white",
                width=2,
                dash=dash
            )
        else:
            self.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                fill="white",
                width=2,
            )

    def line_object(
            self,
            x1: float = .0,
            y1: float = .0,
            x2: float = .0,
            y2: float = .0,
            width: int = 2,
            fill: str = "black",
            name: str = ""
    ):
        if not self.active:
            line = self.create_line(
                x1, y1, x2, y2, width=width, fill=fill
            )
            self.objects[name] = line
        else:
            self.coords(self.objects[name], x1, y1, x2, y2)
            self.update()

    def aspect_line_object(
            self,
            x1: float = .0,
            y1: float = .0,
            x2: float = .0,
            y2: float = .0,
            width: int = 2,
            fill: str = "black",
            key: str = "",
            _key: str = ""
    ):
        if not self.active:
            line = self.create_line(
                x1, y1, x2, y2, width=width, fill=fill
            )
            self.aspect_objects[(key, _key)] = line
        else:
            if (key, _key) not in self.aspect_objects:
                line = self.create_line(
                    x1, y1, x2, y2, width=width, fill=fill
                )
                self.aspect_objects[(key, _key)] = line
            else:
                self.coords(self.aspect_objects[(key, _key)], x1, y1, x2, y2)
                self.update()

    def text_object(
            self,
            x: float = .0,
            y: float = .0,
            width: int = 0,
            _text: str = "",
            font: str = "Arial",
            fill: str = "black",
            name: str = ""
    ):
        if not self.active:
            text = self.create_text(
                x, y, text=_text, width=width, font=font, fill=fill
            )
            self.objects[name] = text
        else:
            self.coords(self.objects[name], x, y)
            self.update()

    def draw_houses(self):
        self.midpoint_of_houses = []
        for i, j in enumerate(self.house_pos):
            degree = j - (self.house_pos[0] - 180)
            if degree < 0:
                degree += 360
            elif degree > 360:
                degree -= 360
            self.midpoint_of_houses.append(degree)
            x1, y1, x2, y2 = self.coordinates(
                degree=degree, r1=60, r2=210
            )
            if i == 0 or i == 3 or i == 6 or i == 9:
                self.line_object(
                    x1, y1, x2, y2, width=4, name=f"house{i}"
                )
            else:
                self.line_object(
                    x1, y1, x2, y2, width=2, name=f"house{i}"
                )

    def draw_signs(self):
        for i, j in enumerate(self.sign_pos):
            x1, y1, x2, y2 = self.coordinates(degree=j, r1=210, r2=260)
            self.line_object(x1, y1, x2, y2, width=2, name=f"sign{i}")

    def draw_house_numbers(self):
        for i, j in enumerate(self.midpoint_of_houses):
            if i == 11:
                midpoint = \
                    (self.midpoint_of_houses[i] +
                     self.midpoint_of_houses[0]) / 2
            else:
                if self.midpoint_of_houses[i] == 360:
                    midpoint = self.midpoint_of_houses[i + 1] / 2
                else:
                    if self.midpoint_of_houses[i + 1] == 0 or \
                            self.midpoint_of_houses[i + 1] < 30:
                        midpoint = \
                            (self.midpoint_of_houses[i] +
                             self.midpoint_of_houses[i + 1] + 360) / 2
                    else:
                        midpoint = \
                            (self.midpoint_of_houses[i] +
                             self.midpoint_of_houses[i + 1]) / 2
            if i == 6:
                if midpoint > 180:
                    midpoint -= 180
            x1, y1, x2, y2 = self.coordinates(
                degree=midpoint, r1=60, r2=110
            )
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            self.text_object(
                x=x, y=y, _text=f"{i + 1}", name=f"midpoint{i}"
            )

    def draw_sign_symbols(self):
        for i, j in enumerate(self.signs):
            if i == 0:
                self.new_asc = j
                if self.new_asc != self.old_asc:
                    self.count += 1
                    self.old_asc = self.new_asc
            end = 30 - (self.house_pos[0] % 30) + 180 \
                - (self.count * 30)
            start = end - 30
            start += (30 * i)
            end += (30 * i)
            if start > 360:
                start -= 360
            if end > 360:
                end -= 360
            if start > 330:
                midpoint = (start + end + 360) / 2
            else:
                midpoint = (start + end) / 2
            if midpoint > 360:
                midpoint -= 360
            x1, y1, x2, y2 = self.coordinates(
                degree=midpoint, r1=210, r2=260
            )
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            self.text_object(
                x=x,
                y=y,
                _text=SIGNS[j]["symbol"],
                font="Arial 25",
                fill=SIGNS[j]["color"],
                name=f"symbols{i}"
            )

    def draw_planets(self):
        for ind, i in enumerate(self.planet_positions):
            for j in self.sign_positions:
                planet = convert_degree(i[-2])
                if planet[1] == j[0]:
                    degree = planet[0] + j[1]
                    x1, y1, x2, y2 = self.coordinates(
                        degree=degree, r1=210, r2=175
                    )
                    x = ((x1 + x2) / 2) + 4
                    y = ((y1 + y2) / 2) + 4
                    self.text_object(
                        x=x,
                        y=y,
                        _text=PLANETS[i[0]]['symbol'],
                        width=0,
                        font="Default 20",
                        name=f"planets{ind}"
                    )
                    x1, y1, x2, y2 = self.coordinates(
                        degree=degree, r1=210, r2=205
                    )
                    self.line_object(
                        x1, y1, x2, y2, width=2, fill="red", name=i[0]
                    )

    def create_aspect(
            self,
            value: float = .0,
            _value: float = .0,
            color: str = "",
            key: str = "",
            _key: str = "",
            r1: int = 160,
            r2: int = 165,
    ):
        x1, y1, x2, y2 = self.coordinates(
            degree=value, r1=r1, r2=r2
        )
        _x1, _y1, _x2, _y2 = self.coordinates(
            degree=_value, r1=r1, r2=r2
        )
        self.aspect_line_object(
            x2, y2, _x2, _y2,
            width=2,
            fill=color,
            key=key,
            _key=_key
        )

    def select_aspect(
            self,
            aspect: float = .0,
            value: float = 0,
            _value: float = 0,
            key: str = "",
            _key: str = ""
    ):
        if 0 < aspect < dms_to_dd(ASPECTS["Conjunction"]["orb"]) or \
                360 - dms_to_dd(ASPECTS["Conjunction"]["orb"]) < \
                aspect < 360:
            self.create_aspect(
                value=value,
                _value=_value,
                color="red",
                key=key,
                _key=_key
            )
        # elif 30 - dms_to_dd(ASPECTS["Semi-Sextile"]["orb"]) < aspect <
        #         30 + dms_to_dd(ASPECTS["Semi-Sextile"]["orb"]) or \
        #         330 - dms_to_dd(ASPECTS["Semi-Sextile"]["orb"]) < \
        #         aspect < 330 + dms_to_dd(ASPECTS["Semi-Sextile"]["orb"]):
        #     self.create_aspect(
        #         value = value,
        #         _value=_value,
        #         color="black",
        #         key=key,
        #         _key=_key
        #     )
        # elif 45 - dms_to_dd(ASPECTS["Semi-Square"]["orb"]) < aspect < \
        #         45 + dms_to_dd(ASPECTS["Semi-Square"]["orb"]) or \
        #         315 - dms_to_dd(ASPECTS["Semi-Square"]["orb"]) < aspect < \
        #         315 + dms_to_dd(ASPECTS["Semi-Square"]["orb"]):
        #     self.create_aspect(
        #         value = value,
        #         _value=_value,
        #         color="black",
        #         key=key,
        #         _key=_key
        #     )
        elif 60 - dms_to_dd(ASPECTS["Sextile"]["orb"]) < aspect < \
                60 + dms_to_dd(ASPECTS["Sextile"]["orb"]) or \
                300 - dms_to_dd(ASPECTS["Sextile"]["orb"]) < aspect < \
                300 + dms_to_dd(ASPECTS["Sextile"]["orb"]):
            self.create_aspect(
                value=value,
                _value=_value,
                color="blue",
                key=key,
                _key=_key
            )
        # elif 72 - dms_to_dd(ASPECTS["Quintile"]["orb"]) < aspect < \
        #         72 + dms_to_dd(ASPECTS["Quintile"]["orb"]) or \
        #         288 - dms_to_dd(ASPECTS["Quintile"]["orb"]) < aspect < \
        #         288 + dms_to_dd(ASPECTS["Quintile"]["orb"]):
        #     self.create_aspect(
        #         value = value,
        #         _value=_value,
        #         color="purple",
        #         key=key,
        #         _key=_key
        #     )
        elif 90 - dms_to_dd(ASPECTS["Square"]["orb"]) < aspect < \
                90 + dms_to_dd(ASPECTS["Square"]["orb"]) or \
                270 - dms_to_dd(ASPECTS["Square"]["orb"]) < aspect < \
                270 + dms_to_dd(ASPECTS["Square"]["orb"]):
            self.create_aspect(
                value=value,
                _value=_value,
                color="red",
                key=key,
                _key=_key
            )
        elif 120 - dms_to_dd(ASPECTS["Trine"]["orb"]) < aspect < \
                120 + dms_to_dd(ASPECTS["Trine"]["orb"]) or \
                240 - dms_to_dd(ASPECTS["Trine"]["orb"]) < aspect < \
                240 + dms_to_dd(ASPECTS["Trine"]["orb"]):
            self.create_aspect(
                value=value,
                _value=_value,
                color="blue",
                key=key,
                _key=_key
            )
        # elif 135 - dms_to_dd(ASPECTS["Sesquiquadrate"]["orb"]) < aspect < \
        #         135 + dms_to_dd(ASPECTS["Sesquiquadrate"]["orb"]) or \
        #         225 - dms_to_dd(ASPECTS["Sesquiquadrate"]["orb"]) < aspect < \
        #         225 + dms_to_dd(ASPECTS["Sesquiquadrate"]["orb"]):
        #     self.create_aspect(
        #         value = value,
        #         _value=_value,
        #         color="orange",
        #         key=key,
        #         _key=_key
        #     )
        # elif 144 - dms_to_dd(ASPECTS["BiQuintile"]["orb"]) < aspect < \
        #         144 + dms_to_dd(ASPECTS["BiQuintile"]["orb"]) or \
        #         216 - dms_to_dd(ASPECTS["BiQuintile"]["orb"]) < aspect < \
        #         216 + dms_to_dd(ASPECTS["BiQuintile"]["orb"]):
        #     self.create_aspect(
        #         value = value,
        #         _value=_value,
        #         color="gray",
        #         key=key,
        #         _key=_key
        #     )
        # elif 150 - dms_to_dd(ASPECTS["Quincunx"]["orb"]) < aspect < \
        #         150 + dms_to_dd(ASPECTS["Quincunx"]["orb"]) or \
        #         210 - dms_to_dd(ASPECTS["Quincunx"]["orb"]) < aspect < \
        #         210 + dms_to_dd(ASPECTS["Quincunx"]["orb"]):
        #     self.create_aspect(
        #         value = value,
        #         _value=_value,
        #         color="pink",
        #         key=key,
        #         _key=_key
        #     )
        elif 180 - dms_to_dd(ASPECTS["Opposite"]["orb"]) < aspect < \
                180 + dms_to_dd(ASPECTS["Opposite"]["orb"]):
            self.create_aspect(
                value=value,
                _value=_value,
                color="red",
                key=key,
                _key=_key
            )
        else:
            if (key, _key) in self.aspect_objects:
                self.delete(self.aspect_objects[(key, _key)])
                self.aspect_objects.pop((key, _key))

    def draw_aspects(self):
        planet_degrees = {}
        for i in self.planet_positions:
            for j in self.sign_positions:
                planet = convert_degree(i[-2])
                if planet[1] == j[0]:
                    degree = planet[0] + j[1]
                    planet_degrees[i[0]] = degree
        for key, value in planet_degrees.items():
            for _key, _value in planet_degrees.items():
                aspect = abs(value - _value)
                if key != _key:
                    self.select_aspect(
                        aspect=aspect,
                        value=value,
                        _value=_value,
                        key=key,
                        _key=_key
                    )


class Menu(tk.Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master.configure(menu=self)
        self.options = tk.Menu(master=self, tearoff=False)
        self.help = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label="Options", menu=self.options)
        self.add_cascade(label="Help", menu=self.help)
        self.options.add_command(
            label="Orb Factors",
            command=self.choose_orb_factor
        )
        self.options.add_command(
            label="House Systems",
            command=self.change_house_system
        )
        self.help.add_command(
            label="About",
            command=self.about
        )
        self.help.add_command(
            label="Check for updates",
            command=self.update_script
        )

    def choose_orb_factor(self):
        toplevel = tk.Toplevel()
        toplevel.title("Orb Factors")
        toplevel.geometry("200x300")
        toplevel.resizable(width=False, height=False)
        default_orbs = [ASPECTS[i]["orb"] for i in ASPECTS]
        orb_entries = []
        frame = tk.Frame(master=toplevel)
        frame.pack()
        for i, j in enumerate(list(ASPECTS.keys())):
            aspect_label = tk.Label(
                master=frame,
                text=f"{j}"
            )
            aspect_label.grid(row=i, column=0, sticky="w")
            orb_entry = tk.Entry(master=frame, width=7)
            orb_entry.grid(row=i, column=1)
            orb_entry.insert(0, default_orbs[i])
            orb_entries.append(orb_entry)
        apply_button = tk.Button(
            master=frame,
            text="Apply",
            command=lambda: self.change_orb_factors(
                orb_entries=orb_entries,
                toplevel=toplevel
            )
        )
        apply_button.grid(row=11, column=0, columnspan=3)

    @staticmethod
    def change_orb_factors(
            orb_entries: list = [],
            toplevel: tk.Toplevel = None
    ):
        error = False
        for i, j in enumerate(ASPECTS):
            if not re.findall(
                    "[0-9]\\u00b0\\s[0-9]*'\\s[0-9]*\"",
                    orb_entries[i].get()
            ):
                error = True
            else:
                ASPECTS[j]["orb"] = orb_entries[i].get()
        if error:
            showinfo(title="Warning", message="Invalid Orb Factor")
        else:
            toplevel.destroy()

    @staticmethod
    def change_hsys(
            parent: tk.Toplevel = None,
            checkbuttons: dict = {}
    ):
        global HSYS
        for i in HOUSE_SYSTEMS:
            if checkbuttons[i][1].get() == "1":
                HSYS = HOUSE_SYSTEMS[i]
        parent.destroy()

    @staticmethod
    def check_uncheck(checkbuttons: dict = {}, hsys: str = ""):
        for i in HOUSE_SYSTEMS:
            if i != hsys:
                checkbuttons[i][1].set("0")
                checkbuttons[i][0].configure(
                    variable=checkbuttons[i][1]
                )

    def configure_checkbuttons(
            self,
            checkbuttons: dict = {},
            hsys: str = ""
    ):
        return checkbuttons[hsys][0].configure(
            command=lambda: self.check_uncheck(
                checkbuttons=checkbuttons,
                hsys=hsys
            )
        )

    def change_house_system(self):
        toplevel = tk.Toplevel()
        toplevel.title("House Systems")
        toplevel.geometry("200x200")
        toplevel.resizable(width=False, height=False)
        hsys_frame = tk.Frame(master=toplevel)
        hsys_frame.pack(side="top")
        button_frame = tk.Frame(master=toplevel)
        button_frame.pack(side="bottom")
        checkbuttons = {}
        for i, j in enumerate(HOUSE_SYSTEMS):
            var = tk.StringVar()
            if HSYS == HOUSE_SYSTEMS[j]:
                var.set(value="1")
            else:
                var.set(value="0")
            checkbutton = tk.Checkbutton(
                master=hsys_frame,
                text=j,
                variable=var
            )
            checkbutton.grid(row=i, column=0, sticky="w")
            checkbuttons[j] = [checkbutton, var]
            self.configure_checkbuttons(
                checkbuttons=checkbuttons,
                hsys=j
            )
        apply_button = tk.Button(
            master=button_frame,
            text="Apply",
            command=lambda: self.change_hsys(
                toplevel,
                checkbuttons,
            )
        )
        apply_button.pack()

    @staticmethod
    def callback(url: str = ""):
        open_new(url)

    def about(self):
        toplevel = tk.Toplevel()
        toplevel.title("About ZodiacMotion")
        name = "ZodiacMotion"
        version, _version = "Version:", __version__
        build_date, _build_date = "Built Date:", "04.03.2020"
        update_date, _update_date = "Update Date:", \
            dt.strftime(
                dt.fromtimestamp(os.stat(sys.argv[0]).st_mtime),
                "%d.%m.%Y"
            )
        developed_by, _developed_by = "Developed By:", \
                                      "Tanberk Celalettin Kutlu"
        contact, _contact = "Contact:", "tckutlu@gmail.com"
        github, _github = "GitHub:", \
                          "https://github.com/dildeolupbiten/ZodiacMotion"
        tframe1 = tk.Frame(master=toplevel, bd="2", relief="groove")
        tframe1.pack(fill="both")
        tframe2 = tk.Frame(master=toplevel)
        tframe2.pack(fill="both")
        tlabel_title = tk.Label(master=tframe1, text=name, font="Arial 25")
        tlabel_title.pack()
        for i, j in enumerate(
                (
                    version,
                    build_date,
                    update_date,
                    developed_by,
                    contact,
                    github
                )
        ):
            tlabel_info_1 = tk.Label(
                master=tframe2,
                text=j,
                font="Arial 12",
                fg="red"
            )
            tlabel_info_1.grid(row=i, column=0, sticky="w")
        for i, j in enumerate(
                (
                    _version,
                    _build_date,
                    _update_date,
                    _developed_by,
                    _contact,
                    _github
                )
        ):
            if j == _github:
                tlabel_info_2 = tk.Label(
                    master=tframe2,
                    text=j,
                    font="Arial 12",
                    fg="blue",
                    cursor="hand2"
                )
                url1 = "https://github.com/dildeolupbiten/ZodiacMotion"
                tlabel_info_2.bind(
                    "<Button-1>",
                    lambda event: self.callback(url1))
            elif j == _contact:
                tlabel_info_2 = tk.Label(
                    master=tframe2,
                    text=j,
                    font="Arial 12",
                    fg="blue",
                    cursor="hand2"
                )
                url2 = "mailto://tckutlu@gmail.com"
                tlabel_info_2.bind(
                    "<Button-1>",
                    lambda event: self.callback(url2))
            else:
                tlabel_info_2 = tk.Label(
                    master=tframe2,
                    text=j,
                    font="Arial 12"
                )
            tlabel_info_2.grid(row=i, column=1, sticky="w")

    @staticmethod
    def update_script():
        url_1 = "https://raw.githubusercontent.com/dildeolupbiten/" \
                "TkMidpoint/master/ZodiacMotion.py"
        url_2 = "https://raw.githubusercontent.com/dildeolupbiten/" \
                "TkMidpoint/master/README.md"
        data_1 = urlopen(
            url=url_1,
            context=ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        )
        data_2 = urlopen(
            url=url_2,
            context=ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        )
        with open(
                file="ZodiacMotion.py",
                mode="r",
                encoding="utf-8"
        ) as f:
            var_1 = [i.decode("utf-8") for i in data_1]
            var_2 = [i.decode("utf-8") for i in data_2]
            var_3 = [i for i in f]
            if var_1 == var_3:
                showinfo(
                    title="Update",
                    message="Program is up-to-date."
                )
            else:
                with open(
                        file="README.md",
                        mode="w",
                        encoding="utf-8"
                ) as g:
                    for i in var_2:
                        g.write(i)
                        g.flush()
                with open(
                        file="ZodiacMotion.py",
                        mode="w",
                        encoding="utf-8"
                ) as h:
                    for i in var_1:
                        h.write(i)
                        h.flush()
                    showinfo(
                        title="Update",
                        message="Program is updated."
                    )
                    if os.name == "posix":
                        Popen(
                            ["python3", "ZodiacMotion.py"]
                        )
                        import signal
                        os.kill(os.getpid(), signal.SIGKILL)
                    elif os.name == "nt":
                        Popen(
                            ["python", "ZodiacMotion.py"]
                        )
                        os.system(f"TASKKILL /F /PID {os.getpid()}")


class Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)
        self.start = False
        self.pframe = None
        self.canvas = None
        self.left_frame = tk.Frame(
            master=self,
            bd=1,
            relief="sunken",
            height=self.master.winfo_screenheight(),
            width=self.master.winfo_screenwidth() / 4
        )
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.right_frame = tk.Frame(
            master=self,
            bd=1,
            relief="sunken",
            height=self.master.winfo_screenheight(),
            width=3 * self.master.winfo_screenwidth() / 4
        )
        self.right_frame.pack(side=tk.LEFT)
        self.entry_names = [
            "Latitude",
            "Longitude",
            "Year",
            "Month",
            "Day",
            "Hour",
            "Minute",
            "Second"
        ]
        self.coordinates = self.entries(
            master=self.left_frame,
            entry_names=[*[self.entry_names[:2]]],
            text="Coordinates",
            side="top"
        )
        self.dates_frame = tk.Frame(master=self.left_frame)
        self.dates_frame.pack()
        self.starting_date = self.entries(
                master=self.dates_frame,
                entry_names=[
                    [*self.entry_names[2:5]],
                    [*self.entry_names[5:]]
                ],
                text="Starting Date",
                side="left",
            )
        self.ending_date = self.entries(
                master=self.dates_frame,
                entry_names=[
                    [*self.entry_names[2:5]],
                    [*self.entry_names[5:]]
                ],
                text="Ending Date",
                side="left",
            )
        self.time_changes = tk.Frame(
            master=self.left_frame,
            bd=1,
            relief="sunken"
        )
        self.time_changes.pack()
        self.chart_per_sec_scale, self.time_increase_scale = \
            self.time_change_widgets()
        self.current_date = self.entries(
                master=self.time_changes,
                entry_names=[
                    [*self.entry_names[2:5]],
                    [*self.entry_names[5:]]
                ],
                text="Current Date",
                side="bottom",
            )
        for i in self.current_date:
            self.current_date[i]["state"] = "disable"
        self.button_frame = tk.Frame(master=self.left_frame)
        self.button_frame.pack(pady=40)
        self.start_animation = tk.Button(
            master=self.button_frame,
            text="Start",
            command=lambda: Thread(
                target=self.start_command,
                daemon=True
            ).start(),
        )
        self.start_animation.pack(side="left", padx=5)
        self.stop_animation = tk.Button(
            master=self.button_frame,
            text="Stop",
            command=self.stop_command,
        )
        self.stop_animation.pack(side="left", padx=5)

    def time_change_widgets(self):
        for i, j, k in zip(
                [
                    "Refresh Chart Per Seconds",
                    "Amount of Time Increase"
                ],
                [10, 3600],
                [.1, 1],
        ):
            label = tk.Label(
                master=self.time_changes,
                text=i,
                font="Default 11 bold"
            )
            label.pack()
            var = self.doublevar(1, j, 0, k),
            scale = self.scale_and_spinbox(
                master=self.time_changes,
                textvariable=var[0],
                increment=var[0][3].get(),
                _from=var[0][2].get(),
                _to=var[0][1].get(),
                digit=6,
                text="Seconds",
            )
            yield scale

    def change_current_date(self, date: dt = None):
        for i in self.current_date:
            self.current_date[i].delete("0", "end")
        self.current_date["Year"].insert(
            0, date.year
        )
        self.current_date["Month"].insert(
            0, date.month
        )
        self.current_date["Day"].insert(
            0, date.day
        )
        self.current_date["Hour"].insert(
            0, date.hour
        )
        self.current_date["Minute"].insert(
            0, date.minute
        )
        self.current_date["Second"].insert(
            0, date.second
        )
        self.update()

    def change_zodiac(
            self, date: dt = None,
            lat: float = .0,
            lon: float = .0
    ):
        zodiac = Zodiac(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=date.hour,
            minute=date.minute,
            second=date.second,
            lat=lat,
            lon=lon,
            hsys=HSYS
        ).patterns()
        if not self.canvas:
            self.canvas = Canvas(
                master=self.right_frame,
                zodiac=zodiac
            )
            self.canvas.active = True
        else:
            self.canvas.zodiac = zodiac
            self.canvas.planet_positions = zodiac[0]
            self.canvas.house_positions = zodiac[1]
            self.canvas.sign_positions = zodiac[2]
            self.canvas.house_pos = [
                i[-1] for i in self.canvas.house_positions
            ]
            self.canvas.sign_pos = [
                i[-1] for i in self.canvas.sign_positions
            ]
            self.canvas.signs = [
                i[0] for i in self.canvas.sign_positions
            ]
            self.canvas.signs = [self.canvas.signs[-1]] + \
                self.canvas.signs[:-1]
            self.canvas.draw_houses()
            self.canvas.draw_signs()
            self.canvas.draw_house_numbers()
            self.canvas.draw_sign_symbols()
            self.canvas.draw_planets()
            self.canvas.draw_aspects()

    @staticmethod
    def progress_info(c: int = 0, s: int = 0, n: float = .0):
        return \
            f"{int(100 * c / s)} %, " \
            f"{round(c / (time() - n), 3)} c/s, " \
            f"{int(s / (c / (time() - n))) - int(time() - n)}" \
            f" seconds remaining."

    def start_command(self):
        s_Y = self.starting_date["Year"].get()
        s_m = self.starting_date["Month"].get()
        s_d = self.starting_date["Day"].get()
        s_H = self.starting_date["Hour"].get()
        s_M = self.starting_date["Minute"].get()
        s_S = self.starting_date["Second"].get()
        e_Y = self.ending_date["Year"].get()
        e_m = self.ending_date["Month"].get()
        e_d = self.ending_date["Day"].get()
        e_H = self.ending_date["Hour"].get()
        e_M = self.ending_date["Minute"].get()
        e_S = self.ending_date["Second"].get()
        lat = self.coordinates["Latitude"].get()
        lon = self.coordinates["Longitude"].get()
        try:
            start = dt.strptime(
                f"{s_Y}.{s_m}.{s_d} {s_H}:{s_M}:{s_S}",
                "%Y.%m.%d %H:%M:%S"
            )
        except ValueError:
            showinfo(
                title="Info",
                message="Invalid date for starting time"
            )
            return
        try:
            end = dt.strptime(
                f"{e_Y}.{e_m}.{e_d} {e_H}:{e_M}:{e_S}",
                "%Y.%m.%d %H:%M:%S"
            )
        except ValueError:
            showinfo(
                title="Info",
                message="Invalid date for ending time"
            )
            return
        if start >= end:
            showinfo(
                title="Info",
                message="Starting time should be greater "
                        "than ending date."
            )
            return
        try:
            lat = float(lat)
        except ValueError:
            showinfo(
                title="Info",
                message="Invalid latitude value."
            )
            return
        try:
            lon = float(lon)
        except ValueError:
            showinfo(
                title="Info",
                message="Invalid longitude value."
            )
            return
        try:
            timezone(
                TimezoneFinder().timezone_at(
                    lat=lat, lng=lon
                )
            )
        except AttributeError:
            showinfo(
                title="Info",
                message="Invalid timezone for given "
                        "latitude and longitude values."
            )
            return
        if float(self.time_increase_scale.get()) <= 0:
            showinfo(
                title="Info",
                message="The amount of increase time "
                        "should be greater than 0."
            )
            return
        if not self.start:
            self.start = True
            if self.canvas:
                for k, v in self.canvas.objects.items():
                    self.canvas.delete(v)
                self.canvas.objects = {}
                self.canvas.destroy()
                self.canvas = None
            if self.pframe:
                self.pframe.destroy()
            for i in self.current_date:
                self.current_date[i]["state"] = "normal"
            s = (end - start).total_seconds()
            c = 0
            n = time()
            self.pframe = tk.Frame(master=self.left_frame)
            pbar = Progressbar(
                master=self.pframe,
                orient="horizontal",
                length=200,
                mode="determinate"
            )
            pstring = tk.StringVar()
            plabel = tk.Label(
                master=self.pframe,
                textvariable=pstring
            )
            self.pframe.pack()
            pbar.pack()
            plabel.pack()
            while start < end:
                start += td(
                    seconds=float(
                        self.time_increase_scale.get()
                    )
                )
                c += float(self.time_increase_scale.get())
                pbar["value"] = c
                pbar["maximum"] = s
                pstring.set(self.progress_info(c=c, s=s, n=n))
                sleep(float(self.chart_per_sec_scale.get()))
                if not self.start:
                    break
                self.update()
                self.change_current_date(date=start)
                self.change_zodiac(date=start, lat=lat, lon=lon)
            if self.start:
                self.change_current_date(date=end)
            for i in self.current_date:
                self.current_date[i]["state"] = "disable"
            self.start = False

    def stop_command(self):
        self.start = False

    @staticmethod
    def max_char(event: tk.Event = None, limit: int = 0):
        if len(event.widget.get()) > limit:
            event.widget.delete(str(limit))

    def entries(
            self,
            master=None,
            entry_names: list = [],
            text: str = "",
            side: str = "",
            pady: int = 0,
            padx: int = 0,
    ):
        entries = {}
        entry_frame = tk.Frame(master=master, bd=1, relief="sunken")
        entry_frame.pack(pady=pady, padx=padx, side=side)
        entry_label = tk.Label(
            master=entry_frame,
            text=text,
            font="Default 11 bold"
        )
        entry_label.pack(expand=True, fill=tk.BOTH)
        for i, j in enumerate(entry_names):
            frame = tk.Frame(master=entry_frame)
            frame.pack()
            for k, m in enumerate(j):
                sub_frame = tk.Frame(master=frame)
                sub_frame.pack(side="left")
                label = tk.Label(master=sub_frame, text=m)
                label.pack()
                if m in ["Month", "Day", "Hour", "Minute", "Second"]:
                    entry = tk.Entry(master=sub_frame, width=2)
                    entry.bind(
                        sequence="<KeyRelease>",
                        func=lambda event: self.max_char(
                            event=event,
                            limit=2
                        )
                    )
                elif m == "Year":
                    entry = tk.Entry(master=sub_frame, width=4)
                    entry.bind(
                        sequence="<KeyRelease>",
                        func=lambda event: self.max_char(
                            event=event,
                            limit=4
                        )
                    )
                else:
                    entry = tk.Entry(master=sub_frame, width=10)
                    entry.bind(
                        sequence="<KeyRelease>",
                        func=lambda event: self.max_char(
                            event=event,
                            limit=10
                        )
                    )
                entry.pack()
                entries[m] = entry
        return entries

    @staticmethod
    def doublevar(*args):
        return [tk.DoubleVar(value=i) for i in args]

    @staticmethod
    def scale_and_spinbox(
            master: None,
            pady: int = 0,
            digit: int = 0,
            increment: float = .0,
            _from: float = .0,
            _to: float = .0,
            text: str = "",
            textvariable: tk.DoubleVar = None,
    ):
        frame = tk.Frame(master=master)
        frame.pack(pady=pady)
        label = tk.Label(master=frame, text=text, width=12)
        label.pack(side="left")
        spinbox = tk.Spinbox(master=frame)
        spinbox["increment"] = increment
        spinbox["textvariable"] = textvariable
        spinbox["from"] = _from
        spinbox["to"] = _to
        spinbox["width"] = digit + 1
        spinbox.pack(side="left")
        scale = tk.Scale(master=frame, orient="horizontal")
        scale["length"] = 200
        scale["sliderlength"] = 15
        scale["digits"] = 1
        scale["resolution"] = increment
        scale["variable"] = textvariable
        scale["from"] = _from
        scale["to"] = _to
        scale["showvalue"] = False
        scale.pack(side="left")
        return scale


def main():
    root = tk.Tk()
    root.title("ZodiacMotion")
    Menu(master=root)
    Frame(master=root).mainloop()


if __name__ == "__main__":
    main()

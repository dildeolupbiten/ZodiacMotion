# -*- coding: utf-8 -*-

from .zodiac import Zodiac
from .modules import tk, cos, sin, radians
from .constants import PLANETS, SIGNS, ASPECTS
from .conversions import dms_to_dd, convert_degree


class Canvas(tk.Canvas):
    def __init__(self, zodiac: Zodiac = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = False
        self.zodiac = zodiac
        self.objects = {}
        self.aspect_objects = {}
        self.midpoint_of_houses = []
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
                self.coords(
                    self.aspect_objects[(key, _key)], x1, y1, x2, y2
                )

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
#        elif 30 - dms_to_dd(ASPECTS["Semi-Sextile"]["orb"]) < aspect <
#                30 + dms_to_dd(ASPECTS["Semi-Sextile"]["orb"]) or \
#                330 - dms_to_dd(ASPECTS["Semi-Sextile"]["orb"]) < \
#                aspect < 330 + dms_to_dd(ASPECTS["Semi-Sextile"]["orb"]):
#            self.create_aspect(
#                value = value,
#                _value=_value,
#                color="black",
#                key=key,
#                _key=_key
#            )
#        elif 45 - dms_to_dd(ASPECTS["Semi-Square"]["orb"]) < aspect < \
#                45 + dms_to_dd(ASPECTS["Semi-Square"]["orb"]) or \
#                315 - dms_to_dd(ASPECTS["Semi-Square"]["orb"]) < aspect < \
#                315 + dms_to_dd(ASPECTS["Semi-Square"]["orb"]):
#            self.create_aspect(
#                value = value,
#                _value=_value,
#                color="black",
#                key=key,
#                _key=_key
#            )
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
#        elif 72 - dms_to_dd(ASPECTS["Quintile"]["orb"]) < aspect < \
#                72 + dms_to_dd(ASPECTS["Quintile"]["orb"]) or \
#                288 - dms_to_dd(ASPECTS["Quintile"]["orb"]) < aspect < \
#                288 + dms_to_dd(ASPECTS["Quintile"]["orb"]):
#            self.create_aspect(
#                value = value,
#                _value=_value,
#                color="purple",
#                key=key,
#                _key=_key
#            )
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
#        elif 135 - dms_to_dd(ASPECTS["Sesquiquadrate"]["orb"]) < aspect < \
#                135 + dms_to_dd(ASPECTS["Sesquiquadrate"]["orb"]) or \
#                225 - dms_to_dd(ASPECTS["Sesquiquadrate"]["orb"]) < aspect < \
#                225 + dms_to_dd(ASPECTS["Sesquiquadrate"]["orb"]):
#            self.create_aspect(
#                value = value,
#                _value=_value,
#                color="orange",
#                key=key,
#                _key=_key
#            )
#        elif 144 - dms_to_dd(ASPECTS["BiQuintile"]["orb"]) < aspect < \
#                144 + dms_to_dd(ASPECTS["BiQuintile"]["orb"]) or \
#                216 - dms_to_dd(ASPECTS["BiQuintile"]["orb"]) < aspect < \
#                216 + dms_to_dd(ASPECTS["BiQuintile"]["orb"]):
#            self.create_aspect(
#                value = value,
#                _value=_value,
#                color="gray",
#                key=key,
#                _key=_key
#            )
#        elif 150 - dms_to_dd(ASPECTS["Quincunx"]["orb"]) < aspect < \
#                150 + dms_to_dd(ASPECTS["Quincunx"]["orb"]) or \
#                210 - dms_to_dd(ASPECTS["Quincunx"]["orb"]) < aspect < \
#                210 + dms_to_dd(ASPECTS["Quincunx"]["orb"]):
#            self.create_aspect(
#                value = value,
#                _value=_value,
#                color="pink",
#                key=key,
#                _key=_key
#            )
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

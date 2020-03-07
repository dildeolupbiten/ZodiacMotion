# -*- coding: utf-8 -*-

from .constants import SIGNS, PLANETS
from .modules import os, dt, tz, swe, timezone, TimezoneFinder
from .conversions import convert_degree, reverse_convert_degree

swe.set_ephe_path(os.path.join(os.getcwd(), "Eph"))


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

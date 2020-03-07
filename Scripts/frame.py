# -*- coding: utf-8 -*-

from .zodiac import Zodiac
from .canvas import Canvas
from .constants import HOUSE_SYSTEMS
from .modules import tk, showinfo, Progressbar
from .modules import td, dt, time, sleep, timezone, TimezoneFinder


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
            side="left"
        )
        self.ending_date = self.entries(
            master=self.dates_frame,
            entry_names=[
                [*self.entry_names[2:5]],
                [*self.entry_names[5:]]
            ],
            text="Ending Date",
            side="left"
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
            side="bottom"
        )
        for i in self.current_date:
            self.current_date[i]["state"] = "disable"
        self.button_frame = tk.Frame(master=self.left_frame)
        self.button_frame.pack(pady=40)
        self.start_animation = tk.Button(
            master=self.button_frame,
            text="Start",
            command=self.start_command
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
                [1, 1],
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
                text="Seconds"
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
            hsys=HOUSE_SYSTEMS["Default"]
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
        global _start, _c
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
            _start = dt.strptime(
                f"{s_Y}.{s_m}.{s_d} {s_H}:{s_M}:{s_S}",
                "%Y.%m.%d %H:%M:%S"
            )
        except ValueError:
            showinfo(
                title="Info",
                message="Invalid date for starting time."
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
                message="Invalid date for ending time."
            )
            return
        if _start >= end:
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
            s = (end - _start).total_seconds()
            _c = 0
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

            def loop():
                global _start, _c
                _start += td(
                    seconds=float(
                        self.time_increase_scale.get()
                    )
                )
                _c += float(self.time_increase_scale.get())
                pbar["value"] = _c
                pbar["maximum"] = s
                pstring.set(self.progress_info(c=_c, s=s, n=n))
                if not self.start:
                    return
                self.change_current_date(date=_start)
                self.change_zodiac(date=_start, lat=lat, lon=lon)
                self.update()
                if _start < end:
                    try:
                        self.after(
                            int(self.chart_per_sec_scale.get() * 1000), loop
                        )
                    except tk.TclError:
                        pass
                else:
                    if self.start:
                        self.change_current_date(date=end)
                    for date in self.current_date:
                        self.current_date[date]["state"] = "disable"
                    self.start = False

            try:
                loop()
            except ZeroDivisionError:
                sleep(0.1)
                loop()

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

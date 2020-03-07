# -*- coding: utf-8 -*-

from Scripts import __version__
from .constants import ASPECTS, HOUSE_SYSTEMS
from .modules import os, re, sys, tk, open_new, showinfo, dt


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
            showinfo(title="Warning", message="Invalid Orb Factor.")
        else:
            toplevel.destroy()

    @staticmethod
    def change_hsys(
            parent: tk.Toplevel = None,
            checkbuttons: dict = {}
    ):
        for i in HOUSE_SYSTEMS:
            if i != "Default":
                if checkbuttons[i][1].get() == "1":
                    HOUSE_SYSTEMS["Default"] = HOUSE_SYSTEMS[i]
        parent.destroy()

    @staticmethod
    def check_uncheck(checkbuttons: dict = {}, hsys: str = ""):
        for i in HOUSE_SYSTEMS:
            if i != hsys and i != "Default":
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
            if j != "Default":
                var = tk.StringVar()
                if HOUSE_SYSTEMS["Default"] == HOUSE_SYSTEMS[j]:
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
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Scripts.modules import tk
from Scripts.frame import Frame
from Scripts.menu import Menu


def main():
    root = tk.Tk()
    root.title("ZodiacMotion")
    Menu(master=root)
    Frame(master=root).mainloop()


if __name__ == "__main__":
    main()

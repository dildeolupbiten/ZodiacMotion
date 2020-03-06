#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Scripts.modules import tk
from Scripts.menu import Menu
from Scripts.frame import Frame


def main():
    root = tk.Tk()
    root.title("ZodiacMotion")
    Menu(master=root)
    Frame(master=root).mainloop()


if __name__ == "__main__":
    main()


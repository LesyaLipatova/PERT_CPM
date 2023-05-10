from main_frame import MainFrame
from tkinter import Tk


def main():
    root = Tk()
    root.wm_title("Автоматизация решения задачи сетевого планирования проекта")
    app = MainFrame(root)
    app.mainloop()


if __name__ == "__main__":
    main()

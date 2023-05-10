from tkinter import *
from tkinter import messagebox
import pandas as pd
from tkinter import filedialog
from collections import namedtuple


class Excel:

    def open_CPM_file():
        aux = 0
        infiles = ""
        excel = True
        df = ''

        while excel:
            try:
                # open the window to select the file
                messagebox.showinfo(title="Información",
                                    message="Ожидается четыре столбца: идентификатор, описание, продолжительность, предшественник")

                infiles = filedialog.askopenfilename(multiple=True)

                if (infiles == ""):
                    break

                # validate if it is an excel file
                if (str(infiles[0]).endswith('.xls') or str(infiles[0]).endswith('.xlsx')):
                    archivo = infiles[0]

                    # creating the dataframe
                    data = pd.ExcelFile(archivo)
                    df = data.parse()

                    # the file must have four columns
                    if (df.shape[1] != 4):
                        messagebox.showinfo(title="Предупреждение",
                                            message="Отсутствуют все четыре столбца, выберите новый файл")
                        continue
                    else:
                        for i in range(df.shape[0]):
                            if (isinstance(df["duracion"][i], str)):
                                aux = 1
                                break
                        if (aux == 1):
                            messagebox.showinfo(title="Предупреждение",
                                                message="Продолжительность должна быть целым числом")
                            continue
                        else:
                            break

                else:
                    messagebox.showinfo(title="Предупреждение", message="Файл должен быть в формате Excel")
                    continue
            except ValueError:
                messagebox.showinfo(title="Предупреждение", message="Файл должен быть в формате Excel")
                continue
        data = namedtuple("data", ["df", "infiles"])
        return data(
            df,
            infiles,
        )


    def open_PERT_file():
        aux = 0
        infiles = ""
        excel = True
        df = ''

        while excel:
            try:
                # open the window to select the file
                messagebox.showinfo(title="Información",
                                    message="Ожидается 6 столбцов:identificacion, descripcion, optTime, likeTime, pessTime, predecessors")

                infiles = filedialog.askopenfilename(multiple=True)

                if (infiles == ""):
                    break

                # validate if it is an excel file
                if (str(infiles[0]).endswith('.xls') or str(infiles[0]).endswith('.xlsx')):
                    archivo = infiles[0]

                    # creating the dataframe
                    data = pd.ExcelFile(archivo)
                    df = data.parse()

                    # the file must have four columns
                    if (df.shape[1] != 6):
                        messagebox.showinfo(title="Предупреждение",
                                            message="Отсутствуют все 7 столбцов, выберите новый файл")
                        continue
                    else:
                        for i in range(df.shape[0]):
                            continue
                        else:
                            break

                else:
                    messagebox.showinfo(title="Предупреждение", message="Файл должен быть в формате Excel")
                    continue
            except ValueError:
                messagebox.showinfo(title="Предупреждение", message="Файл должен быть в формате Excel")
                continue
        data = namedtuple("data", ["df", "infiles"])
        return data(
            df,
            infiles,
        )
import ast
from tkinter import CENTER, END, Label, Button, Entry, Frame, Radiobutton, Scrollbar
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter import *
from tkinter.constants import DISABLED, NORMAL
from tkinter import messagebox
from excel import Excel
from critical_path import CriticalPath
from graph import draw_graph
from math import isnan


class MainFrame(Frame):
    archivoExcel = ""  # Переменная, сохраняющая наименьшее значение для выбранного файла excel
    dataFrame = ""  # Переменная, которая поддерживает фрейм данных pandas, созданный из файла Excel
    auxInput = []  # Вспомогательный вектор, который сохраняет вводимые пользователем данные, когда они вставляют задачи вручную
    rutaCritica = ''  # Список, который получает результаты алгоритма CPM
    nodes = []
    method = ''

    # (Прямой, обратный и критический путь сам по себе)
    def __init__(self, master=None):
        super().__init__(master, width=800, height=700)
        self.master = master
        self.pack()
        excel = Excel
        claseCPM = CriticalPath
        self.create_widgets(excel, claseCPM)

    def recolectarInput(self, input1, input2, input3, input4, tabla, opciones):
        # Вводимые данные собираются из каждого текстового бота (tkinter Entry)
        ident = input1.get()
        if ident in opciones:
            messagebox.showinfo(title="Предупреждение", message="Этот идентификатор уже существует")
        else:
            opciones.append(ident)
            desc = input2.get()
            duracion = input3.get()
            predec = input4.get()
            if duracion.isdigit():
                # Если у него нет предшественника, он помещается в него*, чтобы не было ошибки с реализованным алгоритмом
                if predec == '':
                    predec = float("*")
                    self.auxInput.append(ident + '-' + desc + '-' + duracion + '-' + '.')
                else:
                    self.auxInput.append(ident + '-' + desc + '-' + duracion + '-' + predec)
                # Вставляется в таблицу интерфейса начального состояния
                tabla.insert("", END, text=ident, values=(predec, desc, duracion))
                self.lista_auxiliar = opciones
            else:
                messagebox.showinfo(title="Предупреждение", message="Продолжительность должна быть числовой")

    # В libExcel вызывается функция, которая позволяет загружать файл на диск
    # и то, что находится в файле, вставляется в таблицу интерфейса начального состояния
    # Ему нужно передать класс libExcel и таблицу, которую нужно изменить
    def upload_file_CPM(self, excel, tabla1):
        # Вызываем функцию в libExcel, чтобы она открыла и обработала файл
        self.dataFrame, self.archivoExcel = excel.open_CPM_file()
        # Если какой-либо файл не был выбран, пользователь получает уведомление
        if (self.archivoExcel == ""):
            messagebox.showinfo(title="Предупреждение", message="Файл не выбран")
        else:
            # Если выбран файл, он добавляется в таблицу интерфейса
            for x in range(0, self.dataFrame['identificacion'].size):
                if isinstance(self.dataFrame['predecessors'][x], (float)):
                    if not isnan(self.dataFrame['predecessors'][x]):
                        self.nodes.append((self.dataFrame['predecessors'][x], self.dataFrame['identificacion'][x]))
                else:
                    self.nodes.append((self.dataFrame['predecessors'][x], self.dataFrame['identificacion'][x]))
                tabla1.insert("", END, text=self.dataFrame['identificacion'][x]
                              , values=(self.dataFrame['predecessors'][x], self.dataFrame['descripcion'][x]
                                        , self.dataFrame['duracion'][x]))
        self.method = 'CPM'

    def upload_file_PERT(self, excel, table1):
        # Вызываем функцию в libExcel, чтобы она открыла и обработала файл
        self.dataFrame, self.archivoExcel = excel.open_PERT_file()
        self.dataFrame['duracion'] = None
        # Если какой-либо файл не был выбран, пользователь получает уведомление
        if (self.archivoExcel == ""):
            messagebox.showinfo(title="Предупреждение", message="Файл не выбран")
        else:
            # Если выбран файл, он добавляется в таблицу интерфейса
            for x in range(0, self.dataFrame['identificacion'].size):
                if isinstance(self.dataFrame['predecessors'][x], (float)):
                    if not isnan(self.dataFrame['predecessors'][x]):
                        self.nodes.append((self.dataFrame['predecessors'][x], self.dataFrame['identificacion'][x]))
                else:
                    # (O + 4 * M + P) / 6
                    self.nodes.append((self.dataFrame['predecessors'][x], self.dataFrame['identificacion'][x]))
                self.dataFrame['duracion'][x] = round(((self.dataFrame['O'][x] + 4 * self.dataFrame['likeTime'][x] + self.dataFrame['pessTime'][x]) / 6), 2)
                table1.insert("", END, text=self.dataFrame['identificacion'][x]
                              , values=(self.dataFrame['predecessors'][x], self.dataFrame['descripcion'][x]
                                        , self.dataFrame['duracion'][x]))
        self.method = 'PERT'

    # Функция, которая в соответствии с тем, как были введены данные, заполняет таблицы forwardpass
    # и обратный проход
    # Ему нужно передать класс libCaminoCritico и таблицы, которые нужно изменить
    def llenarTablas(self, llenadoTabla, tabla1, tabla2):
        try:
            # Вспомогательная переменная
            informacion = ''
            # Основные проверки в зависимости от того, как были введены данные
            if (self.archivoExcel == "" and len(self.auxInput) == 0):
                messagebox.showinfo(title="Предупреждение", message="Данные не введены")
                # Класс libCaminoCritico имеет разные методы обработки полученной информации
                # (если вводится с помощью excel или вручную)            elif self.archivoExcel == "":
                informacion = llenadoTabla.procesarInput(CriticalPath, self.auxInput)
            elif len(self.auxInput) == 0:
                if self.method == 'PERT':
                    informacion = llenadoTabla.processArchivoPERT(CriticalPath, self.dataFrame)
                else:
                    informacion = llenadoTabla.processArchivoCPM(CriticalPath, self.dataFrame)

            # После получения информация о методах libCaminoCritico вставляется в соответствующие
            # таблицы интерфейса
            if informacion != '':
                self.rutaCritica = informacion
                Fp = informacion.forwardPass
                bP = informacion.backwardPass
                indices = Fp.index
                # Вставка в таблицу backwardPass
                for x in range(0, Fp['earlyFinish'].size):
                    tabla2.insert("", END, text=indices[x], values=(Fp['earlyFinish'][x], Fp['earlyStart'][x], self.rutaCritica.backwardPass['slack'][x]))
                indices = bP.index
                # Вставка в таблицу forwardPass
                for x in range(0, bP['lateStart'].size):
                    tabla1.insert("", END, text=indices[x],
                                  values=(bP['lateStart'][x], bP['lateFinish'][x], bP['slack'][x]))
        except:
            messagebox.showinfo(title="Предупреждение",
                                message="Произошла ошибка при расчете критического пути. \n Пожалуйста, закройте программу, просмотрите добавленные данные и повторите попытку. \n Это может быть какая-то опечатка или в вашем графе есть циклы.")

    # Функция, которая заполняет текстовые поля с указанием критического пути и при наличии пробелов
    # Нужно, чтобы все текстовые поля, которые нужно изменить, были переданы ему
    def llenarTextbox(self, resp1, resp2, resp3, resp4, resp5):
        # Изменение текстового поля, если RC существует
        if resp1 != "":
            resp1.insert(0, "Да")
        else:
            resp1.insert(0, "Нет")
        # Изменение текстового поля, указывающего, что такое RC
        resp2.insert(0, self.rutaCritica.criticalPath)
        # Изменение текстового поля, которое спрашивает, есть ли слабина
        auxBp = self.rutaCritica.backwardPass
        hasSlack = False
        for x in range(0, auxBp['slack'].size):
            if auxBp['slack'][x] > 0:
                hasSlack = True
                break
        critical_nodes = ast.literal_eval(self.rutaCritica.criticalPath)
        resp3.insert(0, round(self.rutaCritica.forwardPass.earlyFinish.get(critical_nodes[-1]), 2))
        if hasSlack == True:
            # Modificando el textbox que indica
            # la cantidad de eventos qe tienen holgura
            indicesHolgura = []
            cantidadholgura = []
            for x in range(0, auxBp['slack'].size):
                if auxBp['slack'][x] > 0:
                    indicesHolgura.append(auxBp.index[x])
                    cantidadholgura.append(round(auxBp['slack'][x], 2))
            resp4.insert(0, round(sum(cantidadholgura), 2))
            # Modificando el textbox que indica los eventos que tienen
            # holgura con su respectiva holgura
            resp5Text = ''
            for x in range(0, len(indicesHolgura)):
                resp5Text = resp5Text + str(indicesHolgura[x]) + ' -> ' + str(cantidadholgura[x]) + ' \n'
            resp5.insert(0, resp5Text)

    def create_widgets(self, excel, llenadoTabla):

        # Ярлыки
        Label(self, text="Загрузка данных").place(x=20, y=10)
        Label(self,
              text="_____________________________________________________________________________________________________").place(
            x=20, y=30)
        Label(self, text="Идентификатор").place(x=20, y=50)
        Label(self, text="Описание").place(x=140, y=50)
        Label(self, text="Продолжительность").place(x=430, y=50)
        Label(self, text="Предшественник").place(x=20, y=110)
        Label(self,
              text="_____________________________________________________________________________________________________").place(
            x=20, y=130)
        Label(self, text="Исходные данные").place(x=230, y=155)
        Label(self, text="Прямой проход").place(x=230, y=320)
        Label(self, text="Обратный проход").place(x=230, y=485)
        # Label(self, text="Статистика").place(x=650, y=155)
        # Label(self, text="Есть критический путь?").place(x=590, y=195)
        Label(self, text="Критический путь").place(x=590, y=155)
        Label(self, text="Длинна критического пути").place(x=590, y=215)
        Label(self, text="Общее время резерва").place(x=590, y=275)
        Label(self, text="Событие -> резерв ").place(x=590, y=335)

        # Текстовое поле
        # input1
        txt_id = Entry(self, bg="white", state=DISABLED)
        txt_id.place(x=20, y=70, width=100, height=20)

        # input2
        txt_des = Entry(self, bg="white", state=DISABLED)
        txt_des.place(x=140, y=70, width=270, height=20)

        # input3
        txt_du = Entry(self, bg="white", state=DISABLED)
        txt_du.place(x=430, y=70, width=100, height=20)

        # respuesta1
        txt_existeRC = Entry(self, bg="white")
        # txt_existeRC.place(x=590, y=225, width=190, height=20)

        # respuesta2
        txt_RC = Entry(self, bg="white")
        txt_RC.place(x=590, y=185, width=190, height=20)

        # respuesta3
        min_duration = Entry(self, bg="white")
        min_duration.place(x=590, y=245, width=190, height=20)

        # respuesta4
        txt_contador = Entry(self, bg="white")
        txt_contador.place(x=590, y=305, width=190, height=20)

        # respuesta5
        txt_listaHolgura = Entry(self, bg="white")
        txt_listaHolgura.place(x=590, y=365, width=190, height=100)

        # input4
        txt_pre = Entry(self, bg="white", state=DISABLED)
        txt_pre.place(x=260, y=110, width=150, height=20)

        # radiobuttons

        opcion = IntVar()
        rbt_manual = Radiobutton(self, text="Ручной ввод", value=1, variable=opcion,
                                 command=lambda: actualiza(opcion.get()))
        rbt_manual.place(x=140, y=10)
        rbt_archivo = Radiobutton(self, text="Архив", value=2, variable=opcion, command=lambda: actualiza(opcion.get()))
        rbt_archivo.place(x=260, y=10)

        # combo_box

        self.opciones = []
        self.lista_auxiliar = ["Ни один"]
        cmb_pre = Combobox(self, values=self.lista_auxiliar, state=DISABLED)
        cmb_pre.place(x=140, y=110, width=100)

        def string_pre(pre, new, textbox):
            if pre != "":
                if pre.find(new) == -1:
                    pre = pre + ',' + new
                    txt_pre.config(text=pre)
                else:
                    messagebox.showinfo(title="Предупреждение", message="Не может повторять предшественников")
            else:
                if new == "Ни один":
                    new = "."
                pre = new
            textbox.delete(0, "end")
            textbox.insert(0, pre)

        cmb_pre.bind("<<ComboboxSelected>>", lambda _: [string_pre(txt_pre.get(), cmb_pre.get(), txt_pre)])

        # таблица исходных данных

        tv = ttk.Treeview(self, columns=("col1", "col2", "col3"))
        tv.column("#0", width=30)
        tv.column("col1", width=30, anchor=CENTER)
        tv.column("col2", width=150, anchor=CENTER)
        tv.column("col3", width=50, anchor=CENTER)

        tv.heading("#0", text="Идентификатор", anchor=CENTER)
        tv.heading("col1", text="Предшественник", anchor=CENTER)
        tv.heading("col2", text="Описание", anchor=CENTER)
        tv.heading("col3", text="Продолжительность", anchor=CENTER)

        tv.place(x=20, y=180, width=510, height=130)

        # рамка для начальной полосы прокрутки таблицы

        p_aux = Frame(self)
        p_aux.place(x=530, y=180, width=20, height=130)

        # начальная полоса прокрутки таблицы

        scroll_syn = Scrollbar(p_aux)
        scroll_syn.pack(side='right', fill='y')
        scroll_syn.config(command=tv.yview)

        # таблица вперед

        tv1 = ttk.Treeview(self, columns=("col1", "col2"))
        tv1.column("#0", width=30)
        tv1.column("col1", width=30, anchor=CENTER)
        tv1.column("col2", width=150, anchor=CENTER)

        tv1.heading("#0", text="Идентификатор", anchor=CENTER)
        tv1.heading("col1", text="ES", anchor=CENTER)
        tv1.heading("col2", text="EF", anchor=CENTER)

        tv1.place(x=20, y=345, width=510, height=130)

        # таблица задом наперед

        tv2 = ttk.Treeview(self, columns=("col1", "col2", "col3"))
        tv2.column("#0", width=30)
        tv2.column("col1", width=30, anchor=CENTER)
        tv2.column("col2", width=150, anchor=CENTER)
        tv2.column("col3", width=50, anchor=CENTER)

        tv2.heading("#0", text="Идентификатор", anchor=CENTER)
        tv2.heading("col1", text="LS", anchor=CENTER)
        tv2.heading("col2", text="LF", anchor=CENTER)
        tv2.heading("col3", text="Slack", anchor=CENTER)

        tv2.place(x=20, y=510, width=510, height=130)

        # рамка для символа полосы прокрутки таблиц for и back

        p_aux2 = Frame(self)
        p_aux2.place(x=530, y=345, width=20, height=295)

        # функция синхронизирующей прокрутки

        def multiple_yview(*args):
            tv1.yview(*args)
            tv2.yview(*args)

        # символьная полоса прокрутки таблиц for и back

        scroll_syn = Scrollbar(p_aux2)
        scroll_syn.pack(side='right', fill='y')
        scroll_syn.config(command=multiple_yview)

        def borrar():
            txt_pre.delete(0, "end")
            txt_id.delete(0, "end")
            txt_du.delete(0, "end")
            txt_des.delete(0, "end")

        # buttons

        self.btnA = Button(self, text="Добавить"
                           , command=lambda: [self.recolectarInput(txt_id, txt_des, txt_du, txt_pre, tv, self.opciones),
                                              cmb_pre.config(values=self.opciones), borrar()], state=DISABLED)
        self.btnA.place(x=430, y=110, width=100)

        self.btnRC = Button(self, text="Рассчитать критический путь",
                            command=lambda: [self.llenarTablas(llenadoTabla, tv1, tv2),
                                             self.llenarTextbox(txt_existeRC, txt_RC, min_duration, txt_contador,
                                                                txt_listaHolgura),
                                             self.btnRC.config(state=DISABLED)])
        self.btnRC.place(x=590, y=110, width=190)

        self.btnExcelCPM = Button(self, text="Файл Excel CPM",
                                  command=lambda: self.upload_file_CPM(excel, tv) and rbt_manual.config(state=DISABLED),
                                  state=DISABLED)
        self.btnExcelCPM.place(x=340, y=10, width=100)

        self.btnExcelPERT = Button(self, text="Файл Excel PERT",
                                   command=lambda: self.upload_file_PERT(excel, tv) and rbt_manual.config(state=DISABLED),
                                   state=DISABLED)
        self.btnExcelPERT.place(x=470, y=10, width=100)
        self.btn_draw_graph = Button(self, text="Отрисовать граф",
                                     command=lambda: draw_graph(self.nodes,
                                                                self.rutaCritica.criticalPath) and rbt_manual.config(
                                         state=ACTIVE),
                                     state=ACTIVE)
        self.btn_draw_graph.place(x=590, y=65, width=190)

        def actualiza(opcion):

            if opcion == 1:
                self.btnExcelCPM.configure(state=DISABLED)
                self.btnExcelPERT.configure(state=DISABLED)
                self.btnA.configure(state=NORMAL)
                txt_id.configure(state=NORMAL)
                txt_du.configure(state=NORMAL)
                cmb_pre.configure(state='readonly')
                txt_des.configure(state=NORMAL)

                txt_pre.configure(state=NORMAL)
            else:
                self.btnExcelCPM.configure(state=NORMAL)
                self.btnExcelPERT.configure(state=NORMAL)
                self.btnA.configure(state=DISABLED)
                txt_id.configure(state=DISABLED)
                txt_du.configure(state=DISABLED)
                txt_des.configure(state=DISABLED)
                cmb_pre.configure(state=DISABLED)
                txt_pre.configure(state=DISABLED)

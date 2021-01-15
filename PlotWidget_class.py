from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Upgraded_widgets import *


class Parent_Plot_Tab(QWidget):
    def __init__(self, name):
        super(Parent_Plot_Tab, self).__init__()
        self.name = name

        # self.frame = QFrame()
        # self.frame.setStyleSheet("QFrame {background-color: rgb(255, 255, 255);"
        #                          "border-width: 1;"
        #                          "border-radius: 3;"
        #                          "border-style: solid;"
        #                          "border-color: rgb(50,50,50)}"
        #                          )
        # self.main_layout.addWidget(self.frame)
        self.create_layout()
        # self.frame.setLayout(self.lay2)


    def create_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)
        self.setLayout(self.main_layout)


    # def col_or_indexes(self, x,y):

    #     # check if lineEdits contain indexes or column names
    #     # returns 'col_names', 'indexes' or None

    #     print('check')
    #     xs = x.split(',')
    #     xs = [i for i in xs]
    #     ys = y.split(',')
    #     ys = [i for i in ys]
    #     print(xs, ys)

    #     xs2 = set(xs)
    #     ys2 = set(ys)
    #     # c = self.table.col_labels.tolist()
    #     c = ['xx', 'yy', 'zz']
    #     ints = [str(i) for i in range(len(c))]
    #     print(ints)

    #     if (xs2.issubset(set(c)) and ys2.issubset(set(c))):
    #         return ('col_names')
    #     elif (xs2.issubset(set(ints)) and ys2.issubset(set(ints))):
    #         return ('indexes')
    #     else:
    #         return None
    
    
    # def plot(self):
    #     print('plotting')
    #     x,y = self.get_x_y_axis()
    #     r = self.col_or_indexes(x,y)
    #     print(r)

        
class Tab_Plot(Parent_Plot_Tab):
    def __init__(self, name):
        super(Tab_Plot, self).__init__(name)
        self.name = name

    def create_layout(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)

        self.label_x = QLabel(self)
        self.label_x.setText('info')
        self.label_x.setAlignment(Qt.AlignCenter)


        self.l_combobox_kind = Label_and_combobox('plot kind', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])
        self.l_combobox_kind.add_items(['scatter', 'line'])

        self.l_le_hue = Label_and_Lineedit('Hue', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])
        
        # self.b = QPushButton('plot')
        # self.b.clicked.connect(self.plot)

        self.main_layout.addWidget(self.label_x, 0,0)
        self.main_layout.addWidget(self.l_combobox_kind,1,0)
        # self.main_layout.addWidget(self.l_le_hue, 1,1)


        # self.main_layout.addWidget(self.b)

        self.setLayout(self.main_layout)

    def plot(self, table, x_, y_, hue_, ax_):
        print(self.name + ' plot')

        kind = self.l_combobox_kind.get_text()
        print(kind, hue_)

        if hue_ =='':
            hue_ = None

        if kind == 'line':
            plot = sns.lineplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
        elif kind == 'scatter':
            plot = sns.scatterplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
        print(plot)
        print(type(plot))

        return plot


class Tab_Plot2(Parent_Plot_Tab):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)

        self.label_pt = QLabel(self)
        self.label_pt.setText('Plot type')
        self.l_combobox_kind = Label_and_combobox('plot kind', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])
        l = ["strip", "swarm", "box", "violin", "boxen", "point", "bar", "count"]
        self.l_combobox_kind.add_items(l)

        self.l_combobox_col = Label_and_combobox('col argument', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])


        self.main_layout.addWidget(self.label_pt)
        self.main_layout.addWidget(self.l_combobox_kind)
        self.main_layout.addWidget(self.l_combobox_col)

        self.setLayout(self.main_layout)


    def plot(self, table, x_, y_, hue_, ax_):
        print(self.name + ' plot')

        kind = self.l_combobox_kind.get_text()
        print(kind, hue_)

        col = self.l_combobox_col.get_text()
        if col == '':
            col = None

        if hue_ =='':
            hue_ = None

        if kind == 'strip':
            plot = sns.stripplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
        elif kind == 'swarm':
            plot = sns.swarmplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
        elif kind == 'box':
            plot = sns.boxplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
        elif kind == 'violin':
            plot = sns.violinplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
        elif kind == 'boxen':
            plot = sns.boxenplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
        elif kind == 'point':
            plot = sns.pointplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
        elif kind == 'bar':
            plot = sns.barplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
        elif kind == 'count':
            plot = sns.countplot(x=x_, hue = hue_, data=table.dataframe, ax = ax_)

        print(plot)
        print(type(plot))


        return plot




class PlotWidget(QWidget):
    def __init__(self, table):
        super(PlotWidget, self).__init__(table)

        self.main_layout = QVBoxLayout(self)
        self.table = table

        self.canv = PlotCanvas(table, 5, 3)

        self.xx = QPushButton('plot')

        self.under_canv_layout = QGridLayout()

        self.tabs = QTabWidget(self)
        self.tab1 = Tab_Plot("relationships")
        self.tab2 = Tab_Plot2("distributions")
        self.tab3 = Tab_Plot2("p2")
        self.tab4 = Tab_Plot2("p2")
        self.tab5 = Tab_Plot2("p2")
        # self.tab6 = Tab_Plot2("p2")
        # self.tab7 = Tab_Plot2("p2")
        # self.tab8 = Tab_Plot2("p2")
        # self.tab9 = Tab_Plot2("p2")
        # self.tab10 = Tab_Plot2("p2")
        # self.tabs.addTab(self.xx, 'xx')
        # self.tabs.addTab(self.xx, 'xx12')
        self.tabs.addTab(self.tab1, self.tab1.name)
        self.tabs.addTab(self.tab2, "relationships")
        self.tabs.addTab(self.tab3, "distributions")
        self.tabs.addTab(self.tab4, "relationships")
        self.tabs.addTab(self.tab5, "relationships")
        # self.tabs.addTab(self.tab6, "relationships")
        # self.tabs.addTab(self.tab7, "relationships")
        # self.tabs.addTab(self.tab8, "relationships")
        # self.tabs.addTab(self.tab9, "relationships")
        # self.tabs.addTab(self.tab10, "relationships")


        self.list_of_tabs = [self.tab1, self.tab2]

        self.l_sp_number_of_plots = Label_and_spinbox('Number of plots', lay_dir = 'Horizontal')
        self.l_sp_number_of_plots.set_range(0,6)
        self.l_sp_number_of_plots.sp.valueChanged.connect(self.l_sp_number_of_plots_changed)

        self.l_sp_current_of_plots = Label_and_spinbox('current plot', lay_dir = 'Horizontal')
        self.l_sp_current_of_plots.set_range(0,6)
        # self.l_sp_current_of_plots.sp.valueChanged.connect(self.l_sp_number_of_plots_changed)

        # self.b = QPushButton('clear plot')
        # self.b_clear_plot.clicked.connect(self.clear_plot)


        self.l_le_x_axis = Label_and_Lineedit('X Label', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])
        self.l_le_y_axis = Label_and_Lineedit('Y Label', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])
        self.l_le_hue = Label_and_Lineedit('Hue', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])

        self.b_plot = QPushButton('plot')
        self.b_plot.clicked.connect(self.plot)

        self.b_clear_plot = QPushButton('clear plot')
        self.b_clear_plot.clicked.connect(self.clear_plot)

        self.b_switch_axes = QPushButton('switch axes')
        self.b_switch_axes.clicked.connect(self.switch_axes)


        self.checkbox = QCheckBox("col_names/indexes ", self)
        # self.checkbox.stateChanged.connect(lambda:self.checkbox_changed(self.checkbox))
        self.checkbox_reset_plots = QCheckBox("reset plots ", self)
        self.checkbox_reset_plots.setChecked(True)

        self.under_canv_layout.addWidget(self.tabs, 0, 0, 1, 4)
        
        # self.under_canv_layout.setRowStretch(0, 1)
        # self.under_canv_layout.setRowStretch(1, 50)
        # self.under_canv_layout.setRowStretch(2, 50)

        # self.under_canv_layout.setVerticalSpacing(30)

        # self.under_canv_layout.setColumnStretch(0,3)
        # self.under_canv_layout.setColumnStretch(1,1)
        # self.under_canv_layout.setColumnStretch(2,1)

        # self.lay = QHBoxLayout()
        self.under_canv_layout.addWidget(self.l_sp_number_of_plots, 1,0,1,2)
        self.under_canv_layout.addWidget(self.l_sp_current_of_plots, 1,2,1,2)


        self.under_canv_layout.addWidget(self.l_le_x_axis, 2,0)
        self.under_canv_layout.addWidget(self.l_le_y_axis, 2,1)
        self.under_canv_layout.addWidget(self.l_le_hue, 2,2)
        self.under_canv_layout.addWidget(self.checkbox, 2,3)


        # self.under_canv_layout.setVerticalSpacing(0)
        self.under_canv_layout.addWidget(self.b_plot, 3,0)
        self.under_canv_layout.addWidget(self.b_clear_plot, 3,1)
        self.under_canv_layout.addWidget(self.b_switch_axes, 3,2)
        self.under_canv_layout.addWidget(self.checkbox_reset_plots, 3,3)


        # self.b_plot.setMinimumHeight(100)

        # self.under_canv_layout.addStretch(2)

        # self.under_canv_layout.addLayout(self.lay)

        self.frame_under_canv = QFrame(self)
        self.frame_under_canv.setLayout(self.under_canv_layout)
        


        self.splitter_center = QSplitter(Qt.Vertical)
        self.splitter_center.addWidget(self.canv)
        # self.splitter_center.addL(self.under_canv_layout)


        self.splitter_center.addWidget(self.frame_under_canv)
        # self.splitter_center.setStretchFactor(900,300)
        self.splitter_center.setStretchFactor(0, 12)
        self.splitter_center.setStretchFactor(1, 3)


        self.main_layout.addWidget(self.splitter_center)


    def l_sp_number_of_plots_changed(self):
        print('l_sp_number_of_plots_changed')
        value = self.l_sp_number_of_plots.get_value()
        self.canv.update_num_of_subplots(value)


    def clear_axes(self):
        self.l_le_x_axis.set_lineedit_text('')
        self.l_le_y_axis.set_lineedit_text('')

    def get_hue(self):
        hue = self.l_le_hue.get_text()
        return hue
        
    def get_x_y_axis(self):
        x = self.l_le_x_axis.get_text()
        y = self.l_le_y_axis.get_text()
        print(x,y)
        return x,y
    
    def add_axis(self, col_ind, axis = None):
        col_name = self.table.col_labels.tolist()[col_ind]
        if axis == 'x':
            self.l_le_x_axis.update_text(col_name)
        elif axis == 'y':
            self.l_le_y_axis.update_text(col_name)
    
    def add_hue(self, col_ind):
        col_name = self.table.col_labels.tolist()[col_ind]
        self.l_le_hue.update_text(col_name)

    def switch_axes(self):
        print('sa')
        x_text = self.l_le_x_axis.get_text()
        y_text = self.l_le_y_axis.get_text()
        self.l_le_x_axis.set_lineedit_text(y_text)
        self.l_le_y_axis.set_lineedit_text(x_text)

    def which_tab_is_opened(self):
        # this function returns index and object of current opened Tab

        current_tab_index = self.tabs.currentIndex()
        current_tab_obj = self.list_of_tabs[current_tab_index]
        return current_tab_index, current_tab_obj

    def clear_plot(self):
        print('clear all plots')
        # self.canv.ax.clear()
        self.canv.clear_all_plots()

    def plot(self):
        print('Plot Widget plot')
        _, current_tab = self.which_tab_is_opened()
        print(current_tab)

        x, y = self.get_x_y_axis()
        hue = self.get_hue()

        # if self.checkbox_reset_plots.isChecked():
        #     self.clear_plot()
        # plot = current_tab.plot(self.table, x,y,hue, self.canv.ax)
        ax_ind = self.l_sp_current_of_plots.get_value()
        plot = current_tab.plot(self.table, x,y,hue, self.canv.fig.axes[ax_ind-1])
        # self.canv.ax_list.append(self.canv.fig.axes[ax_ind-1])

        self.canv.fig.tight_layout()
        self.canv.draw()


    
class PlotCanvas(FigureCanvas):

    def __init__(self, table, width=40, height=20):
        # super().__init__(table)

        self.fig = Figure(figsize=(width, height), dpi=100, facecolor='lightgrey')

        # self.ax = self.fig.add_subplot(111) # poczatkowe ustawienia
        # self.ax.grid()
        self.fig.subplots_adjust(left = 0.09, right = 0.85)  # umiejscowienie fig w FigureCanvas, robimy miejsce dla legendy
        # self.fig.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.3)
        # self.fig.tight_layout()


        # self.ax = self.fig.add_subplot(111) # poczatkowe ustawienia
        # # self.ax.grid()
        # # self.ax.axis('off')
        # self.ax_list.append(self.ax)
        # print(self.ax.lines)
        self.ax_list = []

        # self.ax2 = self.fig.add_subplot(222)
        # self.ax2.grid()

        # self.ax3= self.fig.add_subplot(223)
        # self.ax3.grid()

        # self.ax4 = self.fig.add_subplot(224)
        # self.ax4.grid()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(table)
        self.table = table

    def change(self):
        print('change')



    def update_num_of_subplots(self, number):
        print('update_num_of_subplots')
        print('number:', number)

        # if len(self.fig.axes) > 0:
        #     self.clear_plots()
        print('fig axes')
        print(self.fig.axes)
        print(len(self.fig.axes))

        print(' ax list')
        print(self.ax_list)
        print(len(self.ax_list))

        len_ax_list = len(self.ax_list)


        if number == 1:
            ax = self.fig.add_subplot(1,1,1)
            # ax.grid()

        if number == 2:
            print('number: ', number)
            for n in range(1,number+1):  # 1,2
                print(n)
                if n in range(1,len_ax_list+1):
                    print('jest plot : ', n)
                    ax = self.ax_list[n-1]
                    ax.change_geometry(1,2,n)
                else:
                    ax = self.fig.add_subplot(1,2,n)

        elif number in range(3,5):
            print('number: ', number)
            for n in range(1,number+1):  #1,2,3
                print(n)
                if n in range(1,len_ax_list+1):
                    print('jest plot : ', n)
                    ax = self.ax_list[n-1]
                    ax.change_geometry(2,2,n)

                else:
                    ax = self.fig.add_subplot(2,2,n)


        # elif number in range(5,7):
        #     # self.ax_list = []
        #     print(number)
        #     for n in range(1,number+1):
        #         if n in range(1,len_ax_list+1):
        #             print('jest plot : ', n)
        #             ax = self.ax_list[n-1]
        #             ax.change_geometry(2,3,n)
        #         else:
        #             ax = self.fig.add_subplot(2,3,n)


        # elif number == 2:
        #     # self.ax_list = []
        #     print(number)
        #     for n in range(1,number+1):  # 1,2
        #         ax = self.fig.add_subplot(1,2,n)
        #         # ax.grid()



        # elif number in range(3,5):
        #     # self.ax_list = []
        #     for n in range(1,number+1):  #1,2,3
        #         ax = self.fig.add_subplot(2,2,n)
        #         # ax.grid()


        # elif number in range(5,7):
        #     # self.ax_list = []
        #     print('num ', number)
        #     for n in range(1,number+1):
        #         ax = self.fig.add_subplot(2,3,n)

        # self.ax_list = self.fig.axes

        # line = ax.lines # get the first line, there might be more
        # print('lines, ', line)
        # print('DATA')
        # print(line.get_xydata())

        # usun co za dużo xd
        if number < len(self.ax_list):
            roznica =  len(self.ax_list) - number
            print('roznica', roznica)
            ax_to_del = self.ax_list[-roznica:]
            self.ax_list = self.ax_list[:-roznica]
            print(ax_to_del)
            for ax in ax_to_del:
                self.fig.delaxes(ax)
            # for en,ax in enumerate(self.fig.axes, start = 1):
            #     ax.change_geometry(2,2,en)
        
            print('po usunieciu')
            print(self.fig.axes)
            print(len(self.fig.axes))
            print(self.ax_list)
            print(len(self.ax_list))

            
        print('fig axes')
        print(self.fig.axes)
        print(len(self.fig.axes))

        print(' ax list')
        print(self.ax_list)
        print(len(self.ax_list))
        self.ax_list = self.fig.axes

        # FigureCanvas.__init__(self, self.fig)
        self.fig.tight_layout()
        self.draw()
        print('d')

    def clear_all_plots(self):
        print('clear plots')
        print(self.fig.axes)
        self.ax_list = []
        for ax in self.fig.axes:
            self.fig.delaxes(ax)
        # self.l_sp_number_of_plots.set_value(0) # zmien wartość na 0 

        self.draw()

        print('clear plots end')


    def plot_indexes(self, t, x, y, h):

        print('plot indexes')
        self.ax.clear()
        print(type(int(x)))

        c = self.table.col_labels.tolist()
        ys = y.split(',')
        xs = x.split(',')
        hs = h.split(',')

        print(h)
        # ..............................................
        labels = []
        if len(xs) == 1:
            if h:
                for y in ys:
                    if t == 'Line plot':
                        sns.lineplot(x=c[int(x)], y=c[int(y)],hue = c[int(h)], data=self.table.dataframe, ax=self.ax)
                    elif t == 'Bar plot':
                        sns.barplot(x = c[int(x)], y = c[int(y)],hue = c[int(h)], data = self.table.dataframe, ax = self.ax)
                    elif t =='Scatter plot':
                        sns.scatterplot(x = c[int(x)], y = c[int(y)],hue = c[int(h)], data = self.table.dataframe, ax = self.ax)
                    else:
                        None
                    labels.append(c[int(y)])


            elif not h:
                for y in ys:
                    if t == 'Line plot':
                        x2 = c[int(x)]
                        y2= c[int(y)]
                        print(x2,y2)
                        sns.lineplot(x=c[int(x)], y=c[int(y)], data=self.table.dataframe, ax=self.ax)
                    elif t == 'Bar plot':
                        sns.barplot(x = c[int(x)], y = c[int(y)], data = self.table.dataframe, ax = self.ax)
                    elif t =='Scatter plot':
                        sns.scatterplot(x = c[int(x)], y = c[int(y)], data = self.table.dataframe, ax = self.ax)
                    else:
                        None
                    labels.append(c[int(y)])

        # if len(xs) == 1:
        #     if len(ys) == 2:
        #         print('2')
        #         if t == 'Line plot':
        #             sns.lineplot(x=c[int(x)], y=c[int(ys[0])],  data=self.table.dataframe, ax=self.ax)
        #             self.ax2 = self.ax.twinx()
        #             sns.lineplot(x=c[int(x)], y=c[int(ys[1])], data=self.table.dataframe, ax=self.ax2)
        #         elif t == 'Bar plot':
        #             sns.barplot(x=c[int(x)], y=c[int(y)], data=self.table.dataframe, ax=self.ax)
        #         elif t == 'Scatter plot':
        #             sns.scatterplot(x=c[int(x)], y=c[int(y)], data=self.table.dataframe,ax=self.ax)
        #         else:
        #             None
        #         # self.ax = self.ax.twinx()



            print('labels', labels)
            self.ax.set_xlabel(c[int(x)])
            self.ax.set_ylabel(c[int(y)])
            # self.ax.legend(labels = labels)
            self.ax.legend()
            self.fig.tight_layout()
            self.draw()


    def plot_col_names(self, t, x, y, h):

        print('plot4')
        self.ax.clear()

        c = self.table.col_labels.tolist()
        ys = y.split(',')
        xs = x.split(',')
        hs = h.split(',')
        xs = [c.index(i) for i in xs]
        ys = [c.index(i) for i in ys]
        xs2 = xs[0]
        print(xs, ys)


        # ..............................................
        labels = []
        if len(xs) == 1:
            if h:
                print('h')
                for y in ys:
                    if t == 'Line plot':
                        sns.lineplot(x=c[int(xs2)], y=c[int(y)], hue = c[int(h)], data=self.table.dataframe, ax=self.ax)
                    elif t == 'Bar plot':
                        sns.barplot(x=c[int(xs2)], y=c[int(y)], data = self.table.dataframe, ax = self.ax)
                    elif t =='Scatter plot':
                        sns.scatterplot(x=c[int(xs2)], y=c[int(y)], data = self.table.dataframe, ax = self.ax)
                    else:
                        None
                    # labels.append(c[int(y)])


            elif not h:
                print('not h')
                for y in ys:
                    if t == 'Line plot':
                        print(xs2, y)
                        sns.lineplot(x=c[int(xs2)], y=c[int(y)], data=self.table.dataframe, ax=self.ax)
                    elif t == 'Bar plot':
                        sns.barplot(x=c[int(xs2)], y=c[int(y)], data = self.table.dataframe, ax = self.ax)
                    elif t =='Scatter plot':
                        sns.scatterplot(x=c[int(xs2)], y=c[int(y)], data = self.table.dataframe, ax = self.ax)
                    else:
                        None
                    # labels.append(c[int(y)])

        # if len(xs) == 1:
        #     if len(ys) == 2:
        #         print('2')
        #         if t == 'Line plot':
        #             sns.lineplot(x=c[int(x)], y=c[int(ys[0])],  data=self.table.dataframe, ax=self.ax)
        #             self.ax2 = self.ax.twinx()
        #             sns.lineplot(x=c[int(x)], y=c[int(ys[1])], data=self.table.dataframe, ax=self.ax2)
        #         elif t == 'Bar plot':
        #             sns.barplot(x=c[int(x)], y=c[int(y)], data=self.table.dataframe, ax=self.ax)
        #         elif t == 'Scatter plot':
        #             sns.scatterplot(x=c[int(x)], y=c[int(y)], data=self.table.dataframe,ax=self.ax)
        #         else:
        #             None
        #         # self.ax = self.ax.twinx()



            print(labels)
            # self.ax.set_xlabel(c[int(x)])
            # self.ax.set_ylabel(c[int(y)])
            # self.ax.legend(labels = labels)
            self.ax.legend()
            self.fig.tight_layout()
            self.draw()
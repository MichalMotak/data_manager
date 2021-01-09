from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd

class PlotCanvas(FigureCanvas):

    def __init__(self, table, width=40, height=20):
        # super().__init__(width, height)

        self.fig = Figure(figsize=(width, height), dpi=100, facecolor='lightgrey')

        self.ax = self.fig.add_subplot(111) # poczatkowe ustawienia
        self.fig.subplots_adjust(left = 0.09, right = 0.85)  # umiejscowienie fig w FigureCanvas, robimy miejsce dla legendy
        self.ax.grid()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(table)
        self.table = table



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
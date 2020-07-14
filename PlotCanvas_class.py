from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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

        # self.setParent(parent)

        # FigureCanvas.setSizePolicy(self,
        #                            QSizePolicy.Expanding,
        #                            QSizePolicy.Expanding)
        # FigureCanvas.updateGeometry(self)

        print(self.table.table_test)
        print(self.table)


    def plot(self):
        print('plot')
        print(self.table)
        print('data shape', self.table.data.shape)
        self.ax.plot(self.table.data[:12,1], self.table.data[:12,2])
        self.draw()
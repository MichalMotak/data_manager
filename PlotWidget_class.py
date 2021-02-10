from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.backends.backend_qt5agg import ToolbarQt

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import UpgradedWidgets 
from CustomDialogWidgets import *
from globals_ import matplotlib_colors_list

from sklearn import pipeline 
from sklearn import impute 
from sklearn import preprocessing
from sklearn import decomposition

class ParentPlotTab(QWidget):
    def __init__(self, name):
        super(ParentPlotTab, self).__init__()
        self.name = name

        self.create_layout()

    def create_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)
        self.setLayout(self.main_layout)

        
class TabPlotRelatonships(ParentPlotTab):


    def __init__(self, name):
        super(TabPlotRelatonships, self).__init__(name)
        self.name = name

    def create_layout(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)


        self.l_combobox_kind = UpgradedWidgets.LabelAndCombobox('plot kind', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        self.l_combobox_kind.add_items(['scatter', 'line'])

        self.l_radiobutton_markers = UpgradedWidgets.LabelAndRadioButton('Markers', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])

        self.l_combobox_err_style = UpgradedWidgets.LabelAndCombobox('err_style (line)', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        self.l_combobox_err_style.add_items(['band', 'bars'])

        self.l_sp_alpha = UpgradedWidgets.LabelAndSpinbox('alpha (scatter)', stretches=[7,3], lay_dir = 'Horizontal', minimal_size=[30,50], double_spinbox=True)
        self.l_sp_alpha.set_value(1.0)
        self.l_sp_alpha.set_step(0.05)
        self.l_sp_alpha.set_range(0.05,1.0)

        self.main_layout.addWidget(self.l_combobox_kind, 0,0)
        self.main_layout.addWidget(self.l_radiobutton_markers, 0,1)
        self.main_layout.addWidget(self.l_combobox_err_style, 1,0)
        self.main_layout.addWidget(self.l_sp_alpha, 1,1)


        self.l_combobox_kind.signal_current_text_changed(self.manage_enability_of_widgets)

        self.setLayout(self.main_layout)

    def manage_enability_of_widgets(self):

        kind = self.l_combobox_kind.get_text()

        if kind == 'line':
            self.l_sp_alpha.setEnabled(False)
            self.l_combobox_err_style.setEnabled(True)
 
        elif kind == 'scatter':
            self.l_combobox_err_style.setEnabled(False)
            self.l_sp_alpha.setEnabled(True)


    def get_parameters(self, plot_kind):

        alpha = self.l_sp_alpha.get_value()
        err_style = self.l_combobox_err_style.get_text()
        markers = self.l_radiobutton_markers.get_state()

        if plot_kind == 'line':
            pars = {"err_style": err_style, "markers" : markers}
            return pars

        elif plot_kind == 'scatter':
            pars = {"alpha": alpha, "markers" : markers}
            return pars


    def plot(self, table, x_, y_, hue_, ax_):
        print(self.name + ' plot')

        kind = self.l_combobox_kind.get_text()
        pars = self.get_parameters(kind)

        print(kind, hue_)

        if hue_ =='':
            hue_ = None

        if kind == 'line':
            plot = sns.lineplot(x=x_, y=y_, hue = hue_, style = hue_, **pars, data=table.dataframe, ax = ax_)

        elif kind == 'scatter':
            plot = sns.scatterplot(x=x_, y=y_, hue = hue_, style = hue_, **pars, data=table.dataframe, ax = ax_)

        print(plot)
        print(type(plot))

        return plot


class TabPlotDistribution(ParentPlotTab):


    def __init__(self, name):
        super(TabPlotDistribution, self).__init__(name)
        self.name = name

    def create_layout(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)

        self.l_combobox_kind = UpgradedWidgets.LabelAndCombobox('plot kind', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        self.l_combobox_kind.add_items(['hist', 'kde', 'ecdf', 'rug'])

        self.l_combobox_multiple = UpgradedWidgets.LabelAndCombobox('multiple', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        self.l_combobox_multiple.add_items(['layer', 'dodge', 'stack', 'fill'])

        self.l_combobox_stat = UpgradedWidgets.LabelAndCombobox('stat', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        self.l_combobox_stat.add_items(['count', 'frequency', 'density', 'probability'])

        self.l_combobox_element = UpgradedWidgets.LabelAndCombobox('element', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        self.l_combobox_element.add_items(['bars', 'step', 'poly'])

        self.l_rb_log_scale = UpgradedWidgets.LabelAndRadioButton('log_scale', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        self.l_rb_fill = UpgradedWidgets.LabelAndRadioButton('fill', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        self.l_rb_fill.set_state(True)

        self.l_rb_cumulative = UpgradedWidgets.LabelAndRadioButton('cumulative', stretches=[7,3], lay_dir = 'Horizontal', minimal_size=[10,50])
        self.l_rb_expand_margins = UpgradedWidgets.LabelAndRadioButton('expand_margins', stretches=[5,5], lay_dir = 'Horizontal', minimal_size=[10,50])

        self.l_sb_bw_adjust = UpgradedWidgets.LabelAndSpinbox('bw_adjust', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50], double_spinbox = True)
        self.l_sb_bw_adjust.set_value(0)                
        self.l_sb_bw_adjust.set_step(0.05)

        self.l_sb_bw_cut = UpgradedWidgets.LabelAndSpinbox('cut', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50], double_spinbox = True)
        self.l_sb_bw_cut.set_step(0.5)

        self.main_layout.addWidget(self.l_combobox_kind, 0,0)
        self.main_layout.addWidget(self.l_combobox_multiple, 0,1)
        self.main_layout.addWidget(self.l_combobox_stat, 0,2,1,2)

        self.main_layout.addWidget(self.l_combobox_element, 1,0)
        self.main_layout.addWidget(self.l_rb_log_scale, 1,1)
        self.main_layout.addWidget(self.l_rb_fill, 1,2)
        self.main_layout.addWidget(self.l_rb_cumulative, 1,3)

        self.main_layout.addWidget(self.l_rb_expand_margins, 3,2,1,2)
        self.main_layout.addWidget(self.l_sb_bw_adjust, 3,0)
        self.main_layout.addWidget(self.l_sb_bw_cut, 3,1)

        self.l_combobox_kind.signal_current_text_changed(self.update_multiple_combobox)
        self.l_combobox_kind.signal_current_text_changed(self.manage_enability_of_widgets)


    def update_multiple_combobox(self):

        kind = self.l_combobox_kind.get_text()

        if kind == 'hist':
            self.l_combobox_multiple.clear()
            self.l_combobox_multiple.add_items(['layer', 'dodge', 'stack', 'fill'])

        elif kind == 'kde':
            self.l_combobox_multiple.clear()
            self.l_combobox_multiple.add_items(['layer', 'stack', 'fill'])

    def manage_enability_of_widgets(self):

        plot_kind = self.l_combobox_kind.get_text()

        if plot_kind == 'hist':
            self.l_combobox_multiple.setEnabled(True)
            self.l_combobox_stat.setEnabled(True)
            self.l_combobox_element.setEnabled(True)
            self.l_rb_log_scale.setEnabled(True)
            self.l_rb_fill.setEnabled(True)
            self.l_rb_cumulative.setEnabled(True)

            self.l_rb_expand_margins.setEnabled(False)
            self.l_sb_bw_adjust.setEnabled(False)
            self.l_sb_bw_cut.setEnabled(False)


        elif plot_kind == 'kde':
            self.l_sb_bw_adjust.setEnabled(True)
            self.l_sb_bw_cut.setEnabled(True)
            self.l_rb_fill.setEnabled(True)
            self.l_rb_cumulative.setEnabled(True)

            self.l_combobox_multiple.setEnabled(False)
            self.l_combobox_stat.setEnabled(False)
            self.l_combobox_element.setEnabled(False)
            self.l_rb_log_scale.setEnabled(False)
            self.l_rb_expand_margins.setEnabled(False)

        elif plot_kind == 'ecdf':
            self.l_combobox_multiple.setEnabled(False)
            self.l_combobox_stat.setEnabled(False)
            self.l_combobox_element.setEnabled(False)
            self.l_rb_log_scale.setEnabled(True)
            self.l_rb_fill.setEnabled(False)
            self.l_rb_cumulative.setEnabled(False)

            self.l_rb_expand_margins.setEnabled(False)
            self.l_sb_bw_adjust.setEnabled(False)
            self.l_sb_bw_cut.setEnabled(False)


        elif plot_kind == 'rug':
            self.l_combobox_multiple.setEnabled(False)
            self.l_combobox_stat.setEnabled(False)
            self.l_combobox_element.setEnabled(False)
            self.l_rb_log_scale.setEnabled(False)
            self.l_rb_fill.setEnabled(False)
            self.l_rb_cumulative.setEnabled(False)

            self.l_rb_expand_margins.setEnabled(True)
            self.l_sb_bw_adjust.setEnabled(False)
            self.l_sb_bw_cut.setEnabled(False)


    def get_parameters(self, plot_kind):

        log_scale = self.l_rb_log_scale.get_state()
        fill = self.l_rb_fill.get_state()
        cumulative = self.l_rb_cumulative.get_state()


        if plot_kind == 'hist':
            multiple = self.l_combobox_multiple.get_text()
            stat = self.l_combobox_stat.get_text()
            element = self.l_combobox_element.get_text()

            pars = {"multiple" : multiple, "stat" : stat, "element" : element,
                    "log_scale" : log_scale, "fill" : fill, "cumulative" : cumulative }
            return pars

        elif plot_kind == 'kde':
            bw_adjust = self.l_sb_bw_adjust.get_value()
            cut = self.l_sb_bw_cut.get_value()

            pars = {"bw_adjust" : bw_adjust, "cut" : cut, "log_scale" : log_scale, 
            "fill" : fill, "cumulative" : cumulative }
            return pars

        elif plot_kind == 'ecdf':
            pars = {"log_scale": log_scale}
            return pars

        elif plot_kind == 'rug':
            expand_margins = self.l_rb_expand_margins.get_state()

            pars = {"expand_margins" : expand_margins}
            return pars

    def plot(self, table, x_, y_, hue_, ax_):
        print(self.name + ' plot')

        kind = self.l_combobox_kind.get_text()
        pars = self.get_parameters(kind)



        if hue_ =='':
            hue_ = None

        if kind == 'hist':
            plot = sns.histplot(x=x_, hue=hue_, **pars, data=table.dataframe, ax = ax_)

        elif kind == 'kde':
            plot = sns.kdeplot(x=x_, hue=hue_, **pars,  data=table.dataframe,  ax = ax_)

        elif kind == 'ecdf':
            plot = sns.ecdfplot(x=x_, hue=hue_, **pars,  data=table.dataframe, ax = ax_)

        elif kind == 'rug':
            plot = sns.rugplot(x=x_, hue=hue_, **pars,  data=table.dataframe,  ax = ax_)

        print(plot)
        print(type(plot))

        return plot


class TabPlotCategoricalScatterplots(ParentPlotTab):

    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)

        self.l_combobox_kind = UpgradedWidgets.LabelAndCombobox('plot kind', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])
        l = ["strip", "swarm"]
        self.l_combobox_kind.add_items(l)

        self.l_sp_size = UpgradedWidgets.LabelAndSpinbox('markers size', stretches=[7,3], lay_dir = 'Horizontal', minimal_size=[30,50])
        self.l_sp_size.set_value(5)

        self.l_le_edgecolor = UpgradedWidgets.LabelAndLineedit('edgecolor', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])
        self.l_le_edgecolor.set_lineedit_text('gray')

        self.l_sp_linewidth = UpgradedWidgets.LabelAndSpinbox('linewidth', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50], double_spinbox=True)
        self.l_sp_linewidth.set_value(0)
        self.l_sp_linewidth.set_step(0.1)

        self.l_sp_jitter = UpgradedWidgets.LabelAndSpinbox('jitter', stretches=[7,3], lay_dir = 'Horizontal', minimal_size=[30,50], double_spinbox=True)
        self.l_sp_jitter.set_value(0.1)
        self.l_sp_jitter.set_step(0.05)

        self.l_radiobutton_dodge = UpgradedWidgets.LabelAndRadioButton('dodge', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[30,50])


        self.main_layout.addWidget(self.l_combobox_kind, 0,0)
        self.main_layout.addWidget(self.l_sp_size, 0,1)
        self.main_layout.addWidget(self.l_le_edgecolor, 0,2)
        self.main_layout.addWidget(self.l_sp_linewidth, 1,0)
        self.main_layout.addWidget(self.l_sp_jitter, 1,1)
        self.main_layout.addWidget(self.l_radiobutton_dodge, 1,2)

        self.l_combobox_kind.signal_current_text_changed(self.manage_enability_of_widgets)

        self.setLayout(self.main_layout)

    def manage_enability_of_widgets(self):

        kind = self.l_combobox_kind.get_text()

        if kind == 'swarm':
            self.l_sp_jitter.setEnabled(False)
        else:
            self.l_sp_jitter.setEnabled(True)


    def get_parameters(self, plot_kind):
        markers_size = self.l_sp_size.get_value()
        edgecolor = self.l_le_edgecolor.get_text()
        linewidth = self.l_sp_linewidth.get_value()
        dodge = self.l_radiobutton_dodge.get_state()

        if edgecolor not in matplotlib_colors_list:
            d = CustomMessageBoxWarning('wrong color')
            edgecolor = 'gray'

        pars_common = {'edgecolor': edgecolor, 'linewidth' : linewidth, 'size': markers_size,'dodge': dodge}

        if plot_kind == 'strip':
            jitter = self.l_sp_jitter.get_value()
            pars_new = {'jitter' : jitter}

            pars = {**pars_common, **pars_new}
            return pars

        elif plot_kind == 'swarm':
            return pars_common


    def plot(self, table, x_, y_, hue_, ax_):
        print(self.name + ' plot')

        kind = self.l_combobox_kind.get_text()
        print(kind, hue_)

        if hue_ =='':
            hue_ = None
        

        pars = self.get_parameters(kind)

        if kind == 'strip':
            plot = sns.stripplot(x=x_, y=y_, hue = hue_,  **pars,
                data=table.dataframe, ax = ax_)

        elif kind == 'swarm':
            plot = sns.swarmplot(x=x_, y=y_, hue = hue_,  **pars,
                data=table.dataframe, ax = ax_)

        print(plot)
        print(type(plot))


        return plot




class TabPlotCategoricalDistribution(ParentPlotTab):

    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)

        self.l_combobox_kind = UpgradedWidgets.LabelAndCombobox('plot kind', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[20,50])
        l = ["box", "violin", "boxen"]
        self.l_combobox_kind.add_items(l)

        # boxplot
        self.l_sp_whis = UpgradedWidgets.LabelAndSpinbox('whis', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[20,50], double_spinbox=True)
        self.l_sp_whis.set_value(1.5)
        self.l_sp_whis.set_step(0.10)
        
        self.l_sp_width = UpgradedWidgets.LabelAndSpinbox('width', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[20,50], double_spinbox=True)
        self.l_sp_width.set_value(0.8)
        self.l_sp_width.set_step(0.05)

        self.l_sp_fliersize = UpgradedWidgets.LabelAndSpinbox('fliersize', stretches=[7,3], lay_dir = 'Horizontal', minimal_size=[20,50], double_spinbox=True)
        self.l_sp_fliersize.set_value(5)
        self.l_sp_fliersize.set_step(0.5)


        # violinplot
        self.l_combobox_inner = UpgradedWidgets.LabelAndCombobox('inner', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[20,50])
        l = ["box", "quartile", "point", "stick"]
        self.l_combobox_inner.add_items(l)

        self.l_rb_split = UpgradedWidgets.LabelAndRadioButton('split', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[20,50])

        self.l_sp_cut = UpgradedWidgets.LabelAndSpinbox('cut', stretches=[7,3], lay_dir = 'Horizontal', minimal_size=[20,50])
        self.l_sp_cut.set_value(2)
        self.l_sp_cut.set_step(1)

        # boxenplot


        # wszystkie
        self.l_rb_dodge = UpgradedWidgets.LabelAndRadioButton('dodge', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[20,50])

        self.l_sp_linewidth = UpgradedWidgets.LabelAndSpinbox('linewidth', stretches=[6,4], lay_dir = 'Horizontal', minimal_size=[20,50], double_spinbox=True)
        self.l_sp_linewidth.set_value(1)
        self.l_sp_linewidth.set_step(0.2)

        self.l_sp_saturation = UpgradedWidgets.LabelAndSpinbox('saturation', stretches=[6,4], lay_dir = 'Horizontal', minimal_size=[20,50], double_spinbox=True)
        self.l_sp_saturation.set_value(1)
        self.l_sp_saturation.set_step(0.05)
        self.l_sp_saturation.set_range(0, 1.0)


        self.main_layout.addWidget(self.l_combobox_kind, 0,0)
        self.main_layout.addWidget(self.l_rb_dodge, 0,1)
        self.main_layout.addWidget(self.l_sp_linewidth, 0,2)
        self.main_layout.addWidget(self.l_sp_saturation, 0,3)

        self.main_layout.addWidget(self.l_sp_whis, 1,1)
        self.main_layout.addWidget(self.l_sp_width, 1,2)
        self.main_layout.addWidget(self.l_sp_fliersize, 1,3)

        self.main_layout.addWidget(self.l_combobox_inner, 2,1)
        self.main_layout.addWidget(self.l_rb_split, 2,2)
        self.main_layout.addWidget(self.l_sp_cut, 2,3)


        self.l_combobox_kind.signal_current_text_changed(self.manage_enability_of_widgets)

        self.setLayout(self.main_layout)

    def manage_enability_of_widgets(self):

        plot_kind = self.l_combobox_kind.get_text()

        self.l_combobox_inner.setEnabled(True)
        self.l_rb_split.setEnabled(True)
        self.l_sp_cut.setEnabled(True)
        self.l_sp_whis.setEnabled(True)
        self.l_sp_width.setEnabled(True)
        self.l_sp_fliersize.setEnabled(True)


        if plot_kind == 'box':
            self.l_combobox_inner.setEnabled(False)
            self.l_rb_split.setEnabled(False)
            self.l_sp_cut.setEnabled(False)

        elif plot_kind == 'violin':
            self.l_sp_whis.setEnabled(False)
            self.l_sp_width.setEnabled(False)
            self.l_sp_fliersize.setEnabled(False)


        elif plot_kind == 'boxen':
            self.l_combobox_inner.setEnabled(False)
            self.l_rb_split.setEnabled(False)
            self.l_sp_cut.setEnabled(False)
            self.l_sp_whis.setEnabled(False)
            self.l_sp_width.setEnabled(False)
            self.l_sp_fliersize.setEnabled(False)


    def get_parameters(self, plot_kind):

        dodge = self.l_rb_dodge.get_state()
        linewidth = self.l_sp_linewidth.get_value()
        saturation = self.l_sp_saturation.get_value()

        pars_common = {'dodge': dodge, 'linewidth' :linewidth, 'saturation':saturation}

        if plot_kind == 'box':
            whis = self.l_sp_whis.get_value()
            width = self.l_sp_width.get_value()
            fliersize = self.l_sp_fliersize.get_value()

            pars_new = {'whis': whis, 'width' : width, 'fliersize' : fliersize}
            pars = {**pars_common, **pars_new}

            return pars

        elif plot_kind == 'violin':
            inner = self.l_combobox_inner.get_text()
            split = self.l_rb_split.get_state()
            cut = self.l_sp_cut.get_value()

            pars_new = {'inner': inner, 'split' : split, 'cut' : cut}
            pars = {**pars_common, **pars_new}

            return pars

        elif plot_kind == 'boxen':
            return pars_common


    def plot(self, table, x_, y_, hue_, ax_):
        print(self.name + ' plot')

        plot_kind = self.l_combobox_kind.get_text()
        print(plot_kind, hue_)

        if hue_ =='':
            hue_ = None
        
        parameters = self.get_parameters(plot_kind)
        print('parameters ', parameters)


        if plot_kind == 'box':
            plot = sns.boxplot(x=x_, y=y_, hue = hue_, **parameters, data=table.dataframe, ax = ax_)

        elif plot_kind == 'violin':
            plot = sns.violinplot(x=x_, y=y_, hue = hue_, **parameters, data=table.dataframe, ax = ax_)

        elif plot_kind == 'boxen':
            plot = sns.boxenplot(x=x_, y=y_, hue = hue_, **parameters, data=table.dataframe, ax = ax_)

        print(plot)
        print(type(plot))


        return plot


class TabPlotCategoricalEstimate(ParentPlotTab):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)

        self.l_combobox_kind = UpgradedWidgets.LabelAndCombobox('plot kind', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        l = ["point", "bar", "count"]
        self.l_combobox_kind.add_items(l)

        self.l_sp_capsize = UpgradedWidgets.LabelAndSpinbox('capsize', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50], double_spinbox=True)
        self.l_sp_capsize.set_value(1.0)
        self.l_sp_capsize.set_step(0.05)
        self.l_sp_capsize.set_range(0.05,5)


        self.l_sp_errwidth = UpgradedWidgets.LabelAndSpinbox('error width', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50], double_spinbox=True)
        self.l_sp_errwidth.set_value(1.0)
        self.l_sp_errwidth.set_step(0.1)
        self.l_sp_errwidth.set_range(0.1, 10)

        self.l_sp_saturation = UpgradedWidgets.LabelAndSpinbox('saturation ', stretches=[7,3], lay_dir = 'Horizontal', minimal_size=[10,50], double_spinbox=True)
        self.l_sp_saturation.set_value(1.0)
        self.l_sp_saturation.set_step(0.05)
        self.l_sp_saturation.set_range(0.05, 1.0)

        self.main_layout.addWidget(self.l_combobox_kind, 0,0)
        self.main_layout.addWidget(self.l_sp_capsize, 0,1)
        self.main_layout.addWidget(self.l_sp_errwidth, 1,0)
        self.main_layout.addWidget(self.l_sp_saturation, 1,1)


        self.l_combobox_kind.signal_current_text_changed(self.manage_enability_of_widgets)

        self.setLayout(self.main_layout)

    def manage_enability_of_widgets(self):
        kind = self.l_combobox_kind.get_text()
        if kind == 'point':
            self.l_sp_saturation.setEnabled(False)
        else:
            self.l_sp_saturation.setEnabled(True)

    def get_parameters(self, plot_kind):
        capsize = self.l_sp_capsize.get_value()
        errwidth = self.l_sp_errwidth.get_value()
        saturation = self.l_sp_saturation.get_value()

        if plot_kind == 'point':
            pars = {"capsize": capsize, "errwidth" : errwidth}
            return pars

        elif plot_kind == 'bar':
            pars = {"capsize": capsize, "errwidth" : errwidth, "saturation" : saturation}
            return pars

        elif plot_kind == 'count':
            pars = {"saturation" : saturation}
            return pars

    def plot(self, table, x_, y_, hue_, ax_):
        print(self.name + ' plot')

        kind = self.l_combobox_kind.get_text()
        print(kind, hue_)

        if hue_ =='':
            hue_ = None

        pars = self.get_parameters(kind)

        if kind == 'point':
            plot = sns.pointplot(x=x_, y=y_, hue = hue_, **pars,
            data=table.dataframe, ax = ax_)

        elif kind == 'bar':
            plot = sns.barplot(x=x_, y=y_, hue = hue_, **pars, data=table.dataframe, ax = ax_)

        elif kind == 'count':
            plot = sns.countplot(x=x_, hue = hue_, **pars,
            data=table.dataframe, ax = ax_)

        print(plot)
        print(type(plot))

        return plot


class TabPlotDimentionReduction(ParentPlotTab):

    def __init__(self, name):
        super(TabPlotDimentionReduction, self).__init__(name)
        self.name = name

    def create_layout(self):
        self.main_layout = QGridLayout(self)

        self.b_create_PCA_plot = QPushButton()
        self.b_create_PCA_plot.setText('create PCA plot')

        self.l_combobox_PCA_labels = UpgradedWidgets.LabelAndCombobox('Predict label for PCA plot')

        self.l_rb_cumsum = UpgradedWidgets.LabelAndRadioButton('Cumsum')

        self.main_layout.addWidget(self.b_create_PCA_plot)
        self.main_layout.addWidget(self.l_combobox_PCA_labels)
        self.main_layout.addWidget(self.l_rb_cumsum)


        self.main_layout.setContentsMargins(5,5,5,5)

    def get_explained_variance(self, pca, cumsum_bool = False):
        exp_var = pca.explained_variance_ratio_

        if cumsum_bool:
            return np.cumsum(exp_var)
        else:
            return exp_var
    
    def get_explained_variance_plot_labels(self, cumsum_bool):

        xlabel = 'Number of components' 
        if cumsum_bool:
            ylabel = 'Cumulative explained variance'
        else:
            ylabel = 'explained variance'

        return xlabel, ylabel

    def plot(self, table, x_, y_, hue_, ax_):

        imputer = impute.SimpleImputer()
        scaler = preprocessing.StandardScaler()

        pca = decomposition.PCA()
        pipe = pipeline.Pipeline( [('imputer', imputer), ('scaler', scaler), ('PCA', pca)] )
        print(pipe)
        Y_index = self.l_combobox_PCA_labels.get_text()

        X_data = table.dataframe.drop(Y_index, 1)
        Y_data = table.dataframe[Y_index]
        print(X_data.shape, Y_data.shape)
        pipe_fitted = pipe.fit(X_data)

        cumsum_bool = self.l_rb_cumsum.get_state()
        exp_var = self.get_explained_variance(pca, cumsum_bool)
        xlabel, ylabel = self.get_explained_variance_plot_labels(cumsum_bool)

        print(exp_var)

        print('plot ', self.name)

        plot = sns.barplot(np.arange(1,len(exp_var)+1), exp_var, ax =ax_)
        for p in plot.patches:
            plot.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
        ax_.set_xlabel(xlabel) 
        ax_.set_ylabel(ylabel)

        return plot

    def update_combobox(self, list_):
        self.l_combobox_PCA_labels.clear()
        self.l_combobox_PCA_labels.add_items(list_)


class TabPlot2(ParentPlotTab):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def create_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5,5,5,5)

        self.label_pt = QLabel(self)
        self.label_pt.setText('Plot type')
        self.l_combobox_kind = UpgradedWidgets.LabelAndCombobox('plot kind', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])
        l = ["strip", "swarm", "box", "violin", "boxen", "point", "bar", "count"]
        self.l_combobox_kind.add_items(l)

        self.l_combobox_col = UpgradedWidgets.LabelAndCombobox('col argument', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[10,50])


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
            # plot = sns.stripplot(x=x_, y=y_, hue = hue_, data=table.dataframe, ax = ax_)
            # plot = sns.catplot(x=x_, y=y_, hue = hue_, kind = 'strip',data=table.dataframe)
            sns.histplot(x=x_, data=table.dataframe)
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
        self.navbar = NavigationToolbar(self.canv, self) 

        # print(self.navbar.toolitems)
        # print(self.navbar.parent)
        # print(self.navbar.canvas)
        # toolbar = self.navbar.findChild(QToolBar)
        anotherWidget=QLineEdit()
        # add the new widget to the existing navigation toolbar
        self.navbar.addWidget(anotherWidget)

        self.under_canv_layout = QGridLayout()

        self.tabs = QTabWidget(self)
        self.tab1 = TabPlotRelatonships("Relationships")
        self.tab2 = TabPlotDistribution("Distribution")
        self.tab3 = TabPlotCategoricalScatterplots('Categorical_Scatterplots')
        self.tab4 = TabPlotCategoricalDistribution("Categorical_Distribution")
        self.tab5 = TabPlotCategoricalEstimate("Categorical_Estimate")
        self.tab6 = TabPlotDimentionReduction("Dimention Reduction")


        self.tabs.addTab(self.tab1, self.tab1.name)
        self.tabs.addTab(self.tab2, self.tab2.name)
        self.tabs.addTab(self.tab3, self.tab3.name)
        self.tabs.addTab(self.tab4, self.tab4.name)
        self.tabs.addTab(self.tab5, self.tab5.name)
        self.tabs.addTab(self.tab6, self.tab6.name)


        self.list_of_tabs = [self.tab1, self.tab2, self.tab3, self.tab4, self.tab5, self.tab6]

        self.l_sp_number_of_plots = UpgradedWidgets.LabelAndSpinbox('Number of plots',stretches=[6,4], lay_dir = 'Horizontal', minimal_size=[25,50])
        self.l_sp_number_of_plots.set_range(0,6)
        self.l_sp_number_of_plots.sp.valueChanged.connect(self.l_sp_number_of_plots_changed)

        self.l_sp_current_of_plots = UpgradedWidgets.LabelAndSpinbox('current plot',stretches=[5,5], lay_dir = 'Horizontal', minimal_size=[25,50])
        self.l_sp_current_of_plots.set_range(0,6)

        self.l_le_x_axis = UpgradedWidgets.LabelAndLineedit('X Label', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[25,50])
        self.l_le_y_axis = UpgradedWidgets.LabelAndLineedit('Y Label', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[25,50])
        self.l_le_hue = UpgradedWidgets.LabelAndLineedit('Hue', stretches=[3,7], lay_dir = 'Horizontal', minimal_size=[25,50])

        self.b_plot = QPushButton('plot')
        self.b_plot.clicked.connect(self.plot)

        self.b_clear_all_plots = QPushButton('delete all plots')
        self.b_clear_all_plots.clicked.connect(self.clear_all_plots)

        self.b_clear_plot = QPushButton('clear current plot')
        self.b_clear_plot.clicked.connect(self.clear_current_plot)

        self.b_switch_axes = QPushButton('switch axes')
        self.b_switch_axes.clicked.connect(self.switch_axes)


        self.checkbox = QCheckBox("col_names/indexes ", self)
        self.checkbox_reset_plots = QCheckBox("reset plots", self)
        self.checkbox_reset_plots.setChecked(True)
        self.checkbox_reset_plots.setToolTip('activated plot will be overwritten')

        self.under_canv_layout.addWidget(self.tabs, 0, 0, 1, 4)

        self.under_canv_layout.addWidget(self.l_sp_number_of_plots, 1,0)
        self.under_canv_layout.addWidget(self.l_sp_current_of_plots, 1,1)
        self.under_canv_layout.addWidget(self.checkbox_reset_plots, 1,3)

        self.under_canv_layout.addWidget(self.l_le_x_axis, 2,0)
        self.under_canv_layout.addWidget(self.l_le_y_axis, 2,1)
        self.under_canv_layout.addWidget(self.l_le_hue, 2,2)
        self.under_canv_layout.addWidget(self.b_switch_axes, 2,3)

        self.under_canv_layout.addWidget(self.b_plot, 3,0)
        self.under_canv_layout.addWidget(self.b_clear_all_plots, 3,1)
        self.under_canv_layout.addWidget(self.b_clear_plot, 3,2)
        self.under_canv_layout.addWidget(self.checkbox, 3,3)


        self.frame_under_canv = QFrame(self)
        self.frame_under_canv.setLayout(self.under_canv_layout)
        


        self.splitter_center = QSplitter(Qt.Vertical)

        self.frame_canv= QFrame()
        self.layout_canv = QVBoxLayout()
        self.layout_canv.addWidget(self.navbar)
        self.layout_canv.addWidget(self.canv)
        self.frame_canv.setLayout(self.layout_canv)


        self.splitter_center.addWidget(self.frame_canv)
        self.splitter_center.addWidget(self.frame_under_canv)
        self.splitter_center.setStretchFactor(0, 12)
        self.splitter_center.setStretchFactor(1, 1)

        index = self.splitter_center.indexOf(self.frame_under_canv)
        self.splitter_center.setCollapsible(index, False)

        self.canv.signal_for_upgrade_widget_spinbox.connect(self.l_sp_number_of_plots.get_signal_for_plot_widget)

        self.main_layout.addWidget(self.splitter_center)

    def update_table(self, table):
        self.table = table

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
        print('switch axes')
        x_text = self.l_le_x_axis.get_text()
        y_text = self.l_le_y_axis.get_text()
        self.l_le_x_axis.set_lineedit_text(y_text)
        self.l_le_y_axis.set_lineedit_text(x_text)

    def which_tab_is_opened(self):
        # this function returns index and object of current opened Tab

        current_tab_index = self.tabs.currentIndex()
        current_tab_obj = self.list_of_tabs[current_tab_index]
        return current_tab_index, current_tab_obj

    def clear_all_plots(self):
        print('clear all plots')
        self.canv.clear_all_plots()

    def clear_current_plot(self):
        index = self.l_sp_current_of_plots.get_value()
        self.canv.clear_current_plot(index)

    def reset_current_plot_value(self):
        self.l_sp_number_of_plots.set_value(0)

    def plot(self):
        print('Plot Widget plot')
        _, current_tab = self.which_tab_is_opened()
        print(current_tab)
        print(current_tab.name)
        print(self.table.col_labels)

        # x, y = self.get_x_y_axis()
        # if x not in self.table.col_labels:
        #     d = CustomMessageBoxWarning('Wrong X label')
        #     return 0
        # elif y not in self.table.col_labels:
        #     d = CustomMessageBoxWarning('Wrong Y label')
        #     return 0
        
        # hue = self.get_hue()
        # if hue not in self.table.col_labels:
        #     d = CustomMessageBoxWarning('Wrong Hue label')
        #     return 0

        ax_ind = self.l_sp_current_of_plots.get_value()
        reset_plots = self.checkbox_reset_plots.isChecked()
        print('reset ', reset_plots)

        if ax_ind <= self.l_sp_number_of_plots.get_value():

            try:
                if reset_plots:
                    self.canv.clear_current_plot(ax_ind)


                x, y = self.get_x_y_axis()
                hue = self.get_hue()

                if current_tab.name != 'Distribution':

                    if x not in self.table.col_labels:
                        d = CustomMessageBoxWarning('Wrong X label')
                        return 0
                    elif y not in self.table.col_labels:
                        d = CustomMessageBoxWarning('Wrong Y label')
                        return 0
                elif current_tab.name == 'Distribution':
                    if x not in self.table.col_labels:
                        d = CustomMessageBoxWarning('Wrong X label')
                        return 0
                
                # hue = self.get_hue()
                # if hue not in self.table.col_labels:
                #     d = CustomMessageBoxWarning('Wrong Hue label')
                #     return 0

                
                plot = current_tab.plot(self.table, x,y, hue, self.canv.fig.axes[ax_ind-1])
      
                self.canv.fig.tight_layout()
                self.canv.draw()
            except IndexError:
                pass
                # d = Custom_Message_Box_Warning('plots not found')
        else:
            d = CustomMessageBoxWarning(f'plot number {ax_ind} is\'nt activated')

    def plot_PCA(self, list_):
        print('plot pca')

        ax_ind = self.l_sp_current_of_plots.get_value()
        reset_plots = self.checkbox_reset_plots.isChecked()
        print('reset ', reset_plots)

        if ax_ind <= self.l_sp_number_of_plots.get_value():

            try:
                if reset_plots:
                    self.canv.clear_current_plot(ax_ind)
                plot = sns.barplot(np.arange(1,len(list_)+1), list_, ax =self.canv.fig.axes[ax_ind-1])
                print('plot type ', type(plot))

                self.canv.fig.tight_layout()
                self.canv.draw()

            except IndexError:
                pass

        else:
            d = CustomMessageBoxWarning(f'plot number {ax_ind} is\'nt activated')



    @pyqtSlot(list)
    def get_signal_from_preprocessing_widget(self, list_):
        print('signal_from_preprocessing_widget', list_)
        # self.signal_for_ml_widget.emit(x)
        # self.plot_PCA(list_)
        self.raise_()

    @pyqtSlot(list)
    def get_signal_from_table_widget(self, list_):
        """ Receive list of columns labels from TableWidget. Update Dimension Reduction with list.

        Args:
            list_ (list): list of columns labels 
        """
        print("signal_from table widget ")
        self.tab6.update_combobox(list_)
        self.raise_()


    
class PlotCanvas(FigureCanvas):
    signal_for_upgrade_widget_spinbox = pyqtSignal(int)

    def __init__(self, table, width=40, height=20):
        # super().__init__(table)

        self.fig = Figure(figsize=(width, height), dpi=100, facecolor='none')
        plt.style.use('dark_background')
        self.ax_list = []

        FigureCanvas.__init__(self, self.fig)
        self.setParent(table)
        self.table = table


    def update_num_of_subplots(self, number):
        print('update_num_of_subplots')
        print('number:', number)

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

        elif number in range(5,7):
            print('number: ', number)
            for n in range(1,number+1):
                print(n)
                if n in range(1,len_ax_list+1):
                    print('jest plot : ', n)
                    ax = self.ax_list[n-1]
                    ax.change_geometry(2,3,n)
                else:
                    ax = self.fig.add_subplot(2,3,n)

        if number < len(self.ax_list):
            roznica =  len(self.ax_list) - number
            print('roznica', roznica)
            ax_to_del = self.ax_list[-roznica:]
            self.ax_list = self.ax_list[:-roznica]
            print(ax_to_del)
            for ax in ax_to_del:
                self.fig.delaxes(ax)

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
        self.grid_for_all_plots()
        self.fig.tight_layout()
        self.draw()
        print('d')


    def grid_for_all_plots(self):
        print('grid')
        for ax in self.fig.axes:
            ax.grid(True, which = 'both')

    def clear_all_plots(self):
        print('clear plots')
        print(self.fig.axes)
        self.ax_list = []
        for ax in self.fig.axes:
            self.fig.delaxes(ax)
        # self.l_sp_number_of_plots.set_value(0) # zmien wartość na 0 

        self.emit_signal_reset_current_plot_value(0)

        self.draw()

        print('clear plots end')
    
    def clear_current_plot(self, index):
        print('ccp')
        print(index)
        # if len(self.fig.self.axes) != 0:
        try:
            ax_to_clear = self.fig.axes[index-1]
            ax_to_clear.clear()
            ax_to_clear.grid(True)
            self.draw()

        except IndexError:
            d = CustomMessageBoxWarning(text='plots not found')


    @pyqtSlot()
    def emit_signal_reset_current_plot_value(self, value):
        print('emit ', value)
        self.signal_for_upgrade_widget_spinbox.emit(value)
        print('emmited')



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
# Data Manager
Data Manager is an desktop application for data analysis, data visualization and creation of machine learning pipelines.


# Libraries used in project
- PyQt5
- Scikit-learn
- Pandas
- MySQL
- Matplotlib
- Seaborn

# Project is based on Widgets
- **MainWindow** - Main window of application, contains all Widgets, allows layout management where its possible to hide certain widgets or using sliders adjust their sizes according to user needs.

- **TableWidget** - Table containing data in Pandas.DataFrame format. Additional menu under right click 				 enables manipulation of DataFrame (sorting, adding rows/columns, clearing or deleting cells/rows/columns etc.). Data can be loaded from files or database.

- **SubwindowDatabase** - Subwindow with login to local MySQL database, accepts commands and executes them, then updates TableWidget with new data.

- **PlotWidget** - PlotCanvas for data visualization with NavigationToolbar. Menu below canvas allows choosing type of plot in TabWidget (types from Seaborn - relationships, Caterogical scatterplots, distribution, estimate etc.) also controlling parameters of plots.

- **PreprocessingWidget** - Widget for creating machine learning pipeline, contains categorical data one hot encoding, Scaling, PCA (Principal Component Analysis).

- **MLWidget** - Widget for executing created ML pipelines. TabWidget contains classification and regression algorithms with control of their parameters. Allows for choosing metrics, type of validation (CrossValidation, KFold)

- **ResultsTableWidget** - storage results from ML Widget in Table similar to TableWidget. Results can be saved in .csv file. Widget enables comparing various pipelines with different methods etc. 


# Screenshots 


- **Screen 1** - Application presentation
![alt text](https://github.com/MichalMotak/data_manager/blob/master/Readme_images/screen1.png?raw=true)
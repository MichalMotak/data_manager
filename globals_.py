
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score, mean_absolute_error, mean_squared_error, r2_score, max_error 

class_metrics_list = ['accuracy', 'recall', 'precision', 'f1', 'roc_auc']
class_metrics_list_functions = [accuracy_score, recall_score, precision_score, f1_score, roc_auc_score]




reg_metrics_list = ['neg_mean_absolute_error', 'neg_mean_squared_error', 'r2', 'max_error']
reg_metrics_list_functions = [mean_absolute_error, mean_squared_error, r2_score, max_error ]
# Decison Tree Regressor

decision_tree_reg_criterion_list = ["mse", "friedman_mse", "mae", "poisson"]

# Linear Regression models

linear_reg_models = ['LinearRegression', 'Ridge', 'Lasso', 'ElasticNet']


# Matplotlib colors

import matplotlib.colors as mcolors
base_colors_list = list(mcolors.BASE_COLORS)
tableau_colors_list = list(mcolors.TABLEAU_COLORS)
css4_colors_list = list(mcolors.CSS4_COLORS)
matplotlib_colors_list = base_colors_list + tableau_colors_list + css4_colors_list



# Normalize function
def normalize_column(series):
    """
    Normalize a pandas Series to the range [0, 1].

    Parameters:
    series (pandas Series): The column to normalize.

    Returns:
    pandas Series: The normalized column.
    """
    normalized_series = (series - series.min()) / (series.max() - series.min())
    return normalized_series



# correlations and distributions

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def corrdot(*args, **kwargs):
    """
    Create a visual representation of the Pearson correlation coefficient.

    This function calculates the Pearson correlation coefficient (r) between two variables
    and represents it using a color-coded dot whose size and color intensity reflect the 
    correlation strength. The correlation value is also displayed as text.

    Parameters:
    *args: 
        args[0] (pd.Series): First variable for correlation analysis.
        args[1] (pd.Series): Second variable for correlation analysis.
    **kwargs: Additional keyword arguments for compatibility with Seaborn's PairGrid.

    Returns:
    None: The function directly modifies the current matplotlib Axes.

    Notes:
    - The size of the dot is proportional to the absolute correlation value.
    - The color is determined by a "coolwarm" colormap, ranging from -1 to 1.
    - The correlation value is displayed inside the dot with a dynamic font size.
    """
    corr_r = args[0].corr(args[1], 'pearson')
    corr_text = f"{corr_r:2.2f}".replace("0.", ".")
    ax = plt.gca()
    ax.set_axis_off()
    marker_size = abs(corr_r) * 10000
    ax.scatter([.5], [.5], marker_size, [corr_r], alpha=0.6, cmap="coolwarm",
               vmin=-1, vmax=1, transform=ax.transAxes)
    font_size = abs(corr_r) * 40 + 5
    ax.annotate(corr_text, [.5, .5], xycoords="axes fraction",
                ha='center', va='center', fontsize=font_size)


def corrfunc(x, y, **kws):
    """
    Annotate a plot with the significance level of the Pearson correlation between two variables.

    This function calculates the Pearson correlation coefficient (r) and the corresponding 
    p-value (p) for the given data arrays. It then determines statistical significance 
    using asterisks:
      - *  (p ≤ 0.05)
      - ** (p ≤ 0.01)
      - *** (p ≤ 0.001)
    
    The significance level is displayed as an annotation on the current plot.

    Parameters:
    x (array-like): First variable for correlation analysis.
    y (array-like): Second variable for correlation analysis.
    **kws: Additional keyword arguments for compatibility with Seaborn's PairGrid.

    Returns:
    None: The function directly annotates the active matplotlib Axes.
    """
    r, p = stats.pearsonr(x, y)
    p_stars = ''
    if p <= 0.05:
        p_stars = '*'
    if p <= 0.01:
        p_stars = '**'
    if p <= 0.001:
        p_stars = '***'
    ax = plt.gca()
    ax.annotate(p_stars, xy=(0.75, 0.7), xycoords=ax.transAxes)


def corr_dist_grid(correlation_data):
    """ 
    Create a grid of plots for visualizing correlation data. 
    This function sets up a seaborn PairGrid for the provided correlation data, with customized 
    plots in the upper, lower, and diagonal sections of the grid. 
    
    Parameters: 
    correlation_data (pd.DataFrame): DataFrame containing the variables for correlation plotting. 
    
    Returns: 
    sns.PairGrid: Seaborn PairGrid object with the customized plots. 
    
    Example: 
    >>> corr_dist_grid(df) 
    """ 
    sns.set_theme(style='white', font_scale=1.6)

    grid = sns.PairGrid(correlation_data, aspect=1.4, diag_sharey=False)
    grid.map_lower(sns.regplot, lowess=True, ci=False, line_kws={'color': 'black'})
    grid.map_diag(sns.histplot, kde=True, color='black')
    grid.map_upper(corrdot)
    grid.map_upper(corrfunc)

    return grid


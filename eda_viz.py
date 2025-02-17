import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math
from scipy import stats


def plot_distributions(df_num):
    """
    Generates boxplots and histograms with KDE for all numerical features in the given DataFrame.
    
    Parameters:
    df_num (pd.DataFrame): A DataFrame containing only numerical columns.
    
    Returns:
    None: Displays the plots.
    """
    for col in df_num.columns:
        fig, (ax_box, ax_hist) = plt.subplots(2, sharex=True, figsize=(6, 3), 
                                              gridspec_kw={"height_ratios": (.15, .85)})

        # Calculate skewness
        skewness = df_num[col].skew()

        # Boxplot
        sns.boxplot(x=df_num[col], ax=ax_box)
        ax_box.set(yticks=[], xlabel=None)  # Remove y-ticks and x-label for boxplot

        # Histogram with KDE
        sns.histplot(x=df_num[col], bins=12, kde=True, stat='density', ax=ax_hist)

        # Remove spines for a cleaner look
        sns.despine(ax=ax_hist)
        sns.despine(ax=ax_box, left=True)

        # Set title for each feature
        ax_hist.set_title(f"Distribution of {col}", fontsize=12, fontweight="bold")

        # Annotate skewness on the histogram
        ax_hist.text(0.95, 0.9, f"Skewness: {skewness:.2f}", 
                     transform=ax_hist.transAxes, fontsize=10, 
                     verticalalignment='top', horizontalalignment='right', 
                     bbox=dict(facecolor='white', alpha=0.6, edgecolor='white'))

        # Adjust layout and show figure
        plt.tight_layout()
        plt.show()
    
#----------------------------------------------------------------------------------------------------------

def plot_correlation_matrix(df_num):
    """
    Generates a heatmap of the correlation matrix for numerical features.
    
    Parameters:
    df_num (pd.DataFrame): A DataFrame containing only numerical columns.
    
    Returns:
    None: Displays the heatmap.
    """
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_num.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix", fontweight="bold", fontsize=14)
    plt.show()
    
#----------------------------------------------------------------------------------------------------------

def categorical_value_counts(df_cat):
    """
    Computes and displays value counts for categorical features in a structured format.
    
    Parameters:
    df_cat (pd.DataFrame): A DataFrame containing only categorical columns.
    
    Returns:
    pd.DataFrame: A DataFrame showing value counts for each categorical feature.
    """
    value_counts = pd.DataFrame()

    for col in df_cat.columns:
        counts = df_cat[col].value_counts().reset_index()
        counts.columns = [col, 'count']
        counts['feature'] = col
        value_counts = pd.concat([value_counts, counts], ignore_index=True, axis=0)

    # Keep only relevant columns
    value_counts = value_counts[['feature', 'count'] + df_cat.columns.tolist()]

    # Combine columns and drop NaN values
    combined_columns = value_counts.apply(lambda row: row.dropna().values, axis=1)
    combined_df = pd.DataFrame(combined_columns.tolist(), columns=['Feature', 'Count', 'Value'])

    # Sort by feature and value
    combined_df = combined_df[['Feature', 'Value', 'Count']].sort_values(by=['Feature', 'Value'])

    print(f'\n Value counts for categorical features: \n {combined_df}')
        
#----------------------------------------------------------------------------------------------------------

def plot_categorical_countplots(df_cat):
    """
    Generates count plots for categorical features in a DataFrame.

    Parameters:
    df_cat (pd.DataFrame): A DataFrame containing only categorical columns.

    Returns:
    None
    """
    num_features = len(df_cat.columns)
    ncols = 2
    nrows = math.ceil(num_features / ncols)  # Ensure enough rows

    # Create subplots
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 2 * num_features))
    axes = axes.flatten()

    # Plot countplots for each categorical feature
    for ax, col in zip(axes, df_cat.columns):
        sns.countplot(data=df_cat, x=col, ax=ax)
        ax.set_title(f'Countplot of {col}', fontsize=12)
        ax.set_xlabel(col)
        ax.set_ylabel('Count')
        ax.tick_params(axis='x', rotation=45)  # Rotate x labels for better visibility

    # Remove any empty subplots if number of features is odd
    for i in range(len(df_cat.columns), len(axes)):
        fig.delaxes(axes[i])

    # Adding a general title
    fig.suptitle('Countplots of the Categorical Features', fontsize=16, fontweight="bold")

    # Adjust layout to prevent overlap
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()
    
#----------------------------------------------------------------------------------------------------------

# correlations and distributions

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


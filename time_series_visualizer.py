import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', header=0, sep = ',', index_col=0, parse_dates = True, names = ['date', 'views'])

# Clean data
df = df[(df['views'] > df['views'].quantile(0.025)) & (df['views'] < df['views'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, axes = plt.subplots(figsize = (12,6))
    axes.plot(df.index, 'views', data = df)
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    df_bar["month"] = pd.Categorical(df_bar["month"], categories=months)
    
    df_bar_pivot = pd.pivot_table(
	df_bar,
	values="views",
	index="year",
	columns="month",
	)
    # Draw bar plot

    ax = df_bar_pivot.plot.bar(xlabel = 'Years', ylabel = 'Average Page Views', figsize = (12,6))
    fig = ax.get_figure()


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    ylimits = (0,200000)

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize =(12,8))
    sns.boxplot(data = df_box, x = 'year', y='views', hue = 'year', ax = ax1)
    ax1.get_legend().remove()
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel("Page Views")
    #ax1.set_ylim(0,200000)
    sns.boxplot(data = df_box, x = 'month', y='views', hue = 'month', ax = ax2, order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel("Page Views")
    #ax2.set_ylim(0,200000)
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

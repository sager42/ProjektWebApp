import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter

def provide_basic_plot(): 
    df = pd.read_csv('myproject/reddit_analyzer/test_labelled_comments.csv') #initializing data
    df['created'] = pd.to_datetime(df['created'], format='ISO8601')

    dum_df = pd.get_dummies(data=df, columns=['label']) #One Hot Encoding labelled data 

    sorted_df = dum_df[['created','label_negative','label_neutral','label_positive']].sort_values(by='created',axis=0,ascending=True)

    #cumulative sum to later show the increments of posts with particular label
    sum_sorted_df = sorted_df[['label_negative','label_neutral','label_positive']].cumsum()
    sum_sorted_df['all_labels_sum']=sum_sorted_df['label_negative']+sum_sorted_df['label_neutral']+sum_sorted_df['label_positive'] #show overall increment of number of posts

    sum_sorted_df['created'] =  sorted_df['created'] #add time column

    #separate into df according to category
    positive_df = sum_sorted_df[['created','label_positive']]
    negative_df = sum_sorted_df[['created','label_negative']]
    neutral_df = sum_sorted_df[['created','label_neutral']]
    cum_sum_df = sum_sorted_df[['created','all_labels_sum']]

    #create bokeh native data sources
    positive_cds = ColumnDataSource(positive_df)
    negative_cds = ColumnDataSource(negative_df)
    neutral_cds = ColumnDataSource(neutral_df)
    sum_cds = ColumnDataSource(cum_sum_df)

    #define properties of the plot
    fig = figure(x_axis_type = 'datetime')
    fig.line(x= 'created',y = 'label_positive', source = positive_cds, color = 'green' ,legend_label ='positive')
    fig.line(x= 'created',y = 'label_neutral', source = neutral_cds, color = 'blue',legend_label ='neutral')
    fig.line(x= 'created',y = 'label_negative', source = negative_cds, color = 'red',legend_label ='negative')
    fig.line(x= 'created',y = 'all_labels_sum', source = sum_cds, color = 'black',legend_label ='sum')
    fig.xaxis.formatter = DatetimeTickFormatter(minutes='%m/%d %H:%M', months="%m/%d %H:%M",
    hours="%m/%d %H:%M",)

    script,div = components(fig)
    return script, div 


class BasicPlot:
    def __init__(self) -> None:
        pass

if __name__ == '__main__':
    provide_basic_plot()
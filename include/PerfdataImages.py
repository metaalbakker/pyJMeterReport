import matplotlib.pyplot as plt
import matplotlib as mp
import re
import numpy as np
import datetime

mp.rcParams.update({'font.size':10})
image_dpi=150
fig_size_plot = 4.5
pagecount_number = 3
kinds_of_plot = []
percentiel=95

#plot_number = 1+int(properties.scatter_graph)+int(properties.percentile_graph)+int(properties.trendline_graph)
#
#if plot_number == 3:
#    fig_size_plot = 4.5
#    pagecount_number = 3
#else:
#    fig_size_plot = 7
#    pagecount_number = 2#

def make_images(perfdata_dataframe, stats_json, time_column, results_dir, graph_dir):
    """
    :param perfdata_json: Make images from columns from the JTLData and PerfmonData classes
    Saves them in the images folder in the working directory (pyJMeterReport
    :return: List of images with location
    """

    list_image_paths = []
    x_as_ticks = []

    #print(perfdata_dataframe)

    ##make the x-axis data
    x_ = perfdata_dataframe.get_dataframe()[time_column].values

    min_time = int(x_.min())
    max_time = int(x_.max())

    for i in range(0, 8, 1):
        x_as_ticks.append(int(min_time + (i * (max_time - min_time) / 7)))

    x_as_ticks_time = []
    for i in x_as_ticks:
        x_as_ticks_time.append(str(datetime.datetime.fromtimestamp(int(i / 1000)).strftime('%H:%M')))

    #loop over the to print columns, dit is alleen voor jtl, kan dit ook apart voor de jtl?
    for data in stats_json:
        for metingstat in stats_json[data]:
            for column in stats_json[data][metingstat][True]:

                metingstat_ = re.sub(r"[^\w\s]", '_',metingstat)  # vervang alle niet decimalen en alfabetische karakters door underscores
                metingstat_ = re.sub(r"\s+", '_', metingstat_)  # vervang alle whitespaces door underscores
                metingstat_ = metingstat_[:150]

                column_ = re.sub(r"[^\w\s]", '_',column)  # vervang alle niet decimalen en alfabetische karakters door underscores
                column_ = re.sub(r"\s+", '_', column_)  # vervang alle whitespaces door underscores
                column_ = column_[:150]

                base_graph_name_ = results_dir+'/'+graph_dir+'/'+data + '_' + metingstat_ + '_' + column_ + '_'

                #y_label_ = perfdata_dataframe.loc[(perfdata_dataframe["label"] == metingstat) & (perfdata_dataframe["success"] == True)]

                #retun dataframe met nodige  info
                y_label_ = perfdata_dataframe.get_yframe(metingstat,column)

                #print(y_label_)

                y_ = y_label_.values
                mean_value_array_ = []
                mean_value_ = stats_json[data][metingstat][True][column]['Mean']
                for v in y_:
                    mean_value_array_.append(mean_value_)

                line_path_ = make_line_plot(x_,y_,x_as_ticks,x_as_ticks_time,mean_value_array_,base_graph_name_,metingstat,column)
                scatter_path_ = make_scatter_plot(x_, y_, x_as_ticks, x_as_ticks_time, mean_value_array_, base_graph_name_,metingstat,column)
                percentile_path_ = make_percentile_plot(x_,y_, base_graph_name_,metingstat,column)

                list_image_paths.append(line_path_)
                list_image_paths.append(scatter_path_)
                list_image_paths.append(percentile_path_)

    return list_image_paths

def make_line_plot(x,y,x_ticks,x_time_ticks,y_avg,graph_name,metingstat,column):

    graph_name_full_ = graph_name+'line.png'

    x, y = (np.array(d) for d in zip(*sorted(zip(x, y))))

    print(graph_name_full_)

    fig = plt.figure(num=None, figsize=(16, fig_size_plot), dpi=image_dpi, facecolor='w', edgecolor='k')
    fig.suptitle('Line Plot - '+metingstat, fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    #ax.set_title('test', fontsize=12)

    # X-As #
    # ax.set_xlabel('Time')
    ax.xaxis.set_ticks(x_ticks)
    ax.set_xticklabels(x_time_ticks)

    # Y-As #

    ax.set_ylabel(column)

    # Plot #
    ax.plot(x, y, color='red', linewidth=0.75, label='Response Time')
    ax.plot(x, y_avg, color='green', linewidth=0.75, label='Average Response Time')
    ax.text(x[0] + (x[-1] - x[0]) * 5 / 100, y_avg[0], 'avg = ' + str(round(y_avg[0], 3)),
            style='italic', bbox={'facecolor': 'wheat', 'alpha': 0.75, 'pad': 4})

    ax.legend()

    plt.savefig(graph_name_full_)
    plt.close()

    return graph_name_full_

def make_scatter_plot(x,y,x_ticks,x_time_ticks,y_avg,graph_name,metingstat,column):

    graph_name_full_ = graph_name+'scatter.png'

    x, y = (np.array(d) for d in zip(*sorted(zip(x, y))))

    print(graph_name_full_)

    fig = plt.figure(num=None, figsize=(16, fig_size_plot), dpi=image_dpi, facecolor='w', edgecolor='k')
    fig.suptitle('Scatter Plot - '+metingstat, fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    #ax.set_title(, fontsize=12)

    # X-As #
    # ax.set_xlabel('Time')
    ax.xaxis.set_ticks(x_ticks)
    ax.set_xticklabels(x_time_ticks)

    # Y-As #

    ax.set_ylabel(column)

    # Plot #
    ax.plot(x, y, marker='.', markersize=2.0, linestyle='None', color='blue', label='Response Time')
    ax.plot(x, y_avg, color='green', linewidth=0.75, label='Average Response Time')
    ax.text(x[0] + (x[-1] - x[0]) * 5 / 100, y_avg[0], 'avg = ' + str(round(y_avg[0], 3)),
            style='italic', bbox={'facecolor': 'wheat', 'alpha': 0.75, 'pad': 4})

    ax.legend()

    plt.savefig(graph_name_full_)
    plt.close()

    return graph_name_full_


def make_percentile_plot(x,y, graph_name, metingstat, column):

    graph_name_full_ = graph_name + 'percentile.png'
    print(graph_name_full_)

    x, y = (np.array(d) for d in zip(*sorted(zip(x, y))))

    x_perc = []
    y_perc = []

    for i in range(1, 201):
        x_perc.append(0.5 * i)
        y_perc.append(np.percentile(y, 0.5 * i))

    x_perc_ticks = ['0', '20', '40', '60', '80', '100']

    fig = plt.figure(num=None, figsize=(16, fig_size_plot), dpi=image_dpi, facecolor='w', edgecolor='k')
    fig.suptitle('Percentile - '+metingstat, fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    #ax.set_title(metingid, fontsize=12)

    # X-As #
    ax.set_xlabel('Percentage[%]')
    ax.set_xticklabels(x_perc_ticks)

    # Y-As #
    ax.set_ylabel(column)

    # Plot #
    ax.plot(x_perc, y_perc, linewidth=0.3, color='green')
    ax.plot(x_perc[int(2 * (percentiel - 0.5))], y_perc[int(2 * (percentiel - 0.5))],
            'ro')  # Place red dots on the percentiles

    # Place Annotation
    ax.annotate(
        str(percentiel) + "% @ " + str(y_perc[int(2 * (percentiel - 0.5))])
        , xy=(x_perc[int(2 * (percentiel - 0.5))], y_perc[int(2 * (percentiel - 0.5))])
        , xytext=((x_perc[int(2 * (percentiel - 0.5))] / 100) - 0.25, 0.5), textcoords='axes fraction'
        , arrowprops=dict(facecolor='black', width=0.5, headwidth=4, shrink=0.10),
    )

    # Save & Close #
    plt.savefig(graph_name_full_)
    plt.close()

    return graph_name_full_

    del x_perc
    del y_perc
    del x_perc_ticks








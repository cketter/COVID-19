#!/usr/bin/python
import os, sys, subprocess
import pandas as pandas
import matplotlib.pyplot as plt

path = 'csse_covid_19_data/csse_covid_19_time_series/'
US_cases = path + 'time_series_covid19_confirmed_US.csv'
US_deaths = path + 'time_series_covid19_deaths_US.csv'
world_cases = path + 'time_series_covid19_confirmed_global.csv'
world_deaths = path + 'time_series_covid19_deaths_global.csv'
last_commit = subprocess.Popen(['git', 'log', '-1', '--format=%cd'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip('\n')

usage = """usage:
../gen_covid19_epi_curve.py <regex> [options]

Options:
-c / --cut        begining of time series [--cut N_days]
-s / --stacked    create stacked bar graph (default transparrent)
-r / --regional   plot regional data for countries outside the US.
                  (Only possible if data is available)
                  (Some countries only have regional data posted here, and I've not summed it!)
-o / --outfile    [--outfile fname]
-s / --save       save plot to file
"""

if len(sys.argv) < 2:
    raise Exception(usage)
place = str(sys.argv[1])
fname = ('../plots/')+place.strip('(').strip(')').replace('|','_').replace(' ', '')+('.png')
cut, stacked, regional, save = (0, False, False, False)
for arg, next_arg in zip(sys.argv, sys.argv[1:]):
    if arg == '-c' or arg == '--cut':
        cut = int(next_arg)
    if next_arg == '-s' or next_arg == '--stacked':
        stacked = True
    if next_arg == '-r' or next_arg == '--regional':
        regional = True
    if arg == '-o' or arg == '--outfile':
        fname = str(next_arg)
    if next_arg == '-s' or next_arg == '--save':
        save = True


def Reshape_US_data(csv):
    df = pandas.read_csv(csv)
    df = df.rename(index=df['Combined_Key'])[df.columns.tolist()[cut+12:]].filter(axis=0, regex=place).diff(axis=1)
    return df


def Reshape_world_data(csv, regional=False):
    df = pandas.read_csv(csv)
    if regional is True:
        key_col = ['Province/State', 'Country/Region']
        df = df[df['Province/State'].notnull()]
    else:
        key_col = ['Country/Region']
        df = df[df['Province/State'].isnull()]
    df.insert(0, 'Combined_Key', df[key_col].apply(lambda x: ', '.join(x[x.notnull()]), axis=1))
    df = df.rename(index=df['Combined_Key'])[df.columns.tolist()[cut+5:]].filter(axis=0, regex=place).diff(axis=1)
    return df


def Dress_Plot(df, idx, ylabel='Daily Number', stacked=False, bottom=None, sharex=None):
    ax = plt.subplot(2, 1, idx, sharex=sharex)
    bottom = bottom
    ax.bar(df.columns,
           list(df.iloc[0]),
           width=0.8,
           alpha=0.3 if stacked is False else 1,
           label=list(df.index)[0],
           bottom=bottom)
    for i in range(1, df.shape[0]):
        if stacked is True:
            bottom = list(df.iloc[i-1])
        ax.bar(df.columns,
               list(df.iloc[i]),
               width=0.8,
               alpha=0.3 if stacked is False else 1,
               label=list(df.index)[i],
               bottom=bottom)
    ax.set_xticklabels(df.columns, rotation=75, fontsize=6)
    ax.set_ylabel(ylabel)
    # ax.legend(loc=2)
    return ax


cases = Reshape_world_data(world_cases, regional=regional).append(Reshape_US_data(US_cases), sort=False)
deaths = Reshape_world_data(world_deaths, regional=regional).append(Reshape_US_data(US_deaths), sort=False)

fig = plt.figure(figsize=[11, 8.5])

ax2 = Dress_Plot(deaths, idx=2, ylabel='Daily Deaths', stacked=stacked)
ax1 = Dress_Plot(cases, idx=1, ylabel='Daily Cases', stacked=stacked, sharex=ax2)
ax1.legend(loc=2)

plt.setp(ax1.get_xticklabels(), fontsize=6, visible=False)
plt.tight_layout(rect=(0, 0, 1, .94))
fig.suptitle("COVID-19 Epidemic Curve, %s,\nsource: https://github.com/CSSEGISandData/COVID-19/ " % (last_commit), y=.97)
if save is True:
    print("saving to %s" % fname)
    plt.savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                orientation='landscape', papertype=None, format=None,
                transparent=False, bbox_inches=None, pad_inches=0.1,
                frameon=None, metadata=None)
else:
    plt.show()

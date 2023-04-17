#!/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import PercentFormatter
import seaborn as sns
import pandas

ticksize = 30
fontsize = 40
linewidth = 6.0

def main() -> None:
    sns.set_style("whitegrid")

    df_firstrq= pandas.read_csv("../RQ1/RQ1.1.csv", sep=";")
    list_first_rq = []
    for index, row in df_firstrq.iterrows():
        list_first_rq = list_first_rq + (int(row["Frequency"]) * [int(row["%Changes"])])

    df_secondrq = pandas.read_csv("../RQ2/RQ2.1.csv", sep=";")
    list_second_rq = []
    for index, row in df_secondrq.iterrows():
        list_second_rq = list_second_rq + (int(row["Frequency"]) * [int(row["%Changes"])])

    fig, ax = plt.subplots(figsize=(20, 8))
    configs = ax.hist(list_first_rq, 100, density=True, histtype='step',
            cumulative=-1, label='Configurations', linewidth=linewidth)

    options = ax.hist(list_second_rq, 100, density=True, histtype='step',
            cumulative=-1, label='Options', linewidth=linewidth)

    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.gca().xaxis.set_major_formatter(PercentFormatter(100))
    ax.tick_params(labelsize=ticksize)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.9])
    colors = [configs[2][0].get_edgecolor(), options[2][0].get_edgecolor()]
    configs = mpatches.Patch(color=colors[0], label="Configurations")
    options = mpatches.Patch(color=colors[1], label="Options")
    lgd = ax.legend([configs, options], ["Configurations", "Options"], loc='center left', fontsize=ticksize, bbox_to_anchor=(1, 0.5))
    ax.set_xlabel('Configurations / Options [%]', fontsize=fontsize, labelpad=20)
    ax.set_ylabel('Releases [%]', fontsize=fontsize)
    fig.savefig("../output/Frequencies.pdf", bbox_extra_artists=(lgd,), bbox_inches="tight")
    plt.close()

    df_firstrq = pandas.read_csv("../RQ1/taus.csv", sep=";")
    list_first_rq = []
    for index, row in df_firstrq.iterrows():
        list_first_rq = list_first_rq + (int(row["Frequency"]) * [float(row["Tau"])])

    df_secondrq = pandas.read_csv("../RQ2/taus.csv", sep=";")
    list_second_rq = []
    for index, row in df_secondrq.iterrows():
        list_second_rq = list_second_rq + (int(row["Frequency"]) * [float(row["Tau"])])

    fig, ax = plt.subplots(figsize=(22, 8))
    ax.hist(list_first_rq, 100, density=True, histtype='step',
            cumulative=-1, label='Configurations', linewidth=linewidth)

    ax.hist(list_second_rq, 100, range=(-1.0, 1.0), density=True, histtype='step',
            cumulative=-1, label='Options', linewidth=linewidth)

    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    ax.tick_params(labelsize=ticksize)
    ax.grid(True)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.9])
    configs = mpatches.Patch(color=colors[0], label="Configurations")
    options = mpatches.Patch(color=colors[1], label="Options")
    lgd = ax.legend([configs, options], ["Configurations", "Options"], loc='center left', fontsize=ticksize,
                    bbox_to_anchor=(1, 0.5))
    ax.set_xlabel("Kendall's Tau", fontsize=fontsize, labelpad=20)
    ax.set_ylabel('Releases [%]', fontsize=fontsize)
    fig.tight_layout()
    fig.savefig("../output/Taus.pdf", bbox_extra_artists=(lgd,), bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()

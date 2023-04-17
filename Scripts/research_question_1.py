from research_question import ResearchQuestion
from case_study import CaseStudy

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy import stats
from pandas import pivot_table
import json


class ResearchQuestion1(ResearchQuestion):
    name = "RQ1"
    configuration_stability_counter = 0
    performance_model_stability_counter = 0

    def __init__(self):
        self.changes_distribution = {}
        self.tau_distribution = []
        for i in range(0, 101):
            self.changes_distribution[i] = 0
        self.revision_counter = 0

    def initialize_for_metrics(self, path: str):
        with open(os.path.join(path, "Changes.md"), 'w') as output_file:
            output_file.write("\n")
            output_file.write("| Case Study | Changes |"
                              "\n")
            output_file.write("| :---: | :---: |\n")
        with open(f"{path}/Taus.md", 'w') as output_file:
            output_file.write("| Case Study | Tau |\n")
            output_file.write("| :---: | :---: |\n")

        with open(f"{path}/AnalysisChanges.md", 'w') as output_file:
            output_file.write("| Case Study | Release | Speedup | Slowdown |\n")
            output_file.write("| :---: | :---: | :---: | :---: |\n")

        with open(os.path.join(path, "TauFrequency.md"), 'w') as tau_values:
            tau_values.write("\n")
            tau_values.write("| Tau | Frequency |")
            tau_values.write("| :---: | :---: |\n")

        with open(os.path.join(path, "taus.csv"), 'w') as tau_values:
            tau_values.write("Tau;Frequency\n")

    def evaluate_metrics(self, case_study: CaseStudy, path: str, input_path: str) -> None:
        pass

    def prepare(self, case_study: CaseStudy, input_path: str) -> None:
        pass

    def search_configurations(self, case_study: CaseStudy, partial_configurations: pd.DataFrame):
        """Searches for configurations fullfilling the given partial configuration."""
        found_configurations = []
        for configuration in case_study.configurations.iterrows():
            configuration_matches = True
            for partial_configuration in partial_configurations.iterrows():

                for relevant_configuration_option in partial_configurations.columns:
                    if int(configuration[1][relevant_configuration_option]) != partial_configuration[1][
                        relevant_configuration_option]:
                        configuration_matches = False
                        break
                if configuration_matches:
                    found_configurations.append(configuration[1])
                    break
        return pd.DataFrame(data=found_configurations, columns=case_study.configurations.columns)

    def generate_plots(self, case_study: CaseStudy, path: str, input_path: str) -> None:
        changed_configurations, relevant_revisions_configs, stability_configurations = self.process_data(case_study,
                                                                                                         path,
                                                                                                         input_path)
        self.create_configurations_options_plot(case_study, changed_configurations, input_path, path,
                                                relevant_revisions_configs, stability_configurations)

    def process_data(self, case_study, path, input_path):
        # Sort the configurations according to their mean over all revisions
        all_configurations = pd.DataFrame(case_study.configurations)
        all_deviations = pd.DataFrame(case_study.deviations)
        revisions = list(dict.fromkeys(case_study.configurations.revision))
        self.revision_counter += len(revisions)
        feature_names = case_study.get_all_feature_names()
        mean_values = case_study.configurations.groupby(feature_names, sort=False).mean(numeric_only=True)
        mean_values.reset_index(inplace=True)
        mean_values = mean_values.sort_values('performance')
        mean_values.reset_index(inplace=True)
        number_configurations = len(mean_values)
        index_converter = dict(zip(mean_values['index'], mean_values.index))
        self.generate_difference_plots(all_configurations, all_deviations, case_study, index_converter,
                                       mean_values, number_configurations, path, revisions)
        self.generate_mean_performance_plots(case_study, path, input_path)
        # Plot them in a scatter plot (x-axis = release; y-axis = % of changed configurations)
        # First step: data preparation for computing % of the changes
        deviation_values = np.zeros((len(revisions), int(len(case_study.configurations) / len(revisions))))
        changed_configurations = np.zeros(len(revisions) - 1)
        for y in range(0, len(revisions)):
            for x in range(0, number_configurations):
                deviation_values[y, index_converter[x]] = float(
                    all_deviations.iloc[y * len(mean_values) + x]['performance'])
        relevant_indices = dict()
        for y in range(0, len(revisions) - 1):
            relevant_indices[y] = list()
            for x in range(0, number_configurations):
                first_configuration = float(
                    all_configurations.iloc[y * number_configurations + x]['performance']) / \
                                      case_study.get_division_factor()
                second_configuration = float(
                    all_configurations.iloc[(y + 1) * number_configurations + x]['performance']) / \
                                       case_study.get_division_factor()
                min_value = 2 * max(first_configuration *
                                    deviation_values[y][index_converter[x]],
                                    second_configuration *
                                    deviation_values[y + 1][index_converter[x]]
                                    )

                if abs(first_configuration - second_configuration) > min_value:
                    changed_configurations[y] += 1
                    relevant_indices[y].append(x)
            changed_configurations[y] = float(changed_configurations[y]) / number_configurations * 100
        # Stability:
        # Rank the configurations for each revision
        # Show the relative amount of configurations whose ranking has changed (probably most of the time 100%)
        revision_rankings = []
        relevant_revisions_configs = list()
        for y in range(0, len(revisions) - 1):
            if len(relevant_indices[y]) < 2:
                self.tau_distribution.append(1.0)
                if len(relevant_indices[y]) == 0:
                    print("Here is one revision without any changing configuration: " + str(revisions[y]))
                continue
            relevant_revisions_configs.append(y)
            self.configuration_stability_counter += 1
            for i in range(0, 2):
                revision_data = all_configurations[all_configurations['revision'] == revisions[y + i]]
                revision_data.reset_index(inplace=True, drop=True)
                revision_data = revision_data[revision_data.index.isin(relevant_indices[y])]
                revision_data = revision_data.sort_values('performance')
                revision_data.reset_index(inplace=True)
                revision_ranking_converter = dict(zip(revision_data['index'], revision_data.index))
                revision_ranking = np.zeros(len(relevant_indices[y]))
                for x in range(0, len(relevant_indices[y])):
                    revision_ranking[x] = revision_ranking_converter[relevant_indices[y][x]]

                revision_rankings.append(revision_ranking)
        stability_configurations = np.zeros(len(relevant_revisions_configs))
        taus = []
        for y in range(0, len(relevant_revisions_configs)):
            tau, p_value = stats.kendalltau(revision_rankings[2 * y], revision_rankings[2 * y + 1])
            stability_configurations[y] = tau
            taus.append(tau)
            self.tau_distribution.append(tau)
        with open(f"{path}/../Taus.md", 'a') as output_file:
            output_file.write(f"| {case_study.name} | {'{0:.2f}'.format(np.mean(taus))} |\n")
        return changed_configurations, relevant_revisions_configs, stability_configurations

    def create_configurations_options_plot(self, case_study, changed_configurations, input_path, path,
                                           relevant_revisions_configs, stability_configurations):
        super().create_directory(os.path.join(path, 'ScatterPlot'))
        if os.path.exists(os.path.join(input_path, case_study.name, "models", "models.csv")):
            with open(os.path.join(input_path, case_study.name, "models", "models.csv")) as models_file:
                # (I) Prepare the data for the changes
                performance_models = pd.read_csv(models_file, sep=";")
                revisions = list(dict.fromkeys(case_study.configurations.revision))
                plot_data = np.zeros((len(revisions), len(performance_models.columns) - 2))
                for y in range(0, len(revisions)):
                    plot_data[y] = performance_models.iloc[y][1:len(
                        performance_models.columns) - 1] / case_study.get_division_factor()

                mean_values = pivot_table(case_study.configurations, values='performance', index=['revision'])
                mean_values = mean_values.iloc[mean_values.index.map(revisions.index).argsort()]

                deviation_values = pivot_table(case_study.deviations, values='performance', index=['revision'])
                deviation_values = deviation_values.iloc[deviation_values.index.map(revisions.index).argsort()]
                deviation_values.reset_index(inplace=True)
                changed_terms = np.zeros(len(revisions) - 1)
                relevant_performance_model_columns = dict()

                for y in range(1, len(revisions)):
                    relevant_performance_model_columns[y - 1] = list()
                    standard_deviation = max(mean_values.iloc[len(revisions) - 1 - y]['performance'] *
                                             deviation_values.iloc[len(revisions) - 1 - y]['performance'],
                                             mean_values.iloc[len(revisions) - y]['performance'] *
                                             deviation_values.iloc[len(revisions) - y]['performance']) / \
                                         case_study.get_division_factor()
                    min_value = 2 * standard_deviation
                    for i in range(0, len(performance_models.columns) - 2):
                        difference = plot_data[y - 1][i] - plot_data[y][i]
                        if abs(difference) > min_value:
                            changed_terms[y - 1] += 1
                            relevant_performance_model_columns[y - 1].append(i)

                    changed_terms[y - 1] = float(changed_terms[y - 1]) / (len(performance_models.columns) - 2) * 100

            self.compute_stability(case_study, changed_configurations, changed_terms, path, plot_data,
                                   relevant_performance_model_columns, relevant_revisions_configs, revisions,
                                   stability_configurations)

    def compute_stability(self, case_study, changed_configurations, changed_terms, path, plot_data,
                          relevant_performance_model_columns, relevant_revisions_configs, revisions,
                          stability_configurations):
        # Prepare the data for the stability
        # First, create the ranking for each revision
        revision_rankings = []
        relevant_revisions_terms = list()
        for y in range(0, len(revisions) - 1):
            if len(relevant_performance_model_columns[y]) < 2:
                continue
            self.performance_model_stability_counter += 1
            relevant_revisions_terms.append(y)
            for i in range(0, 2):
                terms_influence = pd.DataFrame(plot_data[y + i].T)
                terms_influence.rename(columns={0: 'influence'}, inplace=True)
                terms_influence = terms_influence[terms_influence.index.isin(relevant_performance_model_columns[y])]
                terms_influence = terms_influence.iloc[terms_influence.influence.abs().argsort()]
                terms_influence.reset_index(inplace=True)
                revision_ranking_converter = dict(zip(terms_influence['index'], terms_influence.index))
                revision_ranking = np.zeros(len(relevant_performance_model_columns[y]))
                for x in range(0, len(relevant_performance_model_columns[y])):
                    revision_ranking[x] = revision_ranking_converter[relevant_performance_model_columns[y][x]]

                revision_rankings.append(revision_ranking)
        stability_terms = np.zeros(len(relevant_revisions_terms))
        # Then, compare the ranking
        for y in range(0, len(relevant_revisions_terms)):
            tau, p_value = stats.kendalltau(revision_rankings[2 * y], revision_rankings[2 * y + 1])
            stability_terms[y] = tau
        self.create_configurations_or_options_plot(changed_configurations, path, relevant_revisions_configs,
                                                   revisions, stability_configurations, "configurations")
        self.create_configurations_or_options_plot(changed_terms, path, relevant_revisions_terms,
                                                   revisions, stability_terms, "options")
        self.create_facet_grid(case_study, changed_configurations, changed_terms, path, relevant_revisions_configs,
                               relevant_revisions_terms, revisions, stability_configurations, stability_terms)

    def create_configurations_or_options_plot(self, changed_terms, path, relevant_revisions_terms, revisions,
                                              stability_terms, file_name):
        # Generate the plot
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(range(1, len(revisions)), changed_terms, '^r-', markersize=30, linewidth=4)
        ax.set_axisbelow(True)
        ax.set_xlabel("Release", fontsize=50, labelpad=20)
        ax.set_xticks(np.arange(0.5, len(revisions) + 0.5, step=1.0))
        ax.set_xticklabels(revisions, rotation=45, ha='right')
        ax.set_xlim(0.499, len(revisions) - 0.499)
        ax.set_ylabel("Changes [%]", fontsize=50, labelpad=20)
        ax.set_ylim(-5, 105)
        ax.set_yticks(np.arange(0, 110, step=25))
        ax2 = ax.twinx()
        processed_stability_terms = np.zeros(len(revisions) - 1)
        relevant_revision_counter = 0
        for i in range(len(revisions) - 1):
            if i in relevant_revisions_terms:
                processed_stability_terms[i] = stability_terms[relevant_revision_counter]
                relevant_revision_counter += 1
            else:
                processed_stability_terms[i] = 1.0
        ax2.plot(range(1, len(revisions)), processed_stability_terms, 'sb-', markersize=30, linewidth=4)
        ax2.set_ylabel("Kendall's Tau", fontsize=50, labelpad=20)
        ax2.set_ylim(-1.1, 1.1)
        ax2.set_yticks(np.arange(-1, 1.5, step=0.5))
        fig = ax.get_figure()
        fig.tight_layout()
        super().create_directory(os.path.join(path, 'ScatterPlot'))
        fig.savefig(os.path.join(path, 'ScatterPlot', f"{file_name}.pdf"))
        plt.close(fig)

    def create_facet_grid(self, case_study, changed_configurations, changed_terms, path, relevant_revisions_configs,
                          relevant_revisions_terms, revisions, stability_configurations, stability_terms):
        # Merge all data from the changes in one dataframe for the facet grid
        changes = pd.DataFrame(columns=['Revision', 'Changes', 'Level', 'Type'])
        for i in range(1, len(revisions)):
            changes = changes.append({'Revision': i, 'Changes': changed_configurations[i - 1],
                                      'Level': 'Configurations', 'Type': 'Changed'},
                                     ignore_index=True)
            if i - 1 in relevant_revisions_configs:
                changes = changes.append(
                    {'Revision': i,
                     'Changes': (stability_configurations[relevant_revisions_configs.index(i - 1)] + 1) * 50,
                     'Level': 'Configurations', 'Type': 'Stable'},
                    ignore_index=True)
            changes = changes.append({'Revision': i, 'Changes': changed_terms[i - 1], 'Level': 'Terms',
                                      'Type': 'Changed'},
                                     ignore_index=True)
            if i - 1 in relevant_revisions_terms:
                changes = changes.append(
                    {'Revision': i, 'Changes': (stability_terms[relevant_revisions_terms.index(i - 1)] + 1) * 50,
                     'Level': 'Terms', 'Type': 'Stable'},
                    ignore_index=True)
            else:
                changes = changes.append(
                    {'Revision': i, 'Changes': 100.0,
                     'Level': 'Terms', 'Type': 'Stable'},
                    ignore_index=True)
        # Write the information
        changes.to_csv(os.path.join(path, 'ScatterPlot', 'changes.csv'))
        with open(os.path.join(path, 'ScatterPlot', 'releases.txt'), 'w') as fp:
            json.dump(revisions, fp)
        with open(os.path.join(path, 'ScatterPlot', 'case_study_name.txt'), 'w') as fp:
            fp.write(case_study.name)
        # Draw the tau values separately
        pal = dict(Changed="red", Stable="blue")
        g = sns.FacetGrid(changes, col="Level", palette=pal, hue="Type", hue_kws=dict(marker=["^", "s"]),
                          gridspec_kws={"wspace": 0.1}, sharey=True, height=10, aspect=2)
        g = g.map(plt.plot, "Revision", "Changes", linewidth=4, markersize=30)
        # Draw the second y axis on the second plot
        plot_count = 0
        for ax, visibility in zip(g.axes[0], [False, True]):
            ax.set_axisbelow(True)
            ax.set_xlabel("Release", fontsize=50, labelpad=20)
            ax.set_xticks(np.arange(0.5, len(revisions) + 0.5, step=1.0))
            ax.set_xticklabels(revisions, rotation=45, ha='right')
            # ax.set_xlim(0.25, len(revisions) - 0.25)
            ax.set_ylim(-5, 105)
            ax.set_yticks(np.arange(0, 110, step=25))
            if plot_count == 0:
                ax.set_ylabel("Changes [%]", fontsize=50, labelpad=20)
                plot_count = 1
                ax.set_facecolor('white')
            else:
                ax.set_facecolor('#e0e0e0')
                ax.grid(color='white', zorder=10)
            ax2 = ax.twinx()
            ax2.grid(False)
            ax2.set_ylim(-1.1, 1.1)
            ax2.set_yticks(np.arange(-1, 1.5, step=0.5))
            ax2.get_yaxis().set_visible(visibility)
            ax2.set_ylabel("Kendall's Tau", fontsize=50, labelpad=20)
        plt.subplots_adjust(top=0.9, wspace=0.25)
        super().create_directory(os.path.join(path, 'ScatterPlot'))
        g.savefig(os.path.join(path, 'ScatterPlot', 'facet.pdf'))
        sns.set_style("whitegrid")

    def generate_difference_plots(self, all_configurations, all_deviations, case_study, index_converter, mean_values,
                                  number_configurations, path, revisions):
        # (I) Plot them in a heatmap (x-axis = configurations; y-axis = revisions/releases; color = performance)
        # Data preparation
        # all_configurations.set_index(keys=feature_names, inplace=True)
        plot_data = np.zeros((len(revisions), int(len(case_study.configurations) / len(revisions))))
        deviation_values = np.zeros((len(revisions), int(len(case_study.configurations) / len(revisions))))
        for y in range(0, len(revisions)):
            for x in range(0, len(mean_values)):
                plot_data[len(revisions) - 1 - y, index_converter[x]] = float(
                    all_configurations.iloc[y * len(mean_values) + x]['performance']) / case_study.get_division_factor()
                deviation_values[len(revisions) - 1 - y, index_converter[x]] = float(
                    all_deviations.iloc[y * len(mean_values) + x]['performance'])
        cmap = plt.get_cmap('Oranges')
        fontsize = 30
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(1, 1, 1)
        cm = ax.pcolormesh(plot_data, cmap=cmap)
        ax.set_title(case_study.name, fontsize=fontsize)
        ax.set_ylabel('Release', fontsize=fontsize)
        ax.set_xlabel('Configuration', fontsize=fontsize)
        ax.set_yticks(np.arange(0.5, len(revisions) + 0.5, step=1.0))
        ax.set_yticklabels(reversed(revisions), fontsize=20)
        ax.set_xticklabels([])
        cb = fig.colorbar(cm, ax=ax)
        cb.set_label('Performance [s]', fontsize=fontsize)
        cb.ax.tick_params(labelsize=fontsize)
        fig = ax.get_figure()
        fig.tight_layout()
        super().create_directory(os.path.join(path, 'AbsolutePerformance'))
        fig.savefig(os.path.join(path, 'AbsolutePerformance', 'configurationsPerformance.pdf'))
        plt.close(fig)

        # (II) Plot the differences between revisions (x-axis = configurations; y-axis = revisions/releases;
        # color = performance difference between revisions and alternatively performance difference between revision and
        # first revision)
        plot_data2 = np.copy(plot_data)
        revision_frequency = dict()
        for y in range(1, len(revisions)):
            counter = [0, 0]
            for x in range(0, len(mean_values)):
                min_value = 2 * max(plot_data[len(revisions) - 1 - y][x] * \
                                    deviation_values[len(revisions) - 1 - y][x],
                                    plot_data[len(revisions) - y][x] * \
                                    deviation_values[len(revisions) - y][x]
                                    )
                difference = plot_data[len(revisions) - 1 - y][x] - plot_data[len(revisions) - y][x]
                if abs(difference) < min_value:
                    plot_data2[len(revisions) - 1 - y][x] = 0
                else:
                    plot_data2[len(revisions) - 1 - y][x] = difference
                    if difference < 0:
                        counter[0] += 1
                    else:
                        counter[1] += 1
            with open(f"{path}/../AnalysisChanges.md", 'a') as output_file:
                output_file.write(
                    f"| {case_study.name} | {revisions[y - 1]} - {revisions[y]} | {'{0:.2f}'.format(np.mean(counter[0] / len(mean_values) * 100))} | {'{0:.2f}'.format(counter[1] / len(mean_values) * 100)} |\n")

            # Count the frequency per revision
            revision_frequency[revisions[y - 1] + "-" + revisions[y]] = \
                sum(list(map(lambda z: 1 if abs(z) > 0 else 0, plot_data2[len(revisions) - 1 - y]))) / float(
                    number_configurations) * 100
            relative_change = int(revision_frequency[revisions[y - 1] + "-" + revisions[y]])
            self.changes_distribution[int(revision_frequency[revisions[y - 1] + "-" + revisions[y]])] += 1

        plot_data2 = np.delete(plot_data2, len(revisions) - 1, axis=0)
        # Pick a colormap
        cmap = plt.get_cmap('RdBu_r')
        fig = plt.figure(figsize=(15, 8))
        ax = fig.add_subplot(1, 1, 1)
        greatest_value = max(abs(np.amin(plot_data2)), abs(np.amax(plot_data2)))
        cm = ax.pcolormesh(plot_data2, cmap=cmap, vmin=-greatest_value, vmax=greatest_value)
        ax.set_ylabel('Release', fontsize=fontsize)
        ax.set_xlabel('Configuration', fontsize=fontsize)
        ax.set_yticks(range(0, len(revisions)))
        ax.set_yticklabels(reversed(revisions), fontsize=20)
        ax.set_xticklabels([])
        cb = fig.colorbar(cm, ax=ax, extend='both')
        cb.set_label('Performance [s]', fontsize=fontsize)
        cb.ax.tick_params(labelsize=fontsize)
        fig = ax.get_figure()
        fig.tight_layout()
        self.create_directory(os.path.join(path, 'Difference'))
        fig.savefig(os.path.join(path, 'Difference', 'configurationsDifference.pdf'))
        plt.close(fig)

        # Frequency evaluation
        with open(os.path.join(path, "..", "Changes.md"), 'a') as output_file:
            output_file.write("| " + case_study.name + "| ")
            # Sort the frequencies
            self.write_frequency(output_file, revision_frequency)

            output_file.write("|\n")

    def write_frequency(self, output_file, revision_frequency):
        revision_frequency_ranking = list(revision_frequency.keys())
        revision_frequency_ranking = list(filter(lambda z: revision_frequency[z] != 0, revision_frequency_ranking))
        revision_frequency_ranking.sort(key=lambda z: revision_frequency[z], reverse=True)
        for revision in revision_frequency_ranking:
            output_file.write(revision + ": " + "{0:.2f}".format(revision_frequency[revision]) + "%; ")

    def generate_mean_performance_plots(self, case_study: CaseStudy, path: str, input_path: str) -> None:
        if not os.path.exists(input_path + os.sep + case_study.name + os.sep + "defaultConfigurations.csv"):
            return
        # data preparation

        revisions = list(dict.fromkeys(case_study.configurations.revision))

        # Determine all default configurations by reading in all partial configurations provided in
        # defaultConfigurations.csv and searching all configurations that fit to the pattern
        default_configurations = pd.read_csv(
            input_path + os.sep + case_study.name + os.sep + "defaultConfigurations.csv", sep=";")
        found_configurations = self.search_configurations(case_study, default_configurations)

        default_configuration_mean_values = pivot_table(found_configurations, values='performance', index=['revision'])
        default_configuration_mean_values = default_configuration_mean_values.iloc[
            default_configuration_mean_values.index.map(revisions.index).argsort()]

        default_configuration_mean_values['performance'] = default_configuration_mean_values[
                                                               'performance'] / case_study.get_division_factor()

        # Here, it is crucial to maintain the order of the revisions, which is
        # reset by using pivot_table
        mean_values = pivot_table(case_study.configurations, values='performance', index=['revision'])
        mean_values = mean_values.iloc[mean_values.index.map(revisions.index).argsort()]

        mean_values['performance'] = mean_values['performance'] / case_study.get_division_factor()

        deviation_values = pivot_table(case_study.deviations, values='performance', index=['revision'])
        deviation_values = deviation_values.iloc[deviation_values.index.map(revisions.index).argsort()]

        # The channel is for the gray area around the line plot
        channel = pd.DataFrame(index=mean_values.index)
        channel['top'] = mean_values['performance'] * (1.0 + deviation_values['performance'])
        channel['bottom'] = mean_values['performance'] * (1.0 - deviation_values['performance'])

        mean_values = mean_values.reset_index()

        channel.reset_index()

        # creating the figure
        fig = plt.figure(figsize=(16, 8))
        ax = fig.add_subplot(1, 1, 1)
        fontsize = 30

        mean_values = mean_values.reset_index()
        default_configuration_mean_values = default_configuration_mean_values.reset_index()

        # configuring the plot
        x = mean_values.index
        ax.tick_params(axis='x', which='both', bottom=True, labelbottom=True)
        ax.tick_params(labelsize=fontsize)
        # ax.set_title(case_study.name, fontsize=fontsize)
        ax.set_facecolor('white')
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')

        # plotting the line plot with the actual mean values
        all_configurations = case_study.configurations.copy()
        all_configurations['performance'] = all_configurations['performance'] / case_study.get_division_factor()
        all_configurations_with_noise = all_configurations.copy()
        revision_index_mapping = dict(zip(revisions, range(len(revisions))))
        all_configurations_with_noise['revision'] = all_configurations_with_noise['revision'].map(
            revision_index_mapping)
        all_configurations_with_noise['revision'] = all_configurations_with_noise['revision'] + 0.03 * np.random.randn(
            len(all_configurations_with_noise))
        all_configurations_with_noise.plot.scatter(ax=ax, y='performance', zorder=2, legend=False, x='revision', s=50,
                                                   color="limegreen", alpha=0.3)
        # sns.violinplot(x='revision', y='performance', data=all_configurations, ax=ax)
        default_configuration_mean_values.plot(ax=ax, legend=False, zorder=2, y='performance', style=['--'], marker="v",
                                               color="Darkblue", linewidth=5, markersize=20)

        # ax.legend(['Mean execution time', 'Default configuration execution time'], fontsize=fontsize, loc='best')

        # Overwrite the x ticks
        ax.set_xticks(x)
        # ax.set_yticklabels(fontsize=fontsize - 10)
        ax.tick_params(axis='y', labelsize=fontsize - 10)
        ax.set_xticklabels(mean_values['revision'], rotation=45, ha='right', fontsize=fontsize - 10)
        ax.set_xlabel('Release', fontsize=fontsize + 10, labelpad=20)
        ax.set_ylabel('Execution time [s]', fontsize=fontsize + 10, labelpad=20)

        # Set the minimum y ticks to 0
        # ax.set_ylim([0, max(channel['top'] + default_configuration_mean_values['performance']) * 1.5])
        ax.set_xlim(-0.5, len(x) - 0.5)

        fig = ax.get_figure()

        fig.tight_layout()
        super().create_directory(os.path.join(path, 'average'))
        fig.savefig(os.path.join(path, 'average', 'average.pdf'))
        plt.close(fig)

    def finish(self, path: str) -> None:
        with open(f"{path}/TauFrequency.md", 'a') as output_file:
            with open(f"{path}/taus.csv", 'a') as csv_file:
                current = -1
                step = 0.1
                while current < 1:
                    output_file.write(
                        f"|{'{:.1f}'.format(current)} -- {'{:.1f}'.format(current + step)} | {'{:.0f}'.format(len(list(filter(lambda x: current <= x < current + step, self.tau_distribution))))} |\n")
                    csv_file.write(
                        f"{'{:.1f}'.format(current)};{'{:.0f}'.format(len(list(filter(lambda x: current <= x < current + step, self.tau_distribution))))}\n")
                    current += step

        with open(f"{path}/Changes.md", 'a') as output_file:
            output_file.write("\n\n| %Changes | Frequency |"
                              "\n")
            output_file.write("| :---: | :---: |\n")
            for i in range(0, 101):
                output_file.write(f"| {i} | {self.changes_distribution[i]} |\n")

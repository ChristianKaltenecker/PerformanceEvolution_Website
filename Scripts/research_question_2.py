from case_study import CaseStudy
from research_question import ResearchQuestion
from utilities import *
from vif_analysis import VIFAnalyzer

import os
import csv
from shutil import copyfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import pivot_table
import scipy.stats as ss
import seaborn as sns
import subprocess
from typing import Dict
from typing import List
from typing import Tuple
from scipy import stats


class ResearchQuestion2(ResearchQuestion):
    name = "RQ2"

    SPLConqueror_Path = os.path.abspath("../SPLConqueror/SPLConqueror/CommandLine/bin/Release/CommandLine.exe")

    def __init__(self):
        self.case_study_influence_distribution = None
        self.influence_distribution = None
        self.error_count = 0
        self.error_sum = 0.0
        self.distance = 5
        self.ranking_changes = []
        self.average_changes = 0.0
        self.multiple_conf_options_changes = [0, 0]
        self.taus = []
        self.changes_distribution = {}
        for i in range(0, 101):
            self.changes_distribution[i] = 0

    @staticmethod
    def execute_command(command: str) -> str:
        output = subprocess.getstatusoutput(command)
        status_code = output[0]
        message = output[1]

        # Throw an error if the command was not successfully executed
        if status_code != 0:
            raise RuntimeError(message)

        return message

    def initialize_for_metrics(self, path: str):
        self.influence_distribution = self.initialize_influence_distribution()
        self.case_study_influence_distribution = {}

        with open(os.path.join(path, "OutlierAndChanges.md"), 'w') as output_file:
            output_file.write("\n")
            output_file.write("| Case Study | Outlier Terms | "
                              "\n")
            output_file.write("| :---: | :---: |\n")

        with open(os.path.join(path, "ErrorRates.md"), 'w') as output_file:
            output_file.write("\n")
            output_file.write("| Case Study | Release | Error Rate | "
                              "\n")
            output_file.write("| :---: | :---: | :---: |\n")

        with open(os.path.join(path, "Taus.md"), 'w') as tau_values:
            tau_values.write("\n")
            tau_values.write("| Tau | Frequency |")
            tau_values.write("| :---: | :---: |\n")

        with open(os.path.join(path, "taus.csv"), 'w') as tau_values:
            tau_values.write("Tau;Frequency\n")

    def initialize_influence_distribution(self):
        dict_to_return = {}
        for i in range(0, 101, self.distance):
            dict_to_return[i] = 0
        return dict_to_return

    def prepare(self, case_study: CaseStudy, input_path: str) -> None:
        # If no directory 'models' is included, the performance-influence models for each release have to be
        #  created and learned
        input_path = os.path.join(input_path, case_study.name)
        models_path = os.path.join(input_path, 'models')
        revisions = list(dict.fromkeys(case_study.configurations.revision))

        if not os.path.exists(models_path):
            print("\n\t\tCreating new job for " + case_study.name + "...", end="")

            super().create_directory(models_path)

            # Copy the FeatureModel.xml
            copyfile(os.path.join(input_path, "FeatureModel.xml"), os.path.join(models_path, "FeatureModel.xml"))

            # Extract the measurement files
            all_configurations = case_study.configurations
            header = list(filter(lambda x: x != "revision", all_configurations.columns.values))

            deviation_values = pivot_table(case_study.deviations, values='performance', index=['revision'])
            deviation_values = deviation_values.iloc[deviation_values.index.map(revisions.index).argsort()]
            deviation_values = deviation_values.reset_index()

            self.create_iterative_learning_jobs(all_configurations, deviation_values, header, models_path, revisions)

        elif not os.path.exists(os.path.join(models_path, "model_opt.txt")) and \
                not os.path.exists(os.path.join(models_path, "models.csv")):
            # If the iterative models are learned, the results have to be aggregated and new models have to be
            #  learned by using the evaluate-model functionality of SPL Conqueror
            all_terms = dict()
            for revision in revisions:
                performance_model, model_error = self.get_performance_model(
                    os.path.join(models_path, str(revision) + ".log"))
                if performance_model == "":
                    print(f"Performance model is empty in {case_study.name} {revision}!")
                    exit(-1)
                term_dict = self.parse_model(performance_model, case_study)
                self.combine_dicts(all_terms, term_dict)

            # The following 3 case studies include many interactions.
            # Here, we perform the VIF analysis such that individual features instead of interactions are dropped in
            # case of perfect multicollinearity. This way, we preserve the more fine-grained interactions instead
            # of the more coarse-grained individual features.
            if case_study.name not in ["lrzip", "MySQL", "MariaDB"]:
                terms = self.sort_terms(list(all_terms.keys()), case_study)
            else:
                terms = all_terms
            self.write_model(terms, os.path.join(models_path, "model_base.txt"))

            # Optimize the models by using the Variance Influence Factor (VIF)
            vif_analyzer = VIFAnalyzer(case_study, os.path.join(models_path, 'model_base.txt'))
            term_number = len(vif_analyzer.terms)
            # Here, we first apply countermeasures, such as removing one alternative in alternative groups
            model_with_countermeasures = vif_analyzer.apply_multicollinearity_countermeasures()
            if len(model_with_countermeasures) < term_number:
                print(f"In the case study {case_study.name}, some terms were dropped due to countermeasures.")
            # Only afterwards, we apply the VIF analysis and save the conflicts in another file for further
            # investigation.
            new_model = vif_analyzer.apply_iterative_vif(model_with_countermeasures, case_study.Performance,
                                                         os.path.join(models_path, f"conflicts.txt"))

            # Print the new model
            converted_model = list(map(lambda a: " * ".join(a), new_model))
            self.write_model(converted_model, os.path.join(models_path, f'model_opt.txt'))
            self.create_script(models_path, revisions, "opt")
        elif not os.path.exists(os.path.join(models_path, "models.csv")):
            self.extract_models(models_path, revisions, "opt")

    def sort_terms(self, term_list: List[str], case_study: CaseStudy) -> List[str]:
        """
        Sort the terms in the given list.
        The first element is the mandatory feature. Afterwards, the higher interactions follow.
        The last elements are the lower interactions and individual features.
        """
        list_to_sort: List[List[str]] = []
        max_terms = 1
        for term in term_list:
            elements = term.split('*')
            if len(elements) > max_terms:
                max_terms = len(elements)
            list_to_sort.append(elements)

        def term_order(elem: List[str]) -> int:
            if len(elem) == 1 and case_study.is_strictly_mandatory(elem[0]):
                return 0
            else:
                return max_terms + 1 - len(elem)

        list_to_sort.sort(key=term_order)
        list_to_return: List[str] = []
        for term in list_to_sort:
            list_to_return.append(" * ".join(term))
        return list_to_return

    def create_iterative_learning_jobs(self, all_configurations: pd.DataFrame, deviation_values: pd.DataFrame,
                                       header: List[str], models_path: str, revisions: List[str]) -> None:
        # Set up jobs
        with open(os.path.join(models_path, 'jobs.txt'), 'w', newline="\n") as job_file:

            for revision in revisions:
                job_string = "mono " + self.SPLConqueror_Path + " " + os.path.join(models_path,
                                                                                   "learn_" + str(revision) + ".a")
                job_file.write(job_string + "\n")

                # Create measurements file
                with open(os.path.join(models_path, str(revision) + ".csv"), "w", newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=header)
                    writer.writeheader()
                    configurations_revision = all_configurations[all_configurations['revision'] == revision]
                    for index, configuration in configurations_revision.iterrows():
                        configuration_dict = {}
                        for column in header:
                            configuration_dict[column] = configuration[column]
                        writer.writerow(configuration_dict)
                # Create automation script for SPL Conqueror
                with open(os.path.join(models_path, "learn_" + str(revision) + ".a"), "w", newline="\n") as a_file:
                    all_lines = list()
                    # log
                    all_lines.append("log ./" + str(revision) + ".log")
                    # ML-settings
                    all_lines.append(
                        'mlsettings epsilon:0 lossFunction:RELATIVE parallelization:True bagging:False '
                        'considerEpsilonTube:False useBackward:False abortError:'
                        + str(max(1, int(
                            deviation_values[deviation_values['revision'] == revision]['performance'].iloc[
                                0] * 100))) +
                        ' limitFeatureSize:False quadraticFunctionSupport:False crossValidation:False '
                        'learn-logFunction:False learn-accumulatedLogFunction:False '
                        'learn-asymFunction:False learn-ratioFunction:False numberOfRounds:70 '
                        'backwardErrorDelta:1 minImprovementPerRound:0.1 withHierarchy:False')
                    # VM
                    all_lines.append('vm ./FeatureModel.xml')
                    # Measurements
                    all_lines.append(f'all ./{str(revision)}.csv')
                    all_lines.append('nfp performance')
                    # learn-splconqueror
                    all_lines.append('select-all-measurements true')
                    all_lines.append('learn-splconqueror')
                    all_lines.append('clean-global')
                    a_file.writelines(list(map(lambda x: x + "\n", all_lines)))
        command = f"source {os.path.join(models_path, 'jobs.txt')}"
        print(f"Executing command: {command}")
        self.execute_command(command)


    def extract_models(self, models_path: str, revisions: List[str], suffix: str) -> None:
        # (only if all performance-influence models are learned:) Combine all performance-influence models
        #  into one single file for each release
        # Use the model_opt.txt file as header
        with open(os.path.join(models_path, "model_opt.txt"), 'r') as model_file:
            header = model_file.readlines()
            header = list(map(lambda x: x.replace("\n", ""), header))
            header.insert(0, "revision")
            header.insert(len(header), "error")
        with open(os.path.join(models_path, "models.csv"), 'w', newline="\n") as models_file:
            dict_writer = csv.DictWriter(models_file, delimiter=";", fieldnames=header)
            dict_writer.writeheader()
            for revision in revisions:
                revision_dict = dict()
                revision_dict["revision"] = f"{revision}_{suffix}"
                performance_model, model_error = self.get_performance_model(
                    os.path.join(models_path, f"{str(revision)}_{suffix}.log"))
                terms = performance_model.split("+")
                for term in terms:
                    elements = term.strip().split("*")
                    elements = list(map(lambda x: x.strip(), elements))
                    options = ' * '.join(elements[1:])
                    revision_dict[options] = elements[0]
                revision_dict["error"] = model_error
                dict_writer.writerow(revision_dict)

    def create_script(self, models_path: str, revisions: List[str], suffix: str = "") -> None:
        # Learn the model
        # Create automation script for SPL Conqueror
        # Set up slurm jobs
        with open(os.path.join(models_path, 'jobs.txt'), 'w', newline="\n") as job_file:
            if len(suffix) != 0:
                suffix = f"_{suffix}"
            for revision in revisions:
                job_string = f"mono {self.SPLConqueror_Path} {os.path.join(models_path, f'learn_{str(revision)}{suffix}.a')}"
                job_file.write(job_string + "\n")
                with open(os.path.join(models_path, f"learn_{str(revision)}{suffix}.a"), "w",
                          newline="\n") as a_file:
                    all_lines = list()
                    # log
                    all_lines.append(f"log ./{str(revision)}{suffix}.log")
                    # VM
                    all_lines.append('vm ./FeatureModel.xml')
                    # Measurements
                    all_lines.append(f'all ./{str(revision)}.csv')
                    all_lines.append('nfp performance')
                    # truemodel
                    all_lines.append('select-all-measurements true')
                    all_lines.append(f'truemodel model{suffix}.txt')
                    a_file.writelines(list(map(lambda x: x + "\n", all_lines)))

        command = f"source {os.path.join(models_path, 'jobs.txt')}"
        print(f"Executing command: {command}")
        self.execute_command(command)


    @staticmethod
    def get_performance_model(path: str) -> Tuple[str, str]:
        model = ""
        error = "0.0"
        with open(path, "r") as log_file:
            for line in log_file.readlines():
                if ";" in line:
                    elements = line.split(";")
                    model = elements[1]
                    error = elements[2]
            return model, error

    def parse_model(self, model: str, case_study: CaseStudy) -> Dict:
        terms = model.split("+")
        term_dict = dict()
        for term in terms:
            features_in_term = term.split("*")[1:]
            term_list = [[]]
            for feature_in_term in features_in_term:
                # If alternative feature
                feature_in_term = feature_in_term.strip()
                exclusions = case_study.features[feature_in_term].exclusions
                parent = case_study.features[feature_in_term].parent
                if len(exclusions) > 0 \
                        and all(list(map(lambda x: case_study.features[x].parent == parent, exclusions))):
                    alternatives = case_study.features[parent].children
                    valid_alternatives = []
                    for alternative in alternatives:
                        alternative_list = self.multiply_lists(term_list, [alternative])
                        if self.check_valid_configuration(alternative_list, case_study):
                            valid_alternatives.append(alternative)
                    if len(valid_alternatives) == len(case_study.features[parent].children):
                        valid_alternatives = valid_alternatives[1:]
                    term_list = self.multiply_lists(term_list, valid_alternatives)
                else:
                    term_list = self.multiply_lists(term_list, [feature_in_term])
            for term_element in term_list:
                term_dict[' * '.join(term_element)] = 0
        return term_dict

    @staticmethod
    def check_valid_configuration(list_to_check: List[List[str]], case_study: CaseStudy) -> bool:
        measurements = case_study.configurations
        for term in list_to_check:
            current_result = measurements[term[0]] == "1"
            for i in range(1, len(term)):
                other_term = term[i]
                current_result = np.logical_and(current_result, measurements[other_term] == "1")
            if not current_result.any():
                return False
        return True

    @staticmethod
    def multiply_lists(first_list: List, second_list: List) -> List:
        result = list()
        for y in second_list:
            for x in first_list:
                l = list(x)
                l.append(y)
                result.append(sorted(l))
        return result

    @staticmethod
    def combine_dicts(first_dict: Dict, second_dict: Dict) -> None:
        for key in second_dict.keys():
            first_dict[key] = second_dict[key]

    @staticmethod
    def write_model(terms: List[str], path: str) -> None:
        with open(path, 'w') as model_file:
            for term in terms:
                model_file.write(f"{term}\n")

    def evaluate_metrics(self, case_study: CaseStudy, path: str, input_path: str) -> None:
        pass

    def generate_plots(self, case_study: CaseStudy, path: str, input_path: str) -> None:
        self.create_ranking(case_study, input_path, path)

        if os.path.exists(os.path.join(input_path, case_study.name, "models", "models.csv")):
            with open(os.path.join(input_path, case_study.name, "models", "models.csv")) as models_file:
                self.generate_influence_difference_plots(case_study, input_path, models_file, path)

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
                changed = np.zeros(len(revisions) - 1)
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
                        difference = plot_data[y][i] - plot_data[y - 1][i]
                        if abs(difference) > min_value:
                            changed[y - 1] += 1
                            relevant_performance_model_columns[y - 1].append(i)

                    changed[y - 1] = float(changed[y - 1]) / (len(performance_models.columns) - 2) * 100

            # Prepare the data for the stability

            # First, create the ranking for each revision
            revision_rankings = []
            relevant_revisions = list()
            for y in range(0, len(revisions) - 1):
                if len(relevant_performance_model_columns[y]) < 2:
                    # Releases with no changes are stable
                    self.taus.append(1.0)
                    continue
                relevant_revisions.append(y)
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

            stability = np.zeros(len(relevant_revisions))
            # Then, compare the ranking
            for y in range(0, len(relevant_revisions)):
                tau, p_value = stats.kendalltau(revision_rankings[2 * y], revision_rankings[2 * y + 1])
                stability[y] = tau
                self.taus.append(tau)

            # Generate the plot
            fig = plt.figure(figsize=(15, 10))
            ax = fig.add_subplot(1, 1, 1)
            changed_plot = ax.plot(range(1, len(revisions)), changed, 'sr-', markersize=20,
                                   fillstyle='none')
            ax.set_title(case_study.name + " (|T|=" + str(len(performance_models.columns) - 1) + ")")
            ax.set_xlabel("Release")
            ax.set_xticklabels(revisions, rotation=45)
            ax.set_xticks(np.arange(0.5, len(revisions) + 0.5, step=1.0))
            ax.set_ylabel("[%]")
            ax.set_ylim(0, 100)
            ax.set_yticks(np.arange(0, 110, step=25))

            ax2 = ax.twinx()
            stable_plot = ax2.plot([x + 1 for x in relevant_revisions], stability, 'xb-', markersize=20)
            ax2.set_ylabel("Correlation")
            ax2.set_ylim(-1, 1)
            ax2.set_yticks(np.arange(-1, 1.5, step=0.5))

            ax.legend(changed_plot + stable_plot, ['Changed (RQ2.1)', 'Stable (RQ2.2)'])

            fig = ax.get_figure()

            fig.tight_layout()

            super().create_directory(os.path.join(path, 'ScatterPlot'))
            fig.savefig(os.path.join(path, 'ScatterPlot', 'configurations.pdf'))
            plt.close(fig)

            super().create_directory(os.path.join(path, 'ScatterPlot'))
            fig.savefig(os.path.join(path, 'ScatterPlot', 'configurations.pdf'))
            plt.close(fig)

    def create_ranking(self, case_study, input_path, path):
        if os.path.exists(os.path.join(input_path, case_study.name, "models", "models.csv")):
            with open(os.path.join(input_path, case_study.name, "models", "models.csv")) as models_file:
                performance_models = pd.read_csv(models_file, sep=";")
            revisions = list(dict.fromkeys(case_study.configurations.revision))
            performance_models.drop(columns="error", inplace=True)

            # Drop least-influential terms until the 80% are reached
            # Therefore, sort them at first
            performance_models_sort = performance_models.mean()
            performance_models_sort = performance_models_sort.apply(abs)
            performance_models_sort = performance_models_sort.sort_values(ascending=False)
            sum = performance_models_sort.sum()

            # Initialize the influence distribution for the case study
            self.case_study_influence_distribution[case_study.name] = self.initialize_influence_distribution()

            # Update the influence distribution
            for i in range(0, len(performance_models_sort)):
                relative_influence = int(self.get_relative_influence(performance_models_sort[i], sum))
                self.case_study_influence_distribution[case_study.name][relative_influence] += 1
            for i in range(0, 101, self.distance):
                self.case_study_influence_distribution[case_study.name][i] = \
                    self.case_study_influence_distribution[case_study.name][i] / len(performance_models_sort) * 100

            # Now, retrieve the number of terms that is needed to reach 80%
            current = 0.0
            index = 0
            while current < 0.8 and index < len(performance_models_sort):
                current += performance_models_sort[index] / sum
                index += 1

            # Drop all columns beginning from the index
            if index < len(performance_models_sort):
                for i in range(index, len(performance_models_sort)):
                    column_name = performance_models_sort.index[i]
                    performance_models.drop(columns=column_name, inplace=True)

            # Rank the remaining data
            ranking_data = np.zeros((len(revisions), len(performance_models.columns) - 1))
            influence_data = np.zeros((len(revisions), len(performance_models.columns) - 1))
            for y in range(0, len(revisions)):
                influences = list(map(lambda z: abs(z), performance_models.iloc[y][1:len(performance_models.columns)]))
                ranking_data[len(revisions) - 1 - y] = len(influences) + 1 - ss.rankdata(influences).astype(int)
                influence_data[len(revisions) - 1 - y] = influences

            fontsize = 30
            max_rank = 5

            points, paths = self.create_ranking_paths(ranking_data, max_rank)

            super().create_directory(os.path.join(path, 'Ranking'))
            # Create rank plots for each case study
            fig = plt.figure(figsize=(15, 8))
            ax = fig.add_subplot(1, 1, 1)

            for i in range(1, max_rank + 1):
                ax.axhline(i, color='k', alpha=0.05)

            for point in points:
                ax.scatter(point[1], point[0], color='k', s=400)

            linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 10)), (0, (1, 1)), (0, (5, 1)),
                          (0, (3, 10, 1, 10, 1, 10))]
            for path_key in paths.keys():
                created_path = paths[path_key]
                if len(created_path) > 0:
                    for xcoords, ycoords in created_path:
                        ax.plot(xcoords, ycoords, linestyle=linestyles[path_key % len(linestyles)], color='k')

            # ax.legend(fontsize=fontsize - 7)
            fig = ax.get_figure()
            # ax.set_title(case_study.name, fontsize=fontsize)
            ax.set_ylabel("Performance Rank", fontsize=fontsize + 10)
            ax.set_xlabel("Release", fontsize=fontsize + 10, labelpad=20)
            ax.tick_params(labelsize=fontsize - 10)
            ax.set_yticks(range(1, max_rank + 1))
            ax.set_yticklabels(['5', '4', '3', '2', '1'], fontsize=fontsize)
            # ax.set_xticks(np.arange(0.5, len(revisions) + 0.5, step=1.0))
            ax.set_xticks(range(0, len(revisions)))
            ax.set_xticklabels(revisions, rotation=45, ha='right', fontsize=fontsize)

            fig.tight_layout()
            fig.savefig(os.path.join(path, 'Ranking', 'influenceRanking.pdf'))
            plt.close(fig)

            # Apply the difference function over all revisions and list the revisions ordered by the difference
            diff = dict()
            for y in range(1, len(revisions)):
                diff[revisions[y - 1] + "-" + revisions[y]] = 0
                for t in range(0, len(performance_models.columns) - 1):
                    diff[revisions[y - 1] + "-" + revisions[y]] += min(abs(ranking_data[len(revisions) - 1 - y][t] -
                                                                           ranking_data[len(revisions) - y][t]), 1)
                diff[revisions[y - 1] + "-" + revisions[y]] = diff[revisions[y - 1] + "-" + revisions[y]] / len(
                    performance_models.columns) * 100
                self.ranking_changes.append(diff[revisions[y - 1] + "-" + revisions[y]])

    def get_relative_influence(self, influence, total_influence):
        relative_influence = influence / total_influence
        # Returns the influence
        return self.distance * round(relative_influence * 100 / self.distance)

    def create_ranking_paths(self, rankings, max_rank):
        ranking_dict = {}
        for ranking in rankings:
            for i in range(0, len(ranking)):
                if i not in ranking_dict:
                    ranking_dict[i] = []
                if ranking[i] <= max_rank:
                    ranking_dict[i].append(int(max_rank + 1 - ranking[i]))
                else:
                    ranking_dict[i].append(-1)

        # Create the paths
        paths = {}

        points = []
        for i in ranking_dict.keys():
            paths[i] = []
            current_path = ([], [])
            for j in range(0, len(ranking_dict[i])):
                rank = ranking_dict[i][j]
                if rank == -1:
                    if len(current_path[1]) > 0:
                        paths[i].append(current_path)
                    current_path = ([], [])
                else:
                    points.append((max_rank + 1 - rank, j))
                    current_path[1].append(rank)
                    current_path[0].append(len(ranking_dict[i]) - 1 - j)

            if len(current_path[1]) > 0:
                paths[i].append(current_path)
        return points, paths

    def top_x(self, x, diff_top_five, diff_top_five_count, ranking_data, revisions, t, y):
        if ranking_data[len(revisions) - 1 - y][t] <= x:
            diff_top_five[revisions[y - 1] + "-" + revisions[y]] += min(abs(ranking_data[len(revisions) - 1 - y][t] -
                                                                            ranking_data[len(revisions) - y][t]), 1)
            diff_top_five_count += 1
        return diff_top_five_count

    def generate_influence_difference_plots(self, case_study, input_path, models_file, path):
        # (I) Plot the coefficients of the terms with a heatmap
        performance_models = pd.read_csv(models_file, sep=";")
        revisions = list(dict.fromkeys(case_study.configurations.revision))
        plot_data = np.zeros((len(revisions), len(performance_models.columns) - 2))
        for y in range(0, len(revisions)):
            plot_data[len(revisions) - 1 - y] = performance_models.iloc[y][1:len(
                performance_models.columns) - 1] / case_study.get_division_factor()
        fontsize = 30
        cmap = plt.get_cmap('RdBu_r')
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(1, 1, 1)
        greatest_value = max(abs(np.amin(plot_data)), abs(np.amax(plot_data)))
        cm = ax.pcolormesh(plot_data, cmap=cmap, vmin=-greatest_value, vmax=greatest_value)
        ax.set_title(case_study.name, fontsize=fontsize)
        ax.set_ylabel('Release', fontsize=fontsize)
        ax.set_xlabel('Term', fontsize=fontsize)
        ax.set_yticks(np.arange(0.5, len(revisions) + 0.5, step=1.0))
        ax.set_yticklabels(reversed(revisions))
        tmp = list(performance_models.columns[1:-1])
        ax.set_xticks(np.arange(0.5, len(tmp) + 0.5, step=1.0))
        ax.set_xticklabels(tmp, rotation=45, ha='right', fontsize=20)
        cb = fig.colorbar(cm, ax=ax)
        cb.ax.tick_params(labelsize=fontsize)
        cb.set_label('Influence [s]', fontsize=fontsize)
        fig = ax.get_figure()
        fig.tight_layout()
        super().create_directory(os.path.join(path, 'AbsoluteInfluence'))
        fig.savefig(os.path.join(path, 'AbsoluteInfluence', 'configurationsInfluence.pdf'))
        plt.close(fig)
        # (II) Plot the differences of the coefficients of the terms with a heatmap
        plot_data2 = np.copy(plot_data)
        mean_values = pivot_table(case_study.configurations, values='performance', index=['revision'])
        mean_values = mean_values.iloc[mean_values.index.map(revisions.index).argsort()]
        term_dictionary = dict()
        term_ci_dictionary = dict()
        deviation_values = pivot_table(case_study.deviations, values='performance', index=['revision'])
        deviation_values = deviation_values.iloc[deviation_values.index.map(revisions.index).argsort()]
        deviation_values.reset_index(inplace=True)
        with open(os.path.join(input_path, case_study.name, "relevantTerms.txt"), 'w') as term_file:
            for y in range(1, len(revisions)):
                terms = ""

                term_dictionary[revisions[y - 1] + "-" + revisions[y]] = [[], 0, [0, 0, 0, 0, 0, 0, 0], 0]
                term_ci_dictionary[revisions[y - 1] + "-" + revisions[y]] = [[], 0]
                standard_deviation = max(mean_values.iloc[len(revisions) - 1 - y]['performance'] * \
                                         deviation_values.iloc[len(revisions) - 1 - y]['performance'],
                                         mean_values.iloc[len(revisions) - y]['performance'] * \
                                         deviation_values.iloc[len(revisions) - y]['performance']) / \
                                     case_study.get_division_factor()
                min_value = 2 * standard_deviation
                relevant_column_counter = 0
                for i in range(0, len(performance_models.columns) - 2):
                    difference = - (plot_data[len(revisions) - y][i] - plot_data[len(revisions) - 1 - y][i])
                    term_dictionary[revisions[y - 1] + "-" + revisions[y]][3] += 1
                    if abs(difference) > min_value:
                        relevant_column_counter += 1
                        plot_data2[len(revisions) - 1 - y][i] = difference
                        term_dictionary[revisions[y - 1] + "-" + revisions[y]][0].append(
                            performance_models.columns[i + 1])
                        term_dictionary[revisions[y - 1] + "-" + revisions[y]][1] += difference

                        if i == 0:
                            terms += "root; "
                            term_dictionary[revisions[y - 1] + "-" + revisions[y]][2][0] += 1
                        else:
                            terms += performance_models.columns[i + 1] + ";"
                            term_dictionary[revisions[y - 1] + "-" + revisions[y]][2][
                                len(performance_models.columns[i + 1].split('*'))] += 1
                    else:
                        plot_data2[len(revisions) - 1 - y][i] = 0

                    if confidence_interval_disjoint(case_study.name,
                                                    plot_data[len(revisions) - 1 - y][i],
                                                    deviation_values.iloc[len(revisions) - 1 - y][
                                                        'performance'],
                                                    plot_data[len(revisions) - y][i],
                                                    deviation_values.iloc[len(revisions) - y]['performance']):
                        term_ci_dictionary[revisions[y - 1] + "-" + revisions[y]][0].append(
                            performance_models.columns[i])
                        term_ci_dictionary[revisions[y - 1] + "-" + revisions[y]][1] += difference

                self.changes_distribution[
                    int(relevant_column_counter * 100 / (len(performance_models.columns) - 2.0))] += 1

                if terms != "" and terms != performance_models.columns[0]:
                    term_file.write(revisions[y] + ": " + terms + "\n")

                term_dictionary[revisions[y - 1] + "-" + revisions[y]][1] /= standard_deviation
        plot_data2 = np.delete(plot_data2, len(revisions) - 1, axis=0)
        cmap = plt.get_cmap('RdBu_r')
        fig = plt.figure(figsize=(15, 8))
        ax = fig.add_subplot(1, 1, 1)
        greatest_value = max(abs(np.amin(plot_data2)), abs(np.amax(plot_data2)))
        cm = ax.pcolormesh(plot_data2, cmap=cmap, vmin=-greatest_value, vmax=greatest_value)
        ax.set_ylabel('Release', fontsize=fontsize)
        ax.set_xlabel('Configuration Choice', fontsize=fontsize)
        ax.set_yticks(range(0, len(revisions)))
        ax.set_yticklabels(reversed(revisions), fontsize=20)
        tmp = list(performance_models.columns[1:-1])
        tmp[0] = 'root'
        if case_study.name == 'OpenVPN':
            tmp = self.replace_terms(tmp)
            tmp = tmp[0:plot_data2.shape[1]]
        ax.set_xticks(np.arange(0.5, len(tmp) + 0.5, step=1.0))
        ax.set_xticklabels(tmp, rotation=45, ha='right', fontsize=20)
        cb = fig.colorbar(cm, ax=ax, extend='both')
        cb.ax.tick_params(labelsize=fontsize)
        cb.set_label('Influence Difference [s]', fontsize=fontsize)
        fig = ax.get_figure()
        fig.tight_layout()
        self.create_directory(os.path.join(path, 'InfluenceDifference'))
        fig.savefig(os.path.join(path, 'InfluenceDifference', 'influenceDifference.pdf'))
        plt.close(fig)
        # Frequency evaluation
        with open(os.path.join(path, "..", "OutlierAndChanges.md"), 'a') as output_file:
            output_file.write("| " + case_study.name + "| ")
            # Sort the frequencies
            self.write_frequency(output_file, term_dictionary)

            # output_file.write(" | ")
            # self.write_frequency(output_file, term_ci_dictionary)
            output_file.write("|\n")
        with open(os.path.join(path, "..", "ErrorRates.md"), 'a') as output_file:
            self.write_error_rates(output_file, case_study.name, performance_models)

    def replace_terms(self, terms):
        term_replacement_dict = {'root': 'Root', 'lzo': 'LZO', 'auth_sha512': 'SHA512',
                                 'auth_sha1': 'SHA1', 'auth_rsa_sha512': 'RSA SHA512',
                                 'prng_sha512': 'SHA512 PRN Gen.',
                                 'prng_rsa_sha512': 'SHA512 RSA PRN Gen.',
                                 'prng_sha1': 'SHA1 PRN Gen.', 'TCP_NODEAL': 'TCP No Delay',
                                 'AES_128_CBC': 'AES-128-CBC'}
        new_terms = []
        for term in terms:
            configuration_options = term.split('*')
            new_configuration_options = []
            for configuration_option in configuration_options:
                new_configuration_options.append(term_replacement_dict[configuration_option.strip()])
            new_terms.append(' · '.join(new_configuration_options))

        return new_terms

    def write_error_rates(self, output_file, case_study_name, performance_models):
        """
            Writes the error rates of the case study in a README file
            :param output_file:
            :param performance_models:
            :return:
            """
        for i in range(0, len(performance_models)):
            revision = performance_models['revision'][i]
            error = performance_models['error'][i]
            if i == 0:
                output_file.write("| " + case_study_name + " | ")
            else:
                output_file.write("| | ")
            output_file.write(str(revision) + " | " + "{:.2f}".format(error) + "% |\n")
            self.error_sum += float(error)
            self.error_count += 1

    def write_frequency(self, output_file, revision_frequency):
        revision_frequency_ranking = list(revision_frequency.keys())
        revision_frequency_ranking = list(filter(lambda z: revision_frequency[z][1] != 0, revision_frequency_ranking))
        revision_frequency_ranking.sort(key=lambda z: revision_frequency[z][1], reverse=True)
        changes = 0.0
        for revision in revision_frequency_ranking:
            output_file.write(revision + ": ")
            # Write all terms
            output_file.write(str(len(revision_frequency[revision][0])) + " ")
            change = sum(revision_frequency[revision][2]) / float(revision_frequency[revision][3]) * 100
            changes += change
            if revision_frequency[revision][1] > 1 or sum(revision_frequency[revision][2][1:]) > 1:
                self.multiple_conf_options_changes[1] += 1
            elif sum(revision_frequency[revision][2]) > 0:
                self.multiple_conf_options_changes[0] += 1
            output_file.write(str(revision_frequency[revision][2]) + " -- " + "{0:.2f}".format(change) + "%; ")
        if changes > 0:
            self.average_changes += changes / len(revision_frequency_ranking)

    def finish(self, path: str) -> None:
        if self.error_count == 0:
            return

        with open(f"{path}/Taus.md", 'a') as output_file:
            with open(f"{path}/taus.csv", 'a') as csv_file:
                current = -1
                step = 0.1
                while current < 1:
                    output_file.write(
                        f"|{'{:.1f}'.format(current)} -- {'{:.1f}'.format(current + step)} | {'{:.0f}'.format(len(list(filter(lambda x: current <= x < current + step, self.taus))))} |\n")
                    csv_file.write(
                        f"{'{:.1f}'.format(current)};{'{:.0f}'.format(len(list(filter(lambda x: current <= x < current + step, self.taus))))}\n")
                    current += step

        # Now, compute the average distribution
        for i in range(0, 101, self.distance):
            for case_study_name in self.case_study_influence_distribution.keys():
                self.influence_distribution[i] += self.case_study_influence_distribution[case_study_name][i]
            self.influence_distribution[i] /= len(self.case_study_influence_distribution.keys())
        # Compute the distance of all case studies
        distance = dict()
        for case_study_name in self.case_study_influence_distribution.keys():
            distance[case_study_name] = 0
            for i in range(0, 101, self.distance):
                distance[case_study_name] += abs(self.influence_distribution[i] -
                                                 self.case_study_influence_distribution[case_study_name][i])

        # Now find the one that corresponds the average and the outlier
        outlier_case_study = max(distance, key=distance.get)

        # Create two plots and use their case study names on the top
        # The plot should contain a black distribution in the background depicting the average case and a transparent
        # distribution on the foreground depicting the median or the outlier, respectively

        fontsize = 30

        all_influences = range(0, 101, self.distance)
        sns.set_theme(style="whitegrid")
        plt.rcParams['xtick.bottom'] = True
        plt.figure(figsize=(15, 8))
        dataframe = pd.DataFrame()
        dataframe['influence'] = all_influences
        dataframe['frequency'] = list(self.influence_distribution.values())
        ax = sns.barplot(x='influence', y='frequency', data=dataframe, color='b')

        fig = ax.get_figure()
        ax.set_title("All subject systems", fontsize=50, pad=20)
        ax.set_ylabel("Frequency [%]", fontsize=50)
        ax.set_xlabel("Relative Influence", fontsize=50, labelpad=20)
        ax.tick_params(labelsize=fontsize)
        ax.set_xticklabels(self.create_x_label(25))
        ax.set_ylim([0, 100])

        fig.tight_layout()
        fig.savefig(os.path.join(path, 'relativeInfluences.pdf'))
        plt.close(fig)
        dataframe.to_csv(path_or_buf=f"{path}/relativeInfluences.csv")

        plt.figure(figsize=(15, 8))
        dataframe = pd.DataFrame()
        dataframe['influence'] = all_influences
        dataframe['frequency'] = list(self.case_study_influence_distribution[outlier_case_study].values())
        ax = sns.barplot(x='influence', y='frequency', data=dataframe, color='b')

        fig = ax.get_figure()
        ax.set_title(outlier_case_study, fontsize=50, pad=20)
        ax.set_ylabel("Frequency [%]", fontsize=50, labelpad=20)
        ax.set_xlabel("Relative Influence", fontsize=50, labelpad=20)
        ax.tick_params(labelsize=fontsize)
        ax.set_xticklabels(self.create_x_label(25))
        ax.yaxis.set_label_position("right")
        ax.set_ylim([0, 100])

        fig.tight_layout()
        fig.savefig(os.path.join(path, 'outlierInfluences.pdf'))
        plt.close(fig)

        with open(f"{path}/OutlierAndChanges.md", 'a') as output_file:
            output_file.write("\n\n| %Changes | Frequency |"
                              "\n")
            output_file.write("| :---: | :---: |\n")
            for i in range(0, 101):
                output_file.write(f"| {i} | {self.changes_distribution[i]}\n")
        with open(f"{path}/RQ2.1.csv", 'w') as output_file:
            output_file.write("%Changes;Frequency"
                              "\n")
            for i in range(0, 101):
                output_file.write(f"{i};{self.changes_distribution[i]}\n")

    def create_x_label(self, division_factor: int) -> List[str]:
        result = []
        for i in range(0, 101, self.distance):
            if i % division_factor == 0:
                result.append(str(i))
            else:
                result.append('')
        return result

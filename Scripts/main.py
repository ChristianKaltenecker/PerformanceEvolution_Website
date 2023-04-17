#!/bin/env python3
import sys
import os
from typing import List
from case_study import CaseStudy
import seaborn as sns
import matplotlib.pyplot as plt
import warnings


from research_question_1 import ResearchQuestion1
from research_question_2 import ResearchQuestion2

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

NFP = "performance"  # (execution time in our case)
FM = "FeatureModel.xml"
Measurements = "measurements.csv"
Deviations = "deviations.csv"
Results_File = "README_POST.md"

INPUT_PATH = "../PerformanceEvolution_Data"
OUTPUT_PATH = "../output"

Research_Questions = [
                        ResearchQuestion1(),
                        ResearchQuestion2()
                     ]


def list_directories(path: str) -> List:
    """
    Returns the subdirectories of the given path.
    :param path: the path to find the subdirectories from.
    :return: the subdirectories as list.
    """
    for root, dirs, files in os.walk(path):
        return list(filter(lambda x: not x.startswith("."), dirs))


def create_directory(path: str) -> None:
    """
    Creates the given directory if it does not exist already.
    :param path: the path to create
    """
    if not os.path.exists(path):
        os.makedirs(path)


def main() -> None:
    """
    The main method reads in the data of the case studies and evaluates the data with regard to the different
    research questions (1-4) of the study.
    """

    # Read in the path to the case study data
    input_path = INPUT_PATH

    # Read in the output path of the plots
    output_path = OUTPUT_PATH

    fontsize = 30
    plt.rcParams.update({'font.size': fontsize})
    sns.set_style("whitegrid")

    case_studies = sorted(list_directories(input_path), key=str.lower)
    print("Progress:")
    i = -1

    for rq in Research_Questions:
        os.makedirs(os.path.join(output_path, rq.name), exist_ok=True)
        rq.initialize_for_metrics(os.path.join(output_path, rq.name))

    for case_study in case_studies:
        i += 1
        print(case_study + " (" + str(int((float(i) / len(case_studies)) * 100)) + "%)")
        # Read in one case study (i.e., its FM and measurements) after another (and wipe the data to save some RAM)
        cs = CaseStudy(case_study, os.path.join(input_path, case_study, FM),
                       os.path.join(input_path, case_study, Measurements),
                       os.path.join(input_path, case_study, Deviations))

        rq_count = 0
        for rq in Research_Questions:
            rq_count += 1
            print("\t" + rq.get_name() + "...", end="")
            sys.stdout.flush()
            rq.prepare(cs, input_path)
            rq.evaluate_metrics(cs, os.path.join(output_path, rq.name), input_path)
            rq.generate_plots(cs, os.path.join(output_path, rq.name, case_study), input_path)
            print("Finished!")

    for rq in Research_Questions:
        rq.finish(os.path.join(output_path, rq.name))


if __name__ == "__main__":
    main()

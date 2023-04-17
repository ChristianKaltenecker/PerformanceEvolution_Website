from feature import Feature
from typing import List
import pandas as pd
import xml.etree.ElementTree as ET
import sys
import os
from typing import Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CaseStudy:
    Performance = "performance"
    Case_Studies_In_Milliseconds = ["lrzip", "PostgreSQL", "VP8", "VP9"]
    Case_Studies_Reverse_Revisions = ["FastDownward"]

    def __init__(self, name: str, feature_model_path: str, measurements_path: str, deviation_path: str = None) -> None:
        self.name = name
        self.features: Dict[str, Feature] = dict()
        self.configurations = None
        self.deviations = None
        self.workload_list = []
        self.read_feature_model(feature_model_path)
        self.read_measurements(measurements_path)
        if deviation_path is not None:
            self.read_deviations(deviation_path)

    def __str__(self) -> str:
        return self.name

    def get_division_factor(self):
        if self.name in self.Case_Studies_In_Milliseconds:
            return 1000
        return 1

    @staticmethod
    def get_options(node) -> List:
        result = []
        for option_node in node:
            result.append(option_node.text)
        return result

    def read_feature_model(self, path: str) -> None:
        with open(path, 'r') as feature_model_file:
            root = ET.parse(feature_model_file).getroot()

            binary_options = root.find('binaryOptions')
            numeric_options = root.find('numericOptions')

            children_relation = dict()

            # Parse binary options
            for binary_option in binary_options:
                name = str.replace(binary_option.find('name').text, '\n', '')
                mandatory = binary_option.find('optional').text == 'False'
                parent = binary_option.find('parent').text
                excluded_options = self.get_options(binary_option.find('excludedOptions'))
                implied_options = self.get_options(binary_option.find('impliedOptions'))
                self.features[name] = Feature(name, parent, excluded_options, implied_options, mandatory)
                if name != "root" and parent not in children_relation:
                    children_relation[parent] = []
                if name != "root":
                    children_relation[parent].append(name)
                if parent == "workloads":
                    self.workload_list.append(name)

            # Parse numeric options
            if len(numeric_options) > 0:
                for numeric_option in numeric_options:
                    name = numeric_option.find('name').text
                    parent = numeric_option.find('parent').text
                    excluded_options = self.get_options(binary_option.find('excludedOptions'))
                    implied_options = self.get_options(binary_option.find('impliedOptions'))
                    self.features[name] = Feature(name, parent, excluded_options, implied_options)

            # Add children
            for feature_name in children_relation.keys():
                self.features[feature_name].children = children_relation[feature_name]

            # TODO: Parse cross-tree constraints?

            # Add alternatives
            for feature_name in self.features.keys():
                if self.is_alternative_group(feature_name):
                    for child in self.features[feature_name].children:
                        other_children = self.features[feature_name].children.copy()
                        other_children.remove(child)
                        self.features[child].alternatives = other_children

            # Decide whether the features are strictly mandatory
            for feature_name in self.features.keys():
                self.features[feature_name].strictly_mandatory = self.is_strictly_mandatory(feature_name)

    def is_alternative_group(self, feature_name: str) -> bool:
        """
        This method checks whether the given feature is the parent of an alternative group or not. An alternative
        group contains only mandatory features and each of the features excludes all others.
        :param feature_name: the name of the parent node
        :return: <code>True</code> iff the given feature is an alternative group
        """
        if feature_name not in self.features.keys():
            print(f"Feature {feature_name} not in feature list!")
            exit(-1)
        feature: Feature = self.features[feature_name]
        if len(feature.children) <= 1:
            return False
        for child in feature.children:
            child_feature: Feature = self.features[child]
            if not child_feature.mandatory:
                return False
            for other_child in feature.children:
                if other_child == child:
                    continue
                if other_child not in child_feature.exclusions:
                    return False
        return True

    def is_strictly_mandatory(self, feature_name: str) -> bool:
        """
        This method decides whether the given feature is strictly mandatory or not.
        :param feature_name: the feature to check
        :return: <code>true</code> iff the feature and all its parents are mandatory and do not belong to an alternative
         group.
        """
        if feature_name not in self.features.keys():
            print(f"Feature {feature_name} not in feature list!")
            exit(-1)
        if feature_name == "root":
            return True
        feature: Feature = self.features[feature_name]
        # A numerical feature (mandatory = None) is also strictly mandatory
        if not feature.binary:
            return True
        if not feature.mandatory:
            return False
        if len(feature.alternatives) > 0:
            return False
        parent = self.features[feature.parent]
        while parent.name != "root":
            if not parent.mandatory or len(parent.exclusions) > 0:
                return False
            parent = self.features[parent.parent]
        return True

    def get_all_feature_names(self) -> List[str]:
        """
        This method returns a list containing all feature names
        :return a list containing all feature names
        """
        feature_names = []
        for feature in self.features:
            feature_names.append(self.features[feature].name)
        return feature_names

    def read_measurements(self, path: str) -> None:
        with open(path, 'r') as measurements_file:
            self.configurations = pd.read_csv(measurements_file, sep=';', lineterminator='\n', dtype=str)
            if self.name in self.Case_Studies_Reverse_Revisions:
                self.configurations = self.configurations.iloc[::-1]
        self.configurations['performance'] = pd.to_numeric(self.configurations['performance'])
        # add a column for the workloads and give each workload a number
        if 'workloads' in self.features.keys():
            self.configurations['workload'] = 0
            workload_parent_feature: Feature = self.features['workloads']
            for i in range(0, len(workload_parent_feature.children)):
                workload_child = self.features[workload_parent_feature.children[i]]
                self.configurations.loc[self.configurations[workload_child.name] == '1', 'workload'] = \
                    workload_child.name

    def read_deviations(self, path: str) -> None:
        with open(path, 'r') as deviation_file:
            self.deviations = pd.read_csv(deviation_file, sep=';', lineterminator='\n', dtype=str)
        self.deviations['performance'] = pd.to_numeric(self.deviations['performance'])
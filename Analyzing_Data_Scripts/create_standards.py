import numpy as np
import os, csv, sys, json
from matplotlib import pyplot as plt
from pin_analysis_tools import *
import pandas as pd
global box_path
box_path = get_box_pathway()
sys.dont_write_bytecode = True
# adds tech dev tool box to path
sys.path.insert(0, box_path + "Engineering\Tech_Dev_Software\PythonDev\TechDevPythonAnalyticsTools")
from tech_dev_python_analytics_tools import *

def main():
    save_directory = box_path + "Engineering\Pin_Analysis\AnalysisData"
    os.chdir(save_directory)
    good_md, bad_md = get_json_file('Good_and_Bad_Json_Data.txt')
    inst_exp_dict = sort_by_instrument(good_md)
    create_standards(inst_exp_dict)


def get_json_file(file_name):
    """
    grab the json file and load it in
    """

    with open(file_name) as json_file:
        data = json.load(json_file)
        good_md = data['GoodCSVs']
        bad_md = data['BadCSVs']
    return good_md, bad_md

def sort_by_instrument(good_md):
    """
    sort the good sets according to instrument
    """
    instrument_listing = []
    inst_exp_dict = {}
    for md_i in good_md:
        temp = md_i['Instrument']
        if temp not in inst_exp_dict.keys():
            inst_exp_dict[temp] = []
            inst_exp_dict[temp].append(md_i['Experiment'])
        else:
            inst_exp_dict[temp].append(md_i['Experiment'])
    return inst_exp_dict

# create standards according to each instrument
def create_standards(inst_exp_dict):
    """
    Takes the dictionary of instrument-experiment listings and takes the average
    Maps average impedances and standard deviations to an experiment set
    """
    df = pd.DataFrame()
    ef = pd.DataFrame()
    number_of_pins = 108
    number_of_trials = 8
    os.chdir(box_path + "Engineering\Pin_Analysis\GoodCSVs")
    for inst in inst_exp_dict.keys():
        # grabs all the experiments related to instrument
        experiments = inst_exp_dict[inst]
        all_pin_trial_averages= np.zeros((number_of_pins,len(experiments)))
        all_pin_trial_std = np.zeros((number_of_pins, len(experiments)))
        for index, exp in enumerate(experiments):
            # gets average for each experiment builds matrix for each instrument set of experiments
            impedance_matrix = np.zeros((number_of_pins,number_of_trials)) # preallocated for space
            myread = read_whole_csv_file(exp, True, unnecessary_lines=[0,1])
            for i_row, row in enumerate(myread):
                float_array = [float(i) for i in row[4:12]]
                impedance_matrix[i_row, :] = float_array
            average_of_trial = np.mean(impedance_matrix, axis=1)
            ef['pin average impedance ' + inst + ' ' + str(index)] = average_of_trial
            std_trial = np.std(impedance_matrix, axis=1)
            all_pin_trial_averages[:,index:index+1] = average_of_trial.reshape((number_of_pins,1))
            all_pin_trial_std[:, index:index+1] = std_trial.reshape((number_of_pins,1))
        df['pin average impedances ' + inst] = np.mean(all_pin_trial_averages, axis=1)
        df['cartridge_to_cartridge_pin_variation ' + inst] = np.std(all_pin_trial_averages, axis=1)
    os.chdir(box_path + "Engineering\Pin_Analysis\AnalysisData")
    df.to_csv('good pin data by instrument.csv')
    ef.to_csv('all good pin data.csv')

main()

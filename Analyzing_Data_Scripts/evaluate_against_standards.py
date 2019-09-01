global pd, np, os, csv, sys, plt, json
import numpy as np
import os, csv, sys, json
from pin_analysis_tools import *
from PinAnalysis import *
sys.dont_write_bytecode = True
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
box_path = get_box_pathway()
# location for saving data files
save_directory = box_path + "Engineering\Pin_Analysis\AnalysisData"
# adds tech dev tool box to path
sys.path.insert(0, box_path + "Engineering\Tech_Dev_Software\PythonDev\TechDevPythonAnalyticsTools")
from tech_dev_python_analytics_tools import *

def set_boundaries(**kwargs):
    """
    Go through each instument and create a lower and upper cutoff based on cartridge to cartridge_to_cartridge_pin_variation
    """

    if 'num_stds' not in kwargs:
        kwargs['num_stds'] = [5,10]

    # Read in data set averages
    os.chdir(box_path + "Engineering\Pin_Analysis\AnalysisData")
    df = pd.read_csv('good pin data by instrument.csv')
    odf_keys = list(df)
    # take each key in order and get average and pin variation
    instrument_list = []
    for key in odf_keys:
        if 'average' in key:
            split_key = key.split(' ')
            instrument_list.append(split_key[-1])
            #df['Upper Bound ' + split_key[-1]] = df[key] + kwargs['num_stds'][0]*df['cartridge_to_cartridge_pin_variation ' + split_key[-1]]
            df['Lower Bound ' + split_key[-1]] = df[key] - kwargs['num_stds'][1]*df['cartridge_to_cartridge_pin_variation ' + split_key[-1]]
    return df, instrument_list

def evaluate_csvs(df, md_by_inst, add_path, histogram_name):

    os.chdir(box_path + add_path)
    number_of_pins = 108
    number_of_trials = 8

    z_score = pd.DataFrame()

    for inst in md_by_inst.keys():
        # go through each experiment in instrument set
        experiments = md_by_inst[inst]
        all_exp = []
        for i_file in experiments:
            all_exp.append(i_file)
            impedance_matrix = np.zeros((number_of_pins,number_of_trials))
            myread = read_whole_csv_file(i_file, True, unnecessary_lines=[0,1])
            for i_row, row in enumerate(myread):
                float_array = [float(i) for i in row[4:12]]
                impedance_matrix[i_row, :] = float_array
            df['Average Trial ' + i_file] = np.mean(impedance_matrix, axis=1)
            df['Lower Bounds Failure ' + i_file] = df['Average Trial ' + i_file]<df['Lower Bound ' + inst]
            #df['Upper Bounds Failure '+ i_file] = df['Average Trial ' + i_file]>df['Upper Bound ' + inst]

            z_score['Z score ' + i_file] = (df['Average Trial ' + i_file]-df['pin average impedances ' + inst])/df['cartridge_to_cartridge_pin_variation ' + inst]
            df['Z score ' + i_file] = z_score['Z score ' + i_file]
            plt.hist(z_score['Z score ' + i_file], bins=np.arange(-70,10, 0.5))
            boolean_array = (df['Average Trial ' + i_file]<df['Lower Bound ' + inst]) #| (df['Average Trial ' + i_file]>df['Upper Bound ' + inst])
            failed_pins = []
            for index, i in enumerate(boolean_array):
                if i:
                    failed_pins.append(index+9)
            df['Failed Pins ' + i_file] = pd.Series(failed_pins)

        plt.xlabel('z score')
        plt.ylabel('Number of instances')
        plt.title('Z Score of ' + histogram_name + 'Cartridges on Instrument ' + inst)
        plt.legend(all_exp)
        os.chdir(save_directory)
        plt.savefig(histogram_name + ' ' + inst)
        os.chdir(box_path+add_path)
        plt.clf()
    return df, z_score

def plot_pin_distribution(pin_number, df, histogram_name):
    column_frames = list(df)
    temp = []
    for column_frame in list(df):
        if "Average Trial" in column_frame:
            temp.append(df.loc[pin_number-9, column_frame])
    plt.hist(temp)
    plt.xlabel('Impedance')
    plt.ylabel('Number of instances')
    plt.title('Impedance Distribution of Pin ' + str(pin_number))
    plt.savefig(histogram_name + " " + str(pin_number))
    plt.clf()

def main():
    df, instrument_list = set_boundaries(num_stds=[5,10])

    # grabs the metadata of the bad trials
    good_md, bad_md = get_json_file('Good_and_Bad_Json_Data.txt')
    bad_md_list = sort_by_instrument(bad_md)
    df.to_csv('Bounds&Averages.csv')
    df, z_score = evaluate_csvs(df, bad_md_list, "Engineering\Pin_Analysis\BadCSVs", "bad")
    good_md_list = sort_by_instrument(good_md)
    df, z_score = evaluate_csvs(df, good_md_list, "Engineering\Pin_Analysis\GoodCSVs", "good")
    os.chdir(save_directory)
    #plot_pin_distribution(35,df, "Distribution of Pin")
    df.to_csv('All Relevant Data.csv')
    z_score.to_csv('Z Scores.csv')

main()

def set_metadata(path_ontop_box, dict_key):
    """
    path_ontop_box - box + this path will be the desired path to create all meta data
    dict_key - key for json dictionary that this set will be associated with
    """
    # adds tech dev tool box to path
    save_directory = box_path + path_ontop_box
    os.chdir(save_directory)
    my_json_data[dict_key] = []
    for index, i_file in enumerate(os.listdir(os.getcwd())):
        if index==0:
            meta_data_parameters = read_whole_csv_file(i_file, False, desired_lines=[0])
        temp_dict = {}
        temp_lane = read_whole_csv_file(i_file, False, desired_lines=[1])
        for index, key in enumerate(meta_data_parameters[0]):
            temp_dict[key] = temp_lane[0][index]
            temp_dict['Experiment'] = i_file
        my_json_data[dict_key].append(temp_dict)

def write_to_json(filename, json_data):
    """
    filename - (str) file you want to name the json file
    json_data - (json data) in json format of dictionary with option to list inside dictionary
    """
    with open(filename,'w') as outfile:
        json.dump(json_data, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

def main():
    global my_json_data
    my_json_data = {}
    set_metadata('Engineering\Pin_Analysis\BadCSVs', 'BadCSVs')
    set_metadata('Engineering\Pin_Analysis\GoodCSVs', 'GoodCSVs')
    os.chdir(box_path+"Engineering\Pin_Analysis\AnalysisData")
    write_to_json('Good_and_Bad_Json_Data.txt', my_json_data)

global json, os, sys
import json, os, sys
from pin_analysis_tools import *
global box_path
box_path = get_box_pathway()
sys.dont_write_bytecode = True
sys.path.insert(0, box_path + "Engineering\Tech_Dev_Software\PythonDev\TechDevPythonAnalyticsTools")
from tech_dev_python_analytics_tools import *

main()

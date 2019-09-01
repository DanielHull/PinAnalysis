'''
Developer: Daniel Hull dhull@baebies.com
Plese reach out with any questions or points of improvement
Copyright Baebies 2018
See Readme for additional details
'''

import argparse
DESC = 'CLI tool for utilizing CheckPins class and flagging bad cartridges'
USAGE = '''
Basic Usage:
    local_log_file (str) log file of magnitude cartridge data
    normal_dataset_csv (str) name of csv file for normal dataset
    source_location (str) name of the location of the log file AND normal data set
    e.g.
    python thrombophilia_functional_analytics.py "" "ATIIIFluorescenceFilerun6183" ATIII --af_ff_save_location "C:\Users\dhall\Box Sync\Engineering\Boston_Project\Software\\thrombophilia_back_end\\sample_data_folder" --tf_save_location "C:\Users\dhall\Box Sync\Engineering\Boston_Project\Software\thrombophilia_back_end\sample_data_folder\results"
'''

parser = argparse.ArgumentParser(description=DESC, usage=USAGE)
parser.add_argument('normal_dataset_csv', type=str)
parser.add_argument('source_location', type=str)
parser.add_argument('--results_location', type=str, default="C:\Program Files (x86)\Application Development Environment\\results")
args = parser.parse_args()

from check_pins import *
cp_object = CheckPins(args.source_location, args.normal_dataset_csv)
cp_object.grab_analyze_logfile(args.results_location)
cp_object.check_impedances()
cp_object.user_prompt()

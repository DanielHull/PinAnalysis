from pin_analysis_tools import *
import numpy as np
import sys, os
global sys, os, np
global box_path
box_path = get_box_pathway()
sys.dont_write_bytecode = True
# adds tech dev tool box to path (requirement)
sys.path.insert(0, box_path + "Engineering\Tech_Dev_Software\PythonDev\TechDevPythonAnalyticsTools")
from tech_dev_python_analytics_tools import *
from check_pins import *

def test_grab_analyze_logfile():
    # take a log file and check to make sure its averaging properly
    cp = CheckPins("C:\Users\dhall\Box Sync\\Engineering\\Pin_Analysis\\test_folder", "10045_GoodDataSet.csv")
    cp.grab_analyze_logfile("C:\Users\dhall\Box Sync\Engineering\Pin_Analysis\\test_folder\\results")
    os.chdir(box_path + "Engineering\\Pin_Analysis\\test_folder")
    my_read = read_whole_csv_file('average_from_test_file.csv', True)
    read = my_read[0]
    read = read.astype(float)
    np.testing.assert_array_almost_equal(read, cp.average_of_trial)

def test_check_impedances():
    # take a bad csv file and check to make sure it fails
    cp = CheckPins("C:\Users\dhall\Box Sync\\Engineering\\Pin_Analysis\\test_folder", "10045_GoodDataSet.csv")
    cp.grab_analyze_logfile("C:\Users\dhall\Box Sync\Engineering\Pin_Analysis\\test_folder\\results")
    cp.check_impedances()
    assert cp.high_risk_dictionary.keys() == [8, 41, 28]

def test_user_prompt():
    cp = CheckPins("C:\Users\dhall\Box Sync\\Engineering\\Pin_Analysis\\test_folder", "10045_GoodDataSet.csv")
    cp.grab_analyze_logfile("C:\Users\dhall\Box Sync\Engineering\Pin_Analysis\\test_folder\\results")
    cp.check_impedances()
    cp.user_prompt()
    cp = CheckPins("C:\Users\dhall\Box Sync\\Engineering\\Pin_Analysis\\test_folder", "10045_GoodDataSet.csv")
    cp.grab_analyze_logfile("C:\Users\dhall\Box Sync\Engineering\Pin_Analysis\\test_folder\\results_good")
    cp.check_impedances()
    cp.user_prompt()

def main():
    test_grab_analyze_logfile()
    test_check_impedances()
    test_user_prompt()

main()

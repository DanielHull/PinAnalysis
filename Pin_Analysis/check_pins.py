'''
Developer: Daniel Hull dhull@baebies.com
Plese reach out with any questions or points of improvement
Copyright Baebies 2018
See Readme for additional details
'''


class CheckPins:
    def __init__(self, source_location, normal_set_file):
        from pin_analysis_tools import read_whole_csv_file
        import sys, os, csv
        import numpy as np
        global box_path, sys, os, csv, np, read_whole_csv_file    # adds tech dev tool box to path (requirement)
        sys.dont_write_bytecode = True
        self.source_location = source_location
        self.normal_set_file = normal_set_file

    def grab_analyze_logfile(self, results_directory):
        """
        grabs log file from the most recent ADE run
        Assumptions: the log file is an impedance report, magnitude only
        Inputs:
            self
            results_directory - location of the results file (usually default on all systems)
        Returns:
            average_of_trial (numpy array) - averaged data from magnitude log file
        """

        # grabs log file from said folder, most recent file on most recent date
        os.chdir(results_directory)
        current_directory_contents = os.listdir(os.getcwd())
        most_recent_date = current_directory_contents[-1]
        os.chdir(results_directory+'\\'+most_recent_date)
        files = os.listdir(os.getcwd())
        results_file_csv = files[-1]
        self.log_name = results_file_csv

        # analyzes and averages magnitudes of pin impedance
        number_of_pins = 108
        average_of_trial = []
        myread = read_whole_csv_file(self.log_name, True, unnecessary_lines=[0])
        for i_row, row in enumerate(myread):
            average_of_trial.append(row[3])
        average_of_trial = np.array(average_of_trial)
        average_of_trial = average_of_trial.astype(float)
        self.average_of_trial = average_of_trial

    def check_impedances(self):
        """
        takes pin averages and finds the to date average pin file
        Assumptions: data file is under the source_location
        Inputs: self
        Attributes added:
            high_risk_dictionary, medium_risk_dictionary - dictionaries linking pins to z scores
        """

        # goes to location of normal set, takes average and std of each pin
        os.chdir(self.source_location)
        my_read = read_whole_csv_file(self.normal_set_file, True)
        my_read = my_read.astype(float)
        normal_set_averages = np.mean(my_read, axis=0)
        normal_set_std = np.std(my_read, axis=0)

        # calculates z score and finds pins and isolates what is risky
        z_scores = (self.average_of_trial-normal_set_averages)/normal_set_std
        high_risk_dictionary = {}
        medium_risk_dictionary = {}
        for index, score in enumerate(z_scores):
            if score < -10.0:
                high_risk_dictionary[index] = score
            elif score >= -10.0 and score <= -5.0:
                medium_risk_dictionary[index] = score
        self.high_risk_dictionary = high_risk_dictionary
        self.medium_risk_dictionary = medium_risk_dictionary

    def user_prompt(self):
        """
        notify user of any issues via a prompt
        """
        print "Welcome to the cartridge pin test, we hope you feel taken care of"
        print "Please report any issues to Daniel Hull via Slack"
        raw_input("Please press enter to begin: ")
        if not self.high_risk_dictionary and not self.medium_risk_dictionary:
            print "Congratulations, there are no pins that fail this test, please proceed"
            os.chdir(self.source_location)
            with open(self.normal_set_file, 'ab') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.average_of_trial)
            raw_input("Please press enter to exit test: ")
        else:
            print "There are some pins that MAY be of concern"
            print "If there are high risk pins, please do not proceed with this cartridge"
            print "If there are medium risk pins, you should proceed but evaluate"
            adjusted_keys = map(lambda x:x+9, self.medium_risk_dictionary.keys())
            print "The following medium risk pins are "
            print adjusted_keys
            print "Their corresponding z scores are "
            print self.medium_risk_dictionary.values()

            adjusted_keys = map(lambda x:x+9, self.high_risk_dictionary.keys())
            print "The following are high risk pins "
            print adjusted_keys
            print "Their corresponding z scores are "
            print self.high_risk_dictionary.values()
            raw_input("Please press enter to exit test: ")

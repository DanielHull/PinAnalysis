def read_whole_csv_file(csvfile, numpy_option, **kwargs):
    """
    Reads whole of csv file and returns it
    Input: csvfile - csvfile as a string
    numpy_option - (bool) option to read in as a numpy matrix
    Returns:
    data_file_info - data set list of a lists, iterative by line of file (i.e. data_file_info[0] = row one)
    """
    import csv
    import numpy as np
    import sys
    sys.dont_write_bytecode = True
    # handles forgetting to type .csv
    if len(csvfile.split('.'))==1:
        csvfile = csvfile + '.csv'
    data_file_info = []
    if 'desired_lines' in kwargs:
        lines = kwargs['desired_lines']
        with open(csvfile, 'rb') as csvfile:
            myread = csv.reader(csvfile)
            for index, row in enumerate(myread):
                if index in lines:
                    data_file_info.append(row)
    else:
        with open(csvfile, 'rb') as csvfile:
            myread = csv.reader(csvfile)
            for index, row in enumerate(myread):
                data_file_info.append(row)

    if 'unnecessary_lines' in kwargs:
        lines = kwargs['unnecessary_lines']
        lines = sorted(lines, reverse=True)
        for line in lines:
            del data_file_info[line]

    if numpy_option is True:
        data_file_info = np.array(data_file_info)
    return data_file_info

def get_box_pathway():
    """
    Returns the user profile and box pathway, quite useful for variations in whether Box or Box Sync is downloaded locally and testing on multiple devices
    Assumes Box and Box Sync are downloaded to default pathway of the USERPROFILE

    Inputs: n/a
    Returns:
    (str) pathway with slashes for appending
    """
    import os
    import sys
    sys.dont_write_bytecode = True
    user_env = os.environ['USERPROFILE']
    os.chdir(user_env)
    directory_list = os.listdir(user_env)
    Box_boolean = 'Box' in directory_list
    Box_Sync_boolean = 'Box Sync' in directory_list
    if Box_boolean is False and Box_Sync_boolean is False:
        raise ValueError('Box or Box Sync is not in your pathway')
    elif Box_boolean is True and Box_Sync_boolean is True:
        raise ValueError('Program does not know whether to distinguish Box or Box Sync')
    else:
        if Box_boolean is True:
            return user_env + '\Box\\'
        elif Box_Sync_boolean is True:
            return user_env + '\Box Sync\\'

# To Do:

# - Add file name checking to csv_dict_save_single_row and file picker 
# - Add file name entry for load_sbv
# - Add paramater to file saves to check if want a timestamp created

# - To fix:

# - get_headings_fname_load crashes if correct file name not provided


import csv
import os
import sys
import time
import tkinter as tk
from tkinter import filedialog


def check_review_warnings():
    """Check if user wants to review warning messages.

    Returns:
        True if user wants to review warning messages, False otherwise.
    """
    review = ''
    while review == '':
        review = input('\nDo you want to view the warning messages? y/n --> ')
        if review.lower() not in ['y', 'n']:
            print('\n\'{}\' is not a valid answer! Please try again.'.format(
                    review))
            review = ''
        elif review.lower() == 'y':
            return True
        else:
            return False

'''
def check_save_csv(some_data):
    save_data_response = ''
    while save_data_response == '':
        save_data_response = input('\nDo you want to save the changes? y/n: ')
        if save_data_response.lower() not in ('y', 'n'):
            print('\nThat is not a valid response. Please try again.')
            save_data_response = ''
        elif save_data_response.lower() == 'y':
            # Function call to get file name (file_name = function() etc)
            # file_name = 
            # Function call to save file using file_name
        else:
            print('\nThe updated data has not been saved.')
    return
'''

def csv_dict_save_file(file_data, file_name, headings):
    """Save a dictionary to a CSV file.
    
    If the file already exists, the user is asked to confirm that they wish to
    overwrite the existing file. Note that the values must be tuples.
    
    Args:
        file_data (dict): Data to be saved.
        file_name (str): Name of file to save to.
        headings (list): Column headings to be saved.
    """
    # Check that the file can be saved to
    file_available = False
    over = False
    while not file_available:
        # Check if file already exists (True means it does)
        file_exists = os.path.isfile(file_name)
        # Override if the user has selected to overwrite the file
        if over:
            file_exists = False
        if file_exists:  # File already exists
            overwrite = input('{} already exists! Do you want '
                              'to overwrite it? y/n: '.format(file_name))
            if overwrite.lower() not in ['y', 'n']:
                print('\n\'{}\' is not a valid answer! Please try again.'
                      .format(overwrite))
                overwrite = ''
            elif overwrite.lower() == 'y':
                over = True
            else:
                file_name = input('Please enter a new file name: ') + '.csv'
        else:
            try:
                open(file_name, 'w')
            except IOError:
                print('The file \'{}\' is not accessible. Please check the '
                      'file name.'.format(file_name))
                file_name = input('\nWhat file would you like to save to')
                + '.csv'
            else:
                with open(file_name, 'w', newline='') as csv_file:
                    headingWriter = csv.DictWriter(csv_file,
                                                   fieldnames=headings)
                    headingWriter.writeheader()
                    writer = csv.writer(csv_file)
                    writer.writerows((k,) + v for k, v in file_data.items())
                    print('\nThe output file has been saved to {}'.format(
                            file_name))
                    file_available = True
    return


def csv_dict_save_multiple_rows(data, headings, f_name):
    """Save a dictionary to a single line in a csv file.
    
    Keys are saved as the heading row and values are saved to the second row.
    Note that only works for dictionaries where each value is a single item.
    f_name must end in '.csv'
    
    Args:
        data (dict): Dictionary data to be saved to csv.
        headings (list): Headings to use for each column.
        f_name (str): Name to save file to. Must end in '.csv'
    """
    with open(f_name, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(headings)
        for key, value in data.items():
            w.writerow([key, value])


def csv_dict_save_single_row(data, f_name):
    """Save a dictionary to a single line in a csv file.
    
    Keys are saved as the heading row and values are saved to the second row.
    Note that only works for dictionaries where each value is a single item.
    f_name must end in '.csv'
    
    Args:
        data (dict): Dictionary data to be saved to csv.
        f_name (str): Name to save file to. Must end in '.csv'
    """
    with open(f_name, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(data.keys())
        w.writerow(data.values())


def generate_time_string():
    """Generate a timestamp for file names.

    Returns:
        time_str (str): String of timestamp in the format yymmdd-hhmmss.
    """
    time_str = time.strftime('%y%m%d-%H%M%S')
    return time_str


def get_csv_fname_load(ftype):
    """Gets a file name and then loads the CSV data.
    
    Gets a file name that is entered. If the user has just hit enter then the
    file picker is opened. File is then loaded using CSV loader and returned.
    
    Args:
        ftype (str) Type of file to be loaded. Should end with 'File'.
    
    Returns:
        loaded_data (list): Loaded CSV data returned in a list format.
    """
    f_name = input('\nEnter the name of the {} to be processed. Alternatively'
                   ', hit enter to open the open file dialog or type '
                   '\'quit\' to exit the app --> '.format(ftype))
    if f_name in (None, ''): # Open file picker dialog
        f_name = get_load_file_name_picker()
        print('\nLoading {}...'.format(ftype))
        loaded_data = load_csv(f_name, 'p')
        print('\rLoaded {}.'.format(ftype))
    elif f_name.lower() == 'quit': # Exit
        sys.exit()
    else:
        print('\nLoading {}...'.format(f_name))
        loaded_data = load_csv(f_name, 'e')
        print('\nLoaded {}.'.format(f_name))
    return loaded_data


def get_headings_fname_load(ftype):
    """Gets a headings file name and then loads the text data into a list.
    
    Gets a file name that is entered. If the user has just hit enter then the
    file picker is opened. Text file is loaded with comma separated values into
    a list and returns the list. File contents should be one line of comma
    separated values.
    
    Args:
        ftype (str): Type of headings file to be loaded. Should end with 
        'File'.
        
    Returns:
        headings (list): List with each column heading being one item.
    """
    f_name = input('\nEnter the name of the {} to be processed. Alternatively'
                   ', hit enter to open the open file dialog or type '
                   '\'quit\' to exit the app --> '.format(ftype))
    if f_name in (None, ''): # Open file picker dialog
        f_name = get_load_file_name_picker()
        print('\nLoading {}...'.format(ftype))
        # Check correct file before trying to load
        with open(f_name, 'r') as myfile:
            data = myfile.read()
        print('\rLoaded {}.'.format(ftype))
    else:
        print('\nLoading {}...'.format(f_name))
        # Check correct file before trying to load
        with open('{}{}'.format(f_name, '.txt'), 'r') as myfile:
            data = myfile.read()
        print('\nLoaded {}.'.format(f_name))
    # Convert headings string into a list
    headings = data.strip().split(",")
    # print(headings)
    return headings


def get_load_file_name():
    """Get the name of the file to be loaded.
    
    Returns:
        file_name (str): Name of file to be loaded.
    """
    file_name = ''
    valid_file = False
    while not valid_file:
        file_name = input('What file would you like to load with the '
                          'student data? ')
        try:
            f = open(file_name + '.csv', 'r')
        except IOError:
            print('\nSorry, \'{}{}\' does not exist. Please try again.'.format(
                    file_name, '.csv'))
        else:
            valid_file = True
    return file_name


def get_load_file_name_picker():
    """Get the name of the file to be loaded.
    
    Opens a file picker for user to locate the desired file.
    
    Returns:
        file_name (str): Name of the file.
    """
    root = tk.Tk()
    root.withdraw()
    curr_directory = os.getcwd()
    file_path = filedialog.askopenfilename(initialdir = curr_directory)
    return file_path


def get_sbv_fname_load(ftype):
    """Gets a file name and then loads the sbv data.
    
    Gets a file name that is entered. If the user has just hit enter then the
    file picker is opened. File is then loaded using sbv loader and returned.
    
    Args:
        ftype (str) Type of file to be loaded. Should end with 'File'.
    
    Returns:
        loaded_data (list): Loaded sbv data returned in a list format.
    """
    f_name = input('\nEnter the name of the {} to be processed. Alternatively'
                   ', hit enter to open the open file dialog or type '
                   '\'quit\' to exit the app --> '.format(ftype))
    if f_name in (None, ''): # Open file picker dialog
        f_name = get_load_file_name_picker()
        print('\nLoading {}...'.format(ftype))
        loaded_data = load_sbv(f_name)
        print('\rLoaded {}.'.format(ftype))
    elif f_name.lower() == 'quit': # Exit
        sys.exit()
    else:
        print('\nLoading {}...'.format(f_name))
        loaded_data = load_sbv(f_name)
        print('\nLoaded {}.'.format(f_name))
    return loaded_data


def load_csv(file_name, method='p'):
    """Read data from a csv file.
    
    Attempts to load a passed CSV file name. If the file does not exist it will
    ask for a new file name. If method='e' the user will be asked to enter
    text, if the method='p' the file picker will be open so they can navigate
    to the file.

    Args:
        file_name (str): The name of the file to be read.
        method (str): Method for getting a new file name:
            - 'e': User enters name (file must be in present working directory)
            - 'p': File picker will open so user can navigate to file.

    Returns:
        read_data (list): A list containing the data read from the file.
    """
    read_data = []
    # Check that file exists
    valid_file = False
    while not valid_file:
        if method == 'e':
            try:
                file = open(file_name + '.csv', 'r')
            except IOError:
                print('\nSorry, \'{}{}\' does not exist. Please try again'
                      '.'.format(file_name, '.csv'))
                file_name = input('What is the name of the file? --> ')
            else:
                file.readline()
                reader = csv.reader(file, delimiter=',', quotechar='"')
                for row in reader:
                    if row[0] not in (None, ''):
                        read_data.append(row)
                file.close()
                valid_file = True
        elif method == 'p':
            try:
                file = open(file_name, 'r')
            except IOError:
                print('\nSorry, \'{}\' does not exist. Please try again'
                      '.'.format(file_name))
                file_name = get_load_file_name_picker()
            else:
                file.readline()
                reader = csv.reader(file, delimiter=',', quotechar='"')
                for row in reader:
                    if row[0] not in (None, ''):
                        read_data.append(row)
                file.close()
                valid_file = True 
        else:
            return
    return read_data


def load_headings(f_name, method='p'):
    """Load a headings text file into a list.
    
    Attempts to load a passed text file name. If the file does not exist it
    will ask for a new file name. If method='e' the user will be asked to enter
    text, if the method='p' the file picker will be open so they can navigate
    to the file. The file should be a single line of comma separated values
    stored in a text file.

    Args:
        file_name (str): The name of the file to be read.
        method (str): Method for getting a new file name:
            - 'e': User enters name (file must be in present working directory)
            - 'p': File picker will open so user can navigate to file.

    Returns:
        read_data (list): A list containing the data read from the file.
    """
    valid_file = False
    while not valid_file:
        if method == 'e':
            try:
                file = open('{}{}'.format(f_name, '.txt'), 'r')
            except IOError:
                print('\nSorry, \'{}{}\' does not exist. Please try again'
                      '.'.format(f_name, '.txt'))
                f_name = input('What is the name of the file? --> ')
            else:
                with open('{}{}'.format(f_name, '.txt'), 'r') as myfile:
                    read_data = myfile.read()
                valid_file = True
        elif method == 'p':
            try:
                file = open(f_name, 'r')
            except IOError:
                print('\nSorry, \'{}\' does not exist. Please try again'
                      '.'.format(f_name))
                f_name = get_load_file_name_picker()
            else:
                with open('{}'.format(f_name), 'r') as myfile:
                    read_data = myfile.read()
                valid_file = True
        else:
            return
    # Convert headings string into a list
    read_data = read_data.strip().split(",")
    return read_data


'''
def load_csv_picker(file_name):
    """Read data from a csv file.
    
    Reads data provided from a file picker. If the file is not a valid CSV file
    the user is asked to pick another file using the picker.

    Args:
        file_name (str): The name of the file to be read.

    Returns:
        read_data (list): A list containing the data read from the file.
    """
    read_data = []
    # Check that file exists
    valid_file = False
    while not valid_file:
        try:
            file = open(file_name, 'r')
        except IOError:
            print('\nSorry, \'{}\' does not exist. Please try again.'.format(
                    file_name))
            file_name = get_load_file_name_picker()
        else:
            file.readline()
            reader = csv.reader(file, delimiter=',', quotechar='"')
            for row in reader:
                if row[0] not in (None, ''):
                    read_data.append(row)
            file.close()
            valid_file = True
    return read_data
'''


def load_sbv(load_name):
    """Read the contents of an sbv file used for captions.

    Args:
        loadName (str): Name of the file to load.

    Returns:
        captionsList (list): List of captions read from file.
    """
    captionsList = []
    valid_file = False
    while not valid_file:
        print('Opening file')
        try:
            FO = open('{}'.format(load_name), 'r')
        except IOError:
            print('The file does not exist. Check file name.')
            load_name = input('What is the name of the file? ')
        else:
            for line in FO:
                captionsList.append(line.strip())
            FO.close()
            print("File is loaded\n")
            valid_file = True
    return captionsList


def process_error_log(errors, source):
    """Process an Error log.

    Prints a list of fatal errors in the source data. Saves the errors to file
    and then exits the program.

    Args:
        errors (list): List of errors found in the source data.
        source (str): The name of the source data.
    """
    print('\nThe following errors have been identified in the {} data: \n'
          .format(source))
    for line in errors:
        print(line)
    current_time = generate_time_string()
    error_file = 'Error_log_{}{}'.format(current_time, '.txt')
    save_error_log(source, errors, error_file)
    print('The program will now close. Please correct errors before'
          ' trying again.')
    input('Press enter key to exit. ')
    raise SystemExit
    

def process_warning_log(warnings, required):
    """Process a Warnings log.

    If required, prints a list of non-fatal errors in the source data. Saves
    the errors to file. If it is not required (e.g. there has not been any data
    appended to the warnings list) then the function returns without any
    action.

    Args:
        warnings (list): List of errors or potential issues found in the source
        data.
        required (str): If True the function will run, if False then it is
        skipped.
    """
    if not required:
        return
    print('\nThere were errors found in one or more of the data sources. '
          'You should check these errors and correct if necessary before '
          'using the generated files. If you correct the files, it is '
          'recommended that you run this program again to generate new '
          'output files from the correct data.')
    # See if user wants warnings displayed on screen
    review = check_review_warnings()
    if review:
        for line in warnings:
            print(line)
    # Save the warnings to a text file
    current_time = generate_time_string()
    warning_file = 'Warning_log_{}{}'.format(current_time, '.txt')
    save_warning_log(warnings, warning_file)


def save_data_csv(i_data, headings, d_name):
    """Save data to a csv file.
    
    Generates a time string for the file name. d_name just needs to be the name
    of the file without a time string to make it unique. d_name should not have
    the csv extension as this is added by this function. d_name should end with
    a '_'.
    
    Args:
        i_data (list): Data that is to be written to file.
        headings (list): Headings to be written to the file.
        d_name (str): Name of the file to be saved.
    """
    current_time = generate_time_string()
    f_name = '{}{}{}'.format(d_name, current_time, '.csv')
    errors = []
    try:
        open(f_name, 'w')
    except IOError:
        errors.append('Unable to save {} data. Please try again.'.format
                      (d_name))
        message = 'Saving_{}'.format(d_name)
        process_error_log(errors, message)
    else:
        with open(f_name, 'w', newline='') as csv_file:
            headingWriter = csv.DictWriter(csv_file,
                                           fieldnames=headings)
            headingWriter.writeheader()
            writer = csv.writer(csv_file)
            for item in i_data:
                writer.writerows([item])
        print('\n{} has been saved to {}'.format(d_name, f_name))


def save_data_csv_table(i_data, headings, d_name):
    """Save to csv file data required to make a table.
    
    Saves data that is required to make a table. The file name is returned so
    that it can then be loaded. The saved data is for use within the app rather
    than for future storage and retrieval by the user.

    Args:
        i_data (list): Data that is to be written to file.
        headings (list): Headings to be written to the file.
        d_name (str): Name of the file to be saved.
    
    Returns:
        f_name (str): Name of the saved file.
    """
    current_time = generate_time_string()
    f_name = '{}{}{}'.format(d_name, current_time, '.csv')
    errors = []
    try:
        open(f_name, 'w')
    except IOError:
        errors.append('Unable to save {} data. Please try again.'.format
                      (d_name))
        message = 'Saving_{}'.format(d_name)
        process_error_log(errors, message)
    else:
        with open(f_name, 'w', newline='') as csv_file:
            headingWriter = csv.DictWriter(csv_file,
                                           fieldnames=headings)
            headingWriter.writeheader()
            writer = csv.writer(csv_file)
            for item in i_data:
                writer.writerows([item])
    return f_name


def save_error_log(source, error_log, file_name):
    """Save to file the error log.

    Args:
        source (str): Name of the source file or data.
        error_log (list): The errors to be written.
        file_name (str): Name to save the file to.
    """
    try:
        open(file_name, 'w')
    except IOError:
        print('Error log could not be saved as \'{}\' is not accessible.'
              .format(file_name))
    else:
        FO = open(file_name, 'w')
        FO.write(str(source) + '\n')
        for line in error_log:
            FO.write(str(line) + '\n')
        FO.close()
        print('Error log has been saved to {}'.format(file_name))


def save_list_csv(i_data, headings, d_name):
    """Save a list to a csv file.
    
    Generates a time string for the file name. d_name just needs to be the name
    of the file without a time string to make it unique. d_name should not have
    the csv extension as this is added by this function. d_name should end with
    a '_'.

    Args:
        i_data (list): Data that is to be written to file.
        headings (list): Headings to be written to the file.
        d_name (str): Name of the file to be saved.

    Requires:
        genterate_time_string() to be imported from this package.
        csv to be imported.
    """
    current_time = generate_time_string()
    f_name = '{}{}{}'.format(d_name, current_time, '.csv')
    errors = []
    try:
        open(f_name, 'w')
    except IOError:
        errors.append('Unable to save {} data. Please try again.'.format(
                d_name))
        message = 'Saving_{}'.format(d_name)
        process_error_log(errors, message)
    else:
        with open(f_name, 'w', newline='') as csv_file:
            headingWriter = csv.DictWriter(csv_file,
                                           fieldnames=headings)
            headingWriter.writeheader()
            writer = csv.writer(csv_file)
            for item in i_data:
                writer.writerows([item])
        print('{} has been saved to {}'.format(d_name, f_name))


def save_list_to_text(data_list, file_name):
    """Save list to a text file.

    Saves a list to a text file using a user-provided file name. Checks if the
    file already exists and checks if user wishes to override it.

    Args:
        data_list (list): List containing the captions.
        file_name (str): Name to save the file to. Include '.txt' in the name.
    """
    file_available = False
    over = False
    while not file_available:
        # Check if file already exists (True means it does)
        file_exists = os.path.isfile(file_name)
        # Override if the user has selected to overwrite the file
        if over:
            file_exists = False
        if file_exists:  # File already exists
            overwrite = input('\'{}\' already exists! Do you want to overwrite'
                              ' it? y/n: '.format(file_name))
            if overwrite.lower() not in ['y', 'n']:
                print('\n\'{}\' is not a valid answer! Please try again.'
                      .format(overwrite))
                overwrite = ''
            elif overwrite == 'y':
                over = True
            else:
                file_name = input('Please enter a new file name: ') + '.txt'
        else:
            try:
                open(file_name, 'w')
            except IOError:
                print('\'{}\' is not accessible. Please check the file name.')
                file_name = input('\nWhat file would you like to save to? --> '
                                  ) + '.txt'
            else:
                FO = open(file_name, 'w')
                for line in data_list:
                    FO.write(str(line) + '\n')
                FO.close()
                print('\n{} is saved.'.format(file_name))
                file_available = True


def save_list_to_text_single(data_list, headings, file_name):
    """Save list to a single line in a text file.

    Saves a list to a text file using a user-provided file name. Checks if the
    file already exists and checks if user wishes to override it. Saves the
    entire list to one line and includes a header row at the top. If headings
    is empty, heading row is not included.
    
    If file name is provided, it must have .txt at the end of it.
    To not use headings, a headings value of '' should be passed.
    Function will save the file without a comma at the end of the line.

    Args:
        data_list (list): List containing the captions.
        headings (str): Headings to be included.
        file_name (str): Name to save the file to.
    """
    file_available = False
    over = False
    while not file_available:
        # Check if file already exists (True means it does)
        file_exists = os.path.isfile(file_name)
        # Override if the user has selected to overwrite the file
        if over:
            file_exists = False
        if file_exists:  # File already exists
            overwrite = input('\'{}\' already exists! Do you want to overwrite'
                              ' it? y/n: '.format(file_name))
            if overwrite.lower() not in ['y', 'n']:
                print('\n\'{}\' is not a valid answer! Please try again.'
                      .format(overwrite))
                overwrite = ''
            elif overwrite == 'y':
                over = True
            else:
                file_name = input('Please enter a new file name: ') + '.txt'
        else:
            try:
                open(file_name, 'w')
            except IOError:
                print('\'{}\' is not accessible. Please check the file name.')
                file_name = input('\nWhat file would you like to save to? --> '
                                  ) + '.txt'
            else:
                FO = open(file_name, 'w')
                if headings not in (None, ''):
                    FO.write(str(headings) + '\n')
                # Print first item
                first = data_list.pop(0)
                FO.write(str(first))
                # Print subsequent items with a leading comma
                for line in data_list:
                    FO.write(',' + str(line))
                FO.close()
                print('\n{} is saved.'.format(file_name))
                file_available = True


def save_lists_to_text(i_data, headings, d_name):
    """Save list of lists to text file.

    Saves a list of comma separated items to a text file, with one list per
    line. Used for saving a list of lists with one list per line. Uses a
    generated timestamp in the file name.

     Args:
        i_data (list): Data that is to be written to file.
        headings (str): Headings to be written to the file.
        d_name (str): Name of the file to be saved.
    """
    current_time = generate_time_string()
    f_name = '{}{}.txt'.format(d_name, current_time)
    file_available = False
    while not file_available:
        try:
            open(f_name, 'w')
        except IOError:
            print('\'{}\' is not accessible. Try a different file name.')
            f_name = input('\nWhat file would you like to save to? --> ')
            + '.txt'
        else:
            f = open(f_name, "w")
            f.write(headings + '\n')
            save_data = ''
            for item in i_data:
                line = ''
                for element in item:
                    line = line + element + ','
                # Remove final comma
                line_to_save = line[:-1]
                save_data = save_data + str(line_to_save) + '\n'
            f.write(save_data)
            file_available = True
        f.close()
    print('\nFile saved to {}'.format(f_name))


def save_warning_log(warning_log, file_name):
    """Save to file the warnings log.

    Args:
        warning_log (list): The errors to be written.
        file_name (str): Name to save the file to.
    """
    try:
        open(file_name, 'w')
    except IOError:
        print('Warning log could not be saved as \'{}\' is not accessible.'
              .format(file_name))
    else:
        FO = open(file_name, 'w')
        for line in warning_log:
            FO.write(str(line) + '\n')
        FO.close()
        print('\nWarnings log has been saved to {}'.format(file_name))
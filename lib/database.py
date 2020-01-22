import csv
"""
DATABASE FORMAT
Database mustn't have any header and blank lines at the end of file.
Its delimiter should be semicolon.
"""

class Database:
    """
    Purpose: Initialize the attributes of Database object.
    Parameters: ID (string)
                - ID of sampler in a decimal format
    """
    def __init__(self, ID):
        # initialize the name of the csv variable for the sampler
        self.file_name = "sampler_" + ID + ".csv"
        # convert all rows in the csv file to the items in a list
        self.rows = []
        self.read_lines_in_file()
        # get the number of rows in the csv file
        self.number_lines = len(self.rows)
        # intialize the current row to be read to 0
        self.row_number = 0

    """
    Purpose: Convert all rows in the csv file to the items in a list.
    """
    def read_lines_in_file(self):
        with open(self.file_name) as database:
            file = csv.reader(database, delimiter = ";")
            self.rows = [row for row in file]

    """
    Purpose: Get the bag number, time on and time off for the next bag to be filled
    Returns: Tuple of three strings
                - bag - number of the bag to be filled
                - time_on - time at which bag starts to fill
                - time_off - time at which bag stops to fill
    """
    def get_next_bag_and_times(self):
        # get bag number, time_on and time_off from list of rows
        bag = self.rows[self.row_number][0]
        time_on = self.rows[self.row_number][1]
        time_off = self.rows[self.row_number][2]
        # increase current row number by 1
        self.row_number += 1
        return bag, time_on, time_off

    """
    Purpose: Verify if there are more rows to be read from the csv file.
    Returns: Boolean
                - Returns True if file contains some rows that have not been, otherwise returns False.
    """
    def contains_more_lines(self):
        # if the current line number is smaller than number of lines in file
        if self.row_number < self.number_lines:
            # return
            return True
        # otherwise return False
        else:
            return False
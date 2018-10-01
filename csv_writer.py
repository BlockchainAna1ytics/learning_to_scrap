"""
Module that implements the DictToCsvWriter class to easily manipulate the creation of
new CSV files from a list of dictionaries.
This class implements __enter__() and __exit__() methods so it can be used as a context manager.
"""

import csv


class DictToCsvWriter:
    """
    Class used to write more dictionaries to a csv file given the dict keys as list (the header).
    """
    def __init__(self, outfile, header, newline=''):
        """Init method for DictToCsvWriter class

        args:
            :outfile: The .csv file name to be written on disk
            :header: A list of keys representing the CSV header

        kwargs:
            :newline: csv module tends to add a newline after each line written to disk. Leave this to default
            if you want a good looking out file
        """
        self.outfile = outfile
        self.header = header
        self.newline = newline
        self.fd = None
        self.csv_writer = None
        self.to_csv = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._close_file()

    def __del__(self):
        self._close_file()

    def _initialize_writer(self):
        """Helper method that will initialize the csv writer, by passing the file descriptor and the header.
        """
        self._open_file()
        self.csv_writer = csv.DictWriter(self.fd, self.header)

    def _open_file(self):
        """Helper method that will open a file and set the self.fd attribute with the value of the file descriptor
        """
        if not self.fd:
            self.fd = open(self.outfile, 'w', newline=self.newline)

    def _close_file(self):
        """Helper method that will close a file if it's open"""
        if self.fd:
            self.fd.close()
            self.fd = None

    def add_lines(self, list_of_dict):
        """Method that will extend the internal list of dictionaries with additional entries passed as argument

        args:
            :list_of_dict: A list of dictionaries with keys matching the header
        """
        self.to_csv.extend(list_of_dict)

    def write(self):
        """Method used to write the list of dictionaries to the csv file
        """
        if not self.csv_writer:
            self._initialize_writer()
        self.csv_writer.writeheader()
        self.csv_writer.writerows(self.to_csv)

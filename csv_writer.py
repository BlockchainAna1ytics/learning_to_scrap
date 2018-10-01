import csv


class DictToCsvWriter:
    """
    Class used to write more dictionaries with same keys to a csv file.
    """
    def __init__(self, outfile, header=None, newline=''):
        self.outfile = outfile
        self.header = header
        self.newline = newline
        self.fd = None
        self.dict_writer = None
        self.to_csv = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._close_file()

    def __del__(self):
        self._close_file()

    def _initialize_writer(self):
        self._open_file()
        self.dict_writer = csv.DictWriter(self.fd, self.header)

    def _open_file(self):
        if not self.fd:
            self.fd = open(self.outfile, 'w', newline=self.newline)

    def _close_file(self):
        if self.fd:
            self.fd.close()

    def add_line(self, dict_line):
        self.to_csv.append(dict_line)

    def add_lines(self, list_of_dict):
        self.to_csv.extend(list_of_dict)

    def write(self):
        if not self.dict_writer:
            self._initialize_writer()
        self.dict_writer.writeheader()
        self.dict_writer.writerows(self.to_csv)

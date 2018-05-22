# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-10 15:01:37
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-05-23 07:38:54
# @License: MIT LICENSE

import csv
import pandas as pd
import os


base_csv_dir = os.getcwd() + '/'


class CsvWriter(object):
    """The csv data writer class.

    This is a csv data writer which use the context management protocol.
    We can first creat a CsvWriter object, and then use the with..as..
    statement to manage context.

    Attributes:
        filename: The csv file name.
        header: The fieldname for the csv file.
        file_obj: The file object for the csv file.
    """

    def __init__(self, filename, header):
        """CsvWriter class initialize function.

        Arguments:
            filename {str} -- The file name to write.
            header {list} -- The field names list.
        """
        filename = base_csv_dir + filename
        self._file_obj = open(filename, "w", errors="ignore", encoding="utf-8")
        self._writer = csv.DictWriter(self._file_obj, fieldnames=header)
        self._writer.writeheader()

    def __del__(self):
        self.close()

    def close(self):
        if self._file_obj is not None:
            self._file_obj.close()
            self._file_obj = None
            self._writer = None

    def working(self, data):
        """Write a data line to csv file."""
        if self._writer is None:
            raise ValueError("The file is not opened yet.")
        self._writer.writerow(data)


class CsvReader(object):
    """The csv data reader class.

    This is a csv data reader which use the context management protocol.
    We can first creat a CsvWriter object, and then use the with..as..
    statement to manage context.

    Attributes:
        filename: The csv file name.
        file_obj: The file object for the csv file.
    """

    def __init__(self, filename):
        """Initialize the CsvReader class"""
        filename = base_csv_dir + filename
        self._file_obj = open(filename, "r", errors="ignore", encoding="utf-8")
        self._reader = csv.DictReader(self._file_obj)

    def __del__(self):
        self.close()

    def close(self):
        if self._file_obj is not None:
            self._file_obj.close()
            self._file_obj = None
            self._reader = None

    def working(self):
        """Read data lines from the csv file.

        Yields:
            dict -- A piece of the data in dict.
        """
        if self._reader is None:
            raise ValueError("The file is not opened yet.")
        for row in self._reader:
            row_list = [value for key, value in row.items()]
            yield [0] + row_list


class PandasCsvReader(object):

    def __init__(self, filename):
        filename = base_csv_dir + filename
        self._filename = filename

    def working(self):
        return pd.read_csv(self._filename, encoding="utf-8")

    def close(self):
        pass


class PandasCsvWriter(object):

    def __init__(self, filename):
        filename = base_csv_dir + filename
        self._filename = filename

    def working(self, df):
        df.to_csv(self._filename, encoding='utf-8')

    def close(self):
        pass

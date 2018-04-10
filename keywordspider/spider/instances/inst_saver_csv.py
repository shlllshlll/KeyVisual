# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-10 15:01:37
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-10 15:10:11
# @License: MIT LICENSE

import csv


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
        self.filename = filename
        self.header = header
        self.file_obj = open(self.filename, "w", errors="ignore")
        self.writer = csv.DictWriter(self.file_obj, fieldnames=self.header)
        self.writer.writeheader()

    def __del__(self):
        self.file_obj.close()

    def working(self, data):
        """Write a data line to csv file."""
        self.writer.writerow(data)


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
        self.filename = filename
        self.file_obj = open(self.filename, "r", errors="ignore")
        self.reader = csv.DictReader(self.file_obj)

    def __del__(self):
        self.file_obj.close()

    def working(self):
        """Read data lines from the csv file.

        Yields:
            dict -- A piece of the data in dict.
        """
        for row in self.reader:
            yield row

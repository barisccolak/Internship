"""Jobfile.py defines the features of jobfile."""
from __future__ import annotations
import os

_encoding = "cp1252"  # default yaskawa file encoding


class JobFile:
    """Public class to define jobFile."""

    def __init__(self, file_path: str):
        """Initialize."""
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.foldername = None
        self.lines = None
        self.headlines = []
        self.programlines = []
        self.separator = None
        self.error_flag = False

        self.warnings = []

        self.read_file()
        self.save_name()
        self.save_foldername()

        self.read_LVARS()

    def read_LVARS(self):
        """Create a dictionary with the local variables."""
        start_parsing = False  # Flag to indicate when to start parsing LVARS section
        parts = []
        self.LVARS = {}
        for line in self.headlines:
            if line.startswith("///LVARS"):
                start_parsing = True
                continue

            if start_parsing:
                if line.startswith("/"):  # Stop when parameters ends
                    start_parsing = False

                parts = line.strip().split(" ")  # Split the line into parts

            if len(parts) == 2:
                # take
                variable_name = parts[1].strip()
                variable_type = parts[0][:2]
                variable_number = parts[0][2:].strip()

                # store
                self.LVARS[variable_name] = (variable_type, variable_number)

            if start_parsing and line.startswith("///LVARS"):
                start_parsing = (
                    False  # Stop parsing when another ///LVARS section is encountered
                )

    def read_file(self):
        """Class method to read the file and print the content."""
        with open(self.file_path, encoding=_encoding) as file:
            self.lines = file.readlines()

            self.comment_lines = [
                (i, line.strip())
                for i, line in enumerate(self.lines)
                if line.startswith("'")
            ]

            self.command_lines = [
                (i, line.strip())
                for i, line in enumerate(self.lines)
                if not line.startswith("'")
            ]

            for i, line in enumerate(self.lines):
                if line.startswith("NOP"):
                    self.separator = i  # stores the index of NOP
                    self.programlines = self.lines[self.separator :]
                    # add the lines after NOP into headlines
                    self.headlines = self.lines[: self.separator]
                    # add the lines before NOP into headlines

    def save_name(self):
        """Filter the characters in the name line until ' ,' and save as name."""
        until = " "
        self.name = self.headlines[1]
        self.name = self.name[self.name.index(until) :]
        self.name = self.name.strip()  # delete the empty space

    def save_foldername(self):
        """Filter the characters in the folder name."""
        for line in self.headlines:
            if line.startswith("///FOLDERNAME"):
                # split the line with " " and take the second element from the
                # list split ( 0 and 1)
                self.foldername = line.split(" ", 1)[1].strip()
                return

        self.foldername = "!!NOFOLDERNAME!!"
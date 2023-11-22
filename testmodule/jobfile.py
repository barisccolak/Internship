"""Jobfile.py defines the features of jobfile."""
from __future__ import annotations
from pathlib import Path

from .helpers import _read_file_or_bytes


class JobFile:
    """Public class to define jobFile."""

    def __init__(self, file_path: str):
        """Initialize."""
        self.file_path = None
        self.file_name = None
        self.foldername = None
        self.lines = None
        self.headlines = []
        self.programlines = []
        self.separator = None
        self.warnings = []

        self.read_file(file_path)
        self.save_name()
        self.save_foldername()

        self.read_LVARS()

    def __repr__(self):
        """Define representation method of an object."""
        rep = (
            "Job File:\n\t"
            + f"{self.file_name}"
            + "\n"
            + "Path:\n\t"
            + str(self.file_path)
            + "\n"
            + "Foldername:\n\t"
            + str(self.foldername)
            + "\n"
            + "Number of header lines:\n\t"
            + str(len(self.headlines))
            + "\n"
            + "Number of program lines:\n\t"
            + str(len(self.programlines))
            + "\n"
            + "Number of LVARS:\n\t"
            + str(len(self.LVARS))
        )
        return rep

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

    def read_file(self, file_or_contents):
        """Class method to read the file and print the content."""
        if not isinstance(file_or_contents, bytes):
            p = Path(file_or_contents)

            if p.exists():  # check if we have a filename
                self.file_path = p.parent
                self.file_name = p.name

        self.lines = _read_file_or_bytes(file_or_contents).split("\n")

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

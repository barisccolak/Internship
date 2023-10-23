"""Fileparser recieves JBI data and tests their suitability."""

import os
import sys

_encoding = "cp1252"  # default yaskawa file encoding


class Rule:
    """It defines the class Rule."""

    def __init__(self, group, number, logic):
        self.group = group
        self.number = number
        self.logic = logic

    def apply_rule(self, job_file, group, number, file_name):
        """Recieve rule and choose logic.

        Parameters
        ----------
        job_file : ojb:`jobFile`
            Object of a jobFile class.
        group : str
            Group of the warning.
        number : int
            Number of the warning.
        file_name : str
            Name of the file.
        """
        self.logic(job_file, group, number, file_name)
        # add warning prints here.





def check_A(job_file, group, number, file_name):
    """Check (JBI-W, 1).

    Check if program starts with a comment line
    directly after the NOP statement.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.
    file_name : str
        Name of the file.
    """
    if not job_file.programlines[1].startswith("'---------------"):
        print(
            f"{file_name} - {group}{number} - [{job_file.separator+2}]: Every program should start with a comment line directly after the NOP statement."
        )
        job_file.error_flag = True


def check_B(job_file, group, number, file_name):
    """Check (JBI-W, 2).

    Test the job if program command
    SETREG MREG# is listed under
    FOLDERNAME TWINCAT_KOMMUNIKATION.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.
    file_name : str
        Name of the file.
    """

    for i in job_file.programlines:
        if i.startswith("SETREG MREG#"):
            if not job_file.foldername == "TWINCAT_KOMMUNIKATION":
                print(
                    f"{file_name} - {group}{number} [3] :The program command SETREG MREG# should only be allowed when the job is listed under FOLDERNAME TWINCAT_KOMMUNIKATION"
                )
                job_file.error_flag = True
                break


def check_C(job_file, group, number, file_name):
    """Check (JBI-W3).

    If the job is in the folder STANDARD or
    MAIN, the line SET USERFRAME n must be
    present, where n is any numerical value.
    The command SET USERFRAME must be executed
    before the command
    CALL JOB:TRIGGER ARGF"PROGRAMM_EIN" is called.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.
    file_name : str
        Name of the file.
    """
    set_flag_username = False
    set_flag_trigger = False
    index_username = 0
    index_trigger = 0

    if job_file.foldername == "STANDARD" or job_file.foldername == "MAIN":
        for i, line in enumerate(job_file.programlines):
            if line.startswith("SET USERFRAME"):
                set_flag_username = True
                index_username = i
            elif line.startswith('CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"'):
                set_flag_trigger = True
                index_trigger = i

        if set_flag_username is False:
            print(
                f"{file_name} - {group}{number} [{len(job_file.headlines) + index_trigger+1}]: The command SET USERFRAME does not exist"
            )
            job_file.error_flag = True

        if not (
            set_flag_username and set_flag_trigger and index_username <= index_trigger
        ):
            print(
                f"{file_name} - {group}{number} [{len(job_file.headlines) + index_username+1}]: The command SET USERFRAME must be executed before the command  CALL JOB:TRIGGER ARGF PROGRAMM_EIN is called"
            )
            job_file.error_flag = True


def check_D(job_file, group, number, file_name):
    """Check (JBI-W4).

    When a the TCPON command is called,
    the previous line must be a call to
    CALL JOB:SET_TCPON with the same argument
    number in both cases.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.
    file_name : str
        Name of the file.
    """
    argument = None
    index_tcpon = 0
    is_tcpon = False
    tcp_call_arg = None

    for index, item in enumerate(job_file.programlines):
        if item.startswith("TCPON TL#("):
            # Extract the argument number, third char is the argument: "(n) "
            argument = item[-3]
            index_tcpon = index
            is_tcpon = True
            break

    if is_tcpon:
        if index_tcpon > 0 and job_file.programlines[index_tcpon - 1].startswith(
            "CALL JOB:SET_TCPON ARGF"
        ):
            # Extract the argument number from the preceding SET_TCPON command
            tcp_call_arg = job_file.programlines[index_tcpon - 1][-2]

    if (argument != tcp_call_arg) and (argument == tcp_call_arg == None):
        print(argument, tcp_call_arg)
        print(
            f"{file_name} - {group}{number} - [{index_tcpon + len(job_file.headlines)}]: When a the TCPON command is called, the previous line must be a call to CALL JOB:SET_TCPON with the same argument number in both cases."
        )
        job_file.error_flag = True


def check_E(job_file, group, number, file_name):
    """Check (JBI-W5).

    For all jobs in folder MAIN:
    The first program line (after initial
    comments) as well as the final
    program line should be CALL JOB:TRIGGER_RESET.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.
    file_name : str
        Name of the file.
    """
    firstline = None
    lastline = None
    # List of the comment lines indexes
    comment_indexes = []
    is_foldername_main = False

    if job_file.foldername == "MAIN":
        is_foldername_main = True
        # Create a list for the comment block indexes
        for index, item in enumerate(job_file.programlines):
            if item.strip().startswith("'---"):
                comment_indexes.append(index)

        """firstline saver:
        If the line after initial comment
        block contains a single line comment, skip this
        line and save the firstline."""
        if job_file.programlines[comment_indexes[1] + 1].strip().startswith("'"):
            firstline = job_file.programlines[comment_indexes[1] + 2].strip()
        else:
            firstline = job_file.programlines[comment_indexes[1] + 1].strip()

        """lastline saver:
        If the previous line from END command is an " ",
        skip this line and save one before as lastline."""

        if (job_file.programlines[-2]).isspace():
            lastline = job_file.programlines[-3].strip()
        else:
            lastline = job_file.programlines[-2].strip()

    # Check after having firstline, lastline and is_name_ok.
    if firstline == lastline == "CALL JOB:TRIGGER_RESET":
        pass

    else:
        if is_foldername_main is True:
            print(
                f"{file_name} - {group}{number} - [2]: For all jobs in folder MAIN: The first program line (after initial comments) as well as the final program line should be CALL JOB:TRIGGER_RESET."
            )
            job_file.error_flag = True
        else:
            pass


def check_F(job_file, group, number, file_name):
    """Check (JBI-W6).

    ARCON and ARCOFF commands should be enclosed
    in a call of CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
    immediately before the ARCON command and a
    call to CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"
    immediately after the ARCOFF command.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.
    file_name : str
        Name of the file.
    """
    for i in range(len(job_file.programlines) - 1):
        current_line = job_file.programlines[i].strip()
        next_line = job_file.programlines[i + 1].strip()

        """XOR operator: 1 ^ 0 = True, 0 ^ 1 = True
        Check for ARCON"""
        if next_line.startswith("ARCON") ^ current_line.startswith(
            'CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"'
        ):
            print(
                f'{file_name} - {group}{number} - [{i + len(job_file.headlines)+ 1}]: ARCON command should be enclosed in a call of CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN".'
            )
            job_file.error_flag = True
            break

        # Check for ARCOF
        elif current_line.startswith("ARCOF") ^ next_line.startswith(
            'CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"'
        ):
            print(
                f'{file_name} - {group}{number} - [{i + len(job_file.headlines)+ 1}]: ARCOFF commands should be enclosed in a call of CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS".'
            )
            job_file.error_flag = True
            break
        else:
            pass



    

##########################
class JobFile:
    """Public class to define jobFile."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.foldername = None
        self.lines = None
        self.headlines = []
        self.programlines = []
        self.separator = None
        self.error_flag = False
        self.LVARS = {}

        self.read_file()
        self.save_name()
        self.save_foldername()

        self.read_LVARS()
        self.print_LVARS()

        self.rule_list()

    def read_LVARS(self):
        start_parsing = False  # Flag to indicate when to start parsing LVARS section
        parts = []
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

    def print_LVARS(self):
        print("LVARS Dictionary:")
        for variable, (var_type, var_number) in self.LVARS.items():
            print(f"{variable}: ({var_type}, {var_number})")

    def read_file(self):
        """Class method to read the file and print the content."""
        try:
            # ignore is risky! Talk with Cagtay!
            # with open(self.file_path, encoding='utf-8', errors ='ignore'
            with open(self.file_path, encoding=_encoding) as file:
                self.lines = file.readlines()

                for i, line in enumerate(self.lines):
                    if line.startswith("NOP"):
                        self.separator = i  # stores the index of NOP
                        self.programlines = self.lines[self.separator :]
                        # add the lines after NOP into headlines
                        self.headlines = self.lines[: self.separator]
                        # add the lines before NOP into headlines

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except Exception as e:
            raise e

    def save_name(self):
        """Filter the characters in the name line until ' ,' and save as name."""
        until = " "
        self.name = self.headlines[1]
        self.name = self.name[self.name.index(until) :]
        self.name = self.name.strip()  # delete the empty space
        # print("Name:", self.name)

    def save_foldername(self):
        for line in self.headlines:
            if line.startswith("FOLDERNAME"):
                # split the line with " " and take the second element from the list split ( 0 and 1)
                self.foldername = line.split(" ", 1)[1].strip()
                # print("Foldername:", self.foldername)
                return

        # If the "FOLDERNAME" line is not found, set the folder name to NOFOLDERNAME
        self.foldername = "!!NOFOLDERNAME!!"
        # print("Foldername:", self.foldername)

    def rule_list(self):
        """Contains the rules."""
        rules = [
            Rule("JBI-W", 1, logic=check_A),  # finished
            Rule("JBI-W", 2, logic=check_B),  # finished
            Rule("JBI-W", 3, logic=check_C),  # finished
            Rule("JBI-W", 4, logic=check_D),  # finished
            Rule("JBI-W", 5, logic=check_E),  # finished
            Rule("JBI-W", 6, logic=check_F),  # finished
        ]

        for rule in rules:
            rule.apply_rule(self, rule.group, rule.number, self.file_name)

        if self.error_flag is False:
            print(f"{self.file_name} :##### NO ERROR #####")


##########################
def input_file(file_path):
    """Recieve single input file."""
    job = JobFile(file_path)


def input_folder(file_path):
    """Recieve single input folder."""
    for root, dirs, files in os.walk(file_path):
        for file in sorted(files):
            if file.endswith(".JBI"):
                file_path = os.path.join(root, file)  # creates a full path
                job = JobFile(file_path)


def input_files(file_paths):
    """Recieve multiple files as input."""
    for file_path in file_paths:
        if os.path.isfile(file_path):
            input_file(file_path)
        else:
            print(f"Skipping invalid file: {file_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Wrong input.")
        sys.exit(1)

    inputs = sys.argv[1:]  # ignore the first one which is fileparser.py

    if len(inputs) > 1:
        input_files(inputs)
    else:
        input = inputs[0]

        if os.path.isfile(input):
            input_file(input)
        elif os.path.isdir(input):
            input_folder(input)
        else:
            print(f"Invalid path: {input}")

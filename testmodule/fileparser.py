"""Fileparser recieves JBI data and tests their suitability."""

import os


class Rule:
    """It defines the class Rule."""

    def __init__(self, group, number, logic):
        self.group = group
        self.number = number
        self.logic = logic

    def apply_rule(self, job_file, group, number):
        """Recieve rule and choose logic.
        
        Parameters
        ----------
        job_file : ojb:`jobFile`
            Object of a jobFile class.
        group : str
            Group of the warning.
        number : int
            Number of the warning.
        """
        self.logic(job_file, self.group, self.number)


def check_A(job_file, group, number):
    """Check (JBI-W, 1).

    If program starts with a comment line
    directly after the NOP statement.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.
    """
    if not job_file.programlines[1].startswith("'---------------"):
        print(
            f"{file_name} - {group}{number} - +\
            [{job_file.separator+2}]: Every program +\
            should start with +\
            a comment line directly after the NOP statement."
        )


def check_B(job_file, group, number):
    """Check (JBI-W, 2).
    
    Test and allow the job if program command 
    SETREG MREG# is listed unter 
    FOLDERNAME TWINCAT_KOMMUNIKATION.    
    
    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.
    """
    is_allowed_flag = False

    for i in job_file.programlines:
        if (
            i.startswith("SETREG MREG#")
            and job_file.foldername == "TWINCAT_KOMMUNIKATION"
        ):
            is_allowed_flag = True

    if not is_allowed_flag:
        print(
            f"{file_name} - {group}{number} [3] :The program command SETREG MREG# +\
            should only be allowed when the job is +\
            listed under FOLDERNAME TWINCAT_KOMMUNIKATION"
        )


def check_C(job_file, group, number):
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
    """
    set_flag_username = False
    set_flag_trigger = False
    index_username = 0
    index_trigger = 0

    if job_file.foldername == "STANDARD" or job_file.foldername == "MAIN":
        print("yes")
        for i, line in enumerate(job_file.programlines):
            if line.startswith("SET USERNAME"):
                set_flag_username = True
                index_username = i
                print("yesyes")
            elif line.startswith('CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"'):
                set_flag_trigger = True
                index_trigger = i
                print("yesyesyesyes")

        if set_flag_username is False:
            print(
                f"{file_name} - {group}{number} +\
                [{len(job_file.headlines) + index_trigger+1}]: The command +\
                SET USERFRAME must be executed before the +\
                command CALL JOB:TRIGGER ARGF PROGRAMM_EIN is called"
            )

        if not (
            set_flag_username and set_flag_trigger and index_username <= index_trigger
        ):
            print(
                f"{file_name} - {group}{number} +\
                [{len(job_file.headlines) + index_username+1}]: +\
                The command SET USERFRAME must be +\
                executed before the command +\
                CALL JOB:TRIGGER ARGF PROGRAMM_EIN is called"
            )


def check_D(job_file, group, number):
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
    """
    argument = 0
    index_tcpon = 0
    is_tcpon = False
    tcp_call_arg = None

    for index, item in enumerate(job_file.programlines):
        if item.startswith("TCPON TL#("):
            # Extract the argument number, third char is the argument: "(n) "
            argument = int(item[-3])
            index_tcpon = index
            is_tcpon = True
            break

    if is_tcpon:
        if index_tcpon > 0 and job_file.programlines[index_tcpon - 1].startswith(
            "CALL JOB:SET_TCPON ARGF"
        ):
            # Extract the argument number from the preceding SET_TCPON command
            tcp_call_arg = int(job_file.programlines[index_tcpon - 1][-2])

    if argument != tcp_call_arg:
        print(
            f"{file_name} - {group}{number} -+\
            [{index_tcpon + len(job_file.headlines)}]: +\
            When a the TCPON command is called, +\
            the previous line must be a call to +\
            CALL JOB:SET_TCPON with the same +\
            argument number in both cases."
        )

#work in progress
def check_E(job_file, group, number):
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
    """
    firstline = None
    lastline = None
    is_name_ok = True

    if job_file.foldername == "MAIN":
        firstline = job_file.programlines[1]
        print(firstline)
        lastline = job_file.programlines[-1]
        print(lastline)
        is_name_ok = True

    if not (
        (is_name_ok is True)
        and (firstline and lastline != None)
        and (firstline == lastline == "CALL JOB:TRIGGER_RESET")
    ):
        print(
            f"{file_name} - {group}{number} +\
            - [2]: For all jobs in folder MAIN:+\
            The first program line (after initial +\
            comments) as well as the final program +\
            line should be CALL JOB:TRIGGER_RESET."
        )


##########################
class JobFile:
    """Public class to define jobFile."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.name = None
        self.foldername = None
        self.lines = None
        self.headlines = []
        self.programlines = []
        self.separator = None

        self.read_file()
        self.save_name()
        self.save_foldername()
        self.rule_list()

    def read_file(self):
        """Class method to read the file and print the content."""
        try:
            with open(self.file_path) as file:
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
        print("Name:", self.name)

    def save_foldername(self):
        """Filter the characters in the line until ' ,'."""
        until = " "
        self.foldername = self.headlines[2]
        self.foldername = self.foldername[self.foldername.index(until) :]
        self.foldername = self.foldername.strip()  # delete the empty space
        print("Foldername:", self.foldername)

    def rule_list(self):
        """Contains the rules."""
        rules = [
            # Rule("JBI-W", 1, logic=check_A), #finished
            # Rule("JBI-W", 2, logic=check_B), # finished
            # Rule("JBI-W", 3, logic=check_C), #finished
            # Rule("JBI-W", 4, logic=check_D), #finished
            # Rule("JBI-W", 5, logic=check_E)
        ]

        for rule in rules:
            rule.apply_rule(self, rule.group, rule.number)


if __name__ == "__main__":
    head, tail = os.path.split("/mnt/scratch/bcolak/test.JBI")
    file_path = "/mnt/scratch/bcolak/test.JBI"
    file_name = tail
    job = JobFile(file_path)

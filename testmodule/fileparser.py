import os

class Rule:
    def __init__(self, group, number, logic):
        self.group = group
        self.number = number
        self.logic = logic

    def apply_rule(self, job_file, group, number):
        self.logic(job_file, self.group, self.number)

def check_A(job_file, group, number):
    """Check if program starts with a comment line 
    directly after the NOP statement. ("JBI-W", 1)"""
    if not job_file.programlines[1].startswith("'---------------"):
        print(f"{file_name} - {group}{number} - [{job_file.separator+2}]: Every program should start with a comment line directly after the NOP statement." 
        )
        

def check_B(job_file, group, number):
    """Test and allow the job if program command SETREG MREG# is listed unter FOLDERNAME TWINCAT_KOMMUNIKATION.("JBI-W", 2)"""
    is_allowed_flag = False
    counter = 0

    for i in job_file.programlines:
        if (
            i.startswith("SETREG MREG#")
            and job_file.foldername == "WINCAT_KOMMUNIKATION"

        ):
            is_allowed_flag = True
            break
        else: 
            counter += 1
########index of the error is not right.
    if not is_allowed_flag:
        print(f"{file_name} - {group}{number} {len(job_file.headlines) + counter} :The program command SETREG MREG# should only be allowed when the job is listed under FOLDERNAME TWINCAT_KOMMUNIKATION")


def check_C(job_file, group, number):
    """If the job is in the folder STANDARD or MAIN, the line SET USERFRAME n must be present, where n is any numerical value. The command SET USERFRAME must be executed before the command CALL JOB:TRIGGER ARGF"PROGRAMM_EIN" is called."""
    set_flag1 = False
    set_flag2 = False
    index_username = 0
    index_trigger = 0
    
    if self.foldername == "STANDARD" or self.foldername == "MAIN":
        
        for i in job_file.programlines:
            if ( i.startswith("SET USERNAME n"):
                set_flag1 = True
                index_username = i
            elif (i.startswith("CALL JOB:TRIGGER ARGF\"PROGRAMM_EIN\""):
                set_flag2 = True
                index_trigger = i
        if (set_flag1 and set_flag2 == True) and index_username <= index_trigger:
                
                
            







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
                        self.programlines = self.lines[self.separator:]
                        # add the lines after NOP into headlines
                        self.headlines = self.lines[:self.separator]
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
        """Filter the characters in the foldername line
        until ' ,' and save as foldername."""
        until = " "
        self.foldername = self.headlines[2]
        self.foldername = self.foldername[self.foldername.index(until) :]
        self.foldername = self.foldername.strip()  # delete the empty space
        print("Foldername:", self.foldername)

    
    def rule_list(self):
        """Contains the rules."""
        rules = [
            Rule("JBI-W", 1, logic=check_A),
            Rule("JBI-W", 2, logic=check_B),
        ]
        
        for rule in rules: 
            rule.apply_rule(self, rule.group, rule.number)



if __name__ == "__main__":
    head, tail = os.path.split("/mnt/scratch/bcolak/test.JBI")
    file_path = "/mnt/scratch/bcolak/test.JBI"
    file_name = tail
    job = JobFile(file_path)


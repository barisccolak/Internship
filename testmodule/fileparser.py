"""fileparser.py contains a class to test if given .JBI file is operable."""
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

        self.read_LVARS()


    def read_LVARS(self):
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

    def print_LVARS(self):
        print("LVARS Dictionary:")
        for variable, (var_type, var_number) in self.LVARS.items():
            print(f"{variable}: ({var_type}, {var_number})")


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
            raise (f"File not found: {self.file_path}")
        except Exception as e:
            raise (e)

    def save_name(self):
        """Filter the characters in the name line until ' ,' and save as name."""
        until = " "
        self.name = self.headlines[1]
        self.name = self.name[self.name.index(until) :]
        self.name = self.name.strip()  # delete the empty space
        print("name :", self.name)

    def save_foldername(self):
        """Filter the characters in the foldername line
        until ' ,' and save as foldername."""
        until = " "
        self.foldername = self.headlines[2]
        self.foldername = self.foldername[self.foldername.index(until) :]
        self.foldername = self.foldername.strip()  # delete the emtpy space
        print("Foldername :", self.foldername)

    def rule_list(self):
        """Contains the rules."""
        self.rule_post_NOP()
        self.rule_setreg_mreg()


    def rule_post_NOP(self):
        """Check if program starts with a comment line 
        directly after the NOP statement."""
        if not self.programlines[1].startswith("'---------------"):
            print(
                "Every program should start with a comment line directly after the NOP statement."
            )


    def rule_setreg_mreg(self):
        """Test and allow the job if program command SETREG MREG# is listed unter FOLDERNAME TWINCAT_KOMMUNIKATION."""
        is_allowed_flag = False

        for i in self.programlines:
            if (
                i.startswith("SETREG MREG#")
                and self.foldername == "TWINCAT_KOMMUNIKATION"
            ):
                is_allowed_flag = True
                break

        if is_allowed_flag is False:
            print("The program command SETREG MREG# should only be allowed when the job is listed unter FOLDERNAME TWINCAT_KOMMUNIKATION")


if __name__ == "__main__":
    file_path = "/mnt/scratch/bcolak/test.JBI"
    job = JobFile(file_path)

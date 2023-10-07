class jobFile:
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
            with open(self.file_path, "r") as file:
                self.lines = file.readlines()

                for i, line in enumerate(self.lines):
                    if line.startswith("NOP"):
                        self.separator = i  # stores the index of NOP

                        for c in range(i, len(self.lines)):
                            self.programlines.append(
                                self.lines[c]
                            )  # add the programlines

                        break
                    else:
                        self.headlines.append(
                            line
                        )  # add the lines before NOP into headlines

        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            raise (e)

    def save_name(self):
        """Filter the characters in the name line until ' ,' and save as name"""
        until = " "
        self.name = self.headlines[1]
        self.name = self.name[self.name.index(until) :]
        self.name = self.name.strip()  # delete the empty space
        print("name :", self.name)

    def save_foldername(self):
        """Filter the characters in the foldername line until ' ,' and save as foldername"""
        until = " "
        self.foldername = self.headlines[2]
        self.foldername = self.foldername[self.foldername.index(until) :]
        self.foldername = self.foldername.strip()  # delete the emtpy space
        print("Foldername :", self.foldername)

    def rule_list(self):
        """Contains the rules"""
        self.rule_post_NOP(self.separator)
        self.rule_setreg_mreg(self.separator)

    def rule_post_NOP(self, separator):
        """Class method to check if program starts with a comment line directly after the NOP statement."""
        try:
            if not self.programlines[1].startswith("'---------------"):
                raise Exception(
                    "Every program should start with a comment line directly after the NOP statement."
                )

        except Exception as e:
            raise (e)

    def rule_setreg_mreg(self, separator):
        """The program command SETREG MREG# should only be allowed when the job is listed unter FOLDERNAME TWINCAT_KOMMUNIKATION"""
        try:
            is_allowed_flag = False

            for i in self.programlines:
                if (
                    i.startswith("SETREG MREG#")
                    and self.foldername == "TWINCAT_KOMMUNIKATION"
                ):
                    is_allowed_flag = True
                    break

            if is_allowed_flag == True:
                print("no problem")
            else:
                raise Exception(
                    "The program command SETREG MREG# should only be allowed when the job is listed unter FOLDERNAME TWINCAT_KOMMUNIKATION"
                )

        except Exception as e:
            raise (e)


if __name__ == "__main__":
    file_path = "/mnt/scratch/bcolak/test.JBI"
    job = jobFile(file_path)

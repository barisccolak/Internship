"""Read public module contains a class to read a text file."""

class TextFileReader:
    """Class to open a file and print."""

    def __init__(self, file_path):
        """Init file."""
        self.file_path = file_path

    def read_file(self):
        """Class method to read the file and print the content."""
        try:
            with open(self.file_path) as file:
                content = file.read()
                print(content)

        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    file_path = input("Enter the path to the .txt file: ")
    file_reader = TextFileReader(file_path)
    file_reader.read_file()

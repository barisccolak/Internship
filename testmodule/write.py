"""write.py Folder contains a class called LatinGenerator."""
import os
import lorem


class LatinGenerator:
    """Class for creating a file."""

    def __init__(self, file_path):
        self.file_path = file_path

    def create_file(self):
        """Create_file class method creates a text file into given path."""
        if os.path.exists(self.file_path):
            print(f"File '{self.file_path}' already exists.")
        else:
            try:
                with open(self.file_path, "w") as file:
                    file.write(lorem.text())
                print(f"File '{self.file_path}' created successfully.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    file_path = input("Enter the path to create .txt file: ")
    file = LatinGenerator(file_path)
    file.create_file()

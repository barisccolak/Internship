"""Main.py module"""
import os
from pathlib import Path
from testmodule.jobfile import JobFile
from testmodule.rule import Rule, check_w1, check_w2, check_w3, check_w4, check_w5, check_w6, check_w7, check_w8

rules = [
    Rule("JBI-W", 1, logic=check_w1),
    Rule("JBI-W", 2, logic=check_w2),
    Rule("JBI-W", 3, logic=check_w3),
    Rule("JBI-W", 4, logic=check_w4),
    Rule("JBI-W", 5, logic=check_w5),
    Rule("JBI-W", 6, logic=check_w6),
    Rule("JBI-W", 7, logic=check_w7),
    Rule("JBI-W", 8, logic=check_w8),
]



def check_jobfile(file_path: str):
    """Run the rules in a folder or in a file."""
    p = Path(file_path)

    files = []

    if p.is_file():
        files = [p]
    elif p.is_dir():
        files = sorted(p.glob("*.JBI"))
    else:
        raise ValueError(f"Invalid input: '{file_path}' is neither a file nor a directory.")

    for file in files:
        job_file = JobFile(file)
        for rule in rules:
            results = rule.apply_rule(job_file)

            if results is None:
                continue

            if isinstance(results, tuple):
                results = [results]

            for result in results:
                warning = (
                    result[0]
                    + str(result[1])
                    + " ["
                    + str(result[2])
                    + "] : "
                    + result[3]
                )
                print(warning)

def input_folder(file_path: str):
    """Receive single input folder."""
    for root, dirs, files in os.walk(file_path):
        for file in sorted(files):
            if file.endswith(".JBI"):
                file_path = os.path.join(root, file)  # creates a full path
                JobFile(file_path)

def input_file(file_path: str):
    """Receive single input file."""
    job = JobFile(file_path)

    for rule in rules:
        result = rule.apply_rule(job)
        if result is not None:
            warning = (
                result[0] + str(result[1]) + " [" + str(result[2]) + "] : " + result[3]
            )
            print(warning)

def main():
    file_path = "/mnt/scratch/bcolak/Internship/testmodule/test.JBI"
    check_jobfile(file_path)

if __name__ == "__main__":
    main()
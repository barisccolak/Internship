"""Main.py script."""
import argparse
from pathlib import Path

from testmodule.jobfile import JobFile
from testmodule.rule import (
    Rule,
    check_w1,
    check_w2,
    check_w3,
    check_w4,
    check_w5,
    check_w6,
    check_w7,
    check_w8,
)

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


def check_jobfile(input_data: str):
    """Run the rules on a folder on a file or on a string."""
    p = Path(input_data)

    # input_data as a file
    if p.is_file():
        job_file = JobFile(p)
        refactor(p)

    # input_data as a directory
    elif p.is_dir():
        files = sorted(p.glob("*.JBI"))

        for file in files:
            refactor(file)

    # input_data as a string
    else:
        refactor(input_data)


def refactor(input_data):
    """Refactor the output message."""
    job_file = JobFile(input_data)
    for rule in rules:
        results = rule.apply_rule(job_file)

        if results is None:
            continue

        if isinstance(results, tuple):
            results = [results]

        for result in results:
            warning = (
                result[0] + str(result[1]) + " [" + str(result[2]) + "] : " + result[3]
            )
            print(warning)


def main(input_data):
    """Parser arguments."""
    check_jobfile(input_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="YASKAWA fileparser",
        description="Check one or multiple YASKAWA JOB files for logic errors.",
    )
    parser.add_argument(
        "input_data",
        type=str,
        help="path to a single file or folder containing JOB files",
    )
    args = parser.parse_args()

    main(args.input_data)

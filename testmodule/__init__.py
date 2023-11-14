"""Init file is an example."""

from .jobfile import JobFile
from .rule import Rule, check_w1, check_w2, check_w3, check_w4, check_w5, check_w6, check_w7, check_w8
from .main import check_jobfile, input_folder, input_file

#It defines what gets imported when using `from testmodule import *`
__all__ = ["JobFile", "Rule", "check_w1", "check_w2", "check_w3", "check_w4", "check_w5", "check_w6", "check_w7", "check_w8", "check_jobfile", "input_folder", "input_file"]

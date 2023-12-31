from testmodule import JobFile

from testmodule.helpers import _encoding


def test_jobfile_string_input():
    """Test if Jobfile can be created from string input."""
    input_string = """/JOB
//NAME TEST
///FOLDERNAME MAIN
NOP
'A comment
SET USERFRAME
CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
END
"""

    job = JobFile(input_string)
    assert job.foldername == "MAIN"
    assert job.comment_lines[0] == (4, "'A comment")


def test_jobfile_bytes_input():
    """Test if Jobfile can be created from string input."""
    input_string = """/JOB
//NAME TEST
///FOLDERNAME MAIN
NOP
'A comment
SET USERFRAME
CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
END
"""

    job = JobFile(input_string.encode(_encoding))
    assert job.foldername == "MAIN"
    assert job.comment_lines[0] == (4, "'A comment")

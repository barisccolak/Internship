import pytest
from testmodule.jobfile import JobFile
from testmodule.rule import (
    check_w1,
    check_w2,
    check_w3,
    check_w4,
    check_w5,
    check_w6,
    check_w7,
    check_w8,
)


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)


def job_file_generator(
    program: str = None,
    header_extra: str = None,
    jobname: str = "TEST",
    foldername="TESTFOLDER",
    nop="NOP\n",
    end="END\n",
):
    header = "/JOB\n"
    if jobname is not None:
        header += f"//NAME {jobname}\n"
    if foldername is not None:
        header += f"///FOLDERNAME {foldername}\n"
    if header_extra is not None:
        header += header_extra


    if program is not None:
        if not program.startswith("'"):
            program = """'A comment COMMAND\n""" + program
        if not program.endswith("\n"):
            program = program + "\n"
    else:
        program = """'A comment COMMAND\n"""

    job = header + nop + program + end
    return job

# ===========
# CHECK_W1
# ===========
def test_check_w1():
    job_string = job_file_generator()
    job = JobFile(job_string)
    result = check_w1(job, "W", "1")

    assert result is None


def test_check_w1_error():
    job_string = """/JOB
//NAME TEST
///FOLDERNAME MAIN
NOP
CALL JOB:TRIGGER_RESET
END

"""
    job = JobFile(job_string)
    result = check_w1(job, "W", "1")

    assert result[0] == "W"
    assert result[1] == "1"
    assert result[2] == 5
    assert result[3].startswith(
        "Every program should start with a comment line directly after the NOP statement"
    )


# ===========
# CHECK_W2
# ===========
def test_check_w2():
    job_string = job_file_generator(program = "SETREG MREG#\n", foldername = "TWINCAT_KOMMUNIKATION")
    job = JobFile(job_string)
    result = check_w2(job, "W", "1")

    assert result is None


def test_check_w2_error():
    job_string = job_file_generator(program = "SETREG MREG#\n")
    job = JobFile(job_string)
    result = check_w2(job, "W", "2")

    assert result[0] == "W"
    assert result[1] == "2"
    assert result[2] == 3
    assert result[3].startswith("The program command")


# ===========# CHECK_W3
# ===========
def test_check_w3():
      
    program ='''SET USERFRAME
CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w3(job, "W", "3")

    assert result is None


def test_check_w3_error_1():
    program = 'CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"\n'
    job_string = job_file_generator(program, foldername = "STANDARD")
    job = JobFile(job_string)
    result = check_w3(job, "W", "3")

    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 6
    assert result[3] == "The command SET USERFRAME does not exist"


def test_check_w3_error_2():
    program = 'CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"\n'
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w3(job, "W", "3")

    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 6
    assert result[3] == "The command SET USERFRAME does not exist"
    
                                                

def test_check_w3_error_3():
    program ='''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
SET USERFRAME\n'''
    job_string = job_file_generator(program, foldername = "STANDARD")
    job = JobFile(job_string)
    result = check_w3(job, "W", "3")

    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 7
    assert (
        result[3]
        == "The command SET USERFRAME must be executed before the command CALL JOB:TRIGGER ARGF PROGRAMM_EIN is called"
    )


def test_check_w3_error_4():
    program ='''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
SET USERFRAME\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w3(job, "W", "3")

    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 7
    assert (
        result[3]
        == "The command SET USERFRAME must be executed before the command CALL JOB:TRIGGER ARGF PROGRAMM_EIN is called"
    )


# ===========
# CHECK_W4
# ===========

def test_check_w4():
    program = '''CALL JOB:SET_TCPON ARGF5
TCPON TL#(5)\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "3")
    assert result is None


def test_check_w4_error_1():
    program = '''TCPON TL#(5)\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 6
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_2():
    program = '''CALL JOB:SET_TCPON ARGF5\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 6
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_3():
    program = '''TCPON TL#(5)
CALL JOB:SET_TCPON ARGF5\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 6
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_4():
    program = '''CALL JOB:SET_TCPON ARGF5
TCPON TL#(6)\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 7
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_5():
    program = '''CALL JOB:SET_TCPON ARGF5
Another line
TCPON TL#(5)\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 8
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_6():
    program = '''CALL JOB:SET_TCPON ARGF5
TCPON TL#(5)
Another line
CALL JOB:SET_TCPON ARGF5
TCPON TL#(6)\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 10
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_7():
    program = '''CALL JOB:SET_TCPON ARGF5
TCPON TL#(5)
CALL JOB:SET_TCPON ARGF6
TCPON TL#(7))\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 9
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_8():
    program = '''CALL JOB:SET_TCPON ARGF6
TCPON TL#(7)
CALL JOB:SET_TCPON ARGF5
TCPON TL#(5)\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 7
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_9():
    program = '''CALL JOB:SET_TCPON ARGF6
TCPON TL#(7)
Anotherline
CALL JOB:SET_TCPON ARGF5
TCPON TL#(5)\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 7
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_10():
    program = '''CALL JOB:SET_TCPON ARGF6
TCPON TL#(7)
Anotherline
CALL JOB:SET_TCPON ARGF5
TCPON TL#(9)\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 7
    assert result[0][3].startswith("When a TCPON command")

    assert result[0][0] == "W"
    assert result[1][1] == "4"
    assert result[1][2] == 10
    assert result[1][3].startswith("When a TCPON command")


# ===========
# CHECK_W5
# ===========
def test_check_w5():
    program = '''CALL JOB:TRIGGER_RESET
ANOTHER LINE
CALL JOB:TRIGGER_RESET\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w5(job, "W", "5")

    assert result is None


def test_check_w5_error_1():
    program = '''CALL JOB:TRIGGER_RESET
ANOTHER LINE\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w5(job, "W", "5")

    assert result[0] == "W"
    assert result[1] == "5"
    assert result[2] is None
    assert result[3].startswith("For all jobs in folder MAIN")


def test_check_w5_error_2():
    program = '''ANOTHER LINE
CALL JOB:TRIGGER_RESET\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w5(job, "W", "5")

    assert result[0] == "W"
    assert result[1] == "5"
    assert result[2] is None
    assert result[3].startswith("For all jobs in folder MAIN")


def test_check_w5_error_3():
    program = '''ANOTHER LINE
CALL JOB:TRIGGER_RESET
CALL JOB:TRIGGER_RESET\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w5(job, "W", "5")

    assert result[0] == "W"
    assert result[1] == "5"
    assert result[2] is None
    assert result[3].startswith("For all jobs in folder MAIN")


# ===========
# CHECK_W6
# ===========
def test_check_w6():
    program = '''CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
ARCON
ANOTHER LINE
ARCOF
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"
END\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")

    assert result is None


def test_check_w6_error_1():
    program = '''CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
ARCON
ANOTHER LINE
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 8
    assert result[0][3].startswith("ARCOF command should be")


def test_check_w6_error_2():
    program = '''CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
ARCON
ANOTHER LINE
ARCOF\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 9
    assert result[0][3].startswith("ARCOF command should be")


def test_check_w6_error_3():
    program = '''ARCON
ANOTHER LINE
ARCOF
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 5
    assert result[0][3].startswith("ARCON command should be")


def test_check_w6_error_4():
    program = '''CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
ANOTHER LINE
ARCOF
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 6
    assert result[0][3].startswith("ARCON command should be")


def test_check_w6_error_5():
    program = '''CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
ANOTHER LINE
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")
    
    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 6
    assert result[0][3].startswith("ARCON command should be")

    assert result[1][0] == "W"
    assert result[1][1] == "6"
    assert result[1][2] == 7
    assert result[1][3].startswith("ARCOF command should be")


def test_check_w6_error_6():
    program = '''ARCON
ANOTHER LINE
ARCOF\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 5
    assert result[0][3].startswith("ARCON command should be")

    assert result[1][0] == "W"
    assert result[1][1] == "6"
    assert result[1][2] == 8
    assert result[1][3].startswith("ARCOF command should be")


def test_check_w6_error_7():
    program = '''ARCON
CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
ANOTHER LINE
ARCOF
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 5
    assert result[0][3].startswith("ARCON command should be")


def test_check_w6_error_8():
    program = '''CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
ARCON
ANOTHER LINE
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"
ARCOF\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 8
    assert result[0][3].startswith("ARCOF command should be")


def test_check_w6_error_9():
    program = '''ARCON
CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
ANOTHER LINE
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"
ARCOF\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 5
    assert result[0][3].startswith("ARCON command should be")

    assert result[2][0] == "W"
    assert result[2][1] == "6"
    assert result[2][2] == 8
    assert result[2][3].startswith("ARCOF command should be")


# ===========
# CHECK_W7
# ===========
def test_check_w7():
    program = '''CALL JOB:SET_IDS_FULL
CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w7(job, "W", "7")

    assert result is None


def test_check_w7_error_1():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w7(job, "W", "7")

    assert result[0] == "W"
    assert result[1] == "7"
    assert result[2] == 6
    assert result[3].startswith("CALL JOB:SET_IDS_FULL doesn't")


def test_check_w7_error_2():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
CALL JOB:SET_IDS_FULL\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w7(job, "W", "7")

    assert result[0] == "W"
    assert result[1] == "7"
    assert result[2] == 7
    assert result[3].startswith("CALL JOB:SET_IDS_FULL must be called before")


# ===========
# CHECK_W8
# ===========
def test_check_w8():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"
CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"
CALL JOB:TRIGGER ARGF"UI_START"
CALL JOB:TRIGGER ARGF"UI_STOP"
CALL JOB:TRIGGER ARGF"TRIG_EIN"
CALL JOB:TRIGGER ARGF"TRIG_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result is None

def test_check_w8_2():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"
CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result is None

#########################################################################
def test_check_w8_error_1():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"'
    )


def test_check_w8_error_2():
    program = '''CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"'
    )


def test_check_w8_error_3():
    program = '''CALL JOB:TRIGGER ARGF"UI_START"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")
    
    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"UI_START"'
    )


def test_check_w8_error_4():
    program = '''CALL JOB:TRIGGER ARGF"TRIG_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"TRIG_EIN"'
    )


def test_check_w8_error_5():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"'
    )


def test_check_w8_error_6():
    program = '''CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"'
    )


def test_check_w8_error_7():
    program = '''CALL JOB:TRIGGER ARGF"UI_STOP"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"UI_STOP"'
    )


def test_check_w8_error_8():
    program = '''CALL JOB:TRIGGER ARGF"TRIG_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"TRIG_AUS"'
    )


def test_check_w8_error_9():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"
CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"'
    )

    assert result[1][0] == "W"
    assert result[1][1] == "8"
    assert result[1][2] == 7
    assert result[1][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"'
    )


def test_check_w8_error_10():
    program = '''CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"
CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"'
    )

    assert result[1][0] == "W"
    assert result[1][1] == "8"
    assert result[1][2] == 7
    assert result[1][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"'
    )


def test_check_w8_error_11():
    program = '''CALL JOB:TRIGGER ARGF"UI_STOP"
CALL JOB:TRIGGER ARGF"UI_START"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"UI_STOP"'
    )

    assert result[1][0] == "W"
    assert result[1][1] == "8"
    assert result[1][2] == 7
    assert result[1][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"UI_START"'
    )


def test_check_w8_error_12():
    program = '''CALL JOB:TRIGGER ARGF"TRIG_AUS"
CALL JOB:TRIGGER ARGF"TRIG_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"TRIG_AUS"'
    )

    assert result[1][0] == "W"
    assert result[1][1] == "8"
    assert result[1][2] == 7
    assert result[1][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"TRIG_EIN"'
    )


def test_check_w8_error_13():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"
CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 8
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"'
    )


def test_check_w8_error_14():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"
CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 8
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"'
    )


def test_check_w8_error_15():
    program = '''CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"
CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"\n'''
    job_string = job_file_generator(program, foldername = "MAIN")
    job = JobFile(job_string)
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"'
    )

    assert result[1][0] == "W"
    assert result[1][1] == "8"
    assert result[1][2] == 7
    assert result[1][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"'
    )



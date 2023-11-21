import pytest
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


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)


# ===========
# CHECK_W1
# ===========
def test_check_w1():
    job = JobFile("w1_pass.JBI")
    result = check_w1(job, "W", "1")

    assert result is None


def test_check_w1_errors():
    job = JobFile("w1_error.JBI")
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
    job = JobFile("w2_pass.JBI")
    result = check_w2(job, "W", "1")

    assert result is None


def test_check_w2_error():
    job = JobFile("w2_error.JBI")
    result = check_w2(job, "W", "2")

    assert result[0] == "W"
    assert result[1] == "2"
    assert result[2] == 3
    assert result[3].startswith("The program command")


# ===========
# CHECK_W3
# ===========
def test_check_w3():
    job = JobFile("w3_pass.JBI")
    result = check_w3(job, "W", "3")

    assert result is None


def test_check_w3_error_1():
    job = JobFile("w3_error_1.JBI")
    result = check_w3(job, "W", "3")

    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 6
    assert result[3] == "The command SET USERFRAME does not exist"


def test_check_w3_error_2():
    job = JobFile("w3_error_2.JBI")
    result = check_w3(job, "W", "3")

    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 6
    assert result[3] == "The command SET USERFRAME does not exist"


def test_check_w3_error_3():
    job = JobFile("w3_error_3.JBI")
    result = check_w3(job, "W", "3")

    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 7
    assert (
        result[3]
        == "The command SET USERFRAME must be executed before the command CALL JOB:TRIGGER ARGF PROGRAMM_EIN is called"
    )


def test_check_w3_error_4():
    job = JobFile("w3_error_4.JBI")
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
    job = JobFile("w4_pass.JBI")
    result = check_w4(job, "W", "4")

    assert result is None


def test_check_w4_error_1():
    job = JobFile("w4_error_1.JBI")
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 7
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_2():
    job = JobFile("w4_error_2.JBI")
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 6
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_3():
    job = JobFile("w4_error_3.JBI")
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 6
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_4():
    job = JobFile("w4_error_4.JBI")
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 7
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_5():
    job = JobFile("w4_error_5.JBI")
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 8
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_6():
    job = JobFile("w4_error_6.JBI")
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 10
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_7():
    job = JobFile("w4_error_7.JBI")
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 9
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_8():
    job = JobFile("w4_error_8.JBI")
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 7
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_9():
    job = JobFile("w4_error_9.JBI")
    result = check_w4(job, "W", "4")

    assert result[0][0] == "W"
    assert result[0][1] == "4"
    assert result[0][2] == 7
    assert result[0][3].startswith("When a TCPON command")


def test_check_w4_error_10():
    job = JobFile("w4_error_10.JBI")
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
    job = JobFile("w5_pass.JBI")
    result = check_w5(job, "W", "5")

    assert result is None


def test_check_w5_error_1():
    job = JobFile("w5_error_1.JBI")
    result = check_w5(job, "W", "5")

    assert result[0] == "W"
    assert result[1] == "5"
    assert result[2] == None
    assert result[3].startswith("For all jobs in folder MAIN")


def test_check_w5_error_2():
    job = JobFile("w5_error_2.JBI")
    result = check_w5(job, "W", "5")

    assert result[0] == "W"
    assert result[1] == "5"
    assert result[2] == None
    assert result[3].startswith("For all jobs in folder MAIN")


def test_check_w5_error_3():
    job = JobFile("w5_error_3.JBI")
    result = check_w5(job, "W", "5")

    assert result[0] == "W"
    assert result[1] == "5"
    assert result[2] == None
    assert result[3].startswith("For all jobs in folder MAIN")


# ===========
# CHECK_W6
# ===========
def test_check_w6():
    job = JobFile("w6_pass.JBI")
    result = check_w6(job, "W", "6")

    assert result is None


def test_check_w6_error_1():
    job = JobFile("w6_error_1.JBI")
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 8
    assert result[0][3].startswith("ARCOF command should be")


def test_check_w6_error_2():
    job = JobFile("w6_error_2.JBI")
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 9
    assert result[0][3].startswith("ARCOF command should be")


def test_check_w6_error_3():
    job = JobFile("w6_error_3.JBI")
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 5
    assert result[0][3].startswith("ARCON command should be")


def test_check_w6_error_4():
    job = JobFile("w6_error_4.JBI")
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 6
    assert result[0][3].startswith("ARCON command should be")


def test_check_w6_error_5():
    job = JobFile("w6_error_5.JBI")
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
    job = JobFile("w6_error_6.JBI")
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
    job = JobFile("w6_error_7.JBI")
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 5
    assert result[0][3].startswith("ARCON command should be")


def test_check_w6_error_8():
    job = JobFile("w6_error_8.JBI")
    result = check_w6(job, "W", "6")

    assert result[0][0] == "W"
    assert result[0][1] == "6"
    assert result[0][2] == 8
    assert result[0][3].startswith("ARCOF command should be")


def test_check_w6_error_9():
    job = JobFile("w6_error_9.JBI")
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
    job = JobFile("w7_pass.JBI")
    result = check_w7(job, "W", "7")

    assert result is None


def test_check_w7_error_1():
    job = JobFile("w7_error_1.JBI")
    result = check_w7(job, "W", "7")

    assert result[0] == "W"
    assert result[1] == "7"
    assert result[2] == 6
    assert result[3].startswith("CALL JOB:SET_IDS_FULL doesn't")


def test_check_w7_error_2():
    job = JobFile("w7_error_2.JBI")
    result = check_w7(job, "W", "7")

    assert result[0] == "W"
    assert result[1] == "7"
    assert result[2] == 7
    assert result[3].startswith("CALL JOB:SET_IDS_FULL must be called before")


# ===========
# CHECK_W8
# ===========
def test_check_w8():
    job = JobFile("w8_pass.JBI")
    result = check_w8(job, "W", "8")

    assert result is None


def test_check_w8_error_1():
    job = JobFile("w8_error_1.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"'
    )


def test_check_w8_error_2():
    job = JobFile("w8_error_2.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"'
    )


def test_check_w8_error_3():
    job = JobFile("w8_error_3.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"UI_START"'
    )


def test_check_w8_error_4():
    job = JobFile("w8_error_4.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"TRIG_EIN"'
    )


def test_check_w8_error_5():
    job = JobFile("w8_error_5.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"'
    )


def test_check_w8_error_6():
    job = JobFile("w8_error_6.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"'
    )


def test_check_w8_error_7():
    job = JobFile("w8_error_7.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"UI_STOP"'
    )


def test_check_w8_error_8():
    job = JobFile("w8_error_8.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 6
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"TRIG_AUS"'
    )


def test_check_w8_error_9():
    job = JobFile("w8_error_9.JBI")
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
    job = JobFile("w8_error_10.JBI")
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
    job = JobFile("w8_error_11.JBI")
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
    job = JobFile("w8_error_12.JBI")
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
    job = JobFile("w8_error_13.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 8
    assert result[0][3].startswith(
        'Unclosed trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"'
    )


def test_check_w8_error_14():
    job = JobFile("w8_error_14.JBI")
    result = check_w8(job, "W", "8")

    assert result[0][0] == "W"
    assert result[0][1] == "8"
    assert result[0][2] == 8
    assert result[0][3].startswith(
        'Unopened trigger pair: CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"'
    )


def test_check_w8_error_15():
    job = JobFile("w8_error_15.JBI")
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


def test_check_w8_2():
    job = JobFile("w8_pass_2.JBI")
    result = check_w8(job, "W", "8")

    assert result is None

import pytest
from testmodule.fileparser import JobFile, check_A, check_B, check_C

@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)

# ===========
# CHECK_A
# ===========
def test_check_A():
    job = JobFile("A_pass.JBI")
    result = check_A(job, "W", "1")

    assert result is None

def test_check_A_errors():
    job = JobFile("A_error.JBI")
    result = check_A(job, "W", "1")

    assert result[0] == "W"
    assert result[1] == "1"
    assert result[2] == 5
    assert result[3].startswith("Every program should start with a comment line directly after the NOP statement")


# ===========
# CHECK_B
# ===========
def test_check_B():
    job = JobFile("B_pass.JBI")
    result = check_A(job, "W", "1")

    assert result is None

def test_check_B_error():
    job = JobFile("B_error.JBI")
    result = check_B(job, "W", "2")

    assert result[0] == "W"
    assert result[1] == "2"
    assert result[2] == 3
    assert result[3].startswith("The program command")
        
# ===========
# CHECK_C
# ===========
def test_check_C():
    job = JobFile("C_pass.JBI")
    result = check_C(job, "W", "3")

    assert result is None

def test_check_C_error_1():
    job = JobFile("C_error_1.JBI")
    result = check_C(job, "W", "3")

    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 6
    assert result[3] == "The command SET USERFRAME does not exist"

def test_check_C_error_2():
    job = JobFile("C_error_2.JBI")
    result = check_C(job, "W", "3")

    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 6
    assert result[3] == "The command SET USERFRAME does not exist"


def test_check_C_error_3():
    job = JobFile("C_error_3.JBI")
    result = check_C(job, "W", "3")


    assert result[0] == "W"
    assert result[1] == "3"
    assert result[2] == 7
    assert result[3] == "The command SET USERFRAME does not exist"



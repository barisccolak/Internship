from __future__ import annotations
from .jobfile import JobFile
import os

class Rule:
    """It defines the class Rule."""

    def __init__(self, group: str, number: int, logic: Callable):
        self.group = group
        self.number = number
        self.logic = logic

    def apply_rule(self, job_file: JobFile):
        """Recieve rule and choose logic.

        Parameters
        ----------
        job_file : ojb:`jobFile`
            Object of a jobFile class.

        """
        return self.logic(job_file, self.group, self.number)


def check_w1(job_file: JobFile, group: str, number: int) -> tuple[str, int, int, str]:
    """Check (JBI-W, 1).

    Check if program starts with a comment line directly after the NOP statement.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.

    Returns
    -------
    warnings : tuple
        Error messages.
    """
    if not job_file.programlines[1].startswith("'"):
        job_file.error_flag = True
        line = job_file.separator + 2
        msg = "Every program should start with a comment line directly after the NOP statement"
        return (group, number, line, msg)


def check_w2(job_file: JobFile, group: str, number: int) -> tuple[str, int, int, str]:
    """Check (JBI-W, 2).

    Test the job if program command SETREG MREG# is listed
    under FOLDERNAME TWINCAT_KOMMUNIKATION.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.

    Returns
    -------
    warnings : tuple
        Error messages.
    """
    for line in job_file.programlines:
        if line.startswith("SETREG MREG#"):
            if not job_file.foldername == "TWINCAT_KOMMUNIKATION":
                job_file.error_flag = True
                line = [
                    (i, line.strip())
                    for i, line in enumerate(job_file.headlines)
                    if not line.startswith("'")
                ][2][0] + 1
                msg = 'The program command SETREG MREG# should only be allowed when the job is listed under FOLDERNAME TWINCAT_KOMMUNIKATION"'
                return (group, number, line, msg)


def check_w3(job_file: JobFile, group: str, number: int) -> tuple[str, int, int, str]:
    """Check (JBI-W3).

    If the job is in the folder STANDARD or MAIN, the line SET USERFRAME n
    must be present, where n is any numerical value. The command SET USERFRAME
    must be executed before the command CALL JOB:TRIGGER ARGF"PROGRAMM_EIN" is called.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.

    Returns
    -------
    warnings : tuple
        Error messages.
    """
    set_flag_username = False
    set_flag_trigger = False
    index_username = 0
    index_trigger = 0

    if job_file.foldername in ["STANDARD", "MAIN"]:
        for i, line in enumerate(job_file.programlines):
            if line.startswith("SET USERFRAME"):
                set_flag_username = True
                index_username = i
            elif line.startswith('CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"'):
                set_flag_trigger = True
                index_trigger = i

        if not set_flag_username:
            msg = "The command SET USERFRAME does not exist"
            line = len(job_file.headlines) + index_trigger + 1
            job_file.error_flag = True
            return (group, number, line, msg)

        if set_flag_username and set_flag_trigger and index_username > index_trigger:
            msg = "The command SET USERFRAME must be executed before the command CALL JOB:TRIGGER ARGF PROGRAMM_EIN is called"
            line = len(job_file.headlines) + index_username + 1
            job_file.error_flag = True
            return (group, number, line, msg)


def check_w4(
    job_file: JobFile, group: str, number: int
) -> list[tuple[str, int, int, str]]:
    """Check (JBI-W4).

    When a the TCPON command is called, the previous line must be a call to
    CALL JOB:SET_TCPON with the same argument number in both cases.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.

    Returns
    -------
    warnings : list of tuples
        Error messages.
    """
    errors = []
    error_lines = []

    argument = None
    index_tcpon = 0

    for index, item in job_file.command_lines:
        if item.startswith("TCPON TL#("):
            start_index = item.find("(")
            end_index = item.find(")", start_index)
            argument = item[start_index + 1 : end_index]
            index_tcpon = index
            if not job_file.command_lines[index_tcpon - 2][1].startswith(
                "CALL JOB:SET_TCPON ARGF" + argument
            ):
                line = len(job_file.headlines) + index_tcpon - 2
                error_lines.append(line)
                errors.append(
                    "When a TCPON command is called, the previous line must be a call to CALL JOB:SET_TCPON with the same argument number in both cases"
                )

    for index, item in job_file.command_lines:
        if item.startswith("CALL JOB:SET_TCPON ARGF"):
            argument = item[23:]
            index_call = index - 1
            if not job_file.command_lines[index_call + 1][1].startswith(
                "TCPON TL#(" + argument + ")"
            ):
                line = len(job_file.headlines) + index_call - 1
                error_lines.append(line)
                errors.append(
                    "When a TCPON command is called, the previous line must be a call to CALL JOB:SET_TCPON with the same argument number in both cases"
                )

    if errors:
        return [
            (group, number, line, msg)
            for msg, line in zip(errors, error_lines, strict=True)
        ]


def check_w5(job_file: JobFile, group: str, number: int) -> tuple[str, int, int, str]:
    """Check (JBI-W5).

    For all jobs in folder MAIN: The first program line (after initial
    comments) as well as the final program line should be CALL JOB:TRIGGER_RESET.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.

    Returns
    -------
    warnings : tuple
        Error messages.
    """
    if job_file.foldername == "MAIN":
        command_indexes = [
            (i, line.strip())
            for i, line in enumerate(job_file.programlines)
            if not line.startswith("'")
        ]
        if (
            not command_indexes[1][1]
            == command_indexes[-2][1]
            == "CALL JOB:TRIGGER_RESET"
        ):
            msg = "For all jobs in folder MAIN: The first program line (after initial comments) as well as the final program line should be CALL JOB:TRIGGER_RESET"
            return (group, number, None, msg)


def check_w6(
    job_file: JobFile, group: str, number: int
) -> list[tuple[str, int, int, str]]:
    """Check (JBI-W6).

    ARCON and ARCOFF commands should be enclosed in a call of
    CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN" immediately before the ARCON command and a
    call to CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS" immediately after the ARCOF command.

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.

    Returns
    -------
    warnings : list of tuples
        Error messages.
    """
    errors = []
    error_lines = []

    for i in range(len(job_file.programlines) - 1):
        current_line = job_file.programlines[i].strip()
        next_line = job_file.programlines[i + 1].strip()

        # XOR operator: 1 ^ 0 = True, 0 ^ 1 = True
        # Check for ARCON
        if next_line.startswith("ARCON") ^ current_line.startswith(
            'CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"'
        ):
            job_file.error_flag = True
            line = i + len(job_file.headlines) + 1
            error_lines.append(line)
            errors.append(
                'ARCON command should be enclosed in a call of CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"'
            )

        # Check for ARCOF
        elif current_line.startswith("ARCOF") ^ next_line.startswith(
            'CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"'
        ):
            job_file.error_flag = True
            line = i + len(job_file.headlines) + 1
            error_lines.append(line)
            errors.append(
                'ARCOF command should be enclosed in a call of CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"'
            )

        else:
            pass

    if errors:
        return [
            (group, number, line, msg)
            for msg, line in zip(errors, error_lines, strict=True)
        ]


def check_w7(job_file: JobFile, group: str, number: int) -> tuple[str, int, int, str]:
    """Check (JBI-W7).

    If foldername is MAIN, the command CALL JOB:SET_IDS_FULL (with arguments) must be
    present and called before CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"

    Parameters
    ----------
    job_file : ojb:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.

    Returns
    -------
    warnings : tuple
        Error messages.
    """
    index_set = []
    index_trigger = []
    set_string = "CALL JOB:SET_IDS_FULL"
    trigger_string = 'CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"'

    if job_file.foldername != "MAIN":
        return

    for line_number, line in job_file.command_lines:
        if line.startswith(set_string):
            index_set.append(line_number)
        elif line.startswith(trigger_string):
            index_trigger.append(line_number)

    if not index_set and not index_trigger:
        pass
    elif index_set and not index_trigger:
        pass
    elif not index_set and index_trigger:
        msg = "CALL JOB:SET_IDS_FULL doesn't exist"
        line = index_trigger[0] + 1
        return (group, number, line, msg)
    elif (index_set and index_trigger) and (index_set[0] > index_trigger[0]):
        msg = set_string + " must be called before " + trigger_string
        line = index_set[0] + 1
        return (group, number, line, msg)


def check_w8(
    job_file: JobFile, group: str, number: int
) -> list[tuple[str, int, int, str]]:
    """Check (JBI-W8).

    Trigger pairs (ON / OFF) must always be present in "closed" pairs.

    Parameters
    ----------
    job_file : obj:`jobFile`
        Object of a jobFile class.
    group : str
        Group of the warning.
    number : int
        Number of the warning.

    Returns
    -------
    warnings : list of arrays
        Error messages.
    """
    errors = []
    error_lines = []

    trigger_pairs = [
        ('CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"', 'CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"'),
        (
            'CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"',
            'CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"',
        ),
        ('CALL JOB:TRIGGER ARGF"UI_START"', 'CALL JOB:TRIGGER ARGF"UI_STOP"'),
        ('CALL JOB:TRIGGER ARGF"TRIG_EIN"', 'CALL JOB:TRIGGER ARGF"TRIG_AUS"'),
    ]

    for start_trigger, end_trigger in trigger_pairs:
        stack = []

        for line_number, line_content in job_file.command_lines:
            if start_trigger in line_content:
                stack.append((start_trigger, line_number))
            if end_trigger in line_content:
                if not stack:
                    errors.append(f"Unopened trigger pair: {(end_trigger)}")
                    error_lines.append(line_number)
                else:
                    stack.pop()

        for unclosed_trigger in stack:
            error_lines.append(unclosed_trigger[1])
            errors.append(f"Unclosed trigger pair: {(unclosed_trigger[0])}")

    if errors:
        return [
            (group, number, line + 1, msg)
            for msg, line in zip(errors, error_lines, strict=True)
        ]
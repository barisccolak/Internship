## quickstart
Fileparser package contains various rules to verify the a JBI data.

## user guide

### Installation

Install the python package:

    pip install testmodule

To check the rules for a single `.JBI` file:

    python fileparser.py <your-file>

To check the rules for all files in a folder:

    python fileparser.py <your-path>

## List of error codes

- w1 : job should start with a comment line
    directly after the NOP statement.
- w2 : program command `SETREG MREG#` should only be allowed when the job is listed under `FOLDERNAME TWINCAT_KOMMUNIKATION`
- w3 : if the job is in the folder `STANDARD` or `MAIN`, the line `SET USERFRAME n` must be present, where n is any numerical value. The command `SET USERFRAME` must be executed before the command `CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"` is called.
- w4 : if a the `TCPON` command is called, the previous line must be a call to CALL `JOB:SET_TCPON` with the same argument number in both cases.
- w5 : for all jobs in folder `MAIN`: The first program line (after initial comments) as well as the final program line should be `CALL JOB:TRIGGER_RESET`.
- w6 : `ARCON` and `ARCOFF` commands should be enclosed in a call of `CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"` immediately before the `ARCON` command and a call to `CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"` immediately after the `ARCOFF` command.
- w7 :  If foldername is `MAIN`, the command `CALL JOB:SET_IDS_FULL` (with arguments) must be present and called before `CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"`
- w8 : Trigger pairs:

    `CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"`-`CALL JOB:TRIGGER ARGF"PROGRAMM_AUS"`,

    `CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"`-`CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"`,

     `CALL JOB:TRIGGER ARGF"UI_START"`-`CALL JOB:TRIGGER ARGF"UI_STOP"`,

     `CALL JOB:TRIGGER ARGF"TRIG_EIN"`-`CALL JOB:TRIGGER ARGF"TRIG_AUS"`

   must always be present in "closed" pairs.

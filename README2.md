## quickstart
Fileparser package contains various rules to verify the a JBI data.

## user guide

### Installation


    from testmodule import JobFile

    JobFile(`EXAMPLE_FILE.JBI`)

## List of error codes

- w1 : job should start with a comment line
    directly after the NOP statement.
- w2 : program command `SETREG MREG#` should only be allowed when the job is listed under `FOLDERNAME TWINCAT_KOMMUNIKATION`
- w3 : if the job is in the folder `STANDARD` or `MAIN`, the line `SET USERFRAME n` must be present, where n is any numerical value. The command `SET USERFRAME` must be executed before the command `CALL JOB:TRIGGER ARGF"PROGRAMM_EIN"` is called.
- w4 : if a the `TCPON` command is called, the previous line must be a call to CALL `JOB:SET_TCPON` with the same argument number in both cases.
- w5 : for all jobs in folder `MAIN`: The first program line (after initial comments) as well as the final program line should be `CALL JOB:TRIGGER_RESET`.
- w6 : `ARCON` and `ARCOFF` commands should be enclosed in a call of `CALL JOB:TRIGGER ARGF"SCHWEISSEN_EIN"` immediately before the `ARCON` command and a call to `CALL JOB:TRIGGER ARGF"SCHWEISSEN_AUS"` immediately after the `ARCOFF` command.

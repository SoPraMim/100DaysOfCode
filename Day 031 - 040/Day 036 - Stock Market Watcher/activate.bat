::This is a bat script to automate running python scripts with windows task scheduler. 
::Ref: https://stackoverflow.com/questions/49542912/schedule-a-script-developed-in-anaconda-via-windows-task-scheduler/58695782#58695782

@ECHO OFF 
TITLE Execute python script on anaconda environment
ECHO Please Wait...
:: Section 1: Activate the environment.
ECHO ============================
ECHO Conda Activate
ECHO ============================
@CALL "C:\Users\andre\anaconda3\Scripts\activate.bat" TestEnvironment
:: Section 2: Execute python script.
ECHO ============================
ECHO Python test.py
ECHO ============================
python "C:\Git\100DaysOfCode\Day 031 - 040\Day 036 - Stock Market Watcher\main.py"

ECHO ============================
ECHO End
ECHO ============================

PAUSE
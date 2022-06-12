Quantum Program exercise by Justin Graf

This is the script that I wrote for the exercise that was sent out

# Files

The files primary files for the program are : 

    quantum_program_runner.py
        This is where the actual compilation and running of the program happens. The json is loaded and parsed and then 
        ran. The services for AcmeInstrumentsSerice and MadridInstrumentsService are dynamically opened and closed for 
        the programs to be run. 

    instructions.py
        This file holds the classes that I use for the program. These classes store the instruction sets that are used 
        for the so that I can very easily add new instruments by simply adding classes with the proper variables. These 
        classes have a parent class ArithmeticInstructions that have a list of instructions preset but must be overrided 
        for the code to run properly since it is empty by default.

    quantum_tests.py
        This file holds the tests that I wrote. These tests simply check that the program can run a single program json 
        of an instrument, a list of programs for an instrument and a list of programs for multiple instruments.

# Running the program

This program is meant to be run through the command line. It has a #! at the top pointing to /usr/bin/python3, so you 
should only have to make the script executable when running on a Linux system. You can also precede the program with the
python command on the terminal if needed. 

The program has to be run in the file structure that is contained in the 7z file since it uses partially hardcoded paths
for starting the services and the locations of the files for the tests that were written.

The program comes with multiple flags that are used when running the program. The -f flag is used for running with a
specified json file and the -s flag is used for passing in a string for input.

The format for the command is:
    python quantum_program_runner.py [-h] [-f FILE_PATH] [-s JSON_STRING]

# Running the tests

To run the tests that I wrote just use the command:
    python quantum_tests.py

# Choices for the program design

I decided to use the class design for the instruments because is would be easier to add new instruments to the program. 
I simply need to add the instrument class and override the required variables and the code should be able to run the 
program. It also allows me to use less code to manage the steps and endpoints since different instruments require 
different steps and endpoints for running and loading the programs

I used dictionaries for multiple things because they can be keyed to the name of the instrument to make it easier to
chain together the required information while reducing the amount of conditionals I would need to use.

I decided to have the program start and stop the instrument services to keep everything self-contained instead of 
requiring the user to have to do it all manually so that the way the program would run would be more consistent.

I used the dictionaries to store the program code before running so that the services would only have to be started and 
stopped once throughout the run of the program

I tried researching better packages to use for translating the json but everything that I read pointed me back to the 
default python json library. I couldn't find another one with some Googling.

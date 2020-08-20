# engine_start_cycle.py

script lists the time engine takes to start running.
The results are displaied in the following format: <Start Cycle: n Duration: HH:MM:SS>.

Regex is used to identify the related messages.

# How to run
```python3
python3 engine_start_cycle.py [-h] [-- log <log path>]
optional arguments: -h, -- help
show this help message and exit -- log
Engine log file to be parsed for cycles duration. If not provided, the script will assume log file is in $PWD/engine.log
```

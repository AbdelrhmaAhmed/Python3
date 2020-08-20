
# import needed libraries
import re
import time
import argparse
"""
This Python script lists the time engine takes to start running.
The results are displaied <Start Cycle: n Duration: HH:MM:SS>.

Regex is used to identify the related messages.
Author: Abdelrhman Ahmed
"""


class Cycles_info():
    """
    The class is responsible for collecting and calculating (set/get) cycle furations.
    It's also responcible for displaying the messages in the requested format.
    """

    def __init__(self):
        self.cycles_start_times = []
        self.cycles_running_times = []
        self.cycles_duration = []

    def get_start_and_running_times(self, log_to_scan: str) -> list:
        """
        Method to capture start and running times for all cycles.

        :param log_to_scan: The engine log file to scan for time stamps.
        :return: list
        """
        # regex to capture engine messages that indicate the process start time
        cycle_starting_regex = re.compile("^\w+\s+(\d\d?)\s+(\d\d):(\d\d):(\d\d)\s+.*?\s+(starting randengine)\s+.*?(/usr/bin/randengine)]\s*$")
        # regex to capture engine messages that indicate the process running time
        cycle_running_regex = re.compile("^\w+\s+(\d\d?)\s+(\d\d):(\d\d):(\d\d)\s+.*?\s+(randengine is running)\s*$")
        # list that will be loaded with start and running times.
        start_times = []
        running_times = []

        # open engine log file to start capturing the messages
        with open(log_to_scan, 'r') as fileToScan:
            # scan each line of the file
            for line in fileToScan:
                if cycle_starting_regex.match(line):
                    # found a cycle start message; set related time stamp variables
                    day_of_month = int(cycle_starting_regex.match(line).group(1))
                    hours = int(cycle_starting_regex.match(line).group(2))
                    minutes = int(cycle_starting_regex.match(line).group(3))
                    seconds = int(cycle_starting_regex.match(line).group(4))
                    start_times.append([day_of_month, hours, minutes, seconds])

                elif cycle_running_regex.match(line):
                    # found a cycle running message; set related time stamp variables
                    day_of_month = int(cycle_running_regex.match(line).group(1))
                    hours = int(cycle_running_regex.match(line).group(2))
                    minutes = int(cycle_running_regex.match(line).group(3))
                    seconds = int(cycle_running_regex.match(line).group(4))
                    running_times.append([day_of_month, hours, minutes, seconds])

                else:
                    # line is not related to the cycle start/running time
                    continue
        return start_times, running_times

    def set_cycles_start_times(self, values_to_set: list) -> None:
        """
        Method to set cycles_start_times class variable.

        :param values_to_set: The list variable to be passed to the class variable.
        :return: None
        """
        self.cycles_start_times = values_to_set

    def set_cycles_running_times(self, values_to_set: list) -> None:
        """
        Method to set cycles_running_times class variable.

        :param values_to_set: The list variable to be passed to the class variable.
        :return: None
        """
        self.cycles_running_times = values_to_set

    def set_cycles_duration(self) -> None:
        """
        Method to calculate the duration of all detected cycles.

        :return: None
        """
        # List that hold all detected start cycles times
        start_times = self.cycles_start_times
        # List that hold all detected running cycles times
        running_times = self.cycles_running_times
        # list to be populated with cycles duration
        duration = []
        # loop over start_times list, calculate cyles duration and finally update "cycles_duration" class variable
        for index in range(0, len(start_times)):
            try:
                duration_in_hours = running_times[index][1] - start_times[index][1]
                duration_in_minutes = running_times[index][2] - start_times[index][2]
                duration_in_seconds = running_times[index][3] - start_times[index][3]
                total_duration_in_seconds = (duration_in_hours*3600) + (duration_in_minutes*60)+duration_in_seconds
                duration.append(total_duration_in_seconds)
            except IndexError:
                # Execption is thrown when the last "randengine starting" message is detected but no "randengine is running" message was detected
                duration.append("Time-stamp messages are not available")
        self.cycles_duration = duration

    def display_durations(self) -> None:
        """
        Method to print the duration of all detected cycles in therequested format.

        :return: None
        """
        durations = self.cycles_duration
        for index in range(0, len(durations)):
            # Check if cycle time stamps are not available
            if type(durations[index])==str:
                print("Start Cycle: {} {}".format(index+1,durations[index]))
            else:
                print("Start Cycle: {} Duration: {}".format(index+1, time.strftime('%H:%M:%S', time.gmtime(durations[index]))))


def main():
    """
    Main loop.
    """

    # Detect if a log path have been provided to the script while being launched from command-line
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", help=":randengine log file to be scanned for cycles duration.", type=str)
    if parser.parse_args().log:
        randengine_Log = parser.parse_args().log
    else:
        randengine_Log = "engine.log"

    # Create instance of class Cycles_info
    Cycles = Cycles_info()

    # Get and store the time stamps for all "starting randengine" and "randengine is running" messages
    start_times, running_times = Cycles.get_start_and_running_times(randengine_Log)

    # set cycles_start_times variable
    Cycles.set_cycles_start_times(start_times)

    # set cycles_running_times variable
    Cycles.set_cycles_running_times(running_times)

    # Set / calculate each cycle duration
    Cycles.set_cycles_duration()

    # Display cycles duration in the requested format
    Cycles.display_durations()


if __name__ == '__main__':
    main()

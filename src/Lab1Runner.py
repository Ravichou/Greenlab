import psutil
import subprocess
from resource import getrusage, RUSAGE_SELF, RUSAGE_CHILDREN
from .utils import reportPerformances

class Lab1Runner:
    @staticmethod
    def findLongestPalindromeWrapper(command, command_input):
        process = subprocess.Popen(command + " " + command_input,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   shell=True)
        std_out, std_err = process.communicate()

        # Parse the response
        if std_err:
            print("errors " + std_err)
        response = std_out.split("RESPONSE: ")[1]
        std_out = std_out.split("RESPONSE: ")[0].split("\n")
        # Print stdout for lab debugging
        for i, line in enumerate(std_out):
            if i == len(std_out) - 1:
                # Last line
                print(line, end="")
            else:
                print(line)
        return response

    @staticmethod
    def run_test_lab1(command, funcTests):
        functional_validation_passed = True
        print("Running functional tests...")
        for i, test in enumerate(funcTests):
            try:
                result = Lab1Runner.findLongestPalindromeWrapper(command, test['input'])
                assert result == test['output'], f"Expected {test['output']} but got {result}"
                print("Test " + str(i) + " PASSED")
            except AssertionError as e:
                functional_validation_passed = False
                print("Test " + str(i) + " FAILED with error: ")
                print(e)
        return functional_validation_passed

    @staticmethod
    def run_perf_test_lab1(script, perfTest, SCI_service):
        print("Running performance test...")
        try:
            result = Lab1Runner.findLongestPalindromeWrapper(script, perfTest['input'])
            assert result == perfTest['output'], f"Expected {perfTest['output']} but got {result}"
            print("Perf test PASSED! \n")
            print("Gathering performance metrics...")
            # Gather host metrics
            cpu_load = psutil.cpu_percent(interval=None)
            # Gather runner metrics
            self_telemetries = getrusage(RUSAGE_SELF)
            self_cpu_time = self_telemetries.ru_utime + self_telemetries.ru_stime
            self_ram_MB = self_telemetries.ru_maxrss / 1024 / 1024
            # Gather algo metrics
            children_telemetries = getrusage(RUSAGE_CHILDREN)
            child_cpu_time = children_telemetries.ru_utime + children_telemetries.ru_stime
            child_ram_MB = children_telemetries.ru_maxrss / 1024 / 1024

            reportPerformances(cpu_load,
                               self_cpu_time,
                               self_ram_MB,
                               SCI_service(self_cpu_time, self_ram_MB),
                               child_cpu_time,
                               child_ram_MB,
                               SCI_service(child_cpu_time, child_ram_MB))

        except AssertionError as e:
            print("Perf test FAILED with error: ")
            print(e)

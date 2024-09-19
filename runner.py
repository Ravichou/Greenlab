import time
import os
import psutil
import optparse
import importlib

def findLongestPalindromeWrapper(input, isPython, lab = 0):
    if isPython:
        result = lab.findLongestPalindrome(input)
    else:
        import subprocess
        if os.name == 'posix':
            result = subprocess.run(["./LAB1_2.bin", input], stdout = subprocess.PIPE,
                    universal_newlines = True).stdout
        elif os.name == 'nt':
            result = subprocess.run(["LAB1_2.exe", input], stdout = subprocess.PIPE,
                    universal_newlines = True).stdout
    return result

def run_func_test(lab, funcTests, isPython):
    functional_validation_passed = True
    print("Running functional tests...")
    for i, test in enumerate(funcTests):
        try:
            result = findLongestPalindromeWrapper(test['input'], isPython, lab)
            assert result == test['output'], f"Expected {test['output']} but got {result}"
            print("Test "+str(i)+" PASSED")
        except AssertionError as e:
            functional_validation_passed = False
            print("Test "+str(i)+" FAILED with error: ")
            print(e)
    return functional_validation_passed

def run_perf_test(lab, perfTest, isPython, SCI_service):
    try:
        # Technical gap : the elapsed time is not the same as the CPU time. 
        # However we cannot measure CPU time of a dead process in Windows, meaning that the runner is not able to measure the CPU time of the perf test.
        # Measuring the elapsed is a close enough solution, for CPU, as we are monothreaded. 
        # For RAM, we have the same problem but we can't approximate it from the parent.
        # Furthermore we want to apply the same measurement methodology to Python and C++.
        # There are several options:
        # - use Boost Python to import C++ code in Python and measure the CPU time from the Python code
        # - include the RAM and CPU measures in each lab main function, run the labs as subprocesses and return the metrics to the runner.
        start_time = time.time()
        result = findLongestPalindromeWrapper(perfTest['input'], isPython, lab)
        run_time = time.time() - start_time
        assert result == perfTest['output'], f"Expected {perfTest['output']} but got {result}"
        print("Perf test PASSED! \n")
        print("Gathering performance metrics...")

        # Gathering performance metrics
        cpu_time = run_time
        RAM_usage_MB = round(psutil.Process().memory_info().rss / 1024 / 1024, 2)
        cpu_load = psutil.cpu_percent(interval=5) # Wait 5 seconds to get a stable CPU load

        if os.name == 'posix':
            from resource import getrusage, RUSAGE_SELF, RUSAGE_CHILDREN
            self_telemetries = getrusage(RUSAGE_SELF)
            children_telemetries = getrusage(RUSAGE_CHILDREN)
            cpu_time = self_telemetries.ru_utime + self_telemetries.ru_stime
            RAM_usage_MB = self_telemetries.ru_maxrss/1024/1024
            child_cpu_time = children_telemetries.ru_utime + children_telemetries.ru_stime
            child_ram_MB = children_telemetries.ru_maxrss/1024/1024
        elif os.name == 'nt':
            # Windows to be implemented - or not, if we stick to the Docker image
            pass

        print("--- Performance metrics ---")
        print("CPU time : " + str(round(cpu_time,3) * 1000) + " ms")
        print("RAM usage in MB : " + str(RAM_usage_MB))
        print("CPU load in percent : " + str(cpu_load))
        print("SCI score in mgCO2 : " + str(SCI_service(cpu_time, RAM_usage_MB, cpu_load)))
        if os.name == 'posix' and not isPython:
            print("\n", end="")
            print("--- C++ process ---")
            print("C++ CPU time : " + str(round(child_cpu_time, 3) * 1000) + " ms")
            print("C++ RAM in MB : " + str(child_ram_MB))
            print("C++ SCI score in mgCO2 : " + str(SCI_service(child_cpu_time, child_ram_MB, cpu_load)))
        elif os.name == 'nt':
            # Windows to be implemented
            pass

    except AssertionError as e:
        print("Perf test FAILED with error: ")
        print(e)

def main():
    """Main function to parse arguments."""
    parser = optparse.OptionParser()
    parser.add_option(
        "-l", "--lab", help="The lab number", action="store", default=""
    )
    parser.add_option(
        "-s", "--solution", help="Run solutions", action="store_true", default=False
    )
    (options, args) = parser.parse_args()
    if options.solution:
        labsFolder = 'Solutions'
    else:
        labsFolder = 'Labs'
    print("#################################")
    print("############ GREENLAB ###########")
    print("######## Running lab "+options.lab+" ######## \n")
    # Import the SCI module
    SCI = importlib.import_module(labsFolder+'.Lab2.LAB2')
    if options.lab[0] == "1":
        isPython = True
        lab = 0
        tests = importlib.import_module(labsFolder+'.Lab1.tests')
        if options.lab == "1.1":
            lab = importlib.import_module(labsFolder+'.Lab1.Lab1_1.LAB1_1')
        elif options.lab == "1.2":
            import subprocess
            isPython = False
            if os.name == 'posix':
                print("C++ code detected. Compiling C++ code...")
                subprocess.run(["g++", "-o", "LAB1_2.bin", labsFolder+r'/Lab1/Lab1_2/LAB1_2.cpp'])
                print("C++ code compiled!\n")
            elif os.name == 'nt':    
                print("Compiling C++ code...")
                subprocess.run(["g++", "-o", "LAB1_2.exe", labsFolder+r'\Lab1\Lab1_2\LAB1_2.cpp'])
                print("C++ code compiled.\n")
        elif options.lab == "1.3":
            lab = importlib.import_module(labsFolder+'.Lab1.Lab1_3.LAB1_3')
        # Run tests
        if run_func_test(lab, tests.funcTests, isPython):
            print("Functional tests PASSED! \n")
            print("Now running performance test...")
            run_perf_test(lab, tests.perfTest, isPython, SCI.SCI_service)
    elif options.lab == "2":
        tests = importlib.import_module(labsFolder+'.Lab2.tests')
        SCI.main(tests)
    elif options.lab[0] == "3":
        tests = importlib.import_module(labsFolder+'.Lab3.tests')
        if options.lab == "3.1":
            lab = importlib.import_module(labsFolder+'.Lab3.Lab3_1.LAB3_1')
            lab.main(tests.level1)
        elif options.lab == "3.2":
            lab = importlib.import_module(labsFolder+'.Lab3.Lab3_2.LAB3_2')
            lab.main(tests.level2)
    else:
        print("Invalid lab number")
        exit(1)
    print("#################################")

if __name__ == "__main__":
    main()
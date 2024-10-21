import os
import click
import importlib
import subprocess
from src.Lab1Runner import Lab1Runner


def compile_cpp(lab_folder, labs_folder):
    if os.name == 'posix':
        process = subprocess.Popen(["g++", "-o", lab_folder[:-3]+"bin", lab_folder],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        std_out, std_err = process.communicate()
        if std_err:
            print(std_err)
            return None
        return lab_folder[:-3]+"bin"
    elif os.name == 'nt':
        process = subprocess.Popen(["g++", "-o", labs_folder+r'\Lab1\Lab1_2\LAB1_2.exe', labs_folder+r'\Lab1\Lab1_2\LAB1_2.cpp'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        std_out, std_err = process.communicate()
        if std_err:
            print(std_err)
            return None
        return labs_folder+r'\Lab1\Lab1_2\LAB1_2.exe'

@click.command()
@click.option('-l', '--lab_number', required=True, type=click.Choice(['1.1', '1.2', '1.3', '2', '3.1', '3.2']), help='The lab number')
@click.option('-s', '--solution', is_flag=True, default=False, help='Run solutions')
@click.option('-c++', '--run_in_cpp', is_flag=True, default=False, help='Run in c++')
def main(lab_number, solution, run_in_cpp):
    """Main function to parse arguments."""
    labs_folder = 'Solutions' if solution else 'Labs'
    print("#################################")
    print("############ GREENLAB ###########")
    print(f"######## Running lab {lab_number} ######## \n")

    # Import the SCI module
    SCI = importlib.import_module(labs_folder+'.Lab2.LAB2')

    if lab_number.startswith("1"):  # Lab 1
        launch_lab1(lab_number, labs_folder, SCI, run_in_cpp)
    elif lab_number == "2":  # Lab 2
        launch_lab2(labs_folder, SCI)
    elif lab_number.startswith("3"):  # Lab 3
        launch_lab3(lab_number, labs_folder)
    print("#################################")


def launch_lab3(lab_number, labs_folder):
    tests = importlib.import_module(f'{labs_folder}.Lab3.tests')
    if lab_number == "3.1":
        lab_number = importlib.import_module(f'{labs_folder}.Lab3.Lab3_1.LAB3_1')
        lab_number.main(tests.level1)
    elif lab_number == "3.2":
        lab_number = importlib.import_module(f'{labs_folder}.Lab3.Lab3_2.LAB3_2')
        lab_number.main(tests.level2)


def launch_lab2(labs_folder, SCI):
    tests = importlib.import_module(f'{labs_folder}.Lab2.tests')
    SCI.main(tests)


def launch_lab1(lab_number, labs_folder, SCI, run_in_cpp):
    lab_path = ""
    tests = importlib.import_module(f'{labs_folder}.Lab1.tests')
    decimal = lab_number.split(".")[1]
    lab_path = f'{labs_folder}/Lab1/Lab1_{decimal}/LAB1_{decimal}.py'
    command = f"python {lab_path}"
    if lab_number == "1.2" or run_in_cpp:
            # Compile C++ code
        print("C++ code detected. Compiling C++ code...")
        print(lab_path[:-2]+"cpp")
        compiled_script = compile_cpp(lab_path[:-2]+"cpp", labs_folder)
        if compiled_script:
            command = compiled_script
            print("C++ code compiled!\n")
        else:
            print("C++ code compilation failed.")
            exit(1)
        # Run tests
    if Lab1Runner.run_test_lab1(command, tests.funcTests):
        print("Functional tests PASSED! \n")
        print("Now running performance test...")
        Lab1Runner.run_perf_test_lab1(command, tests.perfTest, SCI.SCI_service)


if __name__ == "__main__":
    main()
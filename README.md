# GreenLab v0.3

## What is the repository?

The repository is divided in different labs, that are little exercises.  

The first lab is an introduction that consists in writting little pieces of code about palindroms.

The second lab is an implementation of calculation of carbon emission of an application.

The third lab is to plan a schedule of jobs to minimize carbon emissions within different datacenters.


## Usage

There are 2 ways to do the labs: with or without the Docker image.

## 1. With Docker image

### 1.1. Requirements

The following dependencies need to be installed before running :
* Docker or Podman

### 1.2. Running the labs

From the root of the repository, run:

```shell
./run.sh -l *lab_number*
```

or manually

```shell
docker run --rm -it -v ./Labs:/app/Labs ravichou/greenlab:*version_number* python3 runner.py -l *lab_number*
```
Example:
```shell
docker run --rm -it -v ./Labs:/app/Labs ravichou/greenlab:0.0.3 python3 runner.py -l 1.2
```

## 2. Without Docker image

### 2.1. Requirements

The following dependencies need to be installed before running :
* python v3.11

### 2.2. Installation

Run the following commands, which will create a python environment and install the dependencies:
#### Windows
```shell
py -m venv .venv
.\.venv\Scripts\activate
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
```

#### Linux
```shell
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -r requirements.txt
```

If you get ` Python not found` error while using the `py` or `python3` commands:

This happens because the **Python path doesn't exist in environment variables**.

You can:
1. Rerun the Python installer
2. Choose Modify
3. In optional feature click "Next"
4. In advanced option tick the "**Add Python to environment variables**"
5. Install

### 2.3. Running the labs

#### Windows
```shell
py .\runner.py -l *lab_number*
```
Example:
```shell
py .\runner.py -l 1.1
```

#### Linux
```shell
.venv/bin/python ./runner.py -l *lab_number*
```
Example:
```shell
.venv/bin/python ./runner.py -l 1.1
```

For both Windows and Linux, you can deactivate the virtual environment with the following command:
```shell
deactivate
```

### 2.4. To compile LAB1_2

#### Windows
You need a c++ compiler.

Follow instructions to install MinGW-w64 toolchain here https://code.visualstudio.com/docs/cpp/config-mingw

You can then update your PATH with
```shell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

The compilation is then automatically performed when you start lab 1.2

For reference, the command used:
```shell
g++ .\Labs\Lab1\Lab1_2\LAB1_2.cpp -o LAB1_2.exe
```

#### Unix
Nothing to do here.

The compilation is automatically performed when you start lab 1.2

For reference, the command used:
```shell
g++ ./Labs/Lab1/Lab1_2/LAB1_2.cpp -o LAB1_2.bin
```

## 3. To Do

Runner:
    
    Execute python labs in subprocesses

Lab3:

    Add comparator with/without optimizer
    Add lab 3_3

## 4. Building and publishing Docker image
Run the following command to build the docker image:
```shell
docker build . -t ravichou/greenlab:*version_number*
docker push ravichou/greenlab:*version_number*
```
Then update the image version in config.json

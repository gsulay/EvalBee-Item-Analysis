# EvalBee Item Analysis

A Python program for analyzing item-level data from EvalBee exports.

## Description

This program takes an Excel file exported from EvalBee as input and performs various item-level analyses, including reliability calculations and topic analysis.

## Requirements

* Python 3.x
* pandas
* numpy
* pingouin
* scipy
* openpyxl

## Usage

To run the program, simply execute the script with the path to the input Excel file as an argument:
```bash
python item_analysis.py <input_file.xlsx> [<output_file.xlsx>]
```

## Installation
Install the dependencies using pip or if you are using the Anaconda environment, conda. Python 3.9.x and above is supported.

### Using `pip`.
1. Create the virtual environment.
```bash
#Replace <env> with environment name e.g. `venv`
python3 -m venv <env>
```
2. Activate the environment.
```bash
#On Windows
./<env>/Scripts/activate
#On MacOS/Linux
source ./<env>/bin/activate

```
3. Install the dependencies.
```bash
pip install pandas numpy pingouin scipy openpyxl
```

### Using conda.
1. Create the virtual environment
```bash
#Replace <env> with environment name(e.g. 'venv') and <python_name> with preferred python version(e.g. 3.10) 
conda create -p ./<env> python=<python_version>

```
2. Activate the environment
```bash
conda activate ./<env>
```
3. Install the dependencies.
```bash
conda install -c conda-forge pandas numpy pingouin scipy openpyxl
```
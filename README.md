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
* argparse

## Usage

To run the program, simply execute the script with the path to the input Excel file as an argument:

```bash
python item_analysis.py <input_file.xlsx> [<output_file.xlsx>]
```

# EvalBee Item Analysis  

A Python program for analyzing item-level data from EvalBee exports.  

## Description  

EvalBee Item Analysis is a tool designed to process Excel files exported from EvalBee, providing item-level analyses such as:  
- Reliability calculations  
- Topic analysis  

## Requirements  

Ensure the following are installed:  
- Python 3.9 or later  
- Libraries:  
  - `pandas`  
  - `numpy`  
  - `pingouin`  
  - `scipy`  
  - `openpyxl`  

## Installation  

You can set up the program environment using either `pip` or `conda`.  

### Using `pip`  

1. **Create a virtual environment**  
   ```bash  
   python3 -m venv <env_name>  
   ```  
2. **Activate the virtual environment**  
   - **Windows**:  
     ```bash  
     .\<env_name>\Scripts\activate  
     ```  
   - **macOS/Linux**:  
     ```bash  
     source <env_name>/bin/activate  
     ```  
3. **Install dependencies**  
   ```bash  
   pip install pandas numpy pingouin scipy openpyxl  
   ```  

### Using `conda`  

1. **Create a virtual environment**  
   ```bash  
   conda create -p ./<env_name> python=<python_version>  
   ```  
   Replace `<env_name>` with your preferred environment name (e.g., `venv`) and `<python_version>` with your desired Python version (e.g., 3.10).  

2. **Activate the environment**  
   ```bash  
   conda activate ./<env_name>  
   ```  

3. **Install dependencies**  
   ```bash  
   conda install -c conda-forge pandas numpy pingouin scipy openpyxl  
   ```  

## Usage  

Run the program by providing the path to the input Excel file. Optionally, you can specify an output file path for the results.  
```bash  
python item_analysis.py <input_file.xlsx> [<output_file.xlsx>]  
```  

## Notes  

- Replace `<env_name>` with your chosen environment name in the commands above.  
- Replace `<python_version>` with your preferred Python version when using `conda`.  
- If you encounter issues with dependencies, ensure the correct Python version and library versions are installed.  

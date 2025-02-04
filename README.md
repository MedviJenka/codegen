# CodeGen Automation Tool

## 📌 Overview
This project is an automation tool that sets up and runs a Python script inside a virtual environment. It automatically installs dependencies and **Playwright** if not already installed.

## 🚀 Features
- **Automatic virtual environment setup**
- **Dependency installation from `requirements.txt`**
- **Playwright installation and browser setup**
- **Ensures Python is installed before execution**
- **Runs the `codegen.py` script automatically**
- **Supports interactive user input for custom execution**

---


## 📥 Installation & Usage

### 1️⃣ **Clone the Repository**
If this project is in a Git repository, clone it using:
```sh
git clone <repository-url>
cd codegen
run the run_codegen.ps1
````

### If you encounter powershell installation problem which happened once
 
navigate to project directory
create virtual env manually or py -m venv ./venv
activate the venv
pip install -r requirements.txt
run the code manually in /engine/codegen.py 



## Usage

###  **Run the Script**
```

1. Device Type: The type of device you want to test with.	st or mi or leave empty
2. Output CSV File	The filename where interactions will be saved.	default is: page_base.csv
3. Custom Screen URL	The URL of the screen for testing. Leave blank to use default.	https://www.google.com
4. Generate Code?	Whether to generate Python test code (y/n).
```

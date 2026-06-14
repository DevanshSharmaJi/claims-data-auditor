# claims-data-auditor

**What it does:**

This tool runs a quality check of any claims data and provide specific numbers on where the data is lacking.
It runs the following quality checks on the data:

- missing values
- duplicates
- date check
- amount check
- categories check

The output contains a specific numbers on where the data is lacking in the above mentioned checks.

**How to run it:**

If you don't have python already installed, install it:

`Download and install Python from https://python.org`

Install pandas:

`pip install pandas`

Use the following command in the terminal to execute the code:

`py audit.py claims.csv`

**Sample output:**

<img width="479" height="259" alt="image" src="https://github.com/user-attachments/assets/f2c3422c-d560-4cca-9700-268bf83caae2" />


import pandas as pd
import sys

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

def check_missing(df):
    tot = 0
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            tot += 1
    if tot > 0:
        res1 = "FAIL"
    else:
        res1 = "PASS"
    return res1, tot

def check_duplicates(df, claim_id_col):
    # prints duplicate section
    total = df.shape[0]
    unique_ids = df[claim_id_col].nunique()
    duplicate_ids = total - unique_ids
    if duplicate_ids > 0:
        res2 = "FAIL"
    else:
        res2 = "PASS"
    return res2, duplicate_ids

def check_amounts(df,amount_col):
    # prints billed amount section
    if amount_col in df.columns:
        invalid_amt = df[df[amount_col] <= 0].shape[0]
        if invalid_amt > 0:
            res3 = "FAIL"
        else:
            res3 = "PASS"
    else:
        print("No amount columns found!!")
    return res3, invalid_amt

def check_dates(df, admit_date, discharge_date):
    # prints date logic section
    admit = pd.to_datetime(df[admit_date], errors="coerce")
    discharge = pd.to_datetime(df[discharge_date], errors="coerce")
    wrong_date = (discharge < admit).sum()
    if wrong_date > 0:
        res4 = "FAIL"
    else:
        res4 = "PASS"   
    return res4, wrong_date

def check_categoricals(df, claim_type, diagnosis_code):
    # prints claim type and diagnosis code sections
    valid_types = ["Medical", "Pharmacy", "Dental", "Vision"]
    total_invalid = df[~df[claim_type].isin(valid_types)].shape[0]
    invalid_pct = (100*total_invalid)/df.shape[0]

    val_icd = df[diagnosis_code].str.match(r"^[A-Z]\d").sum()
    inv_icd = df.shape[0] - val_icd
    inv_icd_pct = (100*inv_icd)/df.shape[0]
    if total_invalid > 0:
        res5 = "FAIL"
    else:
        res5 = "PASS"
    if inv_icd > 0:
        res6 = "FAIL"
    else:
        res6 = "PASS"
    return res5, total_invalid, invalid_pct, res6, inv_icd, inv_icd_pct


def run_audit(filepath):
    df = load_data(filepath)
    print("File Loaded")
    # print header
    res1, miss_val = check_missing(df)
    res2, dupe = check_duplicates(df, "claim_id")
    res3, amt = check_amounts(df, "billed_amount")
    res4, wdate = check_dates(df, "service_date", "discharge_date")
    res5, type_issue, type_pct, res6, code_issue, code_pct = check_categoricals(df, "claim_type", "diagnosis_code")
    all_res = [res1, res2, res3, res4, res5, res6]
    failed = 0
    passed = 0
    for i in all_res:
        if i == "FAIL":
            failed += 1
        elif i == "PASS":
            passed += 1
    # call all check functions
    print("========================================")
    print("AUDIT SUMMARY")
    print("========================================")
    print(f"[{res1}] Missing values found in {miss_val} columns")
    print(f"[{res4}] {wdate} structural issues in dates column")
    print(f"[{res2}] {dupe} duplicate claim IDs detected")
    print(f"[{res3}] {amt} invalid billed amounts")
    print(f"[{res5}] {type_issue} invalid claim types ({type_pct:.1f}%)")
    print(f"[{res6}] {code_issue} invalid diagnosis codes ({code_pct:.1f}%)")
    print("========================================")
    print(f"Overall : {failed} checks failed, {passed} passed")
    print("========================================")

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "claims.csv"
    run_audit(filepath)
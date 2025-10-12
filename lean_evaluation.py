import os
import subprocess
import re
import sys
import numpy as np
import pandas as pd
from pydantic import BaseModel
from typing import Optional, get_origin, get_args, Union
from prompt import (
    basic_forms,
    itemized_forms,
    self_employ_forms,
    edu_forms,
    schedule_8812
)
from structured_forms import Form1040, TaxPayer, Student, FilingStatus
import tempfile
from python_evaluation import compute_actual_answer

formalize_system_prompt = "You are a helpful US taxation consultant an expert at structured data extraction. You are given a tax payer's information and a LLM's response to fill out the 1040 form step-by-step according to the information provided. You should convert the unstructured LLM response into the given structure."

formalize_prompt_template = """
IRS Forms for the tax payer:
$forms
Calculate the tax owed by the payer step-by-step according to the information provided by the forms. You should calculate all fields marked with [__]. End your response with:
1. "The total tax owed is $xxx." (xxx is a number) if there is tax owed.
2. "The total tax overpaid is $xxx." (xxx is a number) if there is tax overpaid (and should be refunded).
Your response:
$response
"""

tbd_mark = "[__]"
lean_rules_file = "rules.lean"

rule_list = [
    "wage and tip compensation total",
    "net profit",
    "self employment tax",
    "self employment deductible",
    "additional income",
    "total income",
    "total adjustments",
    "adjusted gross income",
    "standard deductions",
    "itemized deductions",
    "total deductions",
    "taxable income",
    "standard taxes",
    "qualified dividends and capital gains taxes",
    "schedule 2 total part i taxes",
    "schedule 2 taxes copy",
    "accumulated taxes",
    "ctc or other dependent credit",
    "additional child tax credit",
    "american opportunity credit",
    "education credits",
    "schedule 3 line 8",
    "schedule 3 total credits copy",
    "accumulated credits computation",
    "taxes after credits computation",
    "other taxes computation",
    "other additional taxes copy",
    "total tax computation",
    "total other payments and refundable credits computation",
    "total payments computation",
    "amount owed or overpaid computation"
]


#Assumptions on tax_payer data:
#not tax_payer_pydantic.self_employed
#tax_payer_pydantic.qualified_dividends == 0.0
# not (structured_output.num_qualifying_children + structured_output.num_other_dependents > 0)
# not (structured_output.student_list is not None and len(structured_output.student_list) > 0)
lean_rule_list = [
    "rule1",
    "rule5",
    "rule6",
    "rule7",
    "rule8",
    "rule910",
    "rule11",
    "rule12",
    "rule13",
    "rule15",
    "rule16",
    "rule17",
    "rule22",
    "rule23",
    "rule24",
    "rule25",
    "rule26",
    "rule27",
    "rule28",
    "rule29",
    "rule30",
    "rule31"
]

def build_prompt(tax_payer: dict, response: str):
    forms = [basic_forms]
    if tax_payer["itemized"]:
        forms.append(itemized_forms)
    if tax_payer["self_employed"]:
        forms.append(self_employ_forms)
    if tax_payer["has_student_loans_or_education_expenses"]:
        forms.append(edu_forms)
    if tax_payer["child_and_dependent"]:
        forms.append(schedule_8812)
    forms = "".join(forms)
    tbd_fields = []
    for k, v in tax_payer["data"].items():
        forms = forms.replace("$"+k, "$"+f"{v:,}" if not isinstance(v, str) else v)
        if v == "$TBD":
            tbd_fields.append(k)
    for fields in tbd_fields:
        tax_payer["data"].pop(fields)
    forms = forms.replace("$TBD", tbd_mark)
    prompt = formalize_prompt_template.replace("$forms", forms)
    
    prompt = prompt.replace("$name", tax_payer["name"])
    prompt = prompt.replace("$age", str(tax_payer["age"]))
    prompt = prompt.replace("$spouse_age", str(tax_payer["spouse_age"]))
    prompt = prompt.replace("$blind", str(tax_payer["blind"]))
    prompt = prompt.replace("$spouse_blind", str(tax_payer["spouse_blind"]))
    prompt = prompt.replace("$filing_status", tax_payer["filing_status"])
    prompt = prompt.replace("$itemized", str(tax_payer["itemized"]))
    prompt = prompt.replace("$num_qualifying_children", str(tax_payer["num_qualifying_children"]))
    prompt = prompt.replace("$num_other_dependents", str(tax_payer["num_other_dependents"]))
    prompt = prompt.replace("$response", response)
    
    return prompt

def parse(tax_payer: dict, inputs: str):
    api_key = os.environ["OPENAI_API_KEY"]
    prompt = build_prompt(tax_payer, inputs)
    engine = openai.OpenAI(api_key=api_key)
    response = engine.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": formalize_system_prompt},
            {"role": "user", "content": prompt}
        ],
        response_format=Form1040,
        temperature=0.0,
    )
    return response.choices[0].message.parsed

ENUM_MAPPINGS = {
        "single": "FilingStatus.single",
        "married filing jointly": "FilingStatus.married_filing_jointly",
        "married filing separately": "FilingStatus.married_filing_separately",
        "head of household": "FilingStatus.head_of_household",
        "qualifying surviving spouse": "FilingStatus.qualifying_surviving_spouse",
}

def unwrap_optional(typ):
    if get_origin(typ) is Union:
        args = get_args(typ)
        for a in args:
            if a is not type(None):
                return True
    return False

def to_lean_value(obj, field_type=None) -> str:
    is_optional = unwrap_optional(field_type) if field_type else (None, False)
    if isinstance(obj, BaseModel):
        fields = [
            f"{k} := {to_lean_value(v, obj.model_fields[k].annotation)}"
            for k, v in obj.model_dump().items()
        ]
        return f"{{ {', '.join(fields)} }}"
    elif isinstance(obj, list):
        return f"[{', '.join(to_lean_value(x) for x in obj)}]"
    elif obj is None:
        return "none"
    elif isinstance(obj, str):
        if obj in ENUM_MAPPINGS:
            return ENUM_MAPPINGS[obj]
        return f"some \"{obj}\"" if is_optional else f"\"{obj}\""
    elif isinstance(obj, bool):
        return f"some {'true' if obj else 'false'}" if is_optional else ('true' if obj else 'false')
    elif isinstance(obj, (int, float)):
        return f"some {obj}" if is_optional else str(obj)
    else:
        return str(obj)


def model_from_existing(src: BaseModel, dst_cls : type[BaseModel]):
    data = src.model_dump()
    new_data = {}
    for f, info in dst_cls.__fields__.items():
        val = data.get(f)
        t = info.annotation
        if get_origin(t) is Optional:
            t = t.__args__[0]
        if val is None:
            if t is float:
                val = 0.0
            else:
                val = None
        new_data[f] = val
    return dst_cls.model_validate(new_data)


def get_lean_check_code(structured_output):
    lean_check_code_lines = []

    with open(lean_rules_file, "r") as f:
        lean_check_code_lines = f.readlines()
    
    lean_structured_output = to_lean_value(structured_output, Form1040)
    var_name = "s"

    lean_check_code_lines.append(f"def {var_name} : Form1040 := {lean_structured_output}\n\n")
    
    for rule in lean_rule_list:
        lean_check_code_lines.append(f"#eval {rule} {var_name} \n\n")

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        for line in lean_check_code_lines:
            tmp.write(line)
        return tmp.name
    
    

def analyze_response(response: str, tax_payer: dict, tax_payer_pydantic: TaxPayer):
    if response == "":#to test lean
        _,structured_output = compute_actual_answer(tax_payer_pydantic)
        structured_output = model_from_existing(structured_output, Form1040)
    else:
        structured_output = parse(tax_payer, response)

    rule_app_stat = []
    
    name, age, spouse_age, filing_status = structured_output.name, structured_output.age, structured_output.spouse_age, structured_output.filing_status
    if name != tax_payer_pydantic.name or age != tax_payer_pydantic.age or spouse_age != tax_payer_pydantic.spouse_age or filing_status != tax_payer_pydantic.filing_status:
        rule_app_stat.append("Error: basic info")
    else:
        rule_app_stat.append("Correct: basic info")

    lean_check_code_path = get_lean_check_code(structured_output)
    
    print(f"Running lean rules on {lean_check_code_path}")
    result = subprocess.run(["lean", lean_check_code_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error while running lean: {result.stderr}")
        sys.exit(1)
        
    output = result.stdout
    pattern = re.compile(r'"([^"]+)"')
    matches = pattern.findall(output)

    for status_message in matches:
        rule_app_stat.append(status_message)

    print (rule_app_stat)
    
    rule_wise = {r: [] for r in rule_list}
    missing, error, correct = 0,0,0
    for tag in rule_app_stat:
        tag_type = tag[:tag.find(": ")]
        tag_rule = tag[tag.find(": ")+2:]
        if tag_rule in rule_wise:
            rule_wise[tag_rule].append(tag_type)
            if tag_type == "Missing":
                missing += 1
            elif tag_type == "Error":
                error += 1
            else:
                correct += 1
    ratios = {
        "precision": correct / (correct + error),
        "recall": correct / (correct + missing)
    }

    return ratios, structured_output


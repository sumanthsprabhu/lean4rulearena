import os
import re
import json
import argparse
from structured_forms import TaxPayer
from prompt import (
    basic_forms,
    basic_forms_textual,
    itemized_forms,
    self_employ_forms,
    edu_forms,
    schedule_8812
)
import openai
from python_evaluation import compute_actual_answer
from lean_evaluation import analyze_response

query_system_prompt = "You are a helpful US taxation consultant."

query_prompt_template = """
You are given several forms used to report US income tax and the instructions or rules about how to fill the forms. Then you will be given the income and/or payment information about a tax payer According to the given information. You should calculate the income tax owed by this payer.
$example
IRS Forms for the tax payer:
$forms
Calculate the tax owed by the payer step-by-step according to the information provided by the forms. You should calculate all fields marked with [__]. DO NOT round numbers without explicit instructions. End your response with:
1. "The total tax owed is $xxx." (xxx is a number) if there is tax owed.
2. "The total tax overpaid is $xxx." (xxx is a number) if there is tax overpaid (and should be refunded).
Your response:
"""

tbd_mark = "[__]"

#TODO: replace with llm supported
def o1(inputs, system_prompt):
    api_key = os.environ["OPENAI_API_KEY"]
    engine = openai.OpenAI(api_key=api_key)
    response = engine.chat.completions.create(
        model="o1-preview",
        messages=[
            {"role": "user", "content": system_prompt + "\n\n" + inputs}
        ],
    )
    return response.choices[0].message.content

def build_query_prompt(tax_payer):
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
    prompt = query_prompt_template.replace("$forms", forms)
    
    prompt = prompt.replace("$name", tax_payer["name"])
    prompt = prompt.replace("$age", str(tax_payer["age"]))
    prompt = prompt.replace("$spouse_age", str(tax_payer["spouse_age"]))
    prompt = prompt.replace("$blind", str(tax_payer["blind"]))
    prompt = prompt.replace("$spouse_blind", str(tax_payer["spouse_blind"]))
    prompt = prompt.replace("$filing_status", tax_payer["filing_status"])
    prompt = prompt.replace("$itemized", str(tax_payer["itemized"]))
    prompt = prompt.replace("$num_qualifying_children", str(tax_payer["num_qualifying_children"]))
    prompt = prompt.replace("$num_other_dependents", str(tax_payer["num_other_dependents"]))
    
    return prompt

#Assumptions on tax_payer data:
#not tax_payer_pydantic.self_employed
#tax_payer_pydantic.qualified_dividends == 0.0
# not (structured_output.num_qualifying_children + structured_output.num_other_dependents > 0)
# not (structured_output.student_list is not None and len(structured_output.student_list) > 0)
def load_problems(number_problems):
    with open(f"problems/comp_0.json", "r") as f:
        problems = json.load(f)
    filtered = [
        r
        for r in problems
        if (
                not r["dict"].get("self_employed", False) and
                r["dict"].get("qualified_dividends", 0.0) == 0.0 and
                (r["dict"].get("num_qualifying_children") + r["dict"].get("num_other_dependents") <= 0) and
                (not r["dict"].get("student_list")  or len(r["dict"].get("student_list")) == 0)
        )
        ][:number_problems]
    return filtered

def eval_query(tax_payer, tax_payer_pydantic):
    prompt = build_query_prompt(tax_payer)

    response = o1(prompt, query_system_prompt) #TODO: check which LLM to use
    response = response.replace("**", "")

    pattern = r"The total tax (owed|overpaid) is \$((?:\d{1,3}(?:,\d{3})*|\d+)(\.\d+)?)."
    match = re.search(pattern, response)
    if match:
        status = match.group(1)
        value = float(match.group(2).replace(",", ""))
        value = -value if status == "overpaid" else value
        answer, _ = compute_actual_answer(tax_payer_pydantic)
        if np.isclose(value, answer) or (isinstance(value, str) and str(answer) in value):
            acc = True

        # ratios, structured_response = analyze_response(response, tax_payer, tax_payer_pydantic)

    return response, acc
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--number_problems", type=int, default=5)
    parser.add_argument("--test_lean", type=bool, default=True)
    args = parser.parse_args()
    
    problems = load_problems(args.number_problems)

    total_acc = 0
    problem_wise_recall = []
    problem_wise_precision = []

    for i in range(args.number_problems):
        tax_payer, tax_payer_pydantic = problems[i]["dict"], TaxPayer(**problems[i]["pydantic"])
        if not args.test_lean:
            response, acc = eval_query(tax_payer, tax_payer_pydantic)
            if acc:
                total_acc += 1
            ratios, structured_response = analyze_response(response, tax_payer, tax_payer_pydantic)
            problem_wise_recall.append(ratios["recall"])
            problem_wise_precision.append(ratios["precision"])
            print(f"Total accuracy: {total_acc}, Average recall: {sum(problem_wise_recall)/args.number_problems}, Average precision: {sum(problem_wise_precision)/args.number_problems}")
        else:
            ratios, _ = analyze_response("", tax_payer, tax_payer_pydantic)
            print(ratios)
            


import os
import numpy as np
import pandas as pd
import openai

from typing import Union
from prompt import (
    basic_forms,
    itemized_forms,
    self_employ_forms,
    edu_forms,
    schedule_8812
)
from structured_forms import Form1040, TaxPayer, Student


def standard_deduction(filing_status: str, age: int, spouse_age: int, blind: bool, spouse_blind: bool):
    if filing_status == "single":
        box_checked = (age >= 65) + blind
        if box_checked == 2: return 17550
        elif box_checked == 1: return 15700
        else: return 13850
    if filing_status == "married filing jointly":
        box_checked = (age >= 65) + blind + (spouse_age >= 65) + spouse_blind
        if box_checked == 4: return 33700
        elif box_checked == 3: return 32200
        elif box_checked == 2: return 30700
        elif box_checked == 1: return 29200
        else: return 27700
    if filing_status == "head of household":
        box_checked = (age >= 65) + blind
        if box_checked == 2: return 24500
        elif box_checked == 1: return 22650
        else: return 20800
    if filing_status == "married filing separately":
        box_checked = (age >= 65) + blind
        if box_checked == 2: return 16850
        elif box_checked == 1: return 15350
        else: return 13850
    if filing_status == "qualifying surviving spouse":
        box_checked = (age >= 65) + blind
        if box_checked == 2: return 30700
        elif box_checked == 1: return 29200
        else: return 27700
        
def itemized_deduction(tax_payer: Union[TaxPayer, Form1040]):
    medical_dental_expenses = tax_payer.medical_dental_expenses
    total_adjusted_gross_income = tax_payer.adjusted_gross_income
    sche_a_line_4 = max(medical_dental_expenses - 0.075 * total_adjusted_gross_income, 0)
    if tax_payer.filing_status == "married filing separately":
        sche_a_line_5e = min(tax_payer.state_local_income_or_sales_tax + tax_payer.state_local_real_estate_tax + tax_payer.state_local_personal_property_tax, 5000)
    else:
        sche_a_line_5e = min(tax_payer.state_local_income_or_sales_tax + tax_payer.state_local_real_estate_tax + tax_payer.state_local_personal_property_tax, 10000)
    sche_a_line_7 = tax_payer.other_taxes_paid + sche_a_line_5e
    sche_a_line_8 = tax_payer.home_mortgage_interest_and_points + tax_payer.home_mortgage_interest_unreported + tax_payer.home_mortgage_points_unreported
    sche_a_line_10 = sche_a_line_8 + tax_payer.investment_interest
    sche_a_line_14 = tax_payer.charity_cash + tax_payer.charity_non_cash
    sche_a_line_17 = sche_a_line_4 + sche_a_line_7 + sche_a_line_10 + sche_a_line_14 + tax_payer.casualty_and_theft_loss + tax_payer.other_itemized_deductions
    return sche_a_line_17

def tax_table(filing_status: str, taxable_income: int):
    if filing_status == "single":
        cuts = [0, 11000, 44725, 95375, 182100, 231250, 578125, 1e20]
    if filing_status == "married filing separately":
        cuts = [0, 11000, 44725, 95375, 182100, 231250, 346875, 1e20]
    if filing_status == "married filing jointly" or filing_status == "qualifying surviving spouse":
        cuts = [0, 22000, 89450, 190750, 364200, 462500, 693750, 1e20]
    if filing_status == "head of household":
        cuts = [0, 15700, 59850, 95350, 182100, 231250, 578100 ,1e20]

    rate = [0.1, 0.12, 0.22 , 0.24 ,0.32, 0.35, 0.37]
    i = 0
    total = 0
    while taxable_income >= cuts[i]:
        total = total + (min(taxable_income, cuts[i+1]) - cuts[i])*rate[i]
        i = i + 1
    return total

def calc_tax(taxable_income: int, filing_status: str):
    if taxable_income == 0: return 0
    if taxable_income >= 100000: return tax_table(filing_status, taxable_income)
    return tax_table(filing_status, np.floor(taxable_income/50)*50 + 25)

def qualified_dividends_and_capital_gain_tax_worksheet(tax_payer: Union[TaxPayer, Form1040]):
    qdcg_worksheet_line_1 = tax_payer.computed_taxable_income
    qdcg_worksheet_line_2 = tax_payer.qualified_dividends
    qdcg_worksheet_line_3 = 0
    qdcg_worksheet_line_4 = qdcg_worksheet_line_2 + qdcg_worksheet_line_3
    qdcg_worksheet_line_5 = max(qdcg_worksheet_line_1 - qdcg_worksheet_line_4, 0)
    if tax_payer.filing_status == "single" or tax_payer.filing_status == "married filing separately":
        qdcg_worksheet_line_6 = 44625
    elif tax_payer.filing_status == "married filing jointly" or tax_payer.filing_status == "qualifying surviving spouse":
        qdcg_worksheet_line_6 = 89250
    else:
        qdcg_worksheet_line_6 = 59750
    qdcg_worksheet_line_7 = min(qdcg_worksheet_line_1, qdcg_worksheet_line_6)
    qdcg_worksheet_line_8 = min(qdcg_worksheet_line_5, qdcg_worksheet_line_7)
    qdcg_worksheet_line_9 = qdcg_worksheet_line_7 - qdcg_worksheet_line_8
    qdcg_worksheet_line_10 = min(qdcg_worksheet_line_1, qdcg_worksheet_line_4)
    qdcg_worksheet_line_11 = qdcg_worksheet_line_9
    qdcg_worksheet_line_12 = qdcg_worksheet_line_10 - qdcg_worksheet_line_11
    if tax_payer.filing_status == "single":
        qdcg_worksheet_line_13 = 492300
    elif tax_payer.filing_status == "married filing separately":
        qdcg_worksheet_line_13 = 276900
    elif tax_payer.filing_status == "married filing jointly" or tax_payer.filing_status == "qualifying surviving spouse":
        qdcg_worksheet_line_13 = 553850
    else:
        qdcg_worksheet_line_13 = 523050
    qdcg_worksheet_line_14 = min(qdcg_worksheet_line_1, qdcg_worksheet_line_13)
    qdcg_worksheet_line_15 = qdcg_worksheet_line_5 + qdcg_worksheet_line_9
    qdcg_worksheet_line_16 = max(qdcg_worksheet_line_14 - qdcg_worksheet_line_15, 0)
    qdcg_worksheet_line_17 = min(qdcg_worksheet_line_12, qdcg_worksheet_line_16)
    qdcg_worksheet_line_18 = qdcg_worksheet_line_17 * 0.15
    qdcg_worksheet_line_19 = qdcg_worksheet_line_9 + qdcg_worksheet_line_17
    qdcg_worksheet_line_20 = qdcg_worksheet_line_10 - qdcg_worksheet_line_19
    qdcg_worksheet_line_21 = qdcg_worksheet_line_20 * 0.20
    qdcg_worksheet_line_22 = calc_tax(qdcg_worksheet_line_5, tax_payer.filing_status)
    qdcg_worksheet_line_23 = qdcg_worksheet_line_18 + qdcg_worksheet_line_21 + qdcg_worksheet_line_22
    qdcg_worksheet_line_24 = calc_tax(qdcg_worksheet_line_1, tax_payer.filing_status)
    qdcg_worksheet_line_25 = min(qdcg_worksheet_line_23, qdcg_worksheet_line_24)
    return qdcg_worksheet_line_25

def credit_limit_worksheet(tax_payer: Union[TaxPayer, Form1040]):
    ws_a_line_1 = tax_payer.f1040_line_18
    ws_a_line_2 = tax_payer.foreign_tax_credit + tax_payer.dependent_care + tax_payer.computed_education_credits + tax_payer.retirement_savings + tax_payer.elderly_disabled_credits
    ws_a_line_3 = ws_a_line_1 - ws_a_line_2
    ws_a_line_5 = ws_a_line_3
    return ws_a_line_5

def earned_income_worksheet(tax_payer: Union[TaxPayer, Form1040]):
    line_1a = tax_payer.wage_tip_compensation_total
    line_1b = tax_payer.nontaxable_combat_pay
    line_2a = 0 # NOTE: No statutory employee income for Schedule C Line 1
    line_2b = tax_payer.net_profit
    line_3 = line_1a + line_1b + line_2a + line_2b
    if line_3 <= 0:
        return 0
    line_4 = 0
    line_5 = tax_payer.self_employment_deductible
    line_6 = line_4 + line_5
    line_7 = line_3 - line_6
    return line_7

def compute_child_and_dependent_credits(tax_payer: Union[TaxPayer, Form1040]):
    line_1 = tax_payer.adjusted_gross_income
    line_4 = tax_payer.num_qualifying_children
    line_5 = line_4 * 2000
    line_6 = tax_payer.num_other_dependents
    line_7 = line_6 * 500
    line_8 = line_5 + line_7
    if tax_payer.filing_status == "married filing jointly":
        line_9 = 400000
    else:
        line_9 = 200000
    line_10 = max(line_1 - line_9, 0)
    line_10 = np.ceil(line_10 / 1000) * 1000
    line_11 = line_10 * 0.05
    line_12 = line_8 - line_11
    if line_12 <= 0:
        return 0, 0
    
    line_13 = credit_limit_worksheet(tax_payer)
    line_14 = min(line_12, line_13)
    line_16a = line_12 - line_14
    if line_16a <= 0:
        return line_14, 0

    line_16b = line_4 * 1600
    if line_16b == 0:
        return line_14, 0
    
    line_17 = min(line_16a, line_16b)
    line_18a = earned_income_worksheet(tax_payer)
    # line_18b = tax_payer.nontaxable_combat_pay
    line_19 = max(line_18a - 2500, 0)
    line_20 = line_19 * 0.15
    if line_4 < 3:
        line_27 = min(line_17, line_20)
    elif line_20 >= line_17:
        line_27 = line_17
    else:
        line_22 = tax_payer.self_employment_deductible
        line_24 = 0 # EIC and Schedule 3, line 11 are 0 in current version
        line_25 = max(line_22 - line_24, 0)
        line_26 = max(line_20, line_25)
        line_27 = min(line_17, line_26)
        
    return line_14, line_27
    
def compute_education_credits(tax_payer: TaxPayer):
    line_1 = line_10 = 0
    for student in tax_payer.student_list:
        if isinstance(student, Student):
            student = student.model_dump()
        go_to_line_31 = False
        if student["f8863_part_iii_23"] == "Yes":
            go_to_line_31 = True
        elif student["f8863_part_iii_24"] == "No":
            go_to_line_31 = True
        elif student["f8863_part_iii_25"] == "Yes":
            go_to_line_31 = True
        elif student["f8863_part_iii_26"] == "Yes":
            go_to_line_31 = True
        
        if go_to_line_31:
            line_10 += student["qualified_student_expenses"]
        else:
            line_27 = min(student["qualified_student_expenses"], 4000)
            line_28 = max(line_27 - 2000, 0)
            line_29 = line_28 * 0.25
            if line_28 == 0:
                line_1 += line_27
            else:
                line_1 += line_29 + 2000
    
    if tax_payer.filing_status == "married filing jointly":
        line_2 = 180000
    else:
        line_2 = 90000
    line_3 = tax_payer.adjusted_gross_income
    line_4 = line_2 - line_3
    if line_4 <= 0:
        return 0, 0
    
    if tax_payer.filing_status == "married filing jointly":
        line_5 = 20000
    else:
        line_5 = 10000
    if line_4 >= line_5:
        line_6 = 1.000
    else:
        line_6 = round(line_4 / line_5, 3)
    line_7 = line_1 * line_6
    line_8 = line_7 * 0.40 if tax_payer.age >= 24 else 0
    line_9 = line_7 - line_8
    line_11 = min(line_10, 10000)
    line_12 = line_11 * 0.2
    if tax_payer.filing_status == "married filing jointly":
        line_13 = 180000
    else:
        line_13 = 90000
    line_14 = tax_payer.adjusted_gross_income
    line_15 = line_13 - line_14
    if line_15 <= 0:
        line_18 = 0
    else:
        if tax_payer.filing_status == "married filing jointly":
            line_16 = 20000
        else:
            line_16 = 10000
        if line_15 >= line_16:
            line_17 = 1.000
        else:
            line_17 = round(line_15 / line_16, 3)
        line_18 = line_12 * line_17
    clws_line_3 = line_18 + line_9
    clws_line_4 = tax_payer.f1040_line_18
    clws_line_5 = tax_payer.foreign_tax_credit + tax_payer.dependent_care + tax_payer.elderly_disabled_credits
    clws_line_6 = clws_line_4 - clws_line_5
    line_19 = min(clws_line_3, clws_line_6)
    return line_8, line_19
    
def compute_actual_answer(tax_payer: TaxPayer):
    tax_payer.wage_tip_compensation_total = (tax_payer.wage_tip_compensation + 
                        tax_payer.household_employee_wage + 
                        tax_payer.unreported_tip)
    
    if tax_payer.self_employed:
        tax_payer.gross_profit = tax_payer.gross_receipts - tax_payer.returns_and_allowances - tax_payer.cost_of_goods_sold
        tax_payer.gross_income = tax_payer.gross_profit + tax_payer.other_inc_sched_c
        tax_payer.tentative_profit = tax_payer.gross_income - tax_payer.total_expenses
        tax_payer.net_profit = tax_payer.tentative_profit - tax_payer.expenses_of_home
        tax_payer.sche_se_line_4c = tax_payer.net_profit * 0.9235 if tax_payer.net_profit > 0 else tax_payer.net_profit
        if tax_payer.sche_se_line_4c < 400:
            tax_payer.self_employment_tax = tax_payer.self_employment_deductible = 0
        else:
            if tax_payer.total_social_security_wages >= 160200:
                tax_payer.sche_se_line_10 = 0
            else:
                tax_payer.sche_se_line_9 = 160200 - tax_payer.total_social_security_wages
                tax_payer.sche_se_line_10 = min(tax_payer.sche_se_line_4c, tax_payer.sche_se_line_9) * 0.124
            tax_payer.self_employment_tax = tax_payer.sche_se_line_4c * 0.029 + tax_payer.sche_se_line_10
            tax_payer.self_employment_deductible = tax_payer.self_employment_tax * 0.5
    else:
        tax_payer.gross_receipts = tax_payer.net_profit = tax_payer.self_employment_tax = tax_payer.self_employment_deductible = 0
    
    tax_payer.additional_income = (tax_payer.taxable_state_refunds + 
                                    tax_payer.alimony_income +
                                    tax_payer.net_profit +
                                    tax_payer.sale_of_business + 
                                    tax_payer.rental_real_estate_sch1 + 
                                    tax_payer.farm_income + 
                                    tax_payer.unemployment_compensation + 
                                    tax_payer.other_income)
    
    tax_payer.computed_total_income = (tax_payer.wage_tip_compensation_total + 
                            tax_payer.taxable_interest +
                            tax_payer.ordinary_dividends + 
                            tax_payer.taxable_ira_distributions +
                            tax_payer.taxable_pensions +
                            tax_payer.taxable_social_security_benefits +
                            0 + # Capital gains fixed at 0
                            tax_payer.additional_income)
    
    tax_payer.total_adjustments = (tax_payer.educator_expenses + 
                                      tax_payer.hsa_deduction + 
                                      tax_payer.self_employment_deductible + 
                                      tax_payer.ira_deduction + 
                                      tax_payer.student_loan_interest_deduction + 
                                      tax_payer.other_adjustments)
    
    tax_payer.adjusted_gross_income = tax_payer.computed_total_income - tax_payer.total_adjustments
    
    if tax_payer.itemized:
        tax_payer.itemized_deductions = itemized_deduction(tax_payer)
        tax_payer.standard_or_itemized_deductions = tax_payer.itemized_deductions
    else:
        tax_payer.standard_deduction = standard_deduction(tax_payer.filing_status, tax_payer.age, tax_payer.spouse_age, tax_payer.blind, tax_payer.spouse_blind)
        tax_payer.standard_or_itemized_deductions = tax_payer.standard_deduction
    
    tax_payer.total_deductions = (tax_payer.standard_or_itemized_deductions + 
                                     tax_payer.qualified_business_income)
    
    tax_payer.computed_taxable_income = max(tax_payer.adjusted_gross_income - tax_payer.total_deductions, 0)

    if tax_payer.qualified_dividends > 0: # or tax_payer.capital_gains > 0:
        tax_payer.computed_taxes = qualified_dividends_and_capital_gain_tax_worksheet(tax_payer)
    else:
        tax_payer.computed_taxes = calc_tax(tax_payer.computed_taxable_income, tax_payer.filing_status)
    
    tax_payer.schedule_2_total_taxes = tax_payer.amt_f6251 + tax_payer.credit_repayment

    tax_payer.f1040_line_18 = tax_payer.computed_taxes + tax_payer.schedule_2_total_taxes
    
    if tax_payer.has_student_loans_or_education_expenses:
        tax_payer.computed_american_opportunity_credit, tax_payer.computed_education_credits = compute_education_credits(tax_payer)
    else:
        tax_payer.computed_american_opportunity_credit = tax_payer.computed_education_credits = 0
    
    tax_payer.schedule_3_line_8 = (tax_payer.foreign_tax_credit + 
                                    tax_payer.dependent_care + 
                                    tax_payer.computed_education_credits + 
                                    tax_payer.retirement_savings + 
                                    tax_payer.elderly_disabled_credits + 
                                    tax_payer.plug_in_motor_vehicle + 
                                    tax_payer.alt_motor_vehicle)
    
    if tax_payer.num_qualifying_children + tax_payer.num_other_dependents > 0:
        tax_payer.computed_ctc_or_other_dependent_credit, tax_payer.computed_additional_child_tax_credit = compute_child_and_dependent_credits(tax_payer)
    else:
        tax_payer.computed_ctc_or_other_dependent_credit = tax_payer.computed_additional_child_tax_credit = 0
    
    tax_payer.computed_accumulated_credits = tax_payer.schedule_3_line_8 + tax_payer.computed_ctc_or_other_dependent_credit

    tax_payer.computed_taxes_after_credits = tax_payer.f1040_line_18 - tax_payer.computed_accumulated_credits

    tax_payer.computed_other_taxes = tax_payer.other_additional_taxes + tax_payer.self_employment_tax
    
    tax_payer.computed_total_tax = tax_payer.computed_taxes_after_credits + tax_payer.computed_other_taxes
    
    tax_payer.total_other_payments_and_refundable_credits = tax_payer.earned_income_credit + tax_payer.computed_additional_child_tax_credit + tax_payer.computed_american_opportunity_credit + 0 # 0 is the additional child tax credit, the reserved for future use, and the amount from schedule 3 line 15
    
    tax_payer.total_payments = tax_payer.federal_income_tax_withheld + 0 + tax_payer.total_other_payments_and_refundable_credits # 0 is the estimated tax payments

    tax_payer.computed_amount_owed_or_overpaid = tax_payer.computed_total_tax - tax_payer.total_payments

    return tax_payer.computed_amount_owed_or_overpaid, tax_payer

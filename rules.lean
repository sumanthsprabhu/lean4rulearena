inductive FilingStatus
  | single
  | married_filing_jointly
  | married_filing_separately
  | head_of_household
  | qualifying_surviving_spouse
  deriving Repr, BEq



structure Student where
--Form 8863 Part III Line 21
qualified_student_expenses : Int
--Form 8863 Part III Line 23
f8863_part_iii_23 : Bool
--Form 8863 Part III Line 24
f8863_part_iii_24 : Bool
--Form 8863 Part III Line 25
f8863_part_iii_25 : Bool
--Form 8863 Part III Line 26
f8863_part_iii_26 : Bool



structure Form1040 where
--Name of taxpayer
name : String
--Age of taxpayer
age : Int
--Age of taxpayer's spouse
spouse_age : Int
--Filing status of taxpayer
filing_status : FilingStatus
--Taxpayer is blind
blind : Bool
--Taxpayer's spouse is blind
spouse_blind : Bool
--Taxpayer uses itemized deductions
itemized : Bool
--Number of qualifying children
num_qualifying_children : Int
--Number of other dependents
num_other_dependents : Int
--Form 1040 Line 1a
wage_tip_compensation : Float
--Form 1040 Line 1b
household_employee_wage : Float
--Form 1040 Line 1c
unreported_tip : Float
--Form 1040 Line 1d
nontaxable_combat_pay : Float
--Form 1040 Line 1z
wage_tip_compensation_total : Float
--Form 1040 Line 2a
tax_exempt_interest : Float
--Form 1040 Line 2b
taxable_interest : Float
--Form 1040 Line 3a
qualified_dividends : Float
--Form 1040 Line 3b
ordinary_dividends : Float
--Form 1040 Line 4a
ira_distributions : Float
--Form 1040 Line 4b
taxable_ira_distributions : Float
--Form 1040 Line 5a
all_pensions : Float
--Form 1040 Line 5b
taxable_pensions : Float
--Form 1040 Line 6a
social_security_benefits : Float
--Form 1040 Line 6b
taxable_social_security_benefits : Float
--Form 1040 Line 7
capital_gain_or_loss : Float
--Form 1040 Line 8
additional_income : Float
--Form 1040 Line 9
total_income : Float
--Form 1040 Line 10
total_adjustments : Float
--Form 1040 Line 11
adjusted_gross_income : Float
--Form 1040 Line 12
standard_or_itemized_deductions : Float
--Form 1040 Line 13
qualified_business_income : Float
--Form 1040 Line 14
total_deductions : Float
--Form 1040 Line 15
computed_taxable_income : Float
--Form 1040 Line 16
taxes : Float
--Form 1040 Line 17
copy_schedule_2_line_3 : Float
--Form 1040 Line 18
f1040_line_18 : Float
--Form 1040 Line 19
ctc_or_other_dependent_credit : Float
--Form 1040 Line 20
copy_schedule_3_line_8 : Float
--Form 1040 Line 21
accumulated_credits : Float
--Form 1040 Line 22
taxes_after_credits : Float
--Form 1040 Line 23
other_taxes : Float
--Form 1040 Line 24
total_tax : Float
--Form 1040 Line 25
federal_income_tax_withheld : Float
--Form 1040 Line 27
earned_income_credit : Float
--Form 1040 Line 28
additional_child_tax_credit : Float
--Form 1040 Line 29
american_opportunity_credit : Float
--Form 1040 Line 31
copy_schedule_3_line_15 : Float
--Form 1040 Line 32
total_other_payments_and_refundable_credits : Float
--Form 1040 Line 33
total_payments : Float
--Form 1040 Line 37 (negative if overpaid)
amount_owed_or_overpaid : Float
--Schedule 1 Line 1
taxable_state_refunds : Float
--Schedule 1 Line 2a
alimony_income : Float
--Schedule 1 Line 4
sale_of_business : Float
--Schedule 1 Line 5
rental_real_estate_sch1 : Float
--Schedule 1 Line 6
farm_income : Float
--Schedule 1 Line 7
unemployment_compensation : Float
--Schedule 1 Line 8
other_income : Float
--Schedule 1 Line 11
educator_expenses : Float
--Schedule 1 Line 13
hsa_deduction : Float
--Schedule 1 Line 15
self_employment_deductible : Float
--Schedule 1 Line 20
ira_deduction : Float
--Schedule 1 Line 21
student_loan_interest_deduction : Float
--Schedule 1 Line 24
other_adjustments : Float
--Schedule 2 Line 1
amt_f6251 : Float
--Schedule 2 Line 2
credit_repayment : Float
--Schedule 2 Line 3 (= Line 1 + Line 2)
schedule_2_total_taxes : Float
--Schedule 2 Line 4
self_employment_tax : Float
--Schedule 2 Line 17
other_additional_taxes : Float
--Schedule 2 Line 21 (= Line 4 + Line 17)
schedule_2_total_other_taxes : Float
--Schedule 3 Line 1
foreign_tax_credit : Float
--Schedule 3 Line 2
dependent_care : Float
--Schedule 3 Line 3
computed_education_credits : Float
--Schedule 3 Line 4
retirement_savings : Float
--Schedule 3 Line 6d
elderly_disabled_credits : Float
--Schedule 3 Line 6i
plug_in_motor_vehicle : Float
--Schedule 3 Line 6j
alt_motor_vehicle : Float
--Schedule 3 Line 8
schedule_3_line_8 : Float
--Schedule A Line 1 (if itemized)
medical_dental_expenses : Option Float
--Schedule A Line 5a (if itemized)
state_local_income_or_sales_tax : Option Float
--Schedule A Line 5b (if itemized)
state_local_real_estate_tax : Option Float
--Schedule A Line 5c (if itemized)
state_local_personal_property_tax : Option Float
--Schedule A Line 6 (if itemized)
other_taxes_paid : Option Float
--Schedule A Line 8a (if itemized)
home_mortgage_interest_and_points : Option Float
--Schedule A Line 8b
home_mortgage_interest_unreported : Option Float
--Schedule A Line 8c (if itemized)
home_mortgage_points_unreported : Option Float
--Schedule A Line 9 (if itemized)
investment_interest : Option Float
--Schedule A Line 11 (if itemized)
charity_cash : Option Float
--Schedule A Line 12 (if itemized)
charity_non_cash : Option Float
--Schedule A Line 15 (if itemized)
casualty_and_theft_loss : Option Float
--Schedule A Line 16 (if itemized)
other_itemized_deductions : Option Float
--Schedule C Line 1 (if self-employed)
gross_receipts : Option Float
--Schedule C Line 2 (if self-employed)
returns_and_allowances : Option Float
--Schedule C Line 4 (if self-employed)
cost_of_goods_sold : Option Float
--Schedule C Line 6 (if self-employed)
other_inc_sched_c : Option Float
--Schedule C Line 28 (if self-employed)
total_expenses : Option Float
--Schedule C Line 30 (if self-employed)
expenses_of_home : Option Float
--Schedule C Line 31 (if self-employed)
net_profit : Option Float
--Schedule SE Line 8 (if self-employed)
total_social_security_wages : Option Float
--List of students with education expenses
student_list : Option (List Student)



def approx_eq (x y : Float) (eps : Float := 1e-6) : Bool :=
  Float.abs (x - y) ≤ eps




def rule1 (structured_output : Form1040) : String := 
  let computed_total := (structured_output.wage_tip_compensation + 
                        structured_output.household_employee_wage + 
                        structured_output.unreported_tip)
  if approx_eq structured_output.wage_tip_compensation_total computed_total then
    "Correct: wage and tip compensation total"
  else if approx_eq structured_output.wage_tip_compensation_total 0 then
    "Missing: wage and tip compensation total"
  else
    "Error: wage and tip compensation total"




def rule5 (structured_output : Form1040) : String := 
  let net_profit := structured_output.net_profit.getD 0.0
  let computed_additional_income := (structured_output.taxable_state_refunds + 
                                    structured_output.alimony_income + 
                                    net_profit + 
                                    structured_output.sale_of_business + 
                                    structured_output.rental_real_estate_sch1 + 
                                    structured_output.farm_income + 
                                    structured_output.unemployment_compensation + 
                                    structured_output.other_income)
  if approx_eq structured_output.additional_income computed_additional_income then
    "Correct: additional income"
  else if approx_eq structured_output.additional_income 0 then
    "Missing: additional income"
  else
    "Error: additional income"




def rule6 (structured_output : Form1040) : String := 
  let computed_total_income := (structured_output.wage_tip_compensation_total + 
                            structured_output.taxable_interest +
                            structured_output.ordinary_dividends + 
                            structured_output.taxable_ira_distributions +
                            structured_output.taxable_pensions +
                            structured_output.taxable_social_security_benefits +
                            0 + 
                            structured_output.additional_income)
  if approx_eq structured_output.total_income computed_total_income then
    "Correct: total income"
  else if approx_eq structured_output.total_income 0 then
    "Missing: total income"
  else 
    "Error: total income"



def rule7 (structured_output : Form1040) : String := 
  let self_employment_deductible := structured_output.self_employment_deductible
  let computed_total_adjustments := (structured_output.educator_expenses + 
                                      structured_output.hsa_deduction + 
                                      self_employment_deductible + 
                                      structured_output.ira_deduction + 
                                      structured_output.student_loan_interest_deduction + 
                                      structured_output.other_adjustments)
  if approx_eq structured_output.total_adjustments computed_total_adjustments then
    "Correct: total adjustments"
  else if approx_eq structured_output.total_adjustments 0 then
    "Missing: total adjustments"
  else
    "Error: total adjustments"



def rule8 (structured_output : Form1040) : String := 
  let computed_agi := structured_output.total_income - structured_output.total_adjustments
  if approx_eq structured_output.adjusted_gross_income computed_agi then
    "Correct: adjusted gross income"
  else if approx_eq structured_output.adjusted_gross_income 0 then
     "Missing: adjusted gross income"
  else
     "Error: adjusted gross income"



def mymax (x y : Float) : Float := 
  if x < y then y else x



def mymin (x y : Float) : Float :=
  if x < y then x else y



def rule910 (structured_output : Form1040) : String :=
  -- first compute standardized deduction as it will be used in both the cases
  let filing_status := structured_output.filing_status
  let age := structured_output.age
  let spouse_age := structured_output.spouse_age
  let blind := structured_output.blind
  let spouse_blind := structured_output.spouse_blind
  let computed_standardized_deduction :=
    if filing_status == FilingStatus.single then
      let box_checked := 
        (if age ≥ 65 then 1 else 0) +
        (if blind then 1 else 0)
      if box_checked == 2 then 17550
      else if box_checked == 1 then 15700
      else 13850
    else if filing_status == FilingStatus.married_filing_jointly then
      let box_checked := 
        (if age ≥ 65 then 1 else 0) +
        (if blind then 1 else 0) +
        (if spouse_age ≥ 65 then 1 else 0) +
        (if spouse_blind then 1 else 0)      
      if box_checked == 4 then 33700
      else if box_checked == 3 then 32200
      else if box_checked == 2 then 30700
      else if box_checked == 1 then 29200
      else 27700
    else if filing_status == FilingStatus.head_of_household then
      let box_checked := 
        (if age ≥ 65 then 1 else 0) +
        (if blind then 1 else 0)
      if box_checked == 2 then 24500
      else if box_checked == 1 then 22650
      else 20800
    else if filing_status == FilingStatus.married_filing_separately then
      let box_checked := 
        (if age ≥ 65 then 1 else 0) +
        (if blind then 1 else 0)
      if box_checked == 2 then 16850
      else if box_checked == 1 then 15350
      else 13850
    else
      let box_checked := 
        (if age ≥ 65 then 1 else 0) +
        (if blind then 1 else 0)
      if box_checked == 2 then 30700
      else if box_checked == 1 then 29200
      else 27700

  if structured_output.itemized then
    let medical_dental_expenses := structured_output.medical_dental_expenses.getD 0.0
    let total_adjusted_gross_income := structured_output.adjusted_gross_income
    let arg1 := medical_dental_expenses - 0.075 * total_adjusted_gross_income
    let sche_a_line_4 := mymax arg1 0
    let sche_a_line_5e :=
      if structured_output.filing_status == FilingStatus.married_filing_separately then
        mymin ((structured_output.state_local_income_or_sales_tax.getD 0.0) + (structured_output.state_local_real_estate_tax.getD 0.0) + (structured_output.state_local_personal_property_tax.getD 0.0)) 5000
      else
        mymin ((structured_output.state_local_income_or_sales_tax.getD 0.0) + (structured_output.state_local_real_estate_tax.getD 0.0) + (structured_output.state_local_personal_property_tax.getD 0.0)) 10000
    let sche_a_line_7 := (structured_output.other_taxes_paid.getD 0.0) + sche_a_line_5e
    let sche_a_line_8 := (structured_output.home_mortgage_interest_and_points.getD 0.0) + (structured_output.home_mortgage_interest_unreported.getD 0.0) + (structured_output.home_mortgage_points_unreported.getD 0.0)
    let sche_a_line_10 := sche_a_line_8 + (structured_output.investment_interest.getD 0.0)
    let sche_a_line_14 := (structured_output.charity_cash.getD 0.0) + (structured_output.charity_non_cash.getD 0.0)
    let sche_a_line_17 := sche_a_line_4 + sche_a_line_7 + sche_a_line_10 + sche_a_line_14 + (structured_output.casualty_and_theft_loss.getD 0.0) + (structured_output.other_itemized_deductions.getD 0.0)
    let computed_itemized_deductions := sche_a_line_17
    if approx_eq structured_output.standard_or_itemized_deductions computed_standardized_deduction then
      "Missing: itemized deductions"
    else if approx_eq structured_output.standard_or_itemized_deductions computed_itemized_deductions then
      "Correct: itemized deductions"
    else 
      "Error: itemized deductions"
  else
    if approx_eq structured_output.standard_or_itemized_deductions computed_standardized_deduction then 
      "Correct: standard deductions"
    else if approx_eq structured_output.standard_or_itemized_deductions 0 then
      "Missing: standard deductions"
    else 
      "Error: standard deductions"

    

def rule11 (structured_output : Form1040) : String :=
  let computed_total_deductions := structured_output.standard_or_itemized_deductions + structured_output.qualified_business_income
  if approx_eq structured_output.total_deductions computed_total_deductions then
    "Correct: total deductions"
  else if approx_eq structured_output.total_deductions 0 then
    "Missing: total deductions"
  else
    "Error: total deductions"



def rule12 (structured_output : Form1040) : String :=
  let computed_taxable_income := mymax (structured_output.adjusted_gross_income - structured_output.total_deductions) 0
  if approx_eq structured_output.computed_taxable_income computed_taxable_income then
    "Correct: taxable income"
  else if approx_eq structured_output.computed_taxable_income 0 then
    "Missing: taxable income"
  else
    "Error: taxable income"



partial def tax_table_helper (taxable_income : Float) (cut : List Float) (rate : List Float) : Float :=
  match cut, rate with
  | c1::c2::cs, r::rs =>
    if taxable_income >= c1 then
      let arg1 := (mymin taxable_income c2) - c1
      arg1 * r + tax_table_helper taxable_income (c2::cs) rs
    else 0.0
  | _, _ => 0.0




def tax_table (filing_status : FilingStatus) (taxable_income : Float) : Float :=
  let cut := 
    if filing_status == FilingStatus.single then
      [0.0, 11000.0, 44725.0, 95375.0, 182100.0, 231250.0, 578125.0, 1e20]
    else if filing_status == FilingStatus.married_filing_separately then
      [0.0, 11000.0, 44725.0, 95375.0, 182100.0, 231250.0, 346875.0, 1e20]
    else if filing_status == FilingStatus.married_filing_jointly || filing_status == FilingStatus.qualifying_surviving_spouse then
      [0.0, 22000.0, 89450.0, 190750.0, 364200.0, 462500.0, 693750.0, 1e20]
    else
      [0.0, 15700.0, 59850.0, 95350.0, 182100.0, 231250.0, 578100.0, 1e20]
  let rate : List Float := [0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]  
  tax_table_helper taxable_income cut rate



def calc_tax (taxable_income : Float) (filing_status : FilingStatus) : Float :=
  if taxable_income == 0 then
    0
  else if taxable_income ≥ 100000 then
    tax_table filing_status taxable_income
  else
    tax_table filing_status ((taxable_income/50)*50 + 25)



def rule13 (structured_output : Form1040) : String :=
  let computed_taxes := calc_tax structured_output.computed_taxable_income structured_output.filing_status
  -- difference of 10.0 is ok
  if approx_eq computed_taxes structured_output.taxes 10.0 then
    s!"Correct: standard taxes {computed_taxes} {structured_output.taxes}"
  else if approx_eq structured_output.taxes 0 then
    "Missing: standard taxes"
  else 
    "Error: standard taxes"



def rule15 (structured_output : Form1040) : String :=
  if approx_eq structured_output.schedule_2_total_taxes (structured_output.amt_f6251 + structured_output.credit_repayment) then
    "Correct: schedule 2 total part i taxes"
  else if approx_eq structured_output.schedule_2_total_taxes 0 then
    "Missing: schedule 2 total part i taxes"
  else
    "Error: schedule 2 total part i taxes"




def rule16 (structured_output : Form1040) : String :=
  let copy_alternative_minimum_tax := structured_output.schedule_2_total_taxes
  if approx_eq copy_alternative_minimum_tax structured_output.copy_schedule_2_line_3 then
    "Correct: schedule 2 taxes copy"
  else if approx_eq structured_output.copy_schedule_2_line_3 0 then
    "Missing: schedule 2 taxes copy"
  else
    "Error: schedule 2 taxes copy"



def rule17 (structured_output : Form1040) : String :=
  let computed_f1040_line_18 := structured_output.taxes + structured_output.copy_schedule_2_line_3
  if approx_eq structured_output.f1040_line_18 computed_f1040_line_18 then
    "Correct: accumulated taxes"
  else if approx_eq structured_output.f1040_line_18 0 then
    "Missing: accumulated taxes"
  else
    "Error: accumulated taxes"




def rule22 (structured_output : Form1040) : String :=
  let target_schedule_3_line_8 := structured_output.foreign_tax_credit + structured_output.dependent_care + structured_output.computed_education_credits + structured_output.retirement_savings + structured_output.elderly_disabled_credits + structured_output.plug_in_motor_vehicle + structured_output.alt_motor_vehicle
  if approx_eq structured_output.schedule_3_line_8 target_schedule_3_line_8 then 
    "Correct: schedule 3 line 8"
  else if approx_eq structured_output.schedule_3_line_8 0 then
    "Missing: schedule 3 line 8"
  else
    "Error: schedule 3 line 8"




def rule23 (structured_output : Form1040) : String :=
  let copy_total_credits := structured_output.schedule_3_line_8
  if approx_eq structured_output.copy_schedule_3_line_8 copy_total_credits then
    "Correct: schedule 3 total credits copy"
  else if approx_eq structured_output.copy_schedule_3_line_8 0 then
    "Missing: schedule 3 total credits copy"
  else
    "Error: schedule 3 total credits copy"




def rule24 (structured_output : Form1040) : String :=
  let computed_accumulated_credits := structured_output.copy_schedule_3_line_8 + structured_output.ctc_or_other_dependent_credit
  if approx_eq structured_output.accumulated_credits computed_accumulated_credits then
    "Correct: accumulated credits computation"
  else if approx_eq structured_output.accumulated_credits 0 then
    "Missing: accumulated credits computation"
  else
    "Error: accumulated credits computation"



def rule25 (structured_output : Form1040) : String :=
  let computed_taxes_after_credits := mymax (structured_output.f1040_line_18 - structured_output.accumulated_credits) 0.0
  if approx_eq structured_output.taxes_after_credits computed_taxes_after_credits then
    "Correct: taxes after credits computation"
  else if approx_eq structured_output.taxes_after_credits 0 then
     "Missing: taxes after credits computation"
  else
     "Error: taxes after credits computation"




def rule26 (structured_output : Form1040) : String :=
  let computed_other_taxes := structured_output.other_additional_taxes + structured_output.self_employment_tax
  if approx_eq structured_output.schedule_2_total_other_taxes computed_other_taxes then
    "Correct: other taxes computation"
  else if approx_eq structured_output.schedule_2_total_other_taxes 0 then
    "Missing: other taxes computation"
  else
    "Error: other taxes computation"



def rule27 (structured_output : Form1040) : String :=
  let copy_other_additional_taxes := structured_output.schedule_2_total_other_taxes
  if approx_eq structured_output.other_taxes copy_other_additional_taxes then
    "Correct: other additional taxes copy"     
  else if approx_eq structured_output.other_taxes 0 then
    "Missing: other additional taxes copy"
  else
    "Error: other additional taxes copy"




def rule28 (structured_output : Form1040) : String :=
  let computed_total_tax := structured_output.taxes_after_credits + structured_output.other_taxes
  if approx_eq structured_output.total_tax computed_total_tax then
    "Correct: total tax computation"
  else if approx_eq structured_output.total_tax 0 then
    "Missing: total tax computation"
  else
    "Error: total tax computation"



def rule29 (structured_output : Form1040) : String :=
  let computed_total_other_payments := (structured_output.earned_income_credit +
                                     structured_output.additional_child_tax_credit +
                                     structured_output.american_opportunity_credit +
                                     structured_output.copy_schedule_3_line_15)
  if approx_eq structured_output.total_other_payments_and_refundable_credits computed_total_other_payments then
    "Correct: total other payments and refundable credits computation"
  else if approx_eq structured_output.total_other_payments_and_refundable_credits 0 then
    "Missing: total other payments and refundable credits computation"
  else
    "Error: total other payments and refundable credits computation"





def rule30 (structured_output : Form1040) : String :=
  let computed_total_payments := structured_output.federal_income_tax_withheld + 0 + structured_output.total_other_payments_and_refundable_credits
  if approx_eq structured_output.total_payments computed_total_payments then
    "Correct: total payments computation"
  else if approx_eq structured_output.total_payments 0 then
    "Missing: total payments computation"
  else
    "Error: total payments computation"




def rule31 (structured_output : Form1040) : String :=
  let computed_amount_owed_or_overpaid := structured_output.total_tax - structured_output.total_payments
  if approx_eq structured_output.amount_owed_or_overpaid computed_amount_owed_or_overpaid then
    "Correct: amount owed or overpaid computation"
  else if approx_eq structured_output.amount_owed_or_overpaid 0 then
    "Missing: amount owed or overpaid computation"
  else
    "Error: amount owed or overpaid computation"



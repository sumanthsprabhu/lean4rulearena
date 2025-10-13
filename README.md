Extending [RuleArena](https://github.com/SkyRiver-2000/RuleArena/tree/main) tax benchmarks with Lean validator. Apart from the Lean rules and its processing code, other code are from [RuleArena tax](https://github.com/SkyRiver-2000/RuleArena/tree/main/tax)  directory.  

# Running
* Make sure `lean` (v 4.23) is in your path
* Make sure to use python v3.10.* 
* Install `requirements.txt`
* Run `python main.py` (python version is at least v3.10)
* Sample run:
```
$ python main.py 
Querying LLM to fill form
Querying LLM for structured output
Running lean rules on /tmp/tmpsgwlc37e
['Correct: basic info', 'Correct: wage and tip compensation total', 'Correct: additional income', 'Correct: total income', 'Correct: total adjustments', 'Correct: adjusted gross income', 'Error: standard deductions', 'Correct: total deductions', 'Correct: taxable income', 'Error: standard taxes', 'Correct: schedule 2 total part i taxes', 'Correct: schedule 2 taxes copy', 'Correct: accumulated taxes', 'Correct: schedule 3 line 8', 'Correct: schedule 3 total credits copy', 'Correct: accumulated credits computation', 'Correct: taxes after credits computation', 'Correct: other taxes computation', 'Correct: other additional taxes copy', 'Correct: total tax computation', 'Correct: total other payments and refundable credits computation', 'Correct: total payments computation', 'Correct: amount owed or overpaid computation']
Acc: False, Recall: 1.0, Precision: 0.9090909090909091
Querying LLM to fill form
Querying LLM for structured output
Running lean rules on /tmp/tmpvir3hapl
['Correct: basic info', 'Correct: wage and tip compensation total', 'Error: additional income', 'Error: total income', 'Correct: total adjustments', 'Correct: adjusted gross income', 'Error: standard deductions', 'Correct: total deductions', 'Correct: taxable income', 'Error: standard taxes', 'Correct: schedule 2 total part i taxes', 'Correct: schedule 2 taxes copy', 'Correct: accumulated taxes', 'Correct: schedule 3 line 8', 'Correct: schedule 3 total credits copy', 'Correct: accumulated credits computation', 'Correct: taxes after credits computation', 'Correct: other taxes computation', 'Correct: other additional taxes copy', 'Correct: total tax computation', 'Correct: total other payments and refundable credits computation', 'Correct: total payments computation', 'Error: amount owed or overpaid computation']
Acc: False, Recall: 1.0, Precision: 0.7727272727272727
Querying LLM to fill form
Querying LLM for structured output
Running lean rules on /tmp/tmpuo_j0grm
['Correct: basic info', 'Correct: wage and tip compensation total', 'Correct: additional income', 'Correct: total income', 'Correct: total adjustments', 'Correct: adjusted gross income', 'Correct: standard deductions', 'Correct: total deductions', 'Correct: taxable income', 'Correct: standard taxes 28498.560000 28498.560000', 'Correct: schedule 2 total part i taxes', 'Correct: schedule 2 taxes copy', 'Correct: accumulated taxes', 'Error: schedule 3 line 8', 'Correct: schedule 3 total credits copy', 'Correct: accumulated credits computation', 'Correct: taxes after credits computation', 'Correct: other taxes computation', 'Correct: other additional taxes copy', 'Correct: total tax computation', 'Correct: total other payments and refundable credits computation', 'Correct: total payments computation', 'Correct: amount owed or overpaid computation']
Acc: False, Recall: 1.0, Precision: 0.9523809523809523
Querying LLM to fill form
Querying LLM for structured output
Running lean rules on /tmp/tmphrju7ld4
['Correct: basic info', 'Correct: wage and tip compensation total', 'Correct: additional income', 'Correct: total income', 'Correct: total adjustments', 'Correct: adjusted gross income', 'Correct: standard deductions', 'Correct: total deductions', 'Correct: taxable income', 'Correct: standard taxes 5611.000000 5608.000000', 'Correct: schedule 2 total part i taxes', 'Correct: schedule 2 taxes copy', 'Correct: accumulated taxes', 'Correct: schedule 3 line 8', 'Correct: schedule 3 total credits copy', 'Correct: accumulated credits computation', 'Correct: taxes after credits computation', 'Correct: other taxes computation', 'Correct: other additional taxes copy', 'Correct: total tax computation', 'Correct: total other payments and refundable credits computation', 'Correct: total payments computation', 'Correct: amount owed or overpaid computation']
Acc: False, Recall: 1.0, Precision: 1.0
Querying LLM to fill form
Querying LLM for structured output
Running lean rules on /tmp/tmp5ld0n0j1
['Correct: basic info', 'Correct: wage and tip compensation total', 'Correct: additional income', 'Correct: total income', 'Correct: total adjustments', 'Correct: adjusted gross income', 'Error: standard deductions', 'Correct: total deductions', 'Correct: taxable income', 'Correct: standard taxes 36966.720000 36966.720000', 'Correct: schedule 2 total part i taxes', 'Correct: schedule 2 taxes copy', 'Correct: accumulated taxes', 'Correct: schedule 3 line 8', 'Correct: schedule 3 total credits copy', 'Correct: accumulated credits computation', 'Correct: taxes after credits computation', 'Correct: other taxes computation', 'Correct: other additional taxes copy', 'Correct: total tax computation', 'Correct: total other payments and refundable credits computation', 'Correct: total payments computation', 'Correct: amount owed or overpaid computation']
Acc: False, Recall: 1.0, Precision: 0.9523809523809523
Total accuracy: 0, Average recall: 1.0, Average precision: 0.9173160173160173
```
Here, `/tmp/tmp*` are lean files with `rules.lean`, filled form and `eval` of all the rules.
* Use `--number_samples` option to control how many data to run (default=5)
* Use `--lean_test` option to population data from `python_evaluation.py` in place of llm and run lean rules on it.




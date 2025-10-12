Extending [RuleArena](https://github.com/SkyRiver-2000/RuleArena/tree/main) tax benchmarks with Lean validator. Apart from the Lean rules and its processing code, other code are from [RuleArena tax](https://github.com/SkyRiver-2000/RuleArena/tree/main/tax)  directory.  

# Running
* Make sure `lean` (v 4.23) is in your path
* Install `requirements.txt`
* Run `python main.py`
* Sample output:
  ```
  Running lean rules on /var/folders/d0/yzyrg4gd7qx4j5th00trm4ch0000gn/T/tmpul082w48
  ...
  ```
Here, `/var/folders/d0/yzyrg4gd7qx4j5th00trm4ch0000gn/T/tmpul082w48` will have `eval` of all the rules against a specific tax payer data.

# TODO
Support LLM response

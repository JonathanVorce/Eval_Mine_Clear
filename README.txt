*************
* SOLUTION: *
*************
Run "Eval_Mine_Clear_Script.py" from the command line. This script takes two arguments when called:
<Field>  = path to the field file
<Script> = path to the script file to be tested

> python Eval_Mine_Clear_Script.py <Field> <Script>

***************
* ASSIGNMENT: *
***************
See "coding-exercise-swen.pdf" for full explanation of assignment.  

************
* SUMMARY: *
************
Write a script to evaluate your students mine clearing scripts.
    + Starting point value           : 10 * num_mines  
    + For each missile pattern fired : -5 (up to a maximum of 5 * num_mines)  
    + For each movement of the ship  : -2 (up to a maximum of 3 * num_mines)  

************
* TESTING: *
************
Run automated tests from 'Tests\Run_Tests.py'
> cd Tests\
> python Run_Tests.py

For manual testing instructions, see 'Tests\Input_to_Script.txt' for valid Field/Script pairings 
Example testing call:
> python Eval_Mine_Clear_Script.py Tests\Field1.txt Tests\Script1.txt

For unit tests run:
> cd Unit_Tests
> python Field_Unit_Tests.py
*************
* BRANCHES: *
*************
    + Master : can run script in Python v3 and v2

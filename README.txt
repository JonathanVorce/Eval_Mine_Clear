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
See Tests\Input_to_Script.txt for testing instructions.  

Example testing call:
> python Eval_Mine_Clear_Script.py Tests\Field1.txt Tests\Script1.txt

*************
* BRANCHES: *
*************
    + Master : can run script in Python v3 and v2

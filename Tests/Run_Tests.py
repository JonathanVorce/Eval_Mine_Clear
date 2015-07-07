from __future__ import print_function
import pdb
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import Eval_Mine_Clear_Script

_TEST_PAIRS = [ ('..\\Tests\\Field1.txt'   , '..\\Tests\\Script1.txt'   , 'pass (5)' ),
                ('..\\Tests\\Field2.txt'   , '..\\Tests\\Script2.txt'   , 'pass (8)' ),
                ('..\\Tests\\Field1.txt'   , '..\\Tests\\Script3.txt'   , 'pass (1)' ),
                ('..\\Tests\\Field4.txt'   , '..\\Tests\\Script4.txt'   , 'fail (0)' ),
                ('..\\Tests\\Field2.txt'   , '..\\Tests\\Script5.txt'   , 'fail (0)' ),
                ('..\\Tests\\Field2.txt'   , '..\\Tests\\Script7.txt'   , 'pass (18)'),
                ('..\\Tests\\Field5.1.txt' , '..\\Tests\\Script5.1.txt' , 'pass (32)'),
                ('..\\Tests\\Field2.3.txt' , '..\\Tests\\Script2.3.txt' , 'pass (38)'),
                ('..\\Tests\\Field2.4.txt' , '..\\Tests\\Script2.txt'   , 'pass (8)' ),
                ('..\\Tests\\Field2.5.txt' , '..\\Tests\\Script2.txt'   , 'pass (8)' )]
def main():
    _results = []
    sys.argv.insert(1,'')
    sys.argv.insert(2,'')
    
    for _field,_script,_expected_result in _TEST_PAIRS:
        sys.argv[1] = _field
        sys.argv[2] = _script
        _return_str = Eval_Mine_Clear_Script.main()

        _results.append([_field,_script,_return_str==_expected_result])

    _num_tests = len(_TEST_PAIRS)
    _num_failed = 0
    for _f,_s,_r in _results:
        if _r:
            _result = 'ok'
        else:
            _num_failed += 1
            _result = 'FAILED'
        print(_f + '\t' + _s + '\t---RESULTS---> ' + _result)

    print('\n' + str(_num_failed) + ' of ' + str(_num_tests) + ' tests FAILED.')

if __name__ == '__main__' :
    main()
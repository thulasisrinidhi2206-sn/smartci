# Python pytest build failure analysis

Analyze the pytest build log below and give a beginner-friendly diagnosis.

Return exactly these three sections:

## Root cause
Explain why the build failed and identify the relevant exception or assertion mismatch.

## Failing test or file
Name the failing pytest test and source or test file when they are present in the log.

## Suggested solution
Give concrete code or test changes that would fix or diagnose the failure. Keep suggestions consistent with the repository code.

Do not claim that you ran tests. Do not invent log details that are not present.

## Repository
- Project: Python pricing service
- Source module: `src/pricing.py`
- Tests: `tests/test_pricing.py`

## Extracted build information
```text
tests\test_pricing.py:7: AssertionError
tests\test_pricing.py:12: AssertionError
=========================== short test summary info ===========================
```

## Full build log
```text
============================= test session starts =============================

platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0 -- D:\smartci\.venv\Scripts\python.exe

cachedir: .pytest_cache

rootdir: D:\smartci

configfile: pytest.ini

collecting ... collected 4 items



tests/test_pricing.py::test_discount_basic FAILED                        [ 25%]

tests/test_pricing.py::test_discount_boundaries FAILED                   [ 50%]

tests/test_pricing.py::test_discount_invalid PASSED                      [ 75%]

tests/test_pricing.py::test_tax_default PASSED                           [100%]



================================== FAILURES ===================================

_____________________________ test_discount_basic _____________________________



    def test_discount_basic():

>       assert apply_discount(100, 10) == 90.0

E       assert 110.0 == 90.0

E        +  where 110.0 = apply_discount(100, 10)



tests\test_pricing.py:7: AssertionError

__________________________ test_discount_boundaries ___________________________



    def test_discount_boundaries():

        assert apply_discount(100, 0) == 100.0

>       assert apply_discount(100, 100) == 0.0

E       assert 200.0 == 0.0

E        +  where 200.0 = apply_discount(100, 100)



tests\test_pricing.py:12: AssertionError

=========================== short test summary info ===========================

FAILED tests/test_pricing.py::test_discount_basic - assert 110.0 == 90.0

FAILED tests/test_pricing.py::test_discount_boundaries - assert 200.0 == 0.0

========================= 2 failed, 2 passed in 0.17s =========================
```

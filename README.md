# sales-taxes-solution

A solution for the sales-taxes-problem tested on linux. Check the [documentation](https://riccap.github.io/sales-taxes-solution) for further details.

## Run

Go to the src directory and run

```
$ python price_updater.py ../test/input1.txt [../test/input2.txt ...]
```

the output files will be placed in the test dir.

## Test

The solution has been tested against the inputs provided by the sales-taxes-problem.

```
$ make tests
```

or go to the test folder and run

```
$ python -m unittest -b -v test.py
```

## Enhancements

Several enhancements can be implemented:

- A more powerful implementation of the method that checks tax exemption **_is_basic_exempt()** should be provided
- A logging system (to rule out all the print() which are really bad stuff in production code)
- A decision on how to handle exceptions and missing files/permissions should be taken
- A thorough test suite (further details in the comments of test.py)

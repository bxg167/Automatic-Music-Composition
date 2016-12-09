import os
import unittest

file_path = os.path.dirname(__file__)

main_suite = unittest.TestSuite()

# For now, leave these uncommented out, we only want to test Functional tests for now.
unit_test_suite = unittest.TestLoader().discover(os.path.join(file_path, "Unit_Tests"))
main_suite.addTest(unit_test_suite)

# TODO: UNCOMMENT THIS TO RUN ALL THE TESTS
# functional_test_suite = unittest.TestLoader().discover(os.path.join(file_path, "Functional_Tests"))
# main_suite.addTest(functional_test_suite)

results = unittest.TestResult()
main_suite.run(results)

print "Results: "
print "Number of Tests Ran: " + str(results.testsRun)
print "Number of Failures: " + str(len(results.failures))

if results.wasSuccessful():
    print "All tests passed." + "\n"
else:
    print "Some tests failed." + "\n"

    print "Failures: "
    for failure in results.failures:
        for info in failure:
            print info

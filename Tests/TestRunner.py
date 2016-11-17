import os
import unittest

file_path = os.path.dirname(__file__)

main_suite = unittest.TestSuite()


file_conversion_suite = unittest.TestLoader().discover(os.path.join(file_path, "File_Conversion_Tests"))
main_suite.addTest(file_conversion_suite)

gui_suite = unittest.TestLoader().discover(os.path.join(file_path, "GUI_Tests"))
main_suite.addTest(gui_suite)

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

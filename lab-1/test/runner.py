import unittest

from test import TestBorder, TestGeneral

# General test
print("******************************** GENERAL TESTS ********************************")
general = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
unittest.TextTestRunner(verbosity=2).run(general)
# Border tests
print("******************************** BORDER TESTS ********************************")
border = unittest.TestLoader().loadTestsFromTestCase(TestBorder)
unittest.TextTestRunner(verbosity=2).run(border)

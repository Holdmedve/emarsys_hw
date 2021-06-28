import unittest
from main import *

class TestCaseTime(unittest.TestCase):
    def testRaiseExceptionOnInvalidTimeValue(self):
        with self.assertRaises(InvalidTimeValue) as context:
            ValidateTime('0:52-PM-Monday')
        with self.assertRaises(InvalidTimeValue) as context:
            ValidateTime('3:92-PM-Monday')
        with self.assertRaises(InvalidTimeValue) as context:
            ValidateTime('3:52-PP-Monday')
        with self.assertRaises(InvalidTimeValue) as context:
            ValidateTime('3:52-PM-Tomorrow')


    def testRaiseExceptionOnInvalidTimeFormat(self):
        with self.assertRaises(InvalidTimeFormat) as context:
            ValidateTime('1312PM-Tuesday')
        with self.assertRaises(InvalidTimeFormat) as context:    
            ValidateTime('13:12:PM-Tuesday')
        with self.assertRaises(InvalidTimeFormat) as context:
            ValidateTime('1312PM Tuesday')
        with self.assertRaises(InvalidTimeFormat) as context:
            ValidateTime('13:1:2PM Tuesday')
        with self.assertRaises(InvalidTimeFormat) as context:            
            ValidateTime('Tuesday 13:1:2PM')
        with self.assertRaises(InvalidTimeFormat) as context:
            ValidateTime('f894fg4s65sd546fd8s')

    def testRaiseExceptionOnInvalidTurnaroundValue(self):
        with self.assertRaises(InvalidTurnaroundValue) as context:
            ValidateTurnaround('-12')
        with self.assertRaises(InvalidTurnaroundValue) as context:
            ValidateTurnaround('0')
        with self.assertRaises(InvalidTurnaroundValue) as context:
            ValidateTurnaround('manyhours')
        with self.assertRaises(InvalidTurnaroundValue) as context:
            ValidateTurnaround('40')
        with self.assertRaises(InvalidTurnaroundValue) as context:
            ValidateTurnaround('&afsasfa')

    def testReturnCorrectTimeValues(self):
        timeValues = ValidateTime('4:30-PM-Wednesday')
        self.assertTupleEqual(timeValues, (4, 30, 'PM', 'Wednesday'))

        timeValues = ValidateTime('5:00-PM-Friday')
        self.assertTupleEqual(timeValues, (5, 0, 'PM', 'Friday'))

        
    def testReturnCorrectTurnaroundValue(self):
        turnaround = ValidateTurnaround('2')   
        self.assertEqual(2, turnaround)

        turnaround = ValidateTurnaround('02')   
        self.assertEqual(2, turnaround)
        
    def test12to24formatConversion(self):
        converted = Convert12to24format(12, 'PM')
        self.assertEqual(converted, 12)

        converted = Convert12to24format(1, 'PM')
        self.assertEqual(converted, 13)

        converted = Convert12to24format(9, 'AM')
        self.assertEqual(converted, 9)

        converted = Convert12to24format(11, 'AM')
        self.assertEqual(converted, 11)
    
        converted = Convert12to24format(5, 'PM')
        self.assertEqual(converted, 17)

    def test24to12formatConversions(self):
        converted = Convert24to12format(13)
        self.assertEqual(converted, (1, 'PM'))

        converted = Convert24to12format(12)
        self.assertEqual(converted, (12, 'PM'))

        converted = Convert24to12format(9)
        self.assertEqual(converted, (9, 'AM'))

    def testDueDayCalculation(self):
        dueDay = CalculateDueDay('Tuesday', 1)
        self.assertEqual(dueDay, 'Wednesday')

        dueDay = CalculateDueDay('Friday', 2)
        self.assertEqual(dueDay, 'Tuesday')

        dueDay = CalculateDueDay('Thursday', 4)
        self.assertEqual(dueDay, 'Wednesday')

    def testDueDateCalculationOnValidInput(self):
        dueDate = CalculateDueDate('2:33-PM-Tuesday', '8')
        self.assertEqual(dueDate, (2, 33, 'PM', 'Wednesday'))

        dueDate = CalculateDueDate('10:04-AM-Friday', '1')
        self.assertEqual(dueDate, (11, 4, 'AM', 'Friday'))

        dueDate = CalculateDueDate('10:04-AM-Friday', '5')
        self.assertEqual(dueDate, (3, 4, 'PM', 'Friday'))

        dueDate = CalculateDueDate('9:00-AM-Monday', '8')
        self.assertEqual(dueDate, (9, 0, 'AM', 'Tuesday'))

        dueDate = CalculateDueDate('1:09-PM-Tuesday', '22')
        self.assertEqual(dueDate, (11, 9, 'AM', 'Friday'))

        dueDate = CalculateDueDate('2:15-PM-Thursday', '17')
        self.assertEqual(dueDate, (3, 15, 'PM', 'Monday'))

    def testDueDateCalculationOnInvalidInput(self):
        dueDate = CalculateDueDate('22:15-PM-Thursday', '17')
        self.assertEqual(dueDate, (0, 0, '', ''))

        dueDate = CalculateDueDate('2:15-PM-Thursday', '500')
        self.assertEqual(dueDate, (0, 0, '', ''))

        dueDate = CalculateDueDate('2:15-PM-Yesterday', '5')
        self.assertEqual(dueDate, (0, 0, '', ''))


if __name__ == '__main__':
    unittest.main()

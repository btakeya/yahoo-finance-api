import unittest
from unittest import main as test_main
from Utility import to_utc


class TestUtility(unittest.TestCase):

    def setUp(self):
        pass

    def test_kst_to_utc(self):
        # UTC + 0900 = KST
        in_kst_time = '2016-08-03 23:40:30'
        desired_utc_time = '2016-08-03 14:40:30 UTC+0000'
        converted_time = to_utc(in_kst_time)

        self.assertEqual(desired_utc_time, converted_utc_time,
                         'Desired: {} - Converted: {}\n'
                         .format(desired_utc_time, converted_time))

    def test_pdt_to_utc(self):
        # UTC - (0700 + 0100) = PDT
        in_pdt_time = '2016-08-03 23:40:30'
        desired_utc_time = '2016-08-04 06:40:30 UTC+0000'
        converted_time_from_pdt = to_utc(in_pdt_time, from_tz='US/Pacific')

        self.assertNotEqual(desired_utc_time,
                            converted_utc_time_as_pdt,
                            'Desired: {} - Converted: {}\n'
                            .format(desired_utc_time, converted_time_from_pdt))

    def tearDown(self):
        pass


if __name__ == '__main__':
    test_main()

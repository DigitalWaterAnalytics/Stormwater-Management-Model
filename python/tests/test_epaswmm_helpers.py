# Description: Unit tests for the epaswmm module.
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# python imports
import unittest
from datetime import datetime

# third party imports

# local imports
import epaswmm


class TestEPASWMMHelperFunctions(unittest.TestCase):
    """
    Test the SWMM solver functions
    """
    def test_decode_swmm_datetime(self):
        """
        Test the decode_swmm_datetime function
        :return:
        """
        swmm_datetime = epaswmm.decode_swmm_datetime(45612.564826389)
        self.assertEqual(swmm_datetime, datetime(year=2024, month=11, day=16, hour=13, minute=33, second=21))

    def test_encode_swmm_datetime(self):
        """
        Test the encode_swmm_datetime function
        :return:
        """
        swmm_datetime = datetime(year=2024, month=11, day=16, hour=13, minute=33, second=21)
        swmm_datetime_encoded = epaswmm.encode_swmm_datetime(swmm_datetime)
        self.assertAlmostEqual(swmm_datetime_encoded, 45612.564826389)

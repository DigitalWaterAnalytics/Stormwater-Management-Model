# Description: Unit tests for the epaswmm solver module.
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# python imports
import unittest
from datetime import datetime

# third party imports

# local imports
from .data import solver as example_solver_data
from epaswmm import solver


class TestSWMMSolver(unittest.TestCase):

    def setUp(self):
        pass

    @staticmethod
    def progress_callback(progress: float) -> None:
        assert 0 <= progress <= 1.0

    def test_get_swmm_version(self):
        """
        Test the version function of the SWMM solver
        :return:
        """
        version = solver.version()
        self.assertEqual(version, 53000, "SWMM version retrieved successfully")

    def test_swmm_encode_date(self):
        """
        Test the encode_swmm_datetime function
        :return:
        """

        swmm_datetime = datetime(year=2024, month=11, day=16, hour=13, minute=33, second=21)
        swmm_datetime_encoded = solver.encode_swmm_datetime(swmm_datetime)
        self.assertAlmostEqual(swmm_datetime_encoded, 45612.564826389)

    def test_swmm_decode_date(self):
        """
        Test the decode_swmm_datetime function
        :return:
        """
        swmm_datetime = solver.decode_swmm_datetime(45612.564826389)
        self.assertEqual(swmm_datetime, datetime(year=2024, month=11, day=16, hour=13, minute=33, second=21))

    def test_run_solver(self):
        error = solver.run_solver(
            inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
            rpt_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".rpt"),
            out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        )

        self.assertEqual(error, 0, "SWMM solver run successfully.")

    def test_run_solver_with_progress_callback(self):
        error = solver.run_solver(
            inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
            rpt_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".rpt"),
            out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
            swmm_progress_callback=self.progress_callback
        )

        self.assertEqual(error, 0, "SWMM solver with callbacks run successfully.")

    def test_run_solver_invalid_inp_file(self):
        with self.assertRaises(Exception) as context:
            error = solver.run_solver(
                inp_file=example_solver_data.NON_EXISTENT_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".out"),
            )

        self.assertIn('ERROR 303: cannot open input file.', str(context.exception))

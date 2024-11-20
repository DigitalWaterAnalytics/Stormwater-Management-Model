# Description: Unit tests for the epaswmm solver module.
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# python imports
import unittest

# third party imports

# local imports
from .data import solver as example_solver_data
from epaswmm import solver


class TestSWMMSolver(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_swmm_version(self):
        """
        Test the version function of the SWMM solver
        :return:
        """
        version = solver.version()
        self.assertEqual(version, 53000, "SWMM version retrieved successfully")

    def test_run_solver(self):
        error = solver.run_solver(
            inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
            rpt_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".rpt"),
            out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        )

        self.assertEqual(error, 0, "SWMM solver run successfully.")

    def test_run_solver_invalid_inp_file(self):

        with self.assertRaises(Exception) as context:
            error = solver.run_solver(
                inp_file=example_solver_data.NON_EXISTENT_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".out"),
            )

        self.assertIn('ERROR 303: cannot open input file.', str(context.exception))
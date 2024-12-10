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
        """
        Progress callback function for the SWMM solver
        :param progress:
        :return:
        """
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
        """
        Run the SWMM solver to solve the example input file

        :return:
        """
        error = solver.run_solver(
            inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
            rpt_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".rpt"),
            out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        )

        self.assertEqual(error, 0, "SWMM solver run successfully.")

    def test_run_solver_with_progress_callback(self):
        """
        Run the SWMM solver to solve the example input file with progress callback

        :return:
        """
        error = solver.run_solver(
            inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
            rpt_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".rpt"),
            out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
            swmm_progress_callback=self.progress_callback
        )

        self.assertEqual(error, 0, "SWMM solver with callbacks run successfully.")

    def test_run_solver_invalid_inp_file(self):
        """
        Run the SWMM solver with an invalid input file path to test error handling
        :return:
        """
        with self.assertRaises(Exception) as context:
            error = solver.run_solver(
                inp_file=example_solver_data.NON_EXISTENT_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".out"),
            )

        self.assertIn('ERROR 303: cannot open input file.', str(context.exception))

    def test_run_without_context_manager(self):
        """
        Run the SWMM solver without a context manager
        :return:
        """

        swmm_solver = solver.Solver(
            inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
            rpt_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".rpt"),
            out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        )

        swmm_solver.execute()

    def test_run_without_context_manager_step_by_step(self):
        """
        Run the SWMM solver without a context manager and an invalid input file path to test error handling
        :return:
        """

        swmm_solver = solver.Solver(
            inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
            rpt_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".rpt"),
            out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        )

        swmm_solver.initialize()

        while swmm_solver.solver_state != solver.SolverState.FINISHED:
            swmm_solver.step()

        swmm_solver.finalize()

    def test_run_solver_with_context_manager(self):
        """
        Run the SWMM solver with an invalid report file path to test error handling
        :return:
        """

        with solver.Solver(
                inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        ) as swmm_solver:
            swmm_solver.initialize()

            for t in swmm_solver:
                pass

    def test_solver_get_time_attributes(self):
        """
        Test the get_start_date function of the SWMM solver
        :return:
        """
        with solver.Solver(
                inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
                rpt_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out")
        ) as swmm_solver:

            swmm_solver.initialize()

            start_date = swmm_solver.start_datetime

            self.assertEqual(start_date, datetime(year=1998, month=1, day=1))

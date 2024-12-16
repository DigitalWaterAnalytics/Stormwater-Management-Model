# Description: Unit tests for the epaswmm solver module.
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# python imports
import unittest
from datetime import datetime

# third party imports
import os
import sys


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

    def test_get_object_count(self):
        """
        Test the get_object_count function of the SWMM solver
        :return:
        """
        with solver.Solver(
                inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
                rpt_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out")
        ) as swmm_solver:
            swmm_solver.initialize()

            num_raingages = swmm_solver.get_object_count(solver.SWMMObjects.RAIN_GAGE)
            num_subcatchments = swmm_solver.get_object_count(solver.SWMMObjects.SUBCATCHMENT)
            num_nodes = swmm_solver.get_object_count(solver.SWMMObjects.NODE)
            num_links = swmm_solver.get_object_count(solver.SWMMObjects.LINK)
            num_aquifers = swmm_solver.get_object_count(solver.SWMMObjects.AQUIFER)
            num_snowpacks = swmm_solver.get_object_count(solver.SWMMObjects.SNOWPACK)
            num_hydrographs = swmm_solver.get_object_count(solver.SWMMObjects.UNIT_HYDROGRAPH)
            num_lids = swmm_solver.get_object_count(solver.SWMMObjects.LID)
            num_streets = swmm_solver.get_object_count(solver.SWMMObjects.STREET)
            num_inlets = swmm_solver.get_object_count(solver.SWMMObjects.INLET)
            num_transects = swmm_solver.get_object_count(solver.SWMMObjects.TRANSECT)
            num_xsections = swmm_solver.get_object_count(solver.SWMMObjects.XSECTION_SHAPE)
            num_controls = swmm_solver.get_object_count(solver.SWMMObjects.CONTROL_RULE)
            num_pollutants = swmm_solver.get_object_count(solver.SWMMObjects.POLLUTANT)
            num_landuses = swmm_solver.get_object_count(solver.SWMMObjects.LANDUSE)
            num_curves = swmm_solver.get_object_count(solver.SWMMObjects.CURVE)
            num_timeseries = swmm_solver.get_object_count(solver.SWMMObjects.TIMESERIES)
            num_time_patterns = swmm_solver.get_object_count(solver.SWMMObjects.TIME_PATTERN)

            self.assertEqual(num_raingages, 1)
            self.assertEqual(num_subcatchments, 7)
            self.assertEqual(num_nodes, 12)
            self.assertEqual(num_links, 11)
            self.assertEqual(num_aquifers, 0)
            self.assertEqual(num_snowpacks, 0)
            self.assertEqual(num_hydrographs, 0)
            self.assertEqual(num_lids, 0)
            self.assertEqual(num_streets, 0)
            self.assertEqual(num_inlets, 0)
            self.assertEqual(num_transects, 0)
            self.assertEqual(num_xsections, 0)
            self.assertEqual(num_controls, 0)
            self.assertEqual(num_pollutants, 1)
            self.assertEqual(num_landuses, 4)
            self.assertEqual(num_curves, 0)
            self.assertEqual(num_timeseries, 3)
            self.assertEqual(num_time_patterns, 0)

            with self.assertRaises(solver.SWMMSolverException) as context:
                system_vars = swmm_solver.get_object_count(solver.SWMMObjects.SYSTEM)

            self.assertIn('API Error -999904: invalid object type.', str(context.exception))

    def test_get_object_names(self):
        """
        Test the get_object_names function of the SWMM solver
        :return:
        """

        with solver.Solver(
                inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        ) as swmm_solver:
            swmm_solver.initialize()

            raingage_names = swmm_solver.get_object_names(solver.SWMMObjects.RAIN_GAGE)
            subcatchment_names = swmm_solver.get_object_names(solver.SWMMObjects.SUBCATCHMENT)
            node_names = swmm_solver.get_object_names(solver.SWMMObjects.NODE)
            link_names = swmm_solver.get_object_names(solver.SWMMObjects.LINK)
            pollutant_names = swmm_solver.get_object_names(solver.SWMMObjects.POLLUTANT)
            landuse_names = swmm_solver.get_object_names(solver.SWMMObjects.LANDUSE)
            timeseries_names = swmm_solver.get_object_names(solver.SWMMObjects.TIMESERIES)

            self.assertListEqual(raingage_names, ['RainGage'])
            self.assertListEqual(subcatchment_names, ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'])
            self.assertListEqual(node_names, ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10', 'J11', 'O1'])
            self.assertListEqual(link_names, ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11'])
            self.assertListEqual(pollutant_names, ['TSS'])
            self.assertListEqual(landuse_names, ['Residential_1', 'Residential_2', 'Commercial', 'Undeveloped'])
            self.assertListEqual(timeseries_names, ['2-yr', '10-yr', '100-yr'])

    def test_get_object_index(self):
        """
        Test the get_object_index function of the SWMM solver
        :return:
        """

        with solver.Solver(
                inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        ) as swmm_solver:
            swmm_solver.initialize()

            rg_index = swmm_solver.get_object_index(solver.SWMMObjects.RAIN_GAGE, 'RainGage')
            sc_index = swmm_solver.get_object_index(solver.SWMMObjects.SUBCATCHMENT, 'S2')
            node_index = swmm_solver.get_object_index(solver.SWMMObjects.NODE, 'J6')
            link_index = swmm_solver.get_object_index(solver.SWMMObjects.LINK, 'C10')
            pollutant_index = swmm_solver.get_object_index(solver.SWMMObjects.POLLUTANT, 'TSS')
            landuse_index = swmm_solver.get_object_index(solver.SWMMObjects.LANDUSE, 'Commercial')
            timeseries_index = swmm_solver.get_object_index(solver.SWMMObjects.TIMESERIES, '10-yr')

            self.assertEqual(rg_index, 0)
            self.assertEqual(sc_index, 1)
            self.assertEqual(node_index, 5)
            self.assertEqual(link_index, 9)
            self.assertEqual(pollutant_index, 0)
            self.assertEqual(landuse_index, 2)
            self.assertEqual(timeseries_index, 1)

    def test_get_gage_value(self):
        """
        Test the get_gage_value function of the SWMM solver
        :return:
        """

        with solver.Solver(
                inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        ) as swmm_solver:
            swmm_solver.initialize()

            for t in range(12):
                swmm_solver.step()

            rg_value = swmm_solver.get_value(
                object_type=solver.SWMMObjects.RAIN_GAGE.value,
                property_type=solver.SWMMRainGageProperties.GAGE_TOTAL_PRECIPITATION.value,
                index=0,
            )

            self.assertAlmostEqual(rg_value / 12.0, 0.3)

    def test_set_gage_value(self):
        """
        Test the set_gage_value function of the SWMM solver
        :return:
        """

        with solver.Solver(
                inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        ) as swmm_solver:
            swmm_solver.initialize()

            swmm_solver.set_value(
                object_type=solver.SWMMObjects.RAIN_GAGE.value,
                property_type=solver.SWMMRainGageProperties.GAGE_RAINFALL.value,
                index=0,
                value=3.6
            )

            for _ in range(12):
                swmm_solver.step()

            rg_value = swmm_solver.get_value(
                object_type=solver.SWMMObjects.RAIN_GAGE.value,
                property_type=solver.SWMMRainGageProperties.GAGE_TOTAL_PRECIPITATION.value,
                index=0,
            )

            self.assertAlmostEqual(rg_value , 3.6)

    def test_get_subcatchment_value(self):
        """
        Test the get_subcatchment_value function of the SWMM solver
        :return:
        """

        with solver.Solver(
                inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        ) as swmm_solver:
            swmm_solver.initialize()

            for t in range(12):
                swmm_solver.step()

            sc_value = swmm_solver.get_value(
                object_type=solver.SWMMObjects.SUBCATCHMENT.value,
                property_type=solver.SWMMSubcatchmentProperties.RUNOFF.value,
                index=1,
            )

            self.assertAlmostEqual(sc_value, 17.527141504933294)

    def test_set_subcatchment_value(self):
        """
        Test the set_subcatchment_value function of the SWMM solver
        :return:
        """

        with solver.Solver(
                inp_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE,
                rpt_file=example_solver_data.NON_EXISTENT_INPUT_FILE.replace(".inp", ".rpt"),
                out_file=example_solver_data.SITE_DRAINAGE_EXAMPLE_INPUT_FILE.replace(".inp", ".out"),
        ) as swmm_solver:

            swmm_solver.initialize()

            error_code = swmm_solver.set_value(
                object_type=solver.SWMMObjects.SUBCATCHMENT.value,
                property_type=solver.SWMMSubcatchmentProperties.WIDTH.value,
                index=1,
                value=100.0
            )

            for _ in range(12):
                swmm_solver.step()

            sc_value = swmm_solver.get_value(
                object_type=solver.SWMMObjects.SUBCATCHMENT.value,
                property_type=solver.SWMMSubcatchmentProperties.WIDTH.value,
                index=1,
            )

            self.assertAlmostEqual(sc_value, 100.0)

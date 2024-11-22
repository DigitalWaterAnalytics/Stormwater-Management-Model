# Description: Unit tests for the SWMM output module
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# python imports
import json
import unittest
from datetime import datetime
import pickle

# third party imports

# local imports
from .data import output as example_output_data
from epaswmm import output
from epaswmm.output import Output, SWMMOutputException


class TestSWMMOutput(unittest.TestCase):
    """
    Test the SWMM solver functions

    TODO: Add tests to check for exceptions and errors
    """
    def setUp(self):

        self.test_artifacts = {}

        with open(example_output_data.JSON_TIME_SERIES_FILE, 'rb') as f:
            self.test_artifacts = pickle.load(f)

    # def test_output_encode_date(self):
    #     """
    #     Test the encode_swmm_datetime function
    #     :return:
    #     """
    #
    #     swmm_datetime = datetime(year=2024, month=11, day=16, hour=13, minute=33, second=21)
    #     swmm_datetime_encoded = output.encode_swmm_datetime(swmm_datetime)
    #     self.assertAlmostEqual(swmm_datetime_encoded, 45612.564826389)
    #
    # def test_output_decode_date(self):
    #     """
    #     Test the decode_swmm_datetime function
    #     :return:
    #     """
    #     swmm_datetime = output.decode_swmm_datetime(45612.564826389)
    #     self.assertEqual(swmm_datetime, datetime(year=2024, month=11, day=16, hour=13, minute=33, second=21))

    def test_output_unit_system_enum(self):
        """
        Test the output unit system enum
        :return:
        """

        self.assertEqual(output.UnitSystem.US.value, 0, "US unit system value should be 0")
        self.assertEqual(output.UnitSystem.SI.value, 1, "SI unit system value should be 1")

    def test_output_flow_units_enum(self):
        """
        Test the output flow units enum
        :return:
        """

        self.assertEqual(output.FlowUnits.CFS.value, 0, "CFS flow unit value should be 0")
        self.assertEqual(output.FlowUnits.GPM.value, 1, "GPM flow unit value should be 1")
        self.assertEqual(output.FlowUnits.MGD.value, 2, "MGD flow unit value should be 2")
        self.assertEqual(output.FlowUnits.CMS.value, 3, "CMS flow unit value should be 3")
        self.assertEqual(output.FlowUnits.LPS.value, 4, "LPS flow unit value should be 4")
        self.assertEqual(output.FlowUnits.MLD.value, 5, "MLD flow unit value should be 5")

    def test_output_concentration_units_enum(self):
        """
        Test the output concentration units enum
        :return:
        """

        self.assertEqual(output.ConcentrationUnits.MG.value, 0, "MG concentration unit value should be 0")
        self.assertEqual(output.ConcentrationUnits.UG.value, 1, "UG concentration unit value should be 1")
        self.assertEqual(output.ConcentrationUnits.COUNT.value, 2, "COUNT concentration unit value should be 2")
        self.assertEqual(output.ConcentrationUnits.NONE.value, 3, "NONE concentration unit value should be 3")

    def test_output_element_type_enum(self):
        """
        Test the output element type enum
        :return:
        """

        self.assertEqual(output.ElementType.SUBCATCHMENT.value, 0, "SUBCATCHMENT element type value should be 0")
        self.assertEqual(output.ElementType.NODE.value, 1, "NODE element type value should be 1")
        self.assertEqual(output.ElementType.LINK.value, 2, "LINK element type value should be 2")
        self.assertEqual(output.ElementType.SYSTEM.value, 3, "SYSTEM element type value should be 3")
        self.assertEqual(output.ElementType.POLLUTANT.value, 4, "POLLUTANT element type value should be 4")

    def test_output_time_enum(self):
        """
        Test the output time enum
        :return:
        """

        self.assertEqual(output.TimeAttribute.REPORT_STEP.value, 0, "REPORT_STEP time value should be 0")
        self.assertEqual(output.TimeAttribute.NUM_PERIODS.value, 1, "NUM_PERIODS time value should be 1")

    def test_output_subcatch_attribute_enum(self):
        """
        Test the output subcatchment attribute enum
        :return:
        """

        self.assertEqual(output.SubcatchAttribute.RAINFALL.value, 0, "RAINFALL subcatchment attribute value should be 0")
        self.assertEqual(output.SubcatchAttribute.SNOW_DEPTH.value, 1, "SNOW_DEPTH subcatchment attribute value should be 1")
        self.assertEqual(output.SubcatchAttribute.EVAPORATION_LOSS.value, 2, "EVAPORATION_LOSS subcatchment attribute value should be 2")
        self.assertEqual(output.SubcatchAttribute.INFILTRATION_LOSS.value, 3, "INFILTRATION_LOSS subcatchment attribute value should be 3")
        self.assertEqual(output.SubcatchAttribute.RUNOFF_RATE.value, 4, "RUNOFF_RATE subcatchment attribute value should be 4")
        self.assertEqual(output.SubcatchAttribute.GROUNDWATER_OUTFLOW.value, 5, "GROUNDWATER_OUTFLOW subcatchment attribute value should be 5")
        self.assertEqual(output.SubcatchAttribute.GROUNDWATER_TABLE_ELEVATION.value, 6, "GROUNTWATER_TABLE subcatchment attribute value should be 6")
        self.assertEqual(output.SubcatchAttribute.SOIL_MOISTURE.value, 7, "SOIL_MOISTURE subcatchment attribute value should be 7")
        self.assertEqual(output.SubcatchAttribute.POLLUTANT_CONCENTRATION.value, 8, "POLLUTANT_CONCENTRATION subcatchment attribute value should be 8")

    def test_output_node_attribute_enum(self):
        """
        Test the output node attribute enum
        :return:
        """

        self.assertEqual(output.NodeAttribute.INVERT_DEPTH.value, 0, "INVERT_DEPTH node attribute value should be 0")
        self.assertEqual(output.NodeAttribute.HYDRAULIC_HEAD.value, 1, "HYDRAULIC_HEAD node attribute value should be 1")
        self.assertEqual(output.NodeAttribute.STORED_VOLUME.value, 2, "STORED_VOLUME node attribute value should be 2")
        self.assertEqual(output.NodeAttribute.LATERAL_INFLOW.value, 3, "LATERAL_INFLOW node attribute value should be 3")
        self.assertEqual(output.NodeAttribute.TOTAL_INFLOW.value, 4, "TOTAL_INFLOW node attribute value should be 4")
        self.assertEqual(output.NodeAttribute.FLOODING_LOSSES.value, 5, "FLOODING_LOSSES node attribute value should be 5")
        self.assertEqual(output.NodeAttribute.POLLUTANT_CONCENTRATION.value, 6, "POLLUTANT_CONCENTRATION node attribute value should be 6")

    def test_output_link_attribute_enum(self):
        """
        Test the output link attribute enum
        :return:
        """

        self.assertEqual(output.LinkAttribute.FLOW_RATE.value, 0, "FLOW_RATE link attribute value should be 0")
        self.assertEqual(output.LinkAttribute.FLOW_DEPTH.value, 1, "FLOW_DEPTH link attribute value should be 1")
        self.assertEqual(output.LinkAttribute.FLOW_VELOCITY.value, 2, "FLOW_VELOCITY link attribute value should be 2")
        self.assertEqual(output.LinkAttribute.FLOW_VOLUME.value, 3, "FLOW_VOLUME link attribute value should be 3")
        self.assertEqual(output.LinkAttribute.CAPACITY.value, 4, "CAPACITY link attribute value should be 4")
        self.assertEqual(output.LinkAttribute.POLLUTANT_CONCENTRATION.value, 5, "POLLUTANT_CONCENTRATION link attribute value should be 5")

    def test_output_system_attribute_enum(self):
        """
        Test the output system attribute enum
        :return:
        """

        self.assertEqual(output.SystemAttribute.AIR_TEMP.value, 0, "AIR_TEMP system attribute value should be 0")
        self.assertEqual(output.SystemAttribute.RAINFALL.value, 1, "RAINFALL system attribute value should be 1")
        self.assertEqual(output.SystemAttribute.SNOW_DEPTH.value, 2, "SNOW_DEPTH system attribute value should be 2")
        self.assertEqual(output.SystemAttribute.EVAP_INFIL_LOSS.value, 3, "EVAP_INFIL_LOSS system attribute value should be 3")
        self.assertEqual(output.SystemAttribute.RUNOFF_FLOW.value, 4, "RUNOFF_FLOW system attribute value should be 4")
        self.assertEqual(output.SystemAttribute.DRY_WEATHER_INFLOW.value, 5, "DRY_WEATHER_INFLOW system attribute value should be 5")
        self.assertEqual(output.SystemAttribute.GROUNDWATER_INFLOW.value, 6, "GROUNDWATER_INFLOW system attribute value should be 6")
        self.assertEqual(output.SystemAttribute.RDII_INFLOW.value, 7, "RDII_INFLOW system attribute value should be 7")
        self.assertEqual(output.SystemAttribute.DIRECT_INFLOW.value, 8, "DIRECT_INFLOW system attribute value should be 8")
        self.assertEqual(output.SystemAttribute.TOTAL_LATERAL_INFLOW.value, 9, "TOTAL_LATERAL_INFLOW system attribute value should be 9")
        self.assertEqual(output.SystemAttribute.FLOOD_LOSSES.value, 10, "FLOOD_LOSSES system attribute value should be 10")
        self.assertEqual(output.SystemAttribute.OUTFALL_FLOWS.value, 11, "OUTFALL_FLOWS system attribute value should be 11")
        self.assertEqual(output.SystemAttribute.VOLUME_STORED.value, 12, "VOLUME_STORED system attribute value should be 12")
        self.assertEqual(output.SystemAttribute.EVAPORATION_RATE.value, 13, "EVAPORATION_RATE system attribute value should be 13")

    def test_output_open_and_close(self):
        """
        Test the output open and close functions
        :return:
        """
        with Output(example_output_data.EXAMPLE_OUTPUT_FILE_1) as swmm_output:
            pass

        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)

    def test_output_open_error(self):
        """
        Test the output open error function
        :return:
        """
        with self.assertRaises(FileNotFoundError) as context:
            swmm_output = Output(example_output_data.NON_EXISTENT_OUTPUT_FILE)

        self.assertIn(
            member="Error opening the SWMM output file",
            container=str(context.exception),
            msg="Error message should be 'Error opening the SWMM output file'"
        )

    def test_output_get_version(self):
        """
        Test the output get version function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        version = swmm_output.version

        self.assertEqual(version,   51000, "Version should be 51000")

    def test_output_get_size(self):
        """
        Test the output get size function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        size = swmm_output.output_size.values()

        self.assertListEqual(list(size), [8, 14, 13, 1, 2], "Size should be [8, 14, 13, 1, 2]")

    def test_output_get_units(self):
        """
        Test the output get units function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        units = swmm_output.units

        self.assertListEqual(
            list(units),
            [
                output.UnitSystem.US,
                output.FlowUnits.CFS,
                [output.ConcentrationUnits.MG, output.ConcentrationUnits.UG]
            ],
            "Units should be [US, CFS, [MG, UG]]"
        )

    def test_output_get_flow_units(self):
        """
        Test the output get flow units function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        flow_units = swmm_output.flow_units

        self.assertEqual(flow_units, output.FlowUnits.CFS, "Flow units should be CFS")

    def test_output_get_start_date(self):
        """
        Test the output get start date function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        start_date = swmm_output.start_date

        self.assertEqual(start_date, datetime(year=1998, month=1, day=1), "Start date should be 01/01/1998")

    def test_output_get_time_attributes(self):
        """
        Test the output get temporal attributes function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        report_step = swmm_output.get_time_attribute(output.TimeAttribute.REPORT_STEP.value)
        num_periods = swmm_output.get_time_attribute(output.TimeAttribute.NUM_PERIODS.value)

        self.assertEqual(report_step, 3600, "Report step should be 300")
        self.assertEqual(num_periods, 36, "Number of periods should be 365")

    def test_output_get_element_name(self):
        """
        Test the output get element names function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)

        retrieved_subcatch_names = [
            swmm_output.get_element_name(output.ElementType.SUBCATCHMENT.value, i) for i in range(8)
        ]
        subcatch_names = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.assertListEqual(
            retrieved_subcatch_names, subcatch_names, "Subcatchment names should be [1, 2, 3, 4, 5, 6, 7, 8]"
        )

        retrieved_node_names = [
            swmm_output.get_element_name(output.ElementType.NODE.value, i) for i in range(14)
        ]

        node_names = [
            '9', '10', '13', '14', '15', '16', '17', '19', '20', '21', '22', '23', '24', '18'
        ]
        self.assertListEqual(
            retrieved_node_names, node_names,
            "Node names should be [9, 10, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 18]"
        )

        retrieved_link_names = [
            swmm_output.get_element_name(output.ElementType.LINK.value, i) for i in range(13)
        ]
        link_names = ['1', '4', '5', '6', '7', '8', '10', '11', '12', '13', '14', '15', '16']
        self.assertListEqual(
            retrieved_link_names, link_names,
            "Link names should be [1, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16]"
        )

        retrieved_pollutant_names = [
            swmm_output.get_element_name(output.ElementType.POLLUTANT.value, i) for i in range(2)
        ]
        pollutant_names = ['TSS', 'Lead']
        self.assertListEqual(retrieved_pollutant_names, pollutant_names, "Pollutant names should be [TSS, TSS]")

    def test_get_element_name_errors(self):
        """
        Test the output get element name error function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)

        with self.assertRaises(Exception) as context:
            swmm_output.get_element_name(output.ElementType.SYSTEM.value, 0)

        self.assertIn(
            member="nvalid parameter code",
            container=str(context.exception),
            msg="Error message should be 'Invalid element type'"
        )

        with self.assertRaises(Exception) as context:
            swmm_output.get_element_name(output.ElementType.SUBCATCHMENT.value, 8)

        self.assertIn(
            member="element index out of range",
            container=str(context.exception),
            msg="Error message should be 'Index out of range'"
        )

    def test_output_get_element_names(self):
        """
        Test the output get element names error function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)

        retrieved_subcatch_names = swmm_output.get_element_names(output.ElementType.SUBCATCHMENT.value)
        subcatch_names = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.assertListEqual(
            retrieved_subcatch_names, subcatch_names, "Subcatchment names should be [1, 2, 3, 4, 5, 6, 7, 8]"
        )

        retrieved_node_names = swmm_output.get_element_names(output.ElementType.NODE.value)
        node_names = [
            '9', '10', '13', '14', '15', '16', '17', '19', '20', '21', '22', '23', '24', '18'
        ]
        self.assertListEqual(
            retrieved_node_names, node_names,
            "Node names should be [9, 10, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 18]"
        )

        retrieved_link_names = swmm_output.get_element_names(output.ElementType.LINK.value)
        link_names = ['1', '4', '5', '6', '7', '8', '10', '11', '12', '13', '14', '15', '16']
        self.assertListEqual(
            retrieved_link_names, link_names,
            "Link names should be [1, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16]"
        )

        retrieved_pollutant_names = swmm_output.get_element_names(output.ElementType.POLLUTANT.value)
        pollutant_names = ['TSS', 'Lead']
        self.assertListEqual(retrieved_pollutant_names, pollutant_names, "Pollutant names should be [TSS, TSS]")

        with self.assertRaises(SWMMOutputException) as context:
            swmm_output.get_element_names(output.ElementType.SYSTEM.value)

        self.assertIn(
            member="Cannot get element names for the system element type",
            container=str(context.exception),
            msg="Error message should be 'Invalid element type'"
        )

    def test_get_times(self):
        """
        Test the output get timeseries function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        times = swmm_output.times

        self.assertEqual(len(times), 36, "Number of times should be 36")

        self.assertEqual(
            times[0],
            datetime(1998, 1, 1, 1, 0),
            "First time should be 01/01/1998 01:00"
        )

        self.assertEqual(
            times[16],
            datetime(1998, 1, 1, 17, 0),
            "Middle time should be 01/01/1998 14:00"
        )

        self.assertEqual(
            times[-1],
            datetime(1998, 1, 2, 12, 0),
            "Last time should be 01/02/1998 12:00"
        )

    def test_get_subcatchment_timeseries(self):
        """
        Test the output get subcatchment timeseries function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        subcatchment_timeseries = swmm_output.get_subcatchment_timeseries(
            element_index=5,
            attribute=output.SubcatchAttribute.RUNOFF_RATE.value,
        )

        TestSWMMOutput.assert_dict_almost_equal(
            subcatchment_timeseries,
            self.test_artifacts['test_get_subcatchment_timeseries'],
        )

    def test_get_node_timeseries(self):
        """
        Test the output get node timeseries function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        node_timeseries = swmm_output.get_node_timeseries(
            element_index=7,
            attribute=output.NodeAttribute.TOTAL_INFLOW.value,
        )

        TestSWMMOutput.assert_dict_almost_equal(
            node_timeseries,
            self.test_artifacts['test_get_node_timeseries'],
        )

    def test_get_link_timeseries(self):
        """
        Test the output get link timeseries function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        link_timeseries = swmm_output.get_link_timeseries(
            element_index=5,
            attribute=output.LinkAttribute.FLOW_RATE.value,
        )

        TestSWMMOutput.assert_dict_almost_equal(
            link_timeseries,
            self.test_artifacts['test_get_link_timeseries'],
        )

    def test_get_system_timeseries(self):
        """
        Test the output get system timeseries function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        system_timeseries = swmm_output.get_system_timeseries(
            attribute=output.SystemAttribute.RUNOFF_FLOW.value
        )

        TestSWMMOutput.assert_dict_almost_equal(
            system_timeseries,
            self.test_artifacts['test_get_system_timeseries'],
        )

    def test_get_subcatchment_values_by_time_and_attributes(self):
        """
        Test the output get subcatchment values by time and attributes function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        subcatchment_values = swmm_output.get_subcatchment_values_by_time_and_attribute(
            time_index=5,
            attribute=output.SubcatchAttribute.RUNOFF_RATE.value
        )

        TestSWMMOutput.assert_dict_almost_equal(
            subcatchment_values,
            self.test_artifacts['test_get_subcatchment_values_by_time_and_attributes'],
        )

    def test_get_node_values_by_time_and_attributes(self):
        """
        Test the output get node values by time and attributes function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        node_values = swmm_output.get_node_values_by_time_and_attribute(
            time_index=8,
            attribute=output.NodeAttribute.TOTAL_INFLOW.value
        )

        TestSWMMOutput.assert_dict_almost_equal(
            node_values,
            self.test_artifacts['test_get_node_values_by_time_and_attributes'],
        )

    def test_get_link_values_by_time_and_attributes(self):
        """
        Test the output get link values by time and attributes function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        link_values = swmm_output.get_link_values_by_time_and_attribute(
            time_index=10,
            attribute=output.LinkAttribute.FLOW_RATE.value
        )

        TestSWMMOutput.assert_dict_almost_equal(
            link_values,
            self.test_artifacts['test_get_link_values_by_time_and_attributes'],
        )

    def test_get_system_values_by_time_and_attributes(self):
        """
        Test the output get system values by time and attributes function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        system_values = swmm_output.get_system_values_by_time_and_attribute(
            time_index=12,
            attribute=output.SystemAttribute.RUNOFF_FLOW.value
        )

        TestSWMMOutput.assert_dict_almost_equal(
            system_values,
            self.test_artifacts['test_get_system_values_by_time_and_attributes'],
        )

    def test_get_subcatchment_values_by_time_and_index(self):
        """
        Test the output get subcatchment values by time and index function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        subcatchment_values = swmm_output.get_subcatchment_values_by_time_and_element_index(
            time_index=5,
            element_index=3
        )

        TestSWMMOutput.assert_dict_almost_equal(
            subcatchment_values,
            self.test_artifacts['test_get_subcatchment_values_by_time_and_index'],
        )

    def test_get_node_values_by_time_and_index(self):
        """
        Test the output get node values by time and index function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        node_values = swmm_output.get_node_values_by_time_and_element_index(
            time_index=8,
            element_index=4
        )

        TestSWMMOutput.assert_dict_almost_equal(
            node_values,
            self.test_artifacts['test_get_node_values_by_time_and_index'],
        )

    def test_get_link_values_by_time_and_index(self):
        """
        Test the output get link values by time and index function
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        link_values = swmm_output.get_link_values_by_time_and_element_index(
            time_index=10,
            element_index=5
        )

        TestSWMMOutput.assert_dict_almost_equal(
            link_values,
            self.test_artifacts['test_get_link_values_by_time_and_index'],
        )

    def test_get_system_values_by_time(self):
        """
        Test the output get system values by time
        :return:
        """
        swmm_output = Output(example_output_data.EXAMPLE_OUTPUT_FILE_1)
        system_values = swmm_output.get_system_values_by_time(time_index=12)

        TestSWMMOutput.assert_dict_almost_equal(
            system_values,
            self.test_artifacts['test_get_system_values_by_time']
        )

    @staticmethod
    def assert_dict_almost_equal(d1: dict, d2: dict, rtol: float = 1e-5, atol: float = 1e-8):
        """
        Assert that two dictionaries are almost equal
        :param rtol:
        :param d1: First dictionary
        :param d2: Second dictionary
        :return:
        """
        """Assert that two dictionaries are almost equal (with tolerance)."""

        assert set(d1.keys()) == set(d2.keys())  # Check if keys are the same

        for key in d1.keys():
            value1 = d1[key]
            value2 = d2[key]

            if isinstance(value1, dict):
                # If the values are dictionaries, recursively compare them
                TestSWMMOutput.assert_dict_almost_equal(value1, value2, rtol, atol)
            elif isinstance(value1, float):
                # If the values are floats, compare them with tolerance
                assert abs(value1 - value2) <= atol + rtol * abs(value2)
            else:
                # Otherwise, compare them directly
                assert value1 == value2
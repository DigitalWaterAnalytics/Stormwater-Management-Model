# Description: Cython module for epaswmm solver
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# cython: language_level=3

# python and cython imports
from enum import Enum
from typing import List, Tuple, Union, Optional, Dict, Set
from cpython.datetime cimport datetime, timedelta
from libc.stdlib cimport free, malloc

# external imports

# local python and cython imports
# from epaswmm.array import Array1d
cimport epaswmm.solver.solver as solver
cimport epaswmm.epaswmm as cepaswmm
# cython: language_level=3

from epaswmm.solver.solver cimport (
    swmm_Object,
    swmm_NodeType,
    swmm_LinkType,
    swmm_GageProperty,
    swmm_SubcatchProperty,
    swmm_NodeProperty,
    swmm_LinkProperty,
    swmm_SystemProperty,
    swmm_FlowUnitsProperty,
    swmm_API_Errors,
    swmm_run,
    swmm_open,
    swmm_start,
    swmm_step,
    swmm_stride,
    swmm_useHotStart,
    swmm_saveHotStart,
    swmm_end,
    swmm_report,
    swmm_close,
    swmm_getMassBalErr,
    swmm_getVersion,
    swmm_getError,
    swmm_getErrorFromCode,
    swmm_getWarnings,
    swmm_getCount,
    swmm_getName,
    swmm_getIndex,
    swmm_getValue,
    swmm_setValue,
    swmm_getSavedValue,
    swmm_writeLine,
    swmm_decodeDate
)

class SWMMObjects(Enum):
    """
    Enumeration of SWMM objects.

    :ivar SUBCATCH: Subcatchment object
    :type SUBCATCH: int 
    :ivar NODE: Node object
    :type NODE: int
    :ivar LINK: Link object
    :type LINK: int
    :ivar AQUIFER: Aquifer object
    :type AQUIFER: int
    :ivar SNOWPACK: Snowpack object
    :type SNOWPACK: int
    :ivar UNIT_HYDROGRAPH: Unit hydrograph object
    :type UNIT_HYDROGRAPH: int
    :ivar LID: LID object
    :type LID: int
    :ivar STREET: Street object
    :type STREET: int
    :ivar INLET: Inlet object
    :type INLET: int
    :ivar TRANSECT: Transect object
    :type TRANSECT: int
    :ivar XSECTION_SHAPE: Cross-section shape object
    :type XSECTION_SHAPE: int
    :ivar CONTROL_RULE: Control rule object
    :type CONTROL_RULE: int
    :ivar POLLUTANT: Pollutant object
    :type POLLUTANT: int
    :ivar LANDUSE: Land use object
    :type LANDUSE: int
    :ivar CURVE: Curve object
    :type CURVE: int
    :ivar TIMESERIES: Time series object
    :type TIMESERIES: int
    :ivar TIME_PATTERN: Time pattern object
    :type TIME_PATTERN: int
    :ivar SYSTEM: System object
    :type SYSTEM: int
    """
    RAIN_GAGE = swmm_Object.swmm_GAGE
    SUBCATCH = swmm_Object.swmm_SUBCATCH 
    NODE = swmm_Object.swmm_NODE
    LINK = swmm_Object.swmm_LINK
    AQUIFER = swmm_Object.swmm_AQUIFER
    SNOWPACK = swmm_Object.swmm_SNOWPACK
    UNIT_HYDROGRAPH = swmm_Object.swmm_UNIT_HYDROGRAPH
    LID = swmm_Object.swmm_LID
    STREET = swmm_Object.swmm_STREET
    INLET = swmm_Object.swmm_INLET
    TRANSECT = swmm_Object.swmm_TRANSECT
    XSECTION_SHAPE = swmm_Object.smmm_XSECTION_SHAPE
    CONTROL_RULE = swmm_Object.swmm_CONTROL_RULE
    POLLUTANT = swmm_Object.swmm_POLLUTANT
    LANDUSE = swmm_Object.swmm_LANDUSE
    CURVE = swmm_Object.swmm_CURVE
    TIMESERIES = swmm_Object.swmm_TIMESERIES
    TIME_PATTERN = swmm_Object.swmm_TIME_PATTERN
    SYSTEM = swmm_Object.swmm_SYSTEM

class SWMMNodeTypes(Enum):
    """
    Enumeration of SWMM node types.

    :ivar JUNCTION: Junction node
    :type JUNCTION: int
    :ivar OUTFALL: Outfall node
    :type OUTFALL: int
    :ivar STORAGE: Storage node
    :type STORAGE: int
    :ivar DIVIDER: Divider node
    :type DIVIDER: int
    """
    JUNCTION = swmm_NodeType.swmm_JUNCTION
    OUTFALL = swmm_NodeType.swmm_OUTFALL
    STORAGE = swmm_NodeType.swmm_STORAGE
    DIVIDER = swmm_NodeType.swmm_DIVIDER

class SWMMRainGageProperties(Enum):
    """
    Enumeration of SWMM raingage properties.

    :ivar GAGE_TOTAL_PRECIPITATION: Total precipitation
    :type GAGE_TOTAL_PRECIPITATION: int
    :ivar GAGE_SNOW_DEPTH: Snow depth
    :type GAGE_SNOW_DEPTH: int
    :ivar GAGE_SNOWFALL: Snowfall
    :type GAGE_SNOWFALL: int
    """
    GAGE_TOTAL_PRECIPITATION = swmm_GageProperty.swmm_GAGE_TOTAL_PRECIPITATION # Total precipitation
    GAGE_RAINFALL = swmm_GageProperty.swmm_GAGE_RAINFALL # Rainfall
    GAGE_SNOWFALL = swmm_GageProperty.swmm_GAGE_SNOWFALL # Snowfall
    
class SWMMSubcatchmentProperties(Enum):
    """
    Enumeration of SWMM subcatchment properties.

    :ivar AREA: Area
    :type AREA: int
    :ivar RAINGAGE: Raingage
    :type RAINGAGE: int
    :ivar RAINFALL: Rainfall
    :type RAINFALL: int
    :ivar EVAPORATION: Evaporation
    :type EVAPORATION: int
    :ivar INFILTRATION: Infiltration
    :type INFILTRATION: int
    :ivar RUNOFF: Runoff
    :type RUNOFF: int
    :ivar REPORT_FLAG: Report flag
    :type REPORT_FLAG: int
    :ivar POLLUTANT_BUILDUP: Pollutant buildup
    :type POLLUTANT_BUILDUP: int
    :ivar POLLUTANT_PONDED_CONCENTRATION: Pollutant ponded concentration
    :type POLLUTANT_PONDED_CONCENTRATION: int
    :ivar POLLUTANT_TOTAL_LOAD: Pollutant total load
    :type POLLUTANT_TOTAL_LOAD: int
    """
    AREA = swmm_SubcatchProperty.swmm_SUBCATCH_AREA
    RAINGAGE = swmm_SubcatchProperty.swmm_SUBCATCH_RAINGAGE
    RAINFALL = swmm_SubcatchProperty.swmm_SUBCATCH_RAINFALL
    EVAPORATION = swmm_SubcatchProperty.swmm_SUBCATCH_EVAP
    INFILTRATION = swmm_SubcatchProperty.swmm_SUBCATCH_INFIL
    RUNOFF = swmm_SubcatchProperty.swmm_SUBCATCH_RUNOFF
    REPORT_FLAG = swmm_SubcatchProperty.swmm_SUBCATCH_RPTFLAG
    POLLUTANT_BUILDUP = swmm_SubcatchProperty.swmm_SUBCATCH_POLLUTANT_BUILDUP # Pollutant buildup
    POLLUTANT_PONDED_CONCENTRATION = swmm_SubcatchProperty.swmm_SUBCATCH_POLLUTANT_PONDED_CONCENTRATION # Pollutant ponded concentration
    POLLUTANT_RUNOFF_CONCENTRATION = swmm_SubcatchProperty.swmm_SUBCATCH_POLLUTANT_TOTAL_LOAD # Pollutant total load

class SWMMNodeProperties(Enum):
    """
    Enumeration of SWMM node properties.

    :ivar TYPE: Node type
    :type TYPE: int
    :ivar ELEVATION: Elevation
    :type ELEVATION: int
    :ivar MAX_DEPTH: Maximum depth
    :type MAX_DEPTH: int
    :ivar DEPTH: Depth
    :type DEPTH: int
    :ivar HYDRAULIC_HEAD: Hydraulic head
    :type HYDRAULIC_HEAD: int
    :ivar VOLUME: Volume
    :type VOLUME: int
    :ivar LATERAL_INFLOW: Lateral inflow
    :type LATERAL_INFLOW: int
    :ivar TOTAL_INFLOW: Total inflow
    :type TOTAL_INFLOW: int
    :ivar FLOODING: Flooding
    :type FLOODING: int
    :ivar REPORT_FLAG: Report flag
    :type REPORT_FLAG: int
    """
    TYPE = swmm_NodeProperty.swmm_NODE_TYPE
    ELEVATION = swmm_NodeProperty.swmm_NODE_ELEV
    MAX_DEPTH = swmm_NodeProperty.swmm_NODE_MAXDEPTH
    DEPTH = swmm_NodeProperty.swmm_NODE_DEPTH
    HYDRAULIC_HEAD = swmm_NodeProperty.swmm_NODE_HEAD
    VOLUME = swmm_NodeProperty.swmm_NODE_VOLUME
    LATERAL_INFLOW = swmm_NodeProperty.swmm_NODE_LATFLOW
    TOTAL_INFLOW = swmm_NodeProperty.swmm_NODE_INFLOW
    FLOODING = swmm_NodeProperty.swmm_NODE_OVERFLOW
    REPORT_FLAG = swmm_NodeProperty.swmm_NODE_RPTFLAG
    POLLUTANT_CONCENTRATION = swmm_NodeProperty.swmm_NODE_POLLUTANT_CONCENTRATION # Pollutant concentration
    POLLUTANT_INFLOW_CONCENTRATION = swmm_NodeProperty.swmm_NODE_POLLUTANT_INFLOW_CONCENTRATION # Pollutant inflow concentration

class SWMMLinkProperties(Enum):
    """
    Enumeration of SWMM link properties.

    :ivar TYPE: Link type
    :type TYPE: int
    :ivar OFFSET1: Offset 1
    :type OFFSET1: int
    :ivar OFFSET2: Offset 2
    :type OFFSET2: int
    :ivar DIAMETER: Diameter
    :type DIAMETER: int
    :ivar LENGTH: Length
    :type LENGTH: int
    :ivar ROUGHNESS: Roughness
    :type ROUGHNESS: int
    :ivar INLET_HEIGHT: Inlet height
    :type INLET_HEIGHT: int
    :ivar OUTLET_HEIGHT: Outlet height
    :type OUTLET_HEIGHT: int
    :ivar INIT_FLOW: Initial flow
    :type INIT_FLOW: int
    :ivar FLOW_LIMIT: Flow limit
    :type FLOW_LIMIT: int
    :ivar REPORT_FLAG: Report flag
    :type REPORT_FLAG: int
    """
    TYPE = swmm_LinkProperty.swmm_LINK_TYPE
    START_NODE = swmm_LinkProperty.swmm_LINK_NODE1
    END_NODE = swmm_LinkProperty.swmm_LINK_NODE2
    LENGTH = swmm_LinkProperty.swmm_LINK_LENGTH
    SLOPE = swmm_LinkProperty.swmm_LINK_SLOPE
    FULL_DEPTH = swmm_LinkProperty.swmm_LINK_FULLDEPTH
    FULL_FLOW = swmm_LinkProperty.swmm_LINK_FULLFLOW
    SETTING = swmm_LinkProperty.swmm_LINK_SETTING
    TIME_OPEN = swmm_LinkProperty.swmm_LINK_TIMEOPEN
    TIME_CLOSED = swmm_LinkProperty.swmm_LINK_TIMECLOSED
    FLOW = swmm_LinkProperty.swmm_LINK_FLOW
    DEPTH = swmm_LinkProperty.swmm_LINK_DEPTH
    VELOCITY = swmm_LinkProperty.swmm_LINK_VELOCITY
    TOP_WIDTH = swmm_LinkProperty.swmm_LINK_TOPWIDTH
    REPORT_FLAG = swmm_LinkProperty.swmm_LINK_RPTFLAG
    POLLUTANT_CONCENTRATION = swmm_LinkProperty.swmm_LINK_POLLUTANT_CONCENTRATION  # Pollutant concentration
    POLLUTANT_LOAD = swmm_LinkProperty.swmm_LINK_POLLUTANT_LOAD # Pollutant load

class SWMMSystemProperties(Enum):
    """
    Enumeration of SWMM system properties.
    """
    START_DATE = swmm_SystemProperty.swmm_STARTDATE
    CURRENT_DATE = swmm_SystemProperty.swmm_CURRENTDATE
    ELAPSED_TIME = swmm_SystemProperty.swmm_ELAPSEDTIME
    ROUTING_STEP = swmm_SystemProperty.swmm_ROUTESTEP
    MAX_ROUTING_STEP = swmm_SystemProperty.swmm_MAXROUTESTEP
    REPORT_STEP = swmm_SystemProperty.swmm_REPORTSTEP
    TOTAL_STEPS = swmm_SystemProperty.swmm_TOTALSTEPS
    NO_REPORT_FLAG = swmm_SystemProperty.swmm_NOREPORT
    FLOW_UNITS = swmm_SystemProperty.swmm_FLOWUNITS
    END_DATE = swmm_SystemProperty.swmm_ENDDATE
    REPORT_START_DATE = swmm_SystemProperty.swmm_REPORTSTART
    UNIT_SYSTEM = swmm_SystemProperty.swmm_UNITSYSTEM
    SURCHARGE_METHOD = swmm_SystemProperty.swmm_SURCHARGEMETHOD
    ALLOW_PONDING = swmm_SystemProperty.swmm_ALLOWPONDING
    INTERTIAL_DAMPING = swmm_SystemProperty.swmm_INERTIADAMPING
    NORMAL_FLOW_LIMITED = swmm_SystemProperty.swmm_NORMALFLOWLTD
    SKIP_STEADY_STATE = swmm_SystemProperty.swmm_SKIPSTEADYSTATE
    IGNORE_RAINFALL = swmm_SystemProperty.swmm_IGNORERAINFALL
    IGNORE_RDII = swmm_SystemProperty.swmm_IGNORERDII
    IGNORE_SNOWMELT = swmm_SystemProperty.swmm_IGNORESNOWMELT
    IGNORE_GROUNDWATER = swmm_SystemProperty.swmm_IGNOREGWATER
    IGNORE_ROUTING = swmm_SystemProperty.swmm_IGNOREROUTING
    IGNORE_QUALITY = swmm_SystemProperty.swmm_IGNOREQUALITY
    RULE_STEP = swmm_SystemProperty.swmm_RULESTEP
    SWEEP_START = swmm_SystemProperty.swmm_SWEEPSTART
    SWEEP_END = swmm_SystemProperty.swmm_SWEEPEND
    MAX_TRIALS = swmm_SystemProperty.swmm_MAXTRIALS
    NUM_THREADS = swmm_SystemProperty.swmm_NUMTHREADS
    MIN_ROUTE_STEP = swmm_SystemProperty.swmm_MINROUTESTEP
    LENGTHENING_STEP = swmm_SystemProperty.swmm_LENGTHENINGSTEP
    START_DRY_DAYS = swmm_SystemProperty.swmm_STARTDRYDAYS
    COURANT_FACTOR = swmm_SystemProperty.swmm_COURANTFACTOR
    MIN_SURF_AREA = swmm_SystemProperty.swmm_MINSURFAREA
    MIN_SLOPE = swmm_SystemProperty.swmm_MINSLOPE
    RUNOFF_ERROR = swmm_SystemProperty.swmm_RUNOFFERROR
    FLOW_ERROR = swmm_SystemProperty.swmm_FLOWERROR
    QUAL_ERROR = swmm_SystemProperty.swmm_QUALERROR
    HEAD_TOL = swmm_SystemProperty.swmm_HEADTOL
    SYS_FLOW_TOL = swmm_SystemProperty.swmm_SYSFLOWTOL
    LAT_FLOW_TOL = swmm_SystemProperty.swmm_LATFLOWTOL

class SWMMFlowUnits(Enum):
    """
    Enumeration of SWMM flow units.

    :ivar CFS: Cubic feet per second
    :type CFS: int
    :ivar GPM: Gallons per minute
    :type GPM: int
    :ivar MGD: Million gallons per day
    :type MGD: int
    :ivar CMS: Cubic meters per second
    :type CMS: int
    :ivar LPS: Liters per second
    :type LPS: int
    :ivar MLD: Million liters per day
    :type MLD: int
    """
    CFS = swmm_FlowUnitsProperty.swmm_CFS
    GPM = swmm_FlowUnitsProperty.swmm_GPM
    MGD = swmm_FlowUnitsProperty.swmm_MGD
    CMS = swmm_FlowUnitsProperty.swmm_CMS
    LPS = swmm_FlowUnitsProperty.swmm_LPS
    MLD = swmm_FlowUnitsProperty.swmm_MLD

class SWMMAPIErrors(Enum):
    """
    Enumeration of SWMM API errors.

    :ivar PROJECT_NOT_OPENED: Project not opened
    :type PROJECT_NOT_OPENED: int
    :ivar SIMULATION_NOT_STARTED: Simulation not started
    :type SIMULATION_NOT_STARTED: int
    :ivar SIMULATION_NOT_ENDED: Simulation not ended
    :type SIMULATION_NOT_ENDED: int    
    """
    PROJECT_NOT_OPENED = swmm_API_Errors.ERR_API_NOT_OPEN          # API not open
    SIMULATION_NOT_STARTED = swmm_API_Errors.ERR_API_NOT_STARTED       # API not started
    SIMULATION_NOT_ENDED = swmm_API_Errors.ERR_API_NOT_ENDED         # API not ended
    OBJECT_TYPE = swmm_API_Errors.ERR_API_OBJECT_TYPE       # Invalid object type
    OBJECT_INDEX = swmm_API_Errors.ERR_API_OBJECT_INDEX      # Invalid object index
    OBJECT_NAME = swmm_API_Errors.ERR_API_OBJECT_NAME       # Invalid object name
    PROPERTY_TYPE = swmm_API_Errors.ERR_API_PROPERTY_TYPE     # Invalid property type
    PROPERTY_VALUE = swmm_API_Errors.ERR_API_PROPERTY_VALUE    # Invalid property value
    TIME_PERIOD = swmm_API_Errors.ERR_API_TIME_PERIOD       # Invalid time period
    HOTSTART_FILE_OPEN = swmm_API_Errors.ERR_API_HOTSTART_FILE_OPEN # Error opening hotstart file
    HOTSTART_FILE_FORMAT = swmm_API_Errors.ERR_API_HOTSTART_FILE_FORMAT # Invalid hotstart file format

cpdef int run_solver(str inp_file, str rpt_file, str out_file):
    """
    Run a SWMM simulation.
    
    :param inp_file: Input file name
    :param rpt_file: Report file name
    :param out_file: Output file name
    :return: Error code (0 if successful)
    """
    cdef int error_code = 0
    cdef bytes c_inp_file_bytes = inp_file.encode('utf-8')

    if rpt_file is not None:
       rpt_file = inp_file.replace('.inp', '.rpt')
    
    if out_file is not None:
         out_file = inp_file.replace('.inp', '.out')

    cdef bytes c_rpt_file_bytes = rpt_file.encode('utf-8')
    cdef bytes c_out_file_bytes = out_file.encode('utf-8')

    cdef const char* c_inp_file = c_inp_file_bytes
    cdef const char* c_rpt_file = c_rpt_file_bytes
    cdef const char* c_out_file = c_out_file_bytes

    error_code = swmm_open(c_inp_file, c_rpt_file, c_out_file)

    if error_code != 0:
        raise Exception(f'Run failed with message: {get_error_message(error_code)}')

    return error_code

cpdef datetime decode_swmm_datetime(double swmm_datetime):
    """
    Decode a SWMM datetime into a datetime object.
    
    :param swmm_datetime: SWMM datetime float value
    :type swmm_datetime: float
    :return: datetime object
    :rtype: datetime
    """
    cdef int year, month, day, hour, minute, second, day_of_week
    swmm_decodeDate(swmm_datetime, &year, &month, &day, &hour, &minute, &second, &day_of_week)

    return datetime(year, month, day, hour, minute, second)

cpdef int version():
    """
    Get the SWMM version.
    
    :return: SWMM version
    :rtype: str
    """
    cdef int swmm_version = swmm_getVersion()

    return swmm_version

cpdef str get_error_message(int error_code):
    """
    Get the error message for a SWMM error code.
    
    :param error_code: Error code
    :type error_code: int
    :return: Error message
    :rtype: str
    """
    cdef char* c_error_message = <char*>malloc(1024*sizeof(char))
    
    swmm_getErrorFromCode(error_code, &c_error_message)

    error_message = c_error_message.decode('utf-8')

    free(c_error_message)

    return error_message

class SolverState(Enum):
    """
    An enumeration to represent the state of the solver.
    """
    CREATED = 0 
    OPEN = 1
    STARTED = 2
    FINISHED = 3
    ENDED = 4
    REPORTED = 5
    CLOSED = 6

class CallbackType(Enum):
    """
    An enumeration to represent the type of callback.
    """
    BEFORE_INITIALIZE = 0
    BEFORE_OPEN = 1
    AFTER_OPEN = 2
    BEFORE_START = 3
    AFTER_START = 4
    BEFORE_STEP = 5
    AFTER_STEP = 6
    BEFORE_END = 7
    AFTER_END = 8
    BEFORE_REPORT = 9
    AFTER_REPORT = 10
    BEFORE_CLOSE = 11
    AFTER_CLOSE = 12

cdef class Solver:
    """
    A class to represent a SWMM solver.
    """
    cdef str _inp_file
    cdef str _rpt_file
    cdef str _out_file
    cdef bint _save_results
    cdef int _stride_step
    cdef list _before_initialize_callbacks
    cdef list _before_open_callbacks
    cdef list _after_open_callbacks
    cdef list _before_start_callbacks
    cdef list _after_start_callbacks
    cdef list _before_step_callbacks
    cdef list _before_end_callbacks
    cdef list _after_end_callbacks
    cdef list _before_report_callbacks
    cdef list _after_report_callbacks
    cdef list _before_close_callbacks
    cdef list _after_close_callbacks

    def __cinit__(self, str inp_file, str rpt_file, str out_file, bint save_results=True):
        """
        Constructor to create a new SWMM solver.

        :param inp_file: Input file name
        :param rpt_file: Report file name
        :param out_file: Output file name
        """
        self._save_results = save_results
        self._inp_file = inp_file

        if rpt_file is not None:
            self._rpt_file = rpt_file
        else:
            self._rpt_file = inp_file.replace('.inp', '.rpt')

        if out_file is not None:
            self._out_file = out_file
        else:
            self._out_file = inp_file.replace('.inp', '.out')

        self._solver_state = SolverState.CREATED

    def __enter__(self):
        """
        Enter method for context manager.
        """
        if (
            (self._solver_state != SolverState.CREATED) or 
            (self._solver_state != SolverState.CLOSED)
            ):
            raise Exception('')
        else:
            self.initialize()
        
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit method for context manager.
        """
        self.__close()

    def __close(self):
        """
        Close the solver.
        """
        pass

    def __dealloc__(self):
        """
        Destructor to free the solver.
        """
        pass

    def __iter__(self):
        """
        Iterator method for the solver.
        """
        return self
    
    def __next__(self):
        """
        Next method for the solver.
        """
        pass

    @property
    def start_date(self) -> datetime:
        """
        Get the start date of the simulation.
        
        :return: Start date
        :rtype: datetime
        """
        pass

    @property
    def end_date(self) -> datetime:
        """
        Get the end date of the simulation.
        
        :return: End date
        :rtype: datetime
        """
        pass
    
    @property
    def current_date(self) -> datetime:
        """
        Get the current date of the simulation.
        
        :return: Current date
        :rtype: datetime
        """
        pass
    
    @property
    def stride_step(self) -> int:
        """
        Get the stride step of the simulation.
        
        :return: Stride step
        :rtype: int
        """
        pass

    @stride_step.setter
    def stride_step(self, value: int):
        """
        Set the stride time step of the simulation.
        
        :param value: Stride step in seconds
        :type value: int
        """
        pass

    def __validate_error(self, error_code: int) -> None:
        """
        Validate the error code and raise an exception if it is not 0.
        
        :param error_code: Error code to validate
        :type error_code: int
        """
        if error_code != 0:
            raise Exception(f'Run failed with message: {self.__get_error()}')
    
    def status(self) -> SolverState:
        """
        Get the status of the solver.
        
        :return: Solver state
        :rtype: SolverState
        """
        pass

    cpdef str __get_error(self):
        """
        Get the error code from the solver.
        
        :return: Error code
        :rtype: int
        """
        cdef char* c_error_message = <char*>malloc(1024*sizeof(char))
        swmm_getError(c_error_message, 1024)

        error_message = c_error_message.decode('utf-8')

        free(c_error_message)

        return error_message

    def __initialize(self) -> int:
        """
        Open a SWMM input file.
        
        :param inp_file: Input file name
        :param rpt_file: Report file name
        :param out_file: Output file name
        :return: Error code (0 if successful)
        """
        cdef error_code = 0

        cdef bytes c_inp_file_bytes = self._inp_file.encode('utf-8')
        cdef bytes c_rpt_file_bytes = self._rpt_file.encode('utf-8')
        cdef bytes c_out_file_bytes = self._out_file.encode('utf-8')

        cdef const char* c_inp_file = c_inp_file_bytes
        cdef const char* c_rpt_file = c_rpt_file_bytes
        cdef const char* c_out_file = c_out_file_bytes

        error_code = swmm_open(c_inp_file, c_rpt_file, c_out_file)
        self.__validate_error(error_code)

    def __finalize(self) -> int:
        """
        Close a SWMM input file.
        
        :return: Error code (0 if successful)
        """
        cdef error_code = 0

        error_code = swmm_close()
        self.__validate_error(error_code)

    def __start(self, save_hotstart: bool) -> int:
        """
        Start a SWMM simulation.
        
        :param save_hotstart: Flag to save hotstart file
        :return: Error code (0 if successful)
        """
        pass

    def step(self) -> datetime:
        """
        Step a SWMM simulation.
        
        :return: Error code (0 if successful)
        """
        pass 

    def step_stride(self, stride: int) -> int:
        """
        Stride a SWMM simulation.
        
        :param stride: Number of steps to stride
        :return: Error code (0 if successful)
        """
        pass

    def use_hotstart(self, hotstart_file: str) -> int:
        """
        Use a hotstart file.
        
        :param hotstart_file: Hotstart file name
        :return: Error code (0 if successful)
        """
        pass
    
    def save_hotstart(self, hotstart_file: str) -> int:
        """
        Save a hotstart file.
        
        :param hotstart_file: Hotstart file name
        :return: Error code (0 if successful)
        """
        pass
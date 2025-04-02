"""
Helper functions to parse the parameters used for loads and sources
"""
from altdss import altdss
from altdss import Load, PVSystem, Generator
from pygridsim.enums import LoadType, SourceType, GeneratorType
from pygridsim.configs import LOAD_CONFIGURATIONS, SOURCE_CONFIGURATIONS, GENERATOR_CONFIGURATIONS
import pygridsim.defaults as defaults
import random

def _get_enum_obj(enum_class, enum_val):
    enum_obj = None
    enum_val_lower = enum_val.lower().replace(" ", "")
    for enum_type in enum_class:
        if (enum_type.value == enum_val_lower):
            enum_obj = enum_type
    if not enum_obj:
        raise KeyError("invalid enum input")

    return enum_obj

def _random_param(range):
    """
    Given the range of a normal parameter (i.e. normal load for a house), uniformly select value.
    In case the value is not a range and just a value, just return that value

    Args:
        [lower_bound, upper_bound]; range of typical value
    Return:
        Randomly selected value in range
    """
    if type(range) is not list:
        return range

    [max, min] = range
    return random.random() * (max - min) + min

def _get_param(params, name, default):
    """
    Get param or use default
    """
    if name in params:
        return params[name]
    else:
        return default

def _check_valid_params(params, valid_params):
    # Invalid parameter handling
    for key in params:
        if key not in valid_params:
            raise KeyError(f"Parameter {key} is not supported")
        if not isinstance(params[key], (int, float)):
            raise TypeError("Parameter input should be int or float")
        if key in ["kV", "BasekV"] and params[key] < 0:
            raise ValueError("KV cannot be less than 0")

def _make_load_node(load_params, load_type, count):
    """
    Make a load node with the parmeters given, filling in with defaults for
    any undefined but required parameter. Parse through the parameters, potentially throwing errors and warnings if
    one of the parameter names is invalid.

    Args:
        load_params: any specified parameters to override default ones
        load_type: LoadType representing type of load, house, commercial, industrial
        count: how many loads have already been made, to not use repeat names
    Return:
        load object
    """
    _check_valid_params(load_params, defaults.VALID_LOAD_PARAMS)
    load_type_obj = _get_enum_obj(LoadType, load_type)

    load : Load = altdss.Load.new('load' + str(count))
    load.Bus1 = 'load' + str(count)
    load.Phases =_get_param(load_params, "phases", defaults.PHASES)
    for attr in ["kV", "kW", "kvar"]:
        load_type_param = LOAD_CONFIGURATIONS[load_type_obj][attr]
        setattr(load, attr, _get_param(load_params, attr, _random_param(load_type_param)))

    load.Daily = 'default'
    return load

def _make_source_node(source_params, source_type):
    """
    Make a source node with the parmeters given, filling in with defaults for
    any undefined but required parameter. Parse through the parameters, potentially throwing errors and warnings if
    one of the parameter names is invalid. Note that this updates the source node if one already exists

    Args:
        source_params: any specified parameters to override default ones
    Return:
        source object
    """
    _check_valid_params(source_params, defaults.VALID_SOURCE_PARAMS)
    source_type_obj = _get_enum_obj(SourceType, source_type)

    source = altdss.Vsource[0]
    source.Bus1 = 'source'
    source.Phases = _get_param(source_params, "phases", defaults.PHASES)
    source_type_param = SOURCE_CONFIGURATIONS[source_type_obj]["kV"]
    source.BasekV = _get_param(source_params, "kV", _random_param(source_type_param))
    source.Frequency = _get_param(source_params, "frequency", defaults.FREQUENCY)

    for imp in defaults.IMPEDANCE_PARAMS:
        setattr(source, imp, _get_param(source_params, imp, defaults.IMPEDANCE))

    return source

def _make_pv(load_node, params, num_panels, count):
    """
    Make a PV at the load node given, scaling kV by the number of solar panels

    Args:
        load_node: which load to add PVsystem to
        params: any customized parameters
        num_panels: representation of how many solar panels this PVsystem includes
        count: how many pv already made, to not run into duplicates
    """
    _check_valid_params(params, defaults.VALID_PV_PARAMS)
    pv : PVSystem = altdss.PVSystem.new('pv' + str(count))
    pv.Bus1 = load_node
    pv.Phases = _get_param(params, "phases", defaults.PHASES)
    pv.kV = _get_param(params, "kV", _random_param(defaults.SOLAR_PANEL_BASE_KV) * num_panels)

def _make_generator(params, gen_type, count):
    """
    Make a generator in the circuit

    Args:
        params: any customized parameters
        gen_type: type of generator (small, large, industrial) in string
        count: how many generators already made, to not run into duplicates
    """
    _check_valid_params(params, defaults.VALID_GENERATOR_PARAMS)
    gen_type_obj = _get_enum_obj(GeneratorType, gen_type)

    generator : Generator = altdss.Generator.new('generator' + str(count))
    generator.Bus1 = 'generator' + str(count)
    generator.Phases = _get_param(params, "phases", defaults.PHASES)
    for attr in ["kV", "kW"]:
        gen_type_param = GENERATOR_CONFIGURATIONS[gen_type_obj][attr]
        setattr(generator, attr, _get_param(params, attr, _random_param(gen_type_param)))
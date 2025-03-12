"""
Helper functions to parse the parameters used for loads and sources
"""
from altdss import altdss
from altdss import AltDSS, Transformer, Vsource, Load, LoadModel, LoadShape
import pygridsim.defaults as defaults
import random

def random_param(range):
    """
    Given the range of a normal parameter (i.e. normal load for a house), uniformly select value.
    In case the value is not a range and just a value, just return that value

    Args:
        [lower_bound, upper_bound]; range of typical value
    Return:
        Randomly selected value in range
    TODO: allow for non-uniform distributions
    """
    if type(range) is not list:
        return range
    [max, min] = range
    return random.random() * (max - min) + min

def get_param(params, name, default):
    """
    Get param or use default
    """
    if name in params:
        return params[name]
    else:
        return default

def check_valid_params(params, valid_params):
    # Invalid parameter handling
    for param in params:
        if param not in valid_params:
            raise KeyError(f"Parameter {param} is not supported")

def make_load_node(load_params, load_type, count):
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
    check_valid_params(load_params, defaults.VALID_LOAD_PARAMS)

    load : Load = altdss.Load.new('load' + str(count))
    load.Bus1 = 'load' + str(count)
    load.Phases = get_param(load_params, "phases", defaults.PHASES)
    for attr in ["kV", "kW", "kvar"]:
        setattr(load, attr, get_param(load_params, attr, random_param(load_type.value[attr])))
    load.Daily = 'default'

    if (load.kV) < 0:
        raise ValueError("Cannot have negative voltage in load")
    return load

def make_source_node(source_params, source_type):
    """
    Make a source node with the parmeters given, filling in with defaults for
    any undefined but required parameter. Parse through the parameters, potentially throwing errors and warnings if
    one of the parameter names is invalid. Note that this updates the source node if one already exists

    Args:
        source_params: any specified parameters to override default ones
    Return:
        source object
    """
    check_valid_params(source_params, defaults.VALID_SOURCE_PARAMS)

    source = altdss.Vsource[0]
    source.Bus1 = 'source'
    source.Phases = get_param(source_params, "phases", defaults.PHASES)
    source.BasekV = get_param(source_params, "kV", random_param(source_type.value))
    source.Frequency = get_param(source_params, "frequency", defaults.FREQUENCY)

    for imp in ["R0", "R1", "X0", "X1"]:
        setattr(source, imp, get_param(source_params, imp, defaults.IMPEDANCE))

    if (source.BasekV) < 0:
        raise ValueError("Cannot have negative voltage in source")

    return source
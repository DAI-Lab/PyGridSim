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
    load : Load = altdss.Load.new('load' + str(count))
    load.Bus1 = 'load' + str(count)
    load.Phases = get_param(load_params, "phases", defaults.PHASES)
    load.kV = get_param(load_params, "kV", random_param(load_type.value["kV"]))
    load.kW = get_param(load_params, "kW", random_param(load_type.value["kW"]))
    load.kvar = get_param(load_params, "kVar", random_param(load_type.value["kVar"]))
    load.Daily = 'default'
    return load

def make_source_node(source_params, source_type, count, num_in_batch = 1):
    """
    Make a source node with the parmeters given, filling in with defaults for
    any undefined but required parameter. Parse through the parameters, potentially throwing errors and warnings if
    one of the parameter names is invalid.

    Args:
        source_params: any specified parameters to override default ones
        count: how many sources have already been made, to not use repeat names
        num_in_batch: how many to batch into this same source. note this only causes a scaled kV
        TODO: num, once we get the transformer thing working
    Return:
        source object
    
    TODO: There is a whole set of other vsource properties to set, like impedance and resistance
    https://github.com/dss-extensions/AltDSS-Python/blob/2b6fa7e5961cedaf8482c07d377b20bdab4a1bee/altdss/Vsource.py#L694
    """
    source = altdss.Vsource[0]
    #source = altdss.Vsource['source' + str(count)]
    #source: Vsource = altdss.Vsource.new('source' + str(count))
    source.Bus1 = 'source'
    source.Phases = get_param(source_params, "phases", defaults.PHASES)
    source.BasekV = get_param(source_params, "kV", num_in_batch*random_param(source_type.value))
    source.Frequency = get_param(source_params, "frequency", defaults.FREQUENCY)
    return source
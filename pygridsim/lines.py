from altdss import altdss
import defaults
from parameters import random_param, get_param
from dss.enums import LineUnits

def make_line(src, dst, line_type, count, params = {}):
    """
    Add a line between src and dst

    Args:
        src: where line starts (node)
        dst: where line end (node)
        params (optional): any non-default parameters to use TODO
    Returns:
        Line object that was created
    """
    line = altdss.Line.new('line' + str(count))
    line.Phases = defaults.PHASES
    line.Length = get_param(params, "length", random_param(line_type.value)) 
    line.Bus1 = src
    line.Bus2 = dst
    line.Units = LineUnits.km

"""
TODO:
- make_line is the most natural place to add transformers
- could define parser as a helper of make line (i.e. make line takes in the numbers, not nodes)
"""
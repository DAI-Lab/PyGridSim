from altdss import altdss
from altdss import Transformer, Connection
import pygridsim.defaults as defaults
from pygridsim.parameters import get_param, random_param
from dss.enums import LineUnits

def make_line(src, dst, line_type, count, params = {}, transformer = True):
    """
    Add a line between src and dst

    Args:
        src: where line starts (node)
        dst: where line end (node)
        params (optional): any non-default parameters to use. Params can also include transformer params like XHL, Conns
    Returns:
        Line object that was created
    """
    line = altdss.Line.new('line' + str(count))
    line.Phases = defaults.PHASES
    line.Length = get_param(params, "length", random_param(line_type.value)) 
    line.Bus1 = src
    line.Bus2 = dst
    line.Units = LineUnits.km

    if not transformer:
        return

    # automatically add transformer to every line
    transformer: Transformer = altdss.Transformer.new('transformer' + str(count))
    transformer.Phases = defaults.PHASES
    transformer.Windings = defaults.NUM_WINDINGS
    transformer.XHL = get_param(params, "XHL", defaults.XHL) 
    transformer.Buses = [src, dst]
    transformer.Conns = get_param(params, "Conns", [defaults.PRIMARY_CONN, defaults.SECONDARY_CONN])
    transformer.kVs = [altdss.Vsource[src].BasekV, altdss.Load[dst].kV] 
    transformer.end_edit()
from altdss import altdss
from altdss import Transformer, Connection
import pygridsim.defaults as defaults
from pygridsim.parameters import get_param, random_param, check_valid_params
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
    check_valid_params(params, defaults.VALID_LINE_TRANSFORMER_PARAMS)
    line = altdss.Line.new('line' + str(count))
    line.Phases = defaults.PHASES
    line.Length = get_param(params, "length", random_param(line_type.value)) 
    line.Bus1 = src
    line.Bus2 = dst
    line.Units = LineUnits.km

    if (line.Length) < 0:
        raise ValueError("Cannot have negative length")

    if not transformer:
        return

    # automatically add transformer to every line
    transformer: Transformer = altdss.Transformer.new('transformer' + str(count))
    transformer.Phases = defaults.PHASES
    transformer.Windings = defaults.NUM_WINDINGS
    transformer.XHL = get_param(params, "XHL", defaults.XHL) 
    transformer.Buses = [src, dst]
    transformer.Conns = get_param(params, "Conns", [defaults.PRIMARY_CONN, defaults.SECONDARY_CONN])
    # TOOD: edit this for clarity
    if src == "source":
        transformer.kVs = [altdss.Vsource[src].BasekV, altdss.Load[dst].kV] 
    else:
        transformer.kVs = [altdss.Generator[src].kV, altdss.Load[dst].kV] 
    transformer.end_edit()

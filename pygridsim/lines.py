from altdss import altdss
from altdss import Transformer
from pygridsim.configs import LINE_CONFIGURATIONS
import pygridsim.defaults as defaults
from pygridsim.enums import LineType
from pygridsim.parameters import get_param, random_param, check_valid_params, get_enum_obj
from dss.enums import LineUnits

def get_kv(node_name):
    """
    Given a string of a node that exists, fetch its kV or raise error if doesn't exist
    """
    if node_name == "source":
        return altdss.Vsource[node_name].BasekV
    elif "load" in node_name:
        return altdss.Load[node_name].kV
    elif "generator" in node_name:
        return altdss.Generator[node_name].kV
    else:
        raise KeyError("Invalid src or dst name")

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
    line_type_obj = get_enum_obj(LineType, line_type)
    line = altdss.Line.new('line' + str(count))
    line.Phases = defaults.PHASES
    line.Length = get_param(params, "length", random_param(LINE_CONFIGURATIONS[line_type_obj]["length"])) 
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

    transformer.kVs = [get_kv(src), get_kv(dst)]

    transformer.end_edit()

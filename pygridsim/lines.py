from altdss import Transformer, altdss
from dss.enums import LineUnits

import pygridsim.defaults as defaults
from pygridsim.configs import LINE_CONFIGURATIONS
from pygridsim.enums import LineType
from pygridsim.parameters import _check_valid_params, _get_enum_obj, _get_param, _random_param


def _get_kv(node_name):
    if node_name == "source" and node_name in altdss.Vsource:
        return altdss.Vsource[node_name].BasekV
    elif "load" in node_name and node_name in altdss.Load:
        return altdss.Load[node_name].kV
    elif "generator" in node_name and node_name in altdss.Generator:
        return altdss.Generator[node_name].kV
    else:
        raise KeyError("Invalid src or dst name")


def _make_line(src, dst, line_type, count, params={}, transformer=True):
    _check_valid_params(params, defaults.VALID_LINE_TRANSFORMER_PARAMS)
    line_type_obj = _get_enum_obj(LineType, line_type)
    line = altdss.Line.new('line' + str(count))
    line.Phases = defaults.PHASES
    rand_length = _random_param(LINE_CONFIGURATIONS[line_type_obj]["length"])
    line.Length = _get_param(params, "length", rand_length)
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
    transformer.XHL = _get_param(params, "XHL", defaults.XHL)
    transformer.Buses = [src, dst]
    transformer.Conns = [defaults.PRIMARY_CONN, defaults.SECONDARY_CONN]
    transformer.kVs = [_get_kv(src), _get_kv(dst)]

    transformer.end_edit()

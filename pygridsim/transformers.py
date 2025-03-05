from altdss import altdss
from altdss import Transformer, Connection
import pygridsim.defaults as defaults
from pygridsim.parameters import get_param, random_param

def make_transformer(src, dst, count, params):
    """
    Add a Transformer between src and dst

    Args:
        src: where line starts (source node)
        dst: where line end (load node)
        count: number of transformers so far
        params (optional): any non-default parameters to use.
    Returns:
        Transformer object that was created

    TODO:
    - used some of this logic in the line code, if we keep it there then delete this file
    """
    transformer: Transformer = altdss.Transformer.new('transformer' + str(count))
    transformer.Phases = defaults.PHASES
    transformer.Windings = defaults.NUM_WINDINGS
    transformer.XHL = get_param(params, "XHL", defaults.XHL) 
    transformer.Buses = [src, dst]
    transformer.Conns = get_param(params, "Conns", [defaults.PRIMARY_CONN, defaults.SECONDARY_CONN])
    transformer.kVs = [altdss.Vsource[src].BasekV, altdss.Load[dst].kV] 
    transformer.end_edit()
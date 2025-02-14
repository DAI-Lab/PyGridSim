from altdss import altdss
from altdss import Transformer, Connection
import defaults
from parameters import random_param, get_param

def make_transformer(src, dst, count, params):
    """
    Add a Transformer between src and dst

    Args:
        src: where line starts (source node) TODO: just 1 for now
        dst: where line end (load node)
        count: nnumber of transformers so far
        params (optional): any non-default parameters to use TODO
    Returns:
        Transformer object that was created
    """
    # taken from altdss python package
    transformer: Transformer = altdss.Transformer.new('transformer' + str(count))
    transformer.Phases = 3
    transformer.Windings = 2
    transformer.XHL = 8 / 1000
    transformer.Buses = [src, dst]
    transformer.Conns = [Connection.delta, Connection.wye]
    transformer.kVs = [altdss.Vsource[src].BasekV, altdss.Load[dst].kV] 
    #transformer.kVAs = [5000, 5000]
    #transformer.pctRs = [0.5 / 1000, 0.5 / 1000]
    transformer.end_edit()
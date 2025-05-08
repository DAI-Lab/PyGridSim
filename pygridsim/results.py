"""
Defines the set of allowed queries (i.e. baseKV at every node) and
provides helpers for the solve/results function.
"""
import json

from altdss import altdss


def _query_solution(query, name_to_nickname):
    match query:
        case "Voltages":
            bus_vmags = {}
            for bus_name, bus_vmag in zip(altdss.BusNames(), altdss.BusVMag()):
                return_name = bus_name
                if bus_name in name_to_nickname:
                    nickname = name_to_nickname[bus_name]
                    return_name += "/" + nickname
                bus_vmags[return_name] = float(bus_vmag)
            return bus_vmags
        case "Losses":
            vector_losses = altdss.Losses()
            losses = {}
            losses["Active Power Loss"] = vector_losses.real
            losses["Reactive Power Loss"] = vector_losses.imag
            return losses
        case "TotalPower":
            return altdss.TotalPower()
        case _:
            return "Invalid"


def _export_results(results, path):
    with open(path, "w") as json_file:
        json.dump(results, json_file, indent=4)

"""
Defines the set of allowed queries (i.e. baseKV at every node) and
provides helpers for the solve/results function.
"""
import json

from altdss import altdss


def _query_solution(query):
    query_fix = query.lower().replace(" ", "")
    vector_losses = altdss.Losses()
    vector_power = altdss.TotalPower()
    match query_fix:
        case "voltages":
            bus_vmags = {}
            for bus_name, bus_vmag in zip(altdss.BusNames(), altdss.BusVMag()):
                bus_vmags[bus_name] = float(bus_vmag)
            return bus_vmags
        case "losses" | "loss":
            losses = {}
            losses["Active Power Loss"] = vector_losses.real
            losses["Reactive Power Loss"] = vector_losses.imag
            return losses
        case "totalpower" | "power":
            power = {}
            power["Active Power"] = vector_power.real
            power["Reactive Power"] = vector_power.imag
            return power
        case "activeloss" | "activepowerloss" | "realloss" | "realpowerloss":
            return vector_losses.real
        case "reactiveloss" | "reactivepowerloss":
            return vector_losses.imag
        case "activepower" | "realpower":
            return vector_power.real
        case "reactivepower":
            return vector_power.imag
        case _:
            return "Invalid"


def _export_results(results, path):
    with open(path, "w") as json_file:
        json.dump(results, json_file, indent=4)

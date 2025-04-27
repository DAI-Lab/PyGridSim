<p align="left">
<img width=15% src="https://dai.lids.mit.edu/wp-content/uploads/2018/06/Logo_DAI_highres.png" alt=“DAI-Lab” />
<i>An open source project from Data to AI Lab at MIT.</i>
</p>

<!-- Uncomment these lines after releasing the package to PyPI for version and downloads badges -->
[![Development Status](https://img.shields.io/badge/Development%20Status-2%20--%20Pre--Alpha-yellow)](https://pypi.org/search/?c=Development+Status+%3A%3A+2+-+Pre-Alpha)
[![PyPI Shield](https://img.shields.io/pypi/v/pygridsim.svg)](https://pypi.python.org/pypi/pygridsim)
[![Downloads](https://pepy.tech/badge/pygridsim)](https://pepy.tech/project/pygridsim)
[![Run Tests](https://github.com/DAI-Lab/PyGridSim/actions/workflows/tests.yml/badge.svg)](https://github.com/DAI-Lab/PyGridSim/actions/workflows/tests.yml)
[![Github Actions Shield](https://img.shields.io/github/workflow/status/amzhao/PyGridSim/Run%20Tests)](https://github.com/amzhao/PyGridSim/actions)
[![Coverage Status](https://codecov.io/gh/amzhao/PyGridSim/branch/master/graph/badge.svg)](https://codecov.io/gh/amzhao/PyGridSim)



# PyGridSim

PyGridSim is a package for simulating OpenDSS circuits. PyGridSim uses a functional interface to allow users to efficiently generate circuits of various scopes.

- Documentation: https://dtail.gitbook.io/pygridsim
- Homepage: https://dai.lids.mit.edu/

# Overview

PyGridSim allows users to create and customize circuits. Users can either fully specify each component they add to the circuit, or lean on library-provided parameter sets. PyGridSim supports the batch creation of every circuit component, emphasizing scalability and efficiently in building large circuits.

# Installation

## Requirements

**PyGridSim** has been developed and tested on [Python 3.10, 3.11 and 3.12](https://www.python.org/downloads/)

Also, although it is not strictly required, the usage of a [virtualenv](https://virtualenv.pypa.io/en/latest/)
is highly recommended in order to avoid interfering with other software installed in the system
in which **PyGridSim** is run.

These are the minimum commands needed to create a virtualenv using python3.10 for **PyGridSim**:

```bash
pip install virtualenv
virtualenv -p $(which python3.10) PyGridSim-venv
```

Afterwards, you have to execute this command to activate the virtualenv:

```bash
source PyGridSim-venv/bin/activate
```

Remember to execute it every time you start a new console to work on **PyGridSim**!

<!-- Uncomment this section after releasing the package to PyPI for installation instructions
## Install from PyPI

After creating the virtualenv and activating it, we recommend using
[pip](https://pip.pypa.io/en/stable/) in order to install **PyGridSim**:

```bash
pip install pygridsim
```

This will pull and install the latest stable release from [PyPI](https://pypi.org/).
-->

## Install from source

With your virtualenv activated, you can clone the repository and install it from
source by running `make install` on the `stable` branch:

```bash
git clone git@github.com:amzhao/PyGridSim.git
cd PyGridSim
git checkout stable
make install
```

# Quick Start
Users of PyGridSim have the option between creating a fully customized circuit and using PyGridSim-provided parameters to build their circuit. Consider the simplest circuit: one source, one load, and a line connecting them. The following code snippet demonstrates how to model and print results on this circuit on PyGridSim with both methods.

## Customized Circuit Creation
```python
circuit = PyGridSim()

# Add Custom Source and Load
circuit.add_load_nodes(params={"kV": 0.12, "kW": 1, "kvar": 1})
circuit.update_source(params={"kV": 0.5})

# Add Line
circuit.add_lines([("source", "load0")], params={"length": 1})

# Solve and Print Results
circuit.solve()
print(circuit.results(["Voltages", "Losses"]))
circuit.clear()
```

## Defaults-Based Circuit Creation
```python
circuit = PyGridSim()

# Add Custom Source and Load
circuit.add_load_nodes(load_type="house")
circuit.update_source(source_type="turbine")

# Add Line
circuit.add_lines([("source", "load0")], line_type="lv")

# Solve and Print Results
circuit.solve()
print(circuit.results(["Voltages", "Losses"]))
circuit.clear()
```

# Resources

For more details about **PyGridSim** and all its possibilities
and features, please check the [Gitbook page for PyGridSim](https://dtail.gitbook.io/pygridsim)

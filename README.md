<p align="left">
<img width=15% src="https://dai.lids.mit.edu/wp-content/uploads/2018/06/Logo_DAI_highres.png" alt=“DAI-Lab” />
<i>An open source project from Data to AI Lab at MIT.</i>
</p>

<!-- Uncomment these lines after releasing the package to PyPI for version and downloads badges -->
<!--[![PyPI Shield](https://img.shields.io/pypi/v/pygridsim.svg)](https://pypi.python.org/pypi/pygridsim)-->
<!--[![Downloads](https://pepy.tech/badge/pygridsim)](https://pepy.tech/project/pygridsim)-->
[![Github Actions Shield](https://img.shields.io/github/workflow/status/amzhao/PyGridSim/Run%20Tests)](https://github.com/amzhao/PyGridSim/actions)
[![Coverage Status](https://codecov.io/gh/amzhao/PyGridSim/branch/master/graph/badge.svg)](https://codecov.io/gh/amzhao/PyGridSim)



# PyGridSim

PyGridSim is a package with the goal of simulating OpenDSS circuits on Python. PyGridSim uses a functional interface to allow users to efficiently generate circuits of various scopes.

- Documentation: https://amzhao.github.io/PyGridSim
- Homepage: https://github.com/amzhao/PyGridSim

# Overview

PyGridSim allows user to create circuits with the amount of customization they desire. Thus, users can either fully specify each component they add to the circuit, or lean on library-provided parameter sets. PyGridSim supports the batch creation of every circuit component, emphasizing scalability and efficiently in building large circuits.

# Install

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

# What's next?

For more details about **PyGridSim** and all its possibilities
and features, please check the [documentation site](
TODO: gitbool link).

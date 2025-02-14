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

Package to simulate OpenDSS circuits on Python.

NOTE: README comes from dai cookie cutter, will be updated
NOTE: will be moved to Dai lab repository

- Documentation: https://amzhao.github.io/PyGridSim
- Homepage: https://github.com/amzhao/PyGridSim

# Overview

PyGridSim aims to provide accessible access to tools like OpenDSS, AltDSS using Python. The goal is to create large-scale electrical circuits representing residential neighborhoods (and other scenarios) using an intuitive interface, without any background in OpenDSS software.

# Install

## Requirements

**PyGridSim** has been developed and tested on [Python 3.5, 3.6, 3.7 and 3.8](https://www.python.org/downloads/)

Also, although it is not strictly required, the usage of a [virtualenv](https://virtualenv.pypa.io/en/latest/)
is highly recommended in order to avoid interfering with other software installed in the system
in which **PyGridSim** is run.

These are the minimum commands needed to create a virtualenv using python3.6 for **PyGridSim**:

```bash
pip install virtualenv
virtualenv -p $(which python3.6) PyGridSim-venv
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

## Install for Development

If you want to contribute to the project, a few more steps are required to make the project ready
for development.

Please head to the [Contributing Guide](https://amzhao.github.io/PyGridSim/contributing.html#get-started)
for more details about this process.

# Quickstart

In this short tutorial we will guide you through a series of steps that will help you
getting started with **PyGridSim**.

TODO: Create a step by step guide here. Also figure out how to ensure prerequisites properly.

# What's next?

For more details about **PyGridSim** and all its possibilities
and features, please check the [documentation site](
https://amzhao.github.io/PyGridSim/).

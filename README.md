![GitHub](https://img.shields.io/github/license/thiagoneye/project-particulate_transport_simulator)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/thiagoneye/project-particulate_transport_simulator)

# project-particulate_transport_simulator

Simulator for analysis of availability and projection of production in an environment for the production of slabs from particulates, considering the equipment:

- Mills (source of particulate production).
- Silos (particulate intermediate storage area).
- Transport System (set of piping, threads and geared motors, for particulate transport).
- Scale (particulate intermediate storage area).
- Production Lines (particulate processing station for item/plate).

The structure of the manufacturing environment can be seen (illustratively) in the flowchart below.


<img src="others/flowchart.png" width="800px">


The physical principle used to build the tool is to carry out the mass balance along the equipment sets.

## Purpose

Serve as a decision-making tool, considering critical scenarios in the production environment.

## Files

### ./inputs/

The only input is the [dataset.xlsx](https://github.com/thiagoneye/project-particulate_transport_simulator/blob/main/inputs/dataset.xlsx) file, it is divided into spreadsheets containing the main parameters for each equipment.

For each equipment, new lines can be added freely so that new items of that equipment are added, considering only the following restrictions:

- Each silo must be associated with an existing mill, this is possible through the supply parameter.
- Each scale must be associated with a single and respective production line, this is possible through the ID parameter present in each equipment.

### ./outputs/

The first output is the [availability.xlsx](https://github.com/thiagoneye/project-particulate_transport_simulator/blob/main/outputs/availability.xlsx) file, which contains the lost availability and produced item values for each production line.

The second output is the [historic.xlsx](https://github.com/thiagoneye/project-particulate_transport_simulator/blob/main/outputs/historic.xlsx) file, which contains the level value of each equipment for each instant of time.

## Scripts

### main.py

The [main.py](https://github.com/thiagoneye/project-particulate_transport_simulator/blob/main/main.py) script is the one the tool runs on. It reads the input parameters, initializes the equipment, builds the boundary conditions and exports the results. Also, it is possible to determine the simulation time (one week of production, for example) and the time variation in each iteration, in lines 27 and 28.

### preprocessing.py

The [preprocessing.py](https://github.com/thiagoneye/project-particulate_transport_simulator/blob/main/preprocessing.py) script is the one that contains the exported class for reading and pre-processing the input parameters.

### equipments.py

The [equipments.py](https://github.com/thiagoneye/project-particulate_transport_simulator/blob/main/equipments.py) script is the one that contains the exported classes for building the equipment. For each equipment a series of properties and actions are determined.

## Observations

Some particularities that should not be neglected:

- The transport system only supplies one scale at a time.
- When the system switches the scale to supply, a "reversal" time is required, this time can (and should) be changed in the main.py file, on line 74.

## Authorship

The particulate transport simulator was developed by [Thiago Rodrigues](https://github.com/thiagoneye/).

![GitHub](https://img.shields.io/github/license/thiagoneye/project-particulate_transport_simulator)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/thiagoneye/project-particulate_transport_simulator)

# project-particulate_transport_simulator

Simulator for analysis of availability and projection of production in an environment for the production of slabs from particulates, considering the equipment:

- Mills (source of particulate production)
- Silos (particulate intermediate storage area)
- Transport System (set of piping, threads and geared motors, for particulate transport)
- Production Lines (particulate processing station for item/plate)

The physical principle used to build the tool is to carry out the mass balance along the equipment sets.

## Purpose

Serve as a decision-making tool, considering critical scenarios in the production environment.

## Authorship

The particulate transport simulator was developed by [Thiago Rodrigues](https://github.com/thiagoneye/).

## Files

### ./inputs/

The only input is the [dataset.xlsx](https://github.com/thiagoneye/project-particulate_transport_simulator/blob/main/inputs/dataset.xlsx) file, it is divided into spreadsheets containing the main parameters for each equipment.

For each equipment, new lines can be added freely so that new items of that equipment are added, considering only the following restrictions:

- Each silo must be associated with an existing mill, this is possible through the supply parameter.
- Each scale must be associated with a single and respective production line, this is possible through the ID parameter present in each equipment.

### ./outputs/

## Scripts

### preprocessing.py

### equipments.py

### main.py

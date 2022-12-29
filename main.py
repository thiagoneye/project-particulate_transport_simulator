"""
Oxide Plant Simulator
"""

# Paths

PATH = '.\\outputs\\'


# Imports

import numpy as np
import pandas as pd
from preprocessing import PreProcessing
from equipments import (
    Silo,
    TransportSystem,
    Scale,
    ProductionLine
    )


# Simulation Time

idx = 0

time = 6*3*8
dtime = 0.005
time_line = np.around(np.arange(0, time, dtime), decimals=5)

number_of_elements = len(time_line)

# Pre-allocation of Variables

silos = dict()
transport_system = None
scales = dict()
production_lines = dict()

silo_filling = dict()

queue_empty_silos = dict()
queue_partially_empty_silos = dict()
queue_silos = list()
queue_scales = list()

# Preprocessing

data = PreProcessing()

for system in data.equipments.keys():
    for equipment in data.equipments[system]:
        if system == 'silos':
            silo_idx = data.silos_indeces[equipment]
            mill = data.silos['Supply'][silo_idx]
            mill_idx = data.mills_indeces[mill]

            initial_level = None
            initial_level = data.silos['Initial Volume'][silo_idx]

            max_level = None
            max_level = data.silos['Maximum Volume'][silo_idx]

            min_level = None
            min_level = data.silos['Minimum Volume'][silo_idx]

            variation = dict()
            variation['filling'] = data.mills['Output Flow'][mill_idx]
            variation['distributing'] = -data.silos['Output Flow'][silo_idx]

            silos[equipment] = Silo(dtime, number_of_elements, initial_level, max_level, min_level, variation)

        elif system == 'TS':
            transport_system = TransportSystem(dtime, reversal_time=0.01)

        elif system == 'scales':
            scale_idx = data.scales_indeces[equipment]

            initial_level = None
            initial_level = data.scales['Initial Volume'][scale_idx]

            max_level = None
            max_level = data.scales['Maximum Volume'][scale_idx]

            variation = dict()
            variation['filling'] = data.silos['Output Flow'][0]

            scales[equipment] = Scale(dtime, number_of_elements, initial_level, max_level, variation)
        elif system == 'lines':
            line_idx = data.lines_indeces[equipment]

            initial_level = None
            initial_level = 0

            max_level = None
            max_level = data.lines['Maximum Volume'][line_idx]

            variation = None
            variation = -data.lines['Output Flow'][line_idx]

            plate_mass = data.lines['Plate Average Mass'][line_idx]

            production_lines[equipment] = ProductionLine(dtime, number_of_elements, initial_level, max_level, variation, plate_mass)

for mill in data.silos_supply['Supply'].unique():
    queue_empty_silos[mill] = list()
    queue_partially_empty_silos[mill] = list()

# Simulation

for t in time_line:
    for system in data.equipments.keys():
        if system == 'silos':

            # Dynamics of Filling

            silo_filling = list()

            for mill in data.silos_supply['Supply'].unique():
                silos_idx = (data.silos_supply['Supply'] == mill).values
                status = np.array([value.status for value in silos.values()])

                empty_silos = np.array(data.equipments['silos'])[np.logical_and(status == 'empty', silos_idx)]
                partially_empty_silos = np.array(data.equipments['silos'])[np.logical_and(status == 'partially empty', silos_idx)]

                for silo in empty_silos:
                    if silo not in queue_empty_silos[mill]:
                        queue_empty_silos[mill].append(silo)

                for silo in partially_empty_silos:
                    if silo not in queue_partially_empty_silos[mill] and silo not in queue_empty_silos[mill]:
                        queue_partially_empty_silos[mill].append(silo)

                if len(queue_empty_silos[mill]) > 0:
                    silo = queue_empty_silos[mill][0]
                    silos[silo].filling_check(idx)
                    silos[silo].check_status(idx)
                    silo_filling.append(silo)

                    if silos[silo].status == 'full':
                        queue_empty_silos[mill].remove(silo)
                elif len(queue_partially_empty_silos[mill]) > 0:
                    silo = queue_partially_empty_silos[mill][0]
                    silos[silo].filling_check(idx)
                    silos[silo].check_status(idx)
                    silo_filling.append(silo)

                    if silos[silo].status == 'full':
                        queue_partially_empty_silos[mill].remove(silo)

            # Dynamics of Rest

            for silo in data.equipments['silos']:
                if silo not in silo_filling:
                    silos[silo].equipment_at_rest(idx)
                    silos[silo].check_status(idx)

        elif system == 'TS':

            silos_status = np.array([value.status for value in silos.values()])
            non_empty_silos = np.array(data.equipments['silos'])[silos_status != 'empty']

            scales_status = np.array([value.status for value in scales.values()])
            empty_scales = np.array(data.equipments['scales'])[scales_status == 'empty']

            for silo in non_empty_silos:
                if silo not in queue_silos:
                    queue_silos.append(silo)

            for scale in empty_scales:
                if scale not in queue_scales:
                    queue_scales.append(scale)

            if transport_system.status == 'stopped':
                if len(queue_silos) > 0 and len(queue_scales) > 0:
                    transport_system.start_reversal()
            elif transport_system.status == 'reversal':
                transport_system.reversal_time_check()
            elif transport_system.status == 'distributing':
                silo = queue_silos[0]
                silos[silo].distribution_check(idx)

                scale = queue_scales[0]
                scales[scale].filling_check(idx)

                if silos[silo].status == 'empty':
                    queue_silos.remove(silo)

                if scales[scale].status == 'full':
                    transport_system.stop_process()
                    queue_scales.remove(scale)

                if len(queue_silos) == 0 or len(queue_scales) == 0:
                    transport_system.stop_process()

            if transport_system.status != 'stopped':
                transport_system.continue_process()

        elif system == 'scales':

            # Dynamics of Production

            scales_status = np.array([value.status for value in scales.values()])
            full_scales = scales_status == 'full'

            lines_status = np.array([value.status for value in production_lines.values()])
            empty_lines = lines_status == 'stopped'

            lines = np.array(data.equipments['lines'])[np.logical_and(full_scales, empty_lines)]

            for line in lines:
                scales[line].reset_level(idx)
                scales[line].check_status(idx)

                production_lines[line].restart_level(idx)
                production_lines[line].start_production()

            # Dynamics of Rest

            status = np.array([value.status for value in scales.values()])
            level = np.array([value.level[idx] for value in scales.values()])

            scales_at_rest = np.array(data.equipments['scales'])[np.logical_and(level == 0, status != 'empty')]

            for scale in scales_at_rest:
                scales[scale].equipment_at_rest(idx)

            # Check Status

            for scale in data.equipments['scales']:
                scales[scale].check_status(idx)

        elif system == 'lines':

            lines_status = np.array([value.status for value in production_lines.values()])
            lines = np.array(data.equipments['lines'])[lines_status == 'production']

            for line in lines:
                production_lines[line].production_check(idx)

            lines = np.array(data.equipments['lines'])[lines_status == 'stopped']

            for line in lines:
                production_lines[line].idle_time()

    idx += 1

# Export Results - Historic

df1 = pd.DataFrame()
df1['timeline'] = time_line

for equipment in data.equipments['silos']:
    df1['silo-' + equipment] = silos[equipment].level

for equipment in data.equipments['scales']:
    df1['scale-' + equipment] = scales[equipment].level

for equipment in data.equipments['lines']:
    df1['line-' + equipment] = production_lines[equipment].level

df1.to_excel(PATH + 'historic.xlsx', index=False)

# Export Results - Availability

df2 = list()

for line in data.equipments['lines']:
    loss = production_lines[line].loss
    plate_production = production_lines[line].plate_production
    
    df2.append([line, loss, plate_production])

df2 = pd.DataFrame(data=df2, columns=['id', 'loss', 'production'])
df2.to_excel(PATH + 'availability.xlsx', index=False)

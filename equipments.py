"""
Oxide Plant Simulator
"""

# Imports

import numpy as np


# Classes

class FeedingDynamics:
    def __init__(self, dtime, number_of_elements, initial_level, max_level, variation):
        self.status = ''
        self.max_level = max_level
        self.variation = variation
        self.time_variation = dtime

        self.level = np.zeros(number_of_elements)
        self.level[0] = initial_level

    def full_level(self):
        self.status = 'full'

    def empty_level(self):
        self.status = 'empty'

    def equipment_at_rest(self, idx):
        if idx == 0:
            current_level = self.level[idx]
        else:
            current_level = self.level[idx-1]

        self.level[idx] = current_level

    def new_level_increment(self, status, idx):
        if idx == 0 or self.level[idx] != 0:
            current_level = self.level[idx]
        else:
            current_level = self.level[idx-1]

        level_increment = self.variation[status]*self.time_variation
        new_level = current_level + level_increment

        self.level[idx] = new_level

    def filling_check(self, idx):
        if idx == 0 or self.level[idx] != 0:
            current_level = self.level[idx]
        else:
            current_level = self.level[idx-1]

        level_increment = self.variation['filling']*self.time_variation
        new_level = current_level + level_increment

        if new_level > self.max_level:
            self.full_level()
            self.level[idx] = self.max_level
        else:
            self.new_level_increment('filling', idx)


class Silo(FeedingDynamics):
    def __init__(self, dtime, number_of_elements, initial_level, max_level, min_level, variation):
        super().__init__(dtime, number_of_elements, initial_level, max_level, variation)

        self.min_level = min_level

        self.check_status(0)

    def partially_empty_level(self):
        self.status = 'partially empty'

    def distribution_check(self, idx):
        if idx == 0 or self.level[idx] != 0:
            current_level = self.level[idx]
        else:
            current_level = self.level[idx-1]

        level_increment = self.variation['distributing']*self.time_variation
        new_level = current_level + level_increment

        if new_level < self.min_level:
            self.empty_level()
            self.level[idx] = self.min_level
        else:
            self.new_level_increment('distributing', idx)
            self.partially_empty_level()

    def check_status(self, idx):
        last_level = self.level[idx]

        if last_level >= self.max_level:
            self.full_level()
        elif last_level <= self.min_level:
            self.empty_level()
        else:
            self.partially_empty_level()


class TransportSystem:
    def __init__(self, dtime, reversal_time=0.01):
        self.status = 'stopped'
        self.time = 0
        self.variation = dtime
        self.reversal_time = reversal_time

    def restart_time(self):
        self.time = 0

    def stop_process(self):
        self.status = 'stopped'
        self.restart_time()

    def start_reversal(self):
        self.status = 'reversal'
        self.restart_time()

    def continue_process(self):
        self.time += self.variation

    def reversal_time_check(self):
        if self.time + self.variation > self.reversal_time:
            self.status = 'distributing'
            self.restart_time()


class Scale(FeedingDynamics):
    def __init__(self, dtime, number_of_elements, initial_level, max_level, variation):
        super().__init__(dtime, number_of_elements, initial_level, max_level, variation)

        self.min_level = 0

        self.check_status(0)

    def reset_level(self, idx):
        self.level[idx] = self.min_level

    def check_status(self, idx):
        last_level = self.level[idx]

        if last_level >= self.max_level:
            self.full_level()
        else:
            self.empty_level()


class ProductionLine:
    def __init__(self, dtime, number_of_elements, initial_level, max_level, variation, plate_mass):
        self.status = ''
        self.max_level = max_level
        self.variation = variation
        self.time_variation = dtime
        self.plate_mass = plate_mass
        self.plate_production = 0
        self.loss = 0

        self.level = np.zeros(number_of_elements)
        self.level[0] = initial_level

        self.check_status(0)

    def restart_level(self, idx):
        self.level[idx] = self.max_level

    def stop_process(self):
        self.status = 'stopped'

    def start_production(self):
        self.status = 'production'

    def production_check(self, idx):
        if idx == 0 or self.level[idx] == self.max_level:
            current_level = self.level[idx]
        else:
            current_level = self.level[idx-1]

        level_increment = self.variation*self.time_variation
        new_level = current_level + level_increment

        if new_level <= 0:
            self.stop_process()
            self.level[idx] = 0
        else:
            self.level[idx] = new_level
            self.plate_production -= level_increment/self.plate_mass

    def check_status(self, idx):
        current_level = self.level[idx]

        if current_level == self.max_level:
            self.start_production()
        elif current_level <= 0:
            self.stop_process()
            self.level[idx] = 0

    def idle_time(self):
        self.loss += self.time_variation

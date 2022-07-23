from collections import deque
from copy import deepcopy

PARTICLES_HISTORY_DEPTH = 60


class Simulation:
    def __init__(self):
        self.particles_history = deque([{}])
        # for assigning unique ids to particles to keep track of them through time
        self.particle_id_counter = 0
        self.center_of_mass = [0, 0]

    def add_particle(self, particle):
        current_particles = self.get_current_timestep_particles()
        current_particles[self.particle_id_counter] = particle
        self.particle_id_counter += 1

    def get_particles_history(self):
        return self.particles_history

    def get_current_timestep_particles(self):
        return self.particles_history[-1]

    def advance(self, integrator, timestep):
        # make a copy of particles for this new timestep to keep the history intact
        copy_of_particles = deepcopy(self.get_current_timestep_particles())
        self.particles_history.append(copy_of_particles)

        # only keep a certain amount of past snapshots in memory
        if len(self.particles_history) > PARTICLES_HISTORY_DEPTH:
            self.particles_history.popleft()

        integrator.integrate(copy_of_particles, timestep)
        self.update_center_of_mass()
    
    def update_center_of_mass(self):
        # calculate a weighted average on each axis
        mass_sum = 0
        position_sum = [0, 0]
        for particle in self.get_current_timestep_particles().values():
            mass_sum += particle.mass
            position_sum[0] += particle.position[0] * particle.mass
            position_sum[1] += particle.position[1] * particle.mass
        
        self.center_of_mass = [position_sum[0] / mass_sum, position_sum[1] / mass_sum]

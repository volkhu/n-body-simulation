class Euler:
    def __init__(self, force_calculator):
        self.force_calculator = force_calculator

    def integrate(self, simulation, timestep):
        for particle in simulation.particles:
            particle.acceleration = self.force_calculator.get_acceleration(
                particle, simulation.particles)

            particle.velocity[0] += particle.acceleration[0] * timestep
            particle.velocity[1] += particle.acceleration[1] * timestep

            particle.position[0] += particle.velocity[0] * timestep
            particle.position[1] += particle.velocity[1] * timestep

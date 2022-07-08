import math

# If the distance between particles gets too low, gravitational force
# becomes too high and the simulation starts behaving erratically. This
# damping factor effectively adds a minimum distance that can be used
# in force calculations and thus prevents this problem.
MIN_DISTANCE = 5


class AllPairs:
    def __init__(self, gravitational_constant):
        self.gravitational_constant = gravitational_constant

    # calculate how much is this particle being pulled by every
    # other one and sum the values together to get a final result
    def get_acceleration(self, particle, particles):
        acceleration_sum = [0, 0]

        for other in particles.values():
            if particle == other:
                continue

            position_difference = [other.position[0] - particle.position[0],
                                   other.position[1] - particle.position[1]]

            distance = math.sqrt(
                position_difference[0] * position_difference[0] + position_difference[1] * position_difference[1] + MIN_DISTANCE * MIN_DISTANCE)

            force = self.gravitational_constant * \
                (particle.mass * other.mass) / math.pow(distance, 2)

            direction_unit_vector = [position_difference[0] /
                                     distance, position_difference[1] / distance]

            acceleration = force / particle.mass
            acceleration_sum[0] += acceleration * direction_unit_vector[0]
            acceleration_sum[1] += acceleration * direction_unit_vector[1]

        return acceleration_sum

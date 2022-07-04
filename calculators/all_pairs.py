import math


class AllPairs:
    def __init__(self, gravitational_constant):
        self.gravitational_constant = gravitational_constant

    # calculate acceleration for a specified particle taking all others into consideration
    def get_acceleration(self, p, particles):
        acceleration_sum = [0, 0]

        for p2 in particles:
            if p == p2:
                continue

            difference = [p2.position[0] - p.position[0],
                          p2.position[1] - p.position[1]]
            softening = 5
            distance = math.sqrt(
                difference[0] * difference[0] + difference[1] * difference[1] + softening * softening)
            force = self.gravitational_constant * \
                (p.mass * p2.mass) / math.pow(distance, 2)
            acceleration = force / p.mass
            unit_vector = [difference[0] / distance, difference[1] / distance]

            acceleration_sum[0] += acceleration * unit_vector[0]
            acceleration_sum[1] += acceleration * unit_vector[1]

        return acceleration_sum

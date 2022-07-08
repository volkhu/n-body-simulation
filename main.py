import pygame

from display import Display
from controller import Controller
from models.camera import Camera
from models.particle import Particle
from models.simulation import Simulation
from integrators.euler import Euler
from calculators.all_pairs import AllPairs

WINDOW_TITLE = "nsim"
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
WINDOW_REFRESH_RATE = 60
SIMULATION_TIMESTEP = 1.0
GRAVITATIONAL_CONSTANT = 10


def main():
    # create a viewport, camera and user input controller
    display = Display(WINDOW_WIDTH, WINDOW_HEIGHT)
    camera = Camera(display.get_default_camera_position())
    controller = Controller()

    # create simulation with 2 test particles orbiting each other
    simulation = Simulation()
    simulation.add_particle(Particle([0, 0], [0, 0], 100))
    simulation.add_particle(Particle([-200, 0], [0, -2.3], 10))

    # set up a simulation solver
    force_calculator = AllPairs(GRAVITATIONAL_CONSTANT)
    integrator = Euler(force_calculator)

    # main loop
    clock = pygame.time.Clock()
    while not controller.exit_requested:
        controller.handle_input(camera, simulation)
        simulation.advance(integrator, SIMULATION_TIMESTEP)
        display.render(simulation, camera)

        # wait for the next frame
        frame_time = clock.tick(WINDOW_REFRESH_RATE)
        pygame.display.set_caption(
            WINDOW_TITLE + " - " + str(frame_time) + " ms frame time")


if __name__ == "__main__":
    main()

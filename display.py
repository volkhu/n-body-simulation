import math
import pygame
from pygame import gfxdraw


BACKGROUND_COLOR = (32, 32, 32)
PARTICLE_COLOR = (255, 255, 0)
PARTICLE_TRAIL_COLOR = (64, 64, 64)


class Display:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

        self.screen_width = width
        self.screen_height = height

    def render(self, simulation, camera):
        # clear the screen first with a background color
        self.screen.fill(BACKGROUND_COLOR)

        # draw particles and their associated effects
        particles = simulation.get_current_timestep_particles()
        particles_history = simulation.get_particles_history()

        for particle_id in particles.keys():
            self.draw_particle_trail(particle_id, particles_history, camera)

        for particle in particles.values():
            self.draw_particle(particle, camera)

        pygame.display.update()

    def draw_particle(self, particle, camera):
        radius = math.ceil(particle.mass * camera.zoom_factor)
        position_on_screen = self.get_position_on_screen(
            particle.position, camera)

        # cull particles outside the view for both performance and screen coordinate overflow reasons
        if position_on_screen[0] + radius < 0 or position_on_screen[0] - radius > self.screen_width:
            return  # out of horizontal boundaries
        elif position_on_screen[1] + radius < 0 or position_on_screen[1] - radius > self.screen_height:
            return  # out of vertical boundaries

        self.draw_circle(PARTICLE_COLOR, position_on_screen, radius)

    def draw_circle(self, color, position, radius):
        gfxdraw.aacircle(self.screen, int(position[0]), int(
            position[1]), int(radius), color)
        gfxdraw.filled_circle(self.screen, int(
            position[0]), int(position[1]), int(radius), color)

    def draw_particle_trail(self, particle_id, particles_history, camera):
        future_screen_position = None

        for snapshot in reversed(particles_history):
            if particle_id not in snapshot:
                break  # history doesn't go any further back for this particle

            particle = snapshot[particle_id]
            particle_screen_position = self.get_position_on_screen(
                particle.position, camera)

            if future_screen_position:
                pygame.draw.line(self.screen, PARTICLE_TRAIL_COLOR,
                                 particle_screen_position, future_screen_position, 3)

            future_screen_position = particle_screen_position

    def get_position_on_screen(self, world_position, camera):
        position_offset = [world_position[0] - camera.position[0],
                           world_position[1] - camera.position[1]]
        return [position_offset[0] * camera.zoom_factor, position_offset[1] * camera.zoom_factor]

    def get_default_camera_position(self):
        # since the top left corner of the window is the (0, 0) coordinate point,
        # offset the default camera position by half the window size in the opposite
        # direction to center the (0, 0) coordinate point in the window center
        return [-self.screen_width / 2, -self.screen_height / 2]

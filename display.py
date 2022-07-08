import math
import pygame
from pygame import gfxdraw


class Display:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

        self.screen_width = width
        self.screen_height = height

    def render(self, simulation, camera):
        # clear the screen first with a background color
        self.screen.fill((32, 32, 32))

        for particle_id, particle in simulation.get_current_timestep_particles().items():
            self.draw_particle(particle, camera)

        pygame.display.update()

    def draw_particle(self, particle, camera):
        radius = math.ceil(particle.mass * camera.zoom_factor)
        position_offset = [particle.position[0] - camera.position[0],
                           particle.position[1] - camera.position[1]]
        position_on_screen = [
            position_offset[0] * camera.zoom_factor, position_offset[1] * camera.zoom_factor]

        # cull particles outside the view for both performance and screen coordinate overflow reasons
        if position_on_screen[0] + radius < 0 or position_on_screen[0] - radius > self.screen_width:
            return  # out of horizontal boundaries
        elif position_on_screen[1] + radius < 0 or position_on_screen[1] - radius > self.screen_height:
            return  # out of vertical boundaries

        self.draw_circle((255, 255, 0), position_on_screen, radius)

    def draw_circle(self, color, position, radius):
        gfxdraw.aacircle(self.screen, int(position[0]), int(
            position[1]), int(radius), color)
        gfxdraw.filled_circle(self.screen, int(
            position[0]), int(position[1]), int(radius), color)

    def get_default_camera_position(self):
        # since the top left corner of the window is the (0, 0) coordinate point,
        # offset the default camera position by half the window size in the opposite
        # direction to center the (0, 0) coordinate point in the window center
        return [-self.screen_width / 2, -self.screen_height / 2]

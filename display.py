import math
import pygame
from pygame import gfxdraw


BACKGROUND_COLOR = (32, 32, 32)
PARTICLE_COLOR = (255, 255, 0)
PARTICLE_TRAIL_COLOR = (64, 64, 64)
PARTICLE_TRAIL_WIDTH = 3
SSAA_FACTOR = 1.5


class Display:
    def __init__(self, screen_size):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)

        surface_size = (screen_size[0] * SSAA_FACTOR,
                        screen_size[1] * SSAA_FACTOR)
        self.surface = pygame.Surface(surface_size)

    def render(self, simulation, camera):
        # clear the render surface first with a background color
        self.surface.fill(BACKGROUND_COLOR)

        # draw particles and their associated effects
        particles = simulation.get_current_timestep_particles()
        particles_history = simulation.get_particles_history()

        for particle_id in particles.keys():
            self.draw_particle_trail(particle_id, particles_history, camera)

        for particle in particles.values():
            self.draw_particle(particle, camera)

        # copy render surface to the screen and update it
        pygame.transform.smoothscale(
            self.surface, self.screen.get_size(), self.screen)
        pygame.display.update()

    def draw_particle(self, particle, camera):
        radius = math.ceil(particle.mass * camera.zoom_factor)
        position_on_screen = self.get_position_on_screen(
            particle.position, camera)

        # cull particles outside the view for both performance and screen coordinate overflow reasons
        screen_size = self.surface.get_size()
        if position_on_screen[0] + radius < 0 or position_on_screen[0] - radius > screen_size[0]:
            return  # out of horizontal boundaries
        elif position_on_screen[1] + radius < 0 or position_on_screen[1] - radius > screen_size[1]:
            return  # out of vertical boundaries

        self.draw_circle(position_on_screen, radius, PARTICLE_COLOR)

    def draw_particle_trail(self, particle_id, particles_history, camera):
        future_screen_position = None

        for snapshot in reversed(particles_history):
            if particle_id not in snapshot:
                break  # history doesn't go any further back for this particle

            particle = snapshot[particle_id]
            particle_screen_position = self.get_position_on_screen(
                particle.position, camera)

            if future_screen_position:
                self.draw_line(particle_screen_position,
                               future_screen_position, PARTICLE_TRAIL_WIDTH, PARTICLE_TRAIL_COLOR)

            future_screen_position = particle_screen_position

    def draw_circle(self, position, radius, color):
        draw_position = self.get_position_on_render_surface(position)
        pygame.draw.circle(self.surface, color,
                           draw_position, radius * SSAA_FACTOR)

    def draw_line(self, beginning, end, width, color):
        draw_beginning = self.get_position_on_render_surface(beginning)
        draw_end = self.get_position_on_render_surface(end)
        pygame.draw.line(self.surface, color, draw_beginning,
                         draw_end, int(width * SSAA_FACTOR))

    def get_position_on_screen(self, world_position, camera):
        position_offset = [world_position[0] - camera.position[0],
                           world_position[1] - camera.position[1]]
        return [position_offset[0] * camera.zoom_factor, position_offset[1] * camera.zoom_factor]

    def get_position_on_render_surface(self, screen_position):
        return [int(screen_position[0] * SSAA_FACTOR), int(screen_position[1] * SSAA_FACTOR)]

    def get_default_camera_position(self):
        # since the top left corner of the window is the (0, 0) coordinate point,
        # offset the default camera position by half the window size in the opposite
        # direction to center the (0, 0) coordinate point in the window center
        screen_size = self.screen.get_size()
        return [-screen_size[0] / 2, -screen_size[1] / 2]

import math
import pygame
from pygame import gfxdraw


BACKGROUND_COLOR = (32, 32, 32)
CROSSHAIR_COLOR = (255, 32, 0)
CROSSHAIR_SIZE = 15
CROSSHAIR_WIDTH = 1
PARTICLE_COLOR = (255, 255, 0)
PARTICLE_TRAIL_COLOR = (64, 64, 64)
PARTICLE_TRAIL_WIDTH = 3
SSAA_FACTOR = 1.5


class Display:
    def __init__(self, screen_size):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.set_ssaa_enabled(False)
        self.track_center_of_mass = True
    
    def set_ssaa_enabled(self, enabled):
        self.ssaa_factor = SSAA_FACTOR if enabled else 1.0
        screen_size = self.screen.get_size()
        surface_size = (screen_size[0] * self.ssaa_factor, screen_size[1] * self.ssaa_factor)
        self.surface = pygame.Surface(surface_size)
    
    def get_ssaa_enabled(self):
        return self.ssaa_factor > 1.0
    
    def center_camera_on_center_of_mass(self, simulation, camera):
        center_of_screen = self.get_center_of_screen()
        camera.position = simulation.center_of_mass.copy()
        camera.position[0] -= center_of_screen[0] / camera.zoom_factor
        camera.position[1] -= center_of_screen[1] / camera.zoom_factor
    
    def render(self, simulation, camera):
        if self.track_center_of_mass:
            self.center_camera_on_center_of_mass(simulation, camera)
        
        # clear the render surface first with a background color
        self.surface.fill(BACKGROUND_COLOR)

        # draw particles and their associated effects
        particles = simulation.get_current_timestep_particles()
        particles_history = simulation.get_particles_history()

        for particle_id in particles.keys():
            self.draw_particle_trail(particle_id, particles_history, camera)

        for particle in particles.values():
            self.draw_particle(particle, camera)
        
        if self.track_center_of_mass:
            self.draw_tracking_crosshair()
        
        # copy render surface to the screen and update it
        pygame.transform.smoothscale(
            self.surface, self.screen.get_size(), self.screen)
        pygame.display.update()
    
    def draw_particle(self, particle, camera):
        radius = math.ceil(particle.mass * camera.zoom_factor)
        position_on_screen = self.get_position_on_screen(
            particle.position, camera)

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
        if self.is_circle_on_screen(position, radius):
            draw_position = self.get_position_on_render_surface(position)
            pygame.draw.circle(self.surface, color,
                               draw_position, radius * self.ssaa_factor)

    def draw_line(self, beginning, end, width, color):
        if self.is_point_on_screen(beginning) or self.is_point_on_screen(end):
            draw_beginning = self.get_position_on_render_surface(beginning)
            draw_end = self.get_position_on_render_surface(end)
            pygame.draw.line(self.surface, color, draw_beginning,
                             draw_end, int(width * self.ssaa_factor))
    
    def draw_tracking_crosshair(self):
        points = []
        for i in range(4):
            points.append(self.get_center_of_screen())
        
        # horizontal line
        points[0][0] -= CROSSHAIR_SIZE
        points[1][0] += CROSSHAIR_SIZE
        self.draw_line(points[0], points[1], CROSSHAIR_WIDTH, CROSSHAIR_COLOR)
        # vertical line
        points[2][1] -= CROSSHAIR_SIZE
        points[3][1] += CROSSHAIR_SIZE
        self.draw_line(points[2], points[3], CROSSHAIR_WIDTH, CROSSHAIR_COLOR)
    
    def get_position_on_screen(self, world_position, camera):
        position_offset = [world_position[0] - camera.position[0],
                           world_position[1] - camera.position[1]]
        return [position_offset[0] * camera.zoom_factor, position_offset[1] * camera.zoom_factor]

    def get_position_on_render_surface(self, screen_position):
        return [int(screen_position[0] * self.ssaa_factor), int(screen_position[1] * self.ssaa_factor)]
    
    def is_point_on_screen(self, point):
        screen_size = self.screen.get_size()
        
        if point[0] < 0 or point[0] > screen_size[0]:
            return False # out of horizontal boundaries
        if point[1] < 0 or point[1] > screen_size[1]:
            return False # out of vertical boundaries
        
        return True
    
    def is_circle_on_screen(self, position, radius):
        screen_size = self.screen.get_size()
        if position[0] + radius < 0 or position[0] - radius > screen_size[0]:
            return False # out of horizontal boundaries
        elif position[1] + radius < 0 or position[1] - radius > screen_size[1]:
            return False # out of vertical boundaries
        
        return True
    
    def get_default_camera_position(self):
        # since the top left corner of the window is the (0, 0) coordinate point,
        # offset the default camera position by half the window size in the opposite
        # direction to center the (0, 0) coordinate point in the window center
        center_of_screen = self.get_center_of_screen()
        return [-center_of_screen[0], -center_of_screen[1]]
    
    def get_center_of_screen(self):
        screen_size = self.screen.get_size()
        return [screen_size[0] / 2, screen_size[1] / 2]

import pygame
from pygame import gfxdraw
import random
import math


def draw_circle(surface, color, position, radius):
    gfxdraw.aacircle(surface, int(position[0]), int(position[1]), int(radius), color)
    gfxdraw.filled_circle(surface, int(position[0]), int(position[1]), int(radius), color)


class Particle:
    def __init__(self, position, velocity, mass):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.acceleration = None


particles = []
G = 10


# calculate acceleration for a specified particle taking all others into consideration
def get_acceleration(p):
    acceleration_sum = [0, 0]

    for p2 in particles:
        if p == p2:
            continue

        difference = [p2.position[0] - p.position[0], p2.position[1] - p.position[1]]
        softening = 5
        distance = math.sqrt(difference[0] * difference[0] + difference[1] * difference[1] + softening * softening)
        force = G * (p.mass * p2.mass) / math.pow(distance, 2)
        acceleration = force / p.mass
        unit_vector = [difference[0] / distance, difference[1] / distance]

        acceleration_sum[0] += acceleration * unit_vector[0]
        acceleration_sum[1] += acceleration * unit_vector[1]

    return acceleration_sum


def main():
    pygame.init()

    # create a surface on screen
    screen_width = 1600
    screen_height = 900
    half_screen_width = screen_width / 2
    half_screen_height = screen_height / 2
    refresh_rate = 60 # in the future make refresh and simulation rate independent
    screen = pygame.display.set_mode((screen_width, screen_height))

    # some work is required to allow for a resizable window
    # resizing should probably keep whatever is in the center, centered
    # also culling is broken near the bottom and right edges as screen width/height
    # and half width/height are hardcoded right now
    #screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    clock = pygame.time.Clock()
    running = True

    # put some particles in random locations with random mass for testing purposes
    # (set particle count to 0 to disable)
    initial_particle_count = 0
    particle_spread = 1000
    velocity_spread = 1
    for i in range(initial_particle_count):
        # determine particle parameters
        position = [random.randrange(-particle_spread, particle_spread), random.randrange(-particle_spread, particle_spread)]
        velocity = [random.randrange(-velocity_spread, velocity_spread), random.randrange(-velocity_spread, velocity_spread)]
        velocity = [0, 0]
        mass = random.randrange(1, 50)

        # create particle and add to list of all particles
        p = Particle(position, velocity, mass)
        particles.append(p)

    # fixed test particles
    particles.append(Particle([0, 0], [0, 0], 100))
    particles.append(Particle([-200, 0], [0, -2.3], 10))

    # main loop
    view_center = [0, 0]
    zoom_factor = 1.0
    scroll_amount = 10
    dt = 1.0
    frame_time = 1.0 / refresh_rate
    while running:
        # clear the screen to blank first
        screen.fill((32, 32, 32))

        # user input
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            view_center[1] -= scroll_amount * (1.0 / zoom_factor)
        if pressed_keys[pygame.K_s]:
            view_center[1] += scroll_amount * (1.0 / zoom_factor)
        if pressed_keys[pygame.K_a]:
            view_center[0] -= scroll_amount * (1.0 / zoom_factor)
        if pressed_keys[pygame.K_d]:
            view_center[0] += scroll_amount * (1.0 / zoom_factor)

        for p in particles:
            # comment out Leapfrog in favor of simple Euler integration right now

            # if p.acceleration is None:  # check maybe the initial acceleration has not been calculated yet
            #     p.acceleration = get_acceleration(p)

            p.acceleration = get_acceleration(p)

            p.velocity[0] += p.acceleration[0] * dt
            p.velocity[1] += p.acceleration[1] * dt

            p.position[0] += p.velocity[0] * dt
            p.position[1] += p.velocity[1] * dt

            # kick
            # p.velocity[0] = p.velocity[0] + p.acceleration[0] * dt / 2.0
            # p.velocity[1] = p.velocity[1] + p.acceleration[1] * dt / 2.0

            # drift
            # p.position[0] = p.position[0] + p.velocity[0] * dt
            # p.position[1] = p.position[1] + p.velocity[1] * dt

            # update acceleration
            # p.acceleration = get_acceleration(p)

            # kick
            # p.velocity[0] = p.velocity[0] + p.acceleration[0] * dt / 2.0
            # p.velocity[1] = p.velocity[1] + p.acceleration[1] * dt / 2.0

        # draw all particles
        for p in particles:
            radius = math.ceil(p.mass * zoom_factor)
            position_offset = [p.position[0] - view_center[0], p.position[1] - view_center[1]]
            position_on_screen = [half_screen_width + position_offset[0] * zoom_factor, half_screen_height + position_offset[1] * zoom_factor]

            # cull particles outside the view for both performance and screen coordinate overflow reasons
            if position_on_screen[0] + radius < 0 or position_on_screen[0] - radius > screen_width:
                continue  # out of horizontal boundaries
            elif position_on_screen[1] + radius < 0 or position_on_screen[1] - radius > screen_height:
                continue  # out of vertical boundaries

            draw_circle(screen, (255, 255, 0), position_on_screen, radius)

        # update the screen and wait for the next frame
        pygame.display.update()
        frame_time = clock.tick(refresh_rate) / 1000
        pygame.display.set_caption("nsim - " + str(frame_time) + " frame time")

        # event handling just before the beginning of the next frame
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                wheel_movement = event.y

                # calculate the world position that the mouse is on the current frame
                mouse_position = pygame.mouse.get_pos()
                mouse_relative_position = [mouse_position[0] - half_screen_width, mouse_position[1] - half_screen_height]
                world_relative_position = [mouse_relative_position[0] / zoom_factor, mouse_relative_position[1] / zoom_factor]
                world_absolute_position = [view_center[0] + world_relative_position[0], view_center[1] + world_relative_position[1]]

                # update the zoom factor
                zoom_change_factor = 2.0 if pressed_keys[pygame.K_LSHIFT] else 1.1
                while wheel_movement:
                    if wheel_movement > 0:
                        wheel_movement -= 1
                        zoom_factor *= zoom_change_factor
                    else:
                        wheel_movement += 1
                        zoom_factor /= zoom_change_factor

                # update view_center so that the old world pos is at the same point as the mouse was/is
                new_world_relative_position = [mouse_relative_position[0] / zoom_factor, mouse_relative_position[1] / zoom_factor]
                new_world_absolute_position = [view_center[0] + new_world_relative_position[0], view_center[1] + new_world_relative_position[1]]
                old_new_difference = [world_absolute_position[0] - new_world_absolute_position[0], world_absolute_position[1] - new_world_absolute_position[1]]
                view_center = [view_center[0] + old_new_difference[0], view_center[1] + old_new_difference[1]]
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    view_center = [view_center[0] - event.rel[0] * (1.0 / zoom_factor), view_center[1] - event.rel[1] * (1.0 / zoom_factor)]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse click down, start dragging the view
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                elif event.button == 3:  # right mouse click down, create new particle
                    mouse_relative_position = [event.pos[0] - half_screen_width, event.pos[1] - half_screen_height]
                    position = [view_center[0] + mouse_relative_position[0] / zoom_factor, view_center[1] + mouse_relative_position[1] / zoom_factor]
                    velocity = [0, 0]
                    mass = 10

                    p = Particle(position, velocity, mass)
                    particles.append(p)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # left mouse click up
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                running = False


if __name__ == "__main__":
    main()

import pygame
from models.particle import Particle

KEYS_SCROLL_AMOUNT = 15.0


class Controller:
    def __init__(self):
        self.exit_requested = False

    def handle_input(self, camera, simulation):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                wheel_movement = event.y
                cursor_position = pygame.mouse.get_pos()
                self.zoom_around_cursor(
                    camera, cursor_position, wheel_movement)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button down
                    # start dragging the camera
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                elif event.button == 3:  # right mouse button down
                    self.spawn_new_particle(simulation, camera, event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # left mouse button down
                    # keep dragging the camera
                    self.scroll_with_mouse(camera, event.rel)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # left mouse button up
                # stop dragging the camera
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to True to exit the main loop
                self.exit_requested = True

        self.scroll_with_keys(camera)

    def zoom_around_cursor(self, camera, cursor_position, zoom_amount):
        # calculate the world position that the cursor is on the current frame
        world_relative_position = [
            cursor_position[0] / camera.zoom_factor, cursor_position[1] / camera.zoom_factor]
        world_absolute_position = [
            camera.position[0] + world_relative_position[0], camera.position[1] + world_relative_position[1]]

        # zoom faster if left shift is held down
        zoom_change_factor = 2.0 if pygame.key.get_pressed()[
            pygame.K_LSHIFT] else 1.1
        while zoom_amount:
            if zoom_amount > 0:
                zoom_amount -= 1
                camera.zoom_factor *= zoom_change_factor
            else:
                zoom_amount += 1
                camera.zoom_factor /= zoom_change_factor

        # update camera position so that the old world pos is at the same point as the cursor was/is
        new_world_relative_position = [
            cursor_position[0] / camera.zoom_factor, cursor_position[1] / camera.zoom_factor]
        new_world_absolute_position = [
            camera.position[0] + new_world_relative_position[0], camera.position[1] + new_world_relative_position[1]]
        old_new_difference = [world_absolute_position[0] - new_world_absolute_position[0],
                              world_absolute_position[1] - new_world_absolute_position[1]]
        camera.position = [camera.position[0] + old_new_difference[0],
                           camera.position[1] + old_new_difference[1]]

    def spawn_new_particle(self, simulation, camera, position_on_screen):
        position = [camera.position[0] + position_on_screen[0] / camera.zoom_factor,
                    camera.position[1] + position_on_screen[1] / camera.zoom_factor]
        velocity = [0, 0]
        mass = 10

        simulation.particles.append(Particle(position, velocity, mass))

    def scroll_with_mouse(self, camera, movement_offset):
        camera.position = [camera.position[0] - movement_offset[0] * (1.0 / camera.zoom_factor),
                           camera.position[1] - movement_offset[1] * (1.0 / camera.zoom_factor)]

    def scroll_with_keys(self, camera):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            camera.position[1] -= KEYS_SCROLL_AMOUNT * \
                (1.0 / camera.zoom_factor)
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            camera.position[1] += KEYS_SCROLL_AMOUNT * \
                (1.0 / camera.zoom_factor)
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            camera.position[0] -= KEYS_SCROLL_AMOUNT * \
                (1.0 / camera.zoom_factor)
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            camera.position[0] += KEYS_SCROLL_AMOUNT * \
                (1.0 / camera.zoom_factor)

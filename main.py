import pygame
import random
from circle_on_circle import *

# pygame stuff
pygame.init()


# Keep track of objects, add_object and remove_object probably unnecessary
def add_object(self, objects, RigidBody):
    objects.append(RigidBody)
    return objects


def remove_object(self, objects, RigidBody):
    objects.remove(RigidBody)
    return objects


# Movement step
def move_step(dt, objects, g, screendim):
    Cd = 0.5  # Drag coefficient
    AirRes = 1.125
    Tv2 = -1  # Terminal velocity squared

    circle_collision = circle_collision_detection(objects)
    on_circle_collision(circle_collision, objects, dt)

    for i in range(len(objects)):
        r = objects[i].shape.radius

        objects[i].force = vec_plus_vec(objects[i].force, vec_by_float(g, objects[i].shape.mass))
        objects[i].force.x = objects[i].force.x - AirRes * objects[i].linVel.x * 0.1

        if objects[i].position.y >= screendim.y - r:
            objects[i].position.y = screendim.y - r
            objects[i].linVel.y = objects[i].linVel.y * -1
        elif objects[i].position.y <= r:
            objects[i].position.y = r
            objects[i].linVel.y = objects[i].linVel.y * -1

        if objects[i].position.x >= screendim.x - r:
            objects[i].position.x = screendim.x - r
            objects[i].linVel.x = objects[i].linVel.x * -1
        elif objects[i].position.x <= r:
            objects[i].position.x = r
            objects[i].linVel.x = objects[i].linVel.x * -1

        objects[i].linVel = vec_plus_vec(objects[i].linVel,
                                         vec_by_float(objects[i].force, 1 / objects[i].shape.mass * dt))

        # Check for terminal velocity
        Tv2 = (20 * objects[i].shape.mass * g.y) / (AirRes * (math.pi * r * r) * Cd)
        if objects[i].linVel.y > Tv2:
            temp = math.sqrt(Tv2)
            objects[i].linVel.y = temp

        objects[i].position.y = objects[i].position.y + objects[i].linVel.y * dt
        objects[i].position.x = objects[i].position.x + objects[i].linVel.x * dt

        if objects[i].force.y >= g.y:
            objects[i].force = Vector2(0, 0)


# So you can close the window
def check_quit(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    return run


# Draws objects to screen
def draw_objects(objects, surf):
    for n in range(len(objects)):
        tempx = objects[n].position.x
        tempy = objects[n].position.y
        pygame.draw.circle(surf, (255, 0, 0), (tempx, tempy), objects[n].shape.radius)  # error
    return surf


def main():
    # Global variables
    gravity = Vector2(0, 2)
    num_of_objs = 15
    dt = 0.01
    running = True

    # pygame initialization
    screen_d = Vector2(800, 600)
    screen = pygame.display.set_mode((screen_d.x, screen_d.y))
    pygame.display.set_caption("Box o' Physics")
    icon = pygame.image.load("einstein.png")
    pygame.display.set_icon(icon)

    # Create objects
    objects = []
    for n in range(num_of_objs):
        # RigidBody(Vector2 position, Vector2 linVel, float angle, float angVel, Vector2 force, Vector2 torque, Shape shape, float restitution)
        objects.append(
            RigidBody(Vector2(random.randrange(0, screen_d.x), random.randrange(0, screen_d.y)),  # screen_d.x-15
                      Vector2(random.randrange(-15, 15), 0), 0, 0, Vector2(0, 0), 0, BallShape(random.randrange(40, 60), 0, random.randrange(10, 20)), random.randrange(5, 40) / 100))

    # Create screen
    back_color = Vector3(255, 255, 0)
    screen.fill((back_color.x, back_color.y, back_color.z))
    pygame.display.update()

    # Collision stuff
    circle_collision = []

    while running:
        running = check_quit(running)

        # Draw objects
        # Erase object, calculate movement, redraw object in new position
        for n in range(len(objects)):
            pygame.draw.circle(screen, (back_color.x, back_color.y, back_color.z),
                               (objects[n].position.x, objects[n].position.y), objects[n].shape.radius)
        move_step(dt, objects, gravity, screen_d)

        for n in range(len(objects)):
            pygame.draw.circle(screen, (n * 10, 0, 0), (objects[n].position.x, objects[n].position.y),
                               objects[n].shape.radius)

        for i in range(len(circle_collision)):
            obx = objects[int(circle_collision[i].which_circs.x)]
            oby = objects[int(circle_collision[i].which_circs.y)]
            pygame.draw.circle(screen, (255, 0, 255), (obx.position.x, obx.position.y), obx.shape.radius)
            pygame.draw.circle(screen, (255, 0, 255), (oby.position.x, oby.position.y), oby.shape.radius)
        circle_collision = []

        pygame.display.update()  # Make sure you blit a piece of the background over where the object used to be

    pygame.quit()


if __name__ == "__main__":
    main()

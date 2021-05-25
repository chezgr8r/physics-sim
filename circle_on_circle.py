import math
import numpy as np
from vector_math_functions import *


def circle_collision_detection(objects):
    collisions = []

    # Might be more math than necessary
    # Figure out if math.atan() calculates angle from x axis or y axis
    #
    # angle = math.atan(yB - yA, xB - xA)
    # point inside A = (cent_B_x + (radiusB * cos(angle - pi), cent_B_y + (radiusB * sin(angle - pi))
    # point inside B = (cent_A_x + (radiusA * cos(angle), cent_A_y + (radiusA * sin(angle))
    for n in range(len(objects)):
        other_circ = n + 1
        while other_circ < len(objects):
            cx1 = objects[n].position.x
            cy1 = objects[n].position.y
            cr1 = objects[n].shape.radius
            cx2 = objects[other_circ].position.x
            cy2 = objects[other_circ].position.y
            cr2 = objects[other_circ].shape.radius

            dist2 = (cx1 - cx2) * (cx1 - cx2) + (cy1 - cy2) * (cy1 - cy2)

            if dist2 < (cr1 + cr2) * (cr1 + cr2):
                angle = math.atan2(cy2 - cy1, cx2 - cx1)

                if cx1 < cx2:
                    Ax = cx2 + (cr2 * math.cos(angle))#- math.pi
                    Bx = cx1 + (cr1 * math.cos(angle))
                elif cx1 > cx2:
                    Ax = cx2 + (cr2 * math.cos(angle))
                    Bx = cx1 + (cr1 * math.cos(angle))# - math.pi
                else:
                    Ax = cx1
                    Bx = cx2

                if cy1 < cy2:
                    Ay = cy2 + (cr2 * math.sin(angle))# - math.pi
                    By = cy1 + (cr1 * math.sin(angle))
                elif cy1 > cy2:
                    Ay = cy2 + (cr2 * math.sin(angle))
                    By = cy1 + (cr1 * math.sin(angle))# - math.pi
                else:
                    Ay = cy1
                    By = cy2

                collisions.append(CollisionInfo(Vector2(n, other_circ), Vector2(Ax, Ay), Vector2(Bx, By)))

            other_circ = other_circ + 1
    return collisions


def on_circle_collision(collisions, objects, dt):
    if len(collisions) == 0:
        return

    for n in range(len(collisions)):
        circ1x = objects[collisions[n].which_circs.x].position.x
        circ2x = objects[collisions[n].which_circs.y].position.x
        circ1y = objects[collisions[n].which_circs.x].position.y
        circ2y = objects[collisions[n].which_circs.y].position.y

        # dist2 = (circ1x - circ2x)**2 + (circ1y - circ2y)**2

        circ1m = objects[collisions[n].which_circs.x].shape.mass
        circ2m = objects[collisions[n].which_circs.y].shape.mass
        mass_sum = circ1m + circ2m
        inv1m = 1 / circ1m
        inv2m = 1 / circ2m

        vx1 = objects[collisions[n].which_circs.x].linVel.x
        vx2 = objects[collisions[n].which_circs.y].linVel.x
        vy1 = objects[collisions[n].which_circs.x].linVel.y
        vy2 = objects[collisions[n].which_circs.y].linVel.y

        nx = collisions[n].pointB.x - collisions[n].pointA.x
        ny = collisions[n].pointB.y - collisions[n].pointA.y

        # Array normalization may be wrong, convert to numpy.linalg.norm()
        # https://www.kite.com/python/answers/how-to-normalize-an-array-in-numpy-in-python
        nm2 = [nx, ny]
        # nm2 = nx**2 + ny**2
        nx = nx / np.linalg.norm(nm2)
        ny = ny / np.linalg.norm(nm2)
        normal = Vector2(nx, ny)
        #print("normal x: ", nx, " y: ", ny)

        rv = Vector2(vx2 - vx1, vy2 - vy1) # convert to arrays
        #print("rv x: ", rv.x, " rv y: ", rv.y)
        velAlongNormal = np.dot(vec_to_array(rv), vec_to_array(normal))
        #print("velAlongNormal: ", velAlongNormal)
        if velAlongNormal > 40 or velAlongNormal < -40:
            return
        e = min(objects[collisions[n].which_circs.x].restitution, objects[collisions[n].which_circs.x].restitution)
        j = -(1 + e) * math.sqrt((vx2 - vx1)**2 + (vy2 - vy1)**2)
        # j = j / (inv1m + inv2m)
        #print("j: ", j)
        impulse = Vector2(j * normal.x, j * normal.y)
        #print("impulse x: ", nx, " impulse y: ", ny)
        # vx1 = vx1 - inv1m * impulse.x
        # vx2 = vx2 + inv2m * impulse.x
        # vy1 = vy1 - inv1m * impulse.y
        # vy2 = vy2 + inv1m * impulse.y
        # print("circle 2 x: ", vx2, " circle 2 y: ", vy2)
        # sleep(0.01)
        ratio = circ1m / mass_sum
        objects[collisions[n].which_circs.x].linVel.x -= ratio * impulse.x
        objects[collisions[n].which_circs.x].linVel.y -= ratio * impulse.y

        ratio = circ2m / mass_sum
        objects[collisions[n].which_circs.y].linVel.x += ratio * impulse.x
        objects[collisions[n].which_circs.y].linVel.y += ratio * impulse.y

        # objects[collisions[n].which_circs.x].linVel.x = vx1 - inv1m * impulse.x
        # objects[collisions[n].which_circs.y].linVel.x = vx2 + inv2m * impulse.x
        # objects[collisions[n].which_circs.x].linVel.y = vy1 - inv1m * impulse.y
        # objects[collisions[n].which_circs.y].linVel.y = vy2 + inv1m * impulse.y

from structs import *


# Vector operations
def vec_by_float(vec, f):
    return Vector2(vec.x * f, vec.y * f)


def vec_plus_vec(vec1, vec2):
    return Vector2(vec1.x + vec2.x, vec1.y + vec2.y)


def vec_to_array(vec):
    return [vec.x, vec.y]
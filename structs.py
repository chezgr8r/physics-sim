from dataclasses import dataclass


@dataclass
class Vector3:
    x: float
    y: float
    z: float


@dataclass
class Vector2:
    x: float
    y: float


@dataclass
class CollisionInfo:
    which_circs: Vector2
    pointA: Vector2
    pointB: Vector2


@dataclass
class Shape:
    mass: float
    momentOfInertia: float


@dataclass
class BoxShape(Shape):
    width: float
    height: float


@dataclass
class BallShape(Shape):
    radius: float


@dataclass
class RigidBody:
    position: Vector2
    linVel: Vector2
    angle: float
    angVel: float
    force: Vector2
    torque: float
    shape: Shape
    restitution: float


@dataclass
class CollisionPoints:
    A: Vector2 # Furthest point of A into B
    B: Vector2 # Furthest point of B into A
    Normal: Vector2
    Depth: float
    HasCollision: bool


@dataclass
class Transform:
    Position: Vector2
    Scale: Vector2
    Rotation: Vector3

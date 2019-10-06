import numpy as np
from animalai.envs.arena_config import Vector3

def get_angle_looking_center(x, z):
    angle = np.arctan2(x-20, z-20)*180/np.pi + 180
    angle = float(angle)
    return normalize_angle(angle)

def get_random_position():
    x, z = np.random.randint(1, 40, size=2)
    return float(x), float(z)

def get_random_position_close_to_center(max_distance=5):
    x, z = 20 + np.random.uniform(-max_distance, max_distance, size=2)
    return float(x), float(z)

def normalize_angle(angle):
    if angle < 0:
        angle += 360
    if angle >= 360:
        angle -= 360
    return angle

def get_position_in_front_of_agent(x, z, angle, distance):
    theta = (90 - angle)*np.pi/180
    x, z = float(np.cos(theta)*distance + x), float(np.sin(theta)*distance + z)
    return x, z

class CollisionDetected(Exception):
    pass

def detect_collisions(new_item, existing_items):
    """
    Verifies if a new item collides with existing items in the arena

    The idea is that each existing object can be modelled as a rectangle. If any
    of the vertices of the new item is inside the rectangle then we have a collision.
    So we can reduce the problem to detecting if a point is inside a rectangle.

    This method will open the door to add death zones to the arena without the problem
    of having a goal on the top. Or I could use ghost objects that ensure that there
    is a path between the goal and the agent no matter how many obstacles I add.

    If the rotation is 0 the problem is simply to compare values of x and y, let's try to do
    it that way.
    https://stackoverflow.com/questions/31321032/python-test-if-point-is-in-rectangle

    Raises
    ------
    CollisionDetected
    """
    ref_angle = new_item.rotations[0]
    # TODO: verify collision with arena borders
    for item in existing_items:
        detect_collision_between_two_items(new_item, item)

def detect_collision_between_two_items(item_ref, item):
    pass

def _get_object_vertices(item, ref_angle):
    size = item.sizes[0]
    center = item.positions[0]
    angle = item.rotations[0] - ref_angle
    object_radius = np.sqrt(size.x**2 + size.z**2)/2
    vertices = []
    for vertex_idx in range(4):
        vertex_angle = np.arctan2(size.z, size.x) - (vertex_idx*90 + angle)*np.pi/180
        vertex = Vector3(np.cos(vertex_angle)*object_radius, 0, np.sin(vertex_angle)*object_radius)
        vertices.append(vertex)
    return vertices

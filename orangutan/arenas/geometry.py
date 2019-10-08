import numpy as np
from animalai.envs.arena_config import Vector3

from orangutan.arenas.utils import _str_Vector3

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
    detect_object_out_of_arena(new_item)
    for item in existing_items:
        detect_collision_between_two_items(new_item, item)

def detect_collision_between_two_items(item1, item2):
    _detect_collision_between_two_items(item1, item2)
    _detect_collision_between_two_items(item2, item1)

def detect_object_out_of_arena(item):
    EPSILON = 1e-6
    vertices = _get_object_vertices(item, ref_angle=0)
    for vertex in vertices:
        if vertex.x < 0-EPSILON or vertex.x > 40+EPSILON or vertex.z < 0-EPSILON or vertex.z > 40+EPSILON:
            msg = 'vertex: %s is out of arena' % (_str_Vector3(vertex))
            raise CollisionDetected(msg)

def _detect_collision_between_two_items(item_ref, item):
    EPSILON = 1e-6
    try:
        ref_rotations = [item_ref.rotations[0]]
    except IndexError:
        # If no rotation is given try with 0, 45 and 90
        ref_rotations = [0, 45, 90]
    for ref_rotation in ref_rotations:
        vertices = _get_object_vertices(item, ref_rotation)
        try:
            size = item_ref.sizes[0]
            center = item_ref.positions[0]
        except IndexError:
            # This case happens when using random goals, that is why they are placed at the last position
            # when sampling
            return
        x_limits = [center.x - size.x/2, center.x + size.x/2]
        z_limits = [center.z - size.z/2, center.z + size.z/2]
        for vertex in vertices:
            if vertex.x > x_limits[0]+EPSILON and vertex.x < x_limits[1]-EPSILON:
                if vertex.z > z_limits[0]+EPSILON and vertex.z < z_limits[1]-EPSILON:
                    msg = 'vertex: %s, x_limits: %s, z_limits: %s' % (_str_Vector3(vertex), str(x_limits), str(z_limits))
                    raise CollisionDetected(msg)

def _get_object_vertices(item, ref_angle):
    try:
        size = item.sizes[0]
        center = item.positions[0]
    except IndexError:
        # This case happens when using random goals, that is why they are placed at the last position
        # when sampling
        return []
    try:
        angles = [item.rotations[0] - ref_angle]
    except IndexError:
        # If no rotation is given try with 0, 45 and 90
        angles = [-ref_angle, 45 - ref_angle, 90 - ref_angle]
    object_radius = np.sqrt(size.x**2 + size.z**2)/2
    vertices = []
    for angle in angles:
        for vertex_idx in range(4):
            if vertex_idx == 0:
                vertex_angle = np.arctan2(size.z, size.x)
            elif vertex_idx == 1:
                vertex_angle = -np.arctan2(size.z, size.x)
            elif vertex_idx == 2:
                vertex_angle = np.pi + np.arctan2(size.z, size.x)
            elif vertex_idx == 3:
                vertex_angle = np.pi - np.arctan2(size.z, size.x)
            vertex_angle -= angle*np.pi/180
            vertex = Vector3(
                np.cos(vertex_angle)*object_radius + center.x,
                0,
                np.sin(vertex_angle)*object_radius + center.z)
            vertices.append(vertex)
    return vertices

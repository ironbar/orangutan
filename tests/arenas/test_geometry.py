import pytest
from animalai.envs.arena_config import Vector3, RGB, Item, Arena, ArenaConfig

from orangutan.arenas.geometry import get_angle_looking_center, get_position_in_front_of_agent, _get_object_vertices
from orangutan.arenas.utils import _str_Vector3

@pytest.mark.parametrize('x, y, angle', [
    (20, 10, 0),
    (20, 30, 180),
    (10, 20, 90),
    (30, 20, 270),
    (5, 5, 45),
    (5, 35, 45+90),
    (35, 35, 45+90+90),
    (35, 5, 45+90+90+90),
])
def test_get_angle_looking_center(x, y, angle):
    computed_angle = get_angle_looking_center(x, y)
    assert pytest.approx(angle) == computed_angle

@pytest.mark.parametrize('x, z, angle, distance, x_new, z_new', [
    (0, 0, 0, 10, 0, 10),
    (0, 0, 90, 10, 10, 0),
    (0, 0, 180, 10, 0, -10),
    (0, 0, 270, 10, -10, 0),
])
def test_get_position_in_front_of_agent(x, z, angle, distance, x_new, z_new):
    x, z = get_position_in_front_of_agent(x, z, angle, distance)
    assert pytest.approx(x_new) == x
    assert pytest.approx(z_new) == z

@pytest.mark.parametrize('item, ref_angle, vertices', [
    (Item(positions=[Vector3(0, 0, 0)], rotations=[0], sizes=[Vector3(2, 0, 2)]), 0, [Vector3(1, 0, 1), Vector3(1, 0, -1), Vector3(-1, 0, -1), Vector3(-1, 0, 1)]),
    (Item(positions=[Vector3(0, 0, 0)], rotations=[90], sizes=[Vector3(2, 0, 2)]), 0, [Vector3(1, 0, -1), Vector3(-1, 0, -1), Vector3(-1, 0, 1), Vector3(1, 0, 1)]),
    (Item(positions=[Vector3(0, 0, 0)], rotations=[0], sizes=[Vector3(4, 0, 2)]), 0, [Vector3(2, 0, 1), Vector3(2, 0, -1), Vector3(-2, 0, -1), Vector3(-2, 0, 1)]),
])
def test_get_object_vertices(item, ref_angle, vertices):
    computed_vertices = (_get_object_vertices(item, ref_angle))
    for vertex_1, vertex_2 in zip(computed_vertices, vertices):
        msg = '%s != %s' % (_str_Vector3(vertex_1), _str_Vector3(vertex_2))
        assert pytest.approx(vertex_1.x) == vertex_2.x, msg
        assert pytest.approx(vertex_1.y) == vertex_2.y, msg
        assert pytest.approx(vertex_1.z) == vertex_2.z, msg

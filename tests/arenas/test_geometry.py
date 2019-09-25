import pytest

from orangutan.arenas.geometry import get_angle_looking_center, get_position_in_front_of_agent

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

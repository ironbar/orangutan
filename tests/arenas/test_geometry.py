import pytest

from orangutan.arenas.geometry import get_angle_looking_center

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

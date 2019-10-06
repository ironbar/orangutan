from animalai.envs.arena_config import RGB

GRAY = RGB(153, 153, 153)
PINK = RGB(255, 0, 255)
BLUE = RGB(0, 0, 255)

def _str_Vector3(vector3):
    return '(%.1f, %1.f, %.1f)' % (vector3.x, vector3.y, vector3.z)

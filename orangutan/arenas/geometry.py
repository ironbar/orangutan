import numpy as np

def get_angle_looking_center(x, z):
    angle = np.arctan2(x-20, z-20)*180/np.pi + 180
    angle = float(angle)
    return normalize_angle(angle)

def get_random_position():
    x, z = np.random.randint(1, 40, size=2)
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

"""
Map for the position of the agent in the arena
"""
import numpy as np
import matplotlib.pyplot as plt

class ArenaMap():
    """
    Creates a map of the previous positions of the agent in the arena
    """
    def __init__(self):
        self._orientation = 0
        self._orientations = [self._orientation]
        self._position = np.zeros(2)
        self._positions = [self._position.copy()]

    def add_point(self, speed, previous_action):
        rotation = previous_action[0, 1]
        if rotation == 1:
            self._orientation += 6
        elif rotation == 2:
            self._orientation -= 6
        alpha = -1
        speed_factor = 1./10/1.625
        self._position[1] += speed_factor*np.sum(speed*np.array([
            alpha*np.sin(self._orientation*np.pi/180), np.cos(self._orientation*np.pi/180)]))
        self._position[0] -= speed_factor*np.sum(speed*np.array([
            alpha*np.cos(self._orientation*np.pi/180), -np.sin(self._orientation*np.pi/180)]))
        self._positions.append(self._position.copy())
        self._orientations.append(self._orientation)

    def visualize_trajectory(self):
        positions = self._get_normalized_positions_to_last_state()
        plt.scatter(positions[:, 0], positions[:, 1], c=np.linspace(0, 1, len(positions)))

    def _get_normalized_positions_to_last_state(self):
        positions = np.array(self._positions)
        positions -= positions[-1:]
        angles = np.arctan2(positions[:, 0], positions[:, 1]) -self._orientation*np.pi/180
        radius = np.sqrt(np.sum(positions**2, axis=1))
        positions[:, 0] = radius*np.sin(angles)
        positions[:, 1] = radius*np.cos(angles)
        return positions

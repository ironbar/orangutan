"""
Visualize recorded games
Transform .npz files into videos using opencv
"""
import sys
import argparse
import cv2
import os
import numpy as np
import glob
import time
from tqdm import tqdm


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    args = parse_args(args)
    saved_games_filepaths = glob.glob(os.path.join(args.games_path, '*.npz'))
    for saved_games_filepath in tqdm(saved_games_filepaths):
        video_filepath = os.path.join(
            args.output_path,
            '%s.avi' % os.path.splitext(os.path.basename(saved_games_filepath))[0])
        create_video(saved_games_filepath, video_filepath)

def create_video(npz_filepath, video_filepath):
    data = np.load(npz_filepath)
    frames = data['frame'][:, :, :, [2, 1, 0]]
    """
    Codecs and resulting sizes
    DIVX -> 35.1 KB
    XVID -> 35.1 KB
    MJPG -> 60.2
    X264 -> 18
    WMV1 38.9
    WMV2 40.6
    HFYU 246

    I have finally used HFYU and writed each frame 5 times to avoid lossing information
    """
    fourcc = cv2.VideoWriter_fourcc(*'HFYU')
    out = cv2.VideoWriter(video_filepath, fourcc, 100.0, (84, 84), True)
    [_write_n_frames(frame, out, n=5) for frame in frames]
    out.release()

def _write_n_frames(frame, out, n):
    for _ in range(n):
        out.write(frame)


def parse_args(args):
    epilog = """
    python record_games.py "/media/guillermo/Data/Dropbox/02 Inteligencia Artificial/31_animalai/AnimalAI-Olympics/examples/configs/1-Food.yaml" /media/guillermo/Data/Kaggle/animalai/gameplay
    """
    description = """
    Visualize recorded games
    Transform .npz files into videos using opencv
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=epilog)
    parser.add_argument('games_path', help='Path to the dir with recorded games')
    parser.add_argument('output_path', help='Path to folder where the videos are going to be saved')
    return parser.parse_args(args)

if __name__ == '__main__':
    main()

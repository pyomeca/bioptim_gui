import argparse
import pickle as pkl

import bioviz
import numpy as np
import cv2
from pathlib import Path


def merge_videos(video1_path: str, video2_path: str, save_path: str):
    # Open the videos
    video1 = cv2.VideoCapture(video1_path)
    video2 = cv2.VideoCapture(video2_path)

    # Get video properties (frame width, height)
    width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video1.get(cv2.CAP_PROP_FPS))
    frame_count = int(video1.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create a new video writer object
    combined_video = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"XVID"), fps, (2 * width, height))

    # Process each frame
    for i in range(frame_count):
        ret1, frame1 = video1.read()
        ret2, frame2 = video2.read()

        if ret1 and ret2:
            # Resize frames if they are not the same size
            frame2_resized = cv2.resize(frame2, (width, height))

            # Combine frames horizontally
            combined_frame = cv2.hconcat([frame1, frame2_resized])

            # Write to the new video
            combined_video.write(combined_frame)
        else:
            break

    # Release video objects and writer
    video1.release()
    video2.release()
    combined_video.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()


def create_video(biorbd_model_path: str, interpolated_states, save_path: str, cam_setting: str = "front"):
    cam_settings = {
        "front": (0, -5, 2.8),
        "side": (5, 0, 2.8),
    }

    camx, camy, camz = cam_settings.get(cam_setting, (0, -5, 2.8))

    b = bioviz.Viz(
        biorbd_model_path,
        mesh_opacity=1,
        show_global_center_of_mass=False,
        show_gravity_vector=False,
        show_segments_center_of_mass=False,
        show_global_ref_frame=False,
        show_local_ref_frame=False,
        experimental_markers_color=(1, 1, 1),
        background_color=(1.0, 1.0, 1.0),
    )
    b.set_camera_position(camx, camy, camz)
    b.set_camera_focus_point(0, 0, 2.4)
    b.set_camera_zoom(0.25)
    b.maximize()
    b.update()

    q_for_video = interpolated_states[0]["q"][:, :-1]
    for i_phase in range(1, len(interpolated_states) - 1):
        q_for_video = np.hstack((q_for_video, interpolated_states[i_phase]["q"][:, :-1]))
    q_for_video = np.hstack((q_for_video, interpolated_states[len(interpolated_states) - 1]["q"]))
    b.load_movement(q_for_video)

    b.start_recording(save_path)
    for frame in range(q_for_video.shape[1] + 1):
        b.movement_slider[0].setValue(frame)
        b.add_frame()
    b.stop_recording()
    b.quit()


def animate_solution(pkl_path: str) -> None:
    with open(pkl_path, "rb") as f:
        o = pkl.load(f)

    interpolated_states = o["interpolated_states"]
    biomodel_path = o["biomodel_path"]
    coneless_model = o.get("coneless_model", biomodel_path)

    pkl_path = Path(pkl_path)
    save_name = pkl_path.stem

    video_save_folder = str(pkl_path.parent) + "/videos/"
    Path(video_save_folder).mkdir(parents=True, exist_ok=True)

    front_save_path = video_save_folder + save_name + "_front.ogv"
    create_video(coneless_model, interpolated_states, front_save_path, "front")

    side_save_path = video_save_folder + save_name + "_side.ogv"
    create_video(biomodel_path, interpolated_states, side_save_path, "side")

    merge_save_path = video_save_folder + save_name + "_merged.avi"
    merge_videos(front_save_path, side_save_path, merge_save_path)


if __name__ == "__main__":
    # arg parser
    parser = argparse.ArgumentParser()

    parser.add_argument("pickle", type=str, help="Path to the pickle")

    # arg handling
    args = parser.parse_args()

    pkl_path = args.pickle

    animate_solution(pkl_path)

from ffpyplayer.player import MediaPlayer
import cv2
import os
from src.constants.variables import *
from src.sections.intelligent_obj import check_collision


def sound_track(frame_list):
    """
    Displays the output video of the Intelligent Objects with sound
    :param frame_list: List of frames
    :return: 0 if there is no problem. Otherwise -1 is returned
    """
    dirname = os.path.dirname(__file__)
    # Paths for the audio
    background_audio = dirname + '/' + AUDIO_BACK
    act_audio = dirname + '/' + AUDIO_ACT
    # Path to the video
    path_video = dirname + '/' + INTE_V_F + INTE_V
    # Players
    video = cv2.VideoCapture(path_video)
    player = MediaPlayer(background_audio)
    # Counter
    i = 0
    counter = 0
    # Boolean representing if the action sound is being used
    act = False
    while True:
        # Demo
        if demo_sound is True:
            # Arrow hit the Stickman
            if i is 5:
                act = True
                # Display the Action Sound
                player = MediaPlayer(act_audio)
            if counter is 6:
                player = MediaPlayer(background_audio)

        # Normal Execution
        else:
            # There are still frames to check
            if i < len(frame_list) and frame_list[i].arrow is not None:
                # Arrow hit the Stickman
                if check_collision(frame_list[i]):
                    act = True
                    # Display the Action Sound
                    player = MediaPlayer(act_audio)
            else:
                break
            # We played again the background sound after the action sound
            if counter is 15:
                act = False
                # Background sound
                player = MediaPlayer(background_audio)
        # Read the next video frame
        grabbed, frame = video.read()
        # Read the audio
        audio_frame, val = player.get_frame()
        if not grabbed:
            print("End of video")
            break
        if cv2.waitKey(300) & 0xFF == ord("q"):
            break
        cv2.imshow("Video", frame)
        # Check if the action sound is being played
        if act:
            # Action Sound counter
            counter += 1
        i += 1
    video.release()
    cv2.destroyAllWindows()
    return 0

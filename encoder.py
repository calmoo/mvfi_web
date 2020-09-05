import subprocess
import ntpath
import ffmpeg
import os

audio_filenames = []
save_file_destination = "media/processed/"


def encode_video_new(uploaded_files: dict) -> list:

    uploaded_audio_files = uploaded_files["audio_files"]
    uploaded_image_file = uploaded_files["image_file"]
    exported_video_list = []
    for audio_file in uploaded_audio_files:
        output_filepath = encode_video(audio_file, uploaded_image_file)
        exported_video_list.append(output_filepath)
    return exported_video_list


def fetch_file_name(filepath):
    return os.path.splitext(ntpath.basename(filepath))[0]


audio_file = "test.mp3"
image_file = "test.jpg"

fileset = {"audio_files": ["test.mp3", "test2.mp3"],
           "image_file": "test.jpg"}


def encode_video(audio_file, image_file):
    output_file_path = fetch_file_name(audio_file) + '.mp4'
    (
        ffmpeg
            .input(image_file, loop=1)
            .output(save_file_destination + output_file_path, tune='stillimage', acodec='aac', audio_bitrate='192k',
                    pix_fmt='yuv420p',
                    shortest=None)
            .global_args('-i', audio_file)
            .run(capture_stdout=True)
    )
    return output_file_path

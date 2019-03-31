from moviepy.video.io import ffmpeg_tools, VideoFileClip


def get_video_size_by_time(video_file):
    clip = VideoFileClip.VideoFileClip(video_file)
    clip_time = clip.duration
    clip.close()
    return clip_time


def cut_video(input_video, output_video, start_time=0, end_time=30):
    ffmpeg_tools.ffmpeg_extract_subclip(input_video, start_time, end_time, targetname=output_video)

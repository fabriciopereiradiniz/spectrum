from moviepy.editor import *
import pydub.silence as pydub_silence
from pydub import AudioSegment
import os

class VideoProcessor:
    OUTPUT_AUDIO_FILE = "extracted_audio.wav"

    def __init__(self, video_file):
        self.video_file = video_file

    def extract_audio(self):
        video_clip = VideoFileClip(self.video_file)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(self.OUTPUT_AUDIO_FILE)

    def remove_silence_segments(self, output_video_file):
        video_clip = VideoFileClip(self.video_file)
        audio_file = AudioSegment.from_file(self.OUTPUT_AUDIO_FILE)
        dBFS = audio_file.dBFS
        silence_segments = pydub_silence.detect_silence(audio_file, min_silence_len=1000, silence_thresh=dBFS - 16)

        silence_segments = [(start / 1000, stop / 1000) for start, stop in silence_segments]

        video_clips_to_keep = []
        last_end = 0

        for start, stop in silence_segments:

            if start > last_end:
                video_clips_to_keep.append(video_clip.subclip(last_end, start))
            last_end = stop

        if last_end < video_clip.duration:
            video_clips_to_keep.append(video_clip.subclip(last_end, video_clip.duration))

        final_video = concatenate_videoclips(video_clips_to_keep)

        try:
            final_video.write_videofile(output_video_file, codec="libx264")
            print(f"Vídeo de saída salvo em: {output_video_file}")
        except Exception as e:
            print(f"Erro ao salvar o vídeo de saída: {str(e)}")
        finally:
            if os.path.exists(self.OUTPUT_AUDIO_FILE):
                os.remove(self.OUTPUT_AUDIO_FILE)

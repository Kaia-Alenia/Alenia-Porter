import argparse
import sys
import os
from alenia_porter import media_engine

def print_progress(current, total):
    print(f"PROGRESS:{current}/{total}", flush=True)

def main():
    parser = argparse.ArgumentParser(description="Alenia Porter Headless Engine")
    parser.add_argument("input_dir", help="Directory to process")
    parser.add_argument("--vformat", default="webm", help="Target video format")
    parser.add_argument("--aformat", default="ogg", help="Target audio format")
    parser.add_argument("--iformat", default="webp", help="Target image format")
    parser.add_argument("--vextra", default="", help="Extra video arguments")
    parser.add_argument("--aextra", default="", help="Extra audio arguments")
    parser.add_argument("--iextra", default="", help="Extra image arguments")
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    
    def on_complete(processed_files, out_dir, total_orig, total_final):
        print(f"DONE:{processed_files}:{out_dir}", flush=True)

    def on_error(msg):
        print(f"ERROR:{msg}", flush=True)
        sys.exit(1)

    media_engine.convert_media(
        input_directory=input_dir,
        target_audio_format=args.aformat,
        target_video_format=args.vformat,
        target_image_format=args.iformat,
        video_extra_args=args.vextra,
        audio_extra_args=args.aextra,
        image_extra_args=args.iextra,
        recursive=True,
        preserve_structure=False,
        audio_bitrate="320k",
        video_crf="17",
        video_preset="slow",
        image_quality="100",
        audio_enabled=True,
        video_enabled=True,
        image_enabled=True,
        progress_update_callback=print_progress,
        status_update_callback=lambda msg: None,
        completion_callback=on_complete,
        error_callback=on_error,
        headless=True
    )

if __name__ == "__main__":
    main()

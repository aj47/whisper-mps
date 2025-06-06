from . import whisper
from .utils.ytdownloader import download_and_convert_to_mp3
import argparse
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
import json
import logging


parser = argparse.ArgumentParser(description="Automatic Speech Recognition")
parser.add_argument(
    "--file-name",
    required=False,
    type=str,
    help="Path to the audio file to be transcribed.",
)

parser.add_argument(
    "--model-name",
    required=False,
    default="tiny",
    type=str,
    help="Name of the whisper model size. (default: tiny)",
)

parser.add_argument(
    "--youtube-url",
    required=False,
    default=None,
    type=str,
    help="the address from Youtube,like: https://www.youtube.com/watch?v=jaM02mb6JFM",
)

parser.add_argument(
    "--output-file-name",
    required=False,
    default="output.json",
    type=str,
    help="the output file name for the transcribed text JSON",
)

parser.add_argument(
    "--initial_prompt",
    required=False,
    default=None,
    type=str,
    help="Optional text to provide as a prompt for the first window. This can be used to provide custom vocabularies or proper nouns to make it more likely to predict those words correctly. Example: 'custom vocab to know: TensorFlow, PyTorch, MLX'",
)

def worker(file_name, model_name, output_file_name, initial_prompt=None):
    with Progress(
        TextColumn("🤗 [progress.description]"),
        BarColumn(style="yellow1", pulse_style="white"),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task("[yellow]Transcribing...", total=None)
        # Pass initial_prompt to transcribe function if provided
        if initial_prompt:
            text = whisper.transcribe(file_name, model=model_name, initial_prompt=initial_prompt)
        else:
            text = whisper.transcribe(file_name, model=model_name)
        print(text)
        with open(output_file_name, "w", encoding="utf8") as fp:
            json.dump(text, fp, ensure_ascii=False)
        print(
            f"Voila!✨ Your file has been transcribed go check it out over here 👉 {output_file_name}"
        )

def main():
    args = parser.parse_args()
    file_name = args.file_name
    model_name = args.model_name
    youtube_url = args.youtube_url
    output_file_name = args.output_file_name
    initial_prompt = args.initial_prompt
    if not output_file_name.lower().endswith('.json'):
        output_file_name = output_file_name + '.json'
    if youtube_url is not None:
        print(f'start downloading audios: {args.youtube_url}')
        audio_path = download_and_convert_to_mp3(youtube_url)
        worker(audio_path, model_name, output_file_name, initial_prompt)
    else:
        if file_name is None:
            logging.error(f"local file_name should not be none!")
            return None
        worker(file_name, model_name, output_file_name, initial_prompt)


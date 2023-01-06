from pprint import pformat
import subprocess
import codecs
from typing import List
import os
import re
import logging
from pathlib import Path
import typer
import boto3
from pydub import AudioSegment
from rich.progress import track

# Create an Amazon Polly client
polly_client = boto3.client('polly')


def _convert_to_list_of_paragraphs(text):
    # Split the text on newline, be language agnostic
    paragraphs = re.split(r'[\r\n]+', text)

    # Remove empty strings
    paragraphs = [p for p in paragraphs if p.strip()]

    return paragraphs

def _polly(text, outfile: Path, voice='Salli'):
    # Call the synthesize_speech function
    response = polly_client.synthesize_speech(
        TextType='ssml',
        OutputFormat='mp3',
        VoiceId=voice,
        Text=text,
    )

    # Get the synthesized audio from the response
    audio_stream = response['AudioStream']

    # Write the synthesized audio to a file
    with outfile.open('wb') as f:
        f.write(audio_stream.read())

def run_on_file(
        infile: Path,
        outdir: Path,
        voice='Salli',
        paragraph_space_sec: int = 2
    ):
    logging.info("Processing file: %s", infile)

    # Read the file
    with infile.open() as f:
        text = f.read()

    # Convert the file to a list of paragraphs
    # We do that to preserve the character limits of the API
    list_of_paragraphs = _convert_to_list_of_paragraphs(text)
    outfiles: List[Path] = []

    for line in track(list_of_paragraphs, description=f"Converting {infile} to audio"):
        # Create the SSML text
        rendered = '<speak><amazon:effect name="drc">' + line.strip() + f'<break time="{paragraph_space_sec}s"/></amazon:effect></speak>'

        # Create the file name for this paragraph
        file_name = outdir / f'polly_out{len(outfiles):05}.mp3'
        outfiles.append(file_name)
        _polly(rendered, file_name, voice=voice)

    # Concatenate all the files
    outfile = outdir / infile
    outfile = outfile.with_suffix('.mp3')
    combined_audio = AudioSegment.empty()

    for file in track(outfiles, description=f"Concatenating files to {outfile}"):
        audio = AudioSegment.from_mp3(file)
        combined_audio += audio

    combined_audio.export(outfile, format='mp3')

    # Remove the temp files
    for file in track(outfiles, description=f"Removing temp files"):
        file.unlink()

    return outfile

def run_on_file_or_dir(
    infile_or_dir: Path,
    outdir: Path,
    voice='Salli',
    paragraph_space_sec: int = 2
):
    """
    Converts either a file or a directory of files to amazon polly audio.

    Files must already be converted to the file format described in the readme.

    Does not work recursively.

    If infile_or_dir is a directory, this will create a new file in outdir for each file in infile_or_dir with the same name and .mp3 extension.

    If infile_or_dir is a file, this will create a single file in outdir with the same name and .mp3 extension.
    """
    if infile_or_dir.is_file():
        return run_on_file(infile_or_dir, outdir, voice=voice, paragraph_space_sec=paragraph_space_sec)
    elif infile_or_dir.is_dir():
        if not outdir.is_dir():
            raise ValueError(f"Output directory does not exist: {outdir}")
        for file in infile_or_dir.iterdir():
            run_on_file(file, outdir, voice=voice, paragraph_space_sec=paragraph_space_sec)
    else:
        raise ValueError(f"Input file or directory does not exist: {infile_or_dir}")

if __name__=="__main__":
    typer.run(run_on_file_or_dir)
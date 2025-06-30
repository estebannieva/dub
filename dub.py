#!/usr/bin/env python3
import sys
import pysrt
import boto3
import tempfile
from pathlib import Path
from pydub import AudioSegment

def build_ssml(text: str, duration_ms: int) -> str:
    """
    Wrap text in SSML to enforce a maximum duration.
    Polly will adjust speech rate to fit the target window.
    """
    return (
        f'<speak>'
        f'<prosody amazon:max-duration="{duration_ms}ms">{text}</prosody>'
        f'</speak>'
    )

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 dub.py <subtitle.srt>")
        sys.exit(1)
    srt_file = Path(sys.argv[1])
    if not srt_file.exists():
        print(f"Error: {srt_file} not found.")
        sys.exit(1)

    subs = pysrt.open(str(srt_file))
    combined = AudioSegment.empty()

    # Initialize Polly client. AWS credentials read from env or ~/.aws/credentials and ~/.aws/config:
    #   export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
    #   export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    #   export AWS_DEFAULT_REGION="us-west-2"
    #
    # Example ~/.aws/credentials:
    #   [default]
    #   aws_access_key_id = AKIAIOSFODNN7EXAMPLE
    #   aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    #
    # Example ~/.aws/config:
    #   [default]
    #   region = us-west-2
    #   output = json
    polly = boto3.client('polly')

    with tempfile.TemporaryDirectory(prefix="dubs_") as tmpdir:
        tmpdir_path = Path(tmpdir)
        for sub in subs:
            duration_ms = sub.end.ordinal - sub.start.ordinal
            ssml = build_ssml(sub.text, duration_ms)

            resp = polly.synthesize_speech(
                TextType='ssml',
                Text=ssml,
                VoiceId='Conchita',
                Engine='neural',
                OutputFormat='mp3'
            )
            clip_path = tmpdir_path / f"{sub.index}.mp3"
            clip_path.write_bytes(resp['AudioStream'].read())
            combined += AudioSegment.from_file(clip_path)

        out_path = Path("audio.mp3")
        combined.export(out_path, format="mp3")

    # At this point, TemporaryDirectory is auto-deleted
    print("🚀 Done. Created:", out_path.name)

if __name__ == "__main__":
    main()

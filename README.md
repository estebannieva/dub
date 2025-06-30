# 🚀 Dubbing Tool

A simple tool that converts `.srt` subtitles into a single, fully synchronized audio file using Amazon Polly.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## AWS Credentials

```bash
export AWS_ACCESS_KEY_ID="AKIA…"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnF…"
export AWS_DEFAULT_REGION="us-west-2"
```

## Usage

```bash
python3 dub.py subtitle.srt
```

## Deactivate environment

```bash
deactivate
```

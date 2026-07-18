# 🎵 Cosmic Harmony Composer

AI music generator using an **LSTM neural network** (TensorFlow/Keras), trained and run entirely **locally — no external API, no API key, no internet dependency** for generation.

## Why no Claude/OpenAI/Google API key?
This is a generative deep-learning task, not a text/chat task — it doesn't call any LLM at all. The model is a small LSTM trained from scratch on musical note sequences (you provide/generate the training data), and MIDI export is handled by `music21`. Everything is free and open source.

## Features
- Trains a 2-layer LSTM (128 units each) on a sample cosmic musical corpus in ~30-60 seconds
- Generates 50-500 note original compositions
- Exports playable `.mid` files named after a cosmic theme (Nebula Dreams, Black Hole Mystery, etc.)
- Live training/generation progress indicators
- Download button for generated MIDI
- Space-themed responsive UI

## Setup

```bash
cd task3-cosmic-harmony-composer
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000**

1. Click **Train Model** (takes ~30-60 seconds on CPU)
2. Choose number of notes and click **Generate Cosmic Symphony**
3. Click **Download MIDI File**

## Playing the MIDI file
- **Windows**: Windows Media Player, or any DAW
- **Mac**: GarageBand, QuickTime
- **Linux**: Audacity, `fluidsynth`
- **Online**: onlinesequencer.net, musicxml.com

Convert to MP3 if needed:
```bash
fluidsynth -a alsa -m alsa_seq -F output.wav soundfont.sf2 input.mid
ffmpeg -i output.wav output.mp3
```

## Project Structure
```
task3-cosmic-harmony-composer/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/main.js
├── models/              (saved trained model + note mappings)
├── generated_music/     (output MIDI files)
└── README.md
```

## Tech Stack
- Backend: Flask
- Deep Learning: TensorFlow/Keras (LSTM)
- Music: Music21 (MIDI generation)
- Frontend: HTML/CSS/JavaScript, no frameworks

## Notes
- TensorFlow install is the heaviest dependency here (~500MB+). On low-resource machines, training still completes in well under a minute since the sample corpus is small.
- You can substitute your own MIDI files for richer training data — see `get_notes_from_sample_data()` in `app.py` for where to plug in real corpora (e.g. from freely licensed MIDI archives).

## License
MIT

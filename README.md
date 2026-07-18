# 🎵 Cosmic Harmony Composer

![Cosmic Harmony Banner](./docs/images/banner.svg)

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://tensorflow.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-green)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![No API Keys Required](https://img.shields.io/badge/No%20API%20Keys-Required-brightgreen)](.)

> **AI music generator using an LSTM neural network** — trained and run entirely **locally** with no external APIs, no API keys, and no internet dependency for generation.

---

## 🌟 Why This Is Different

Unlike ChatGPT, Claude, or Google's music APIs, **Cosmic Harmony Composer is a true deep-learning generative model**:

✅ **No LLM calls** — This is a specialized neural network for music, not a language model  
✅ **No API keys needed** — Train and generate entirely offline  
✅ **100% open source** — TensorFlow, Keras, and Music21  
✅ **Lightweight** — Trains in 30-60 seconds on CPU  
✅ **Privacy-first** — Your compositions never leave your machine  

---

## 🎨 Features at a Glance

| Feature | Details |
|---------|---------|
| **Neural Architecture** | 2-layer LSTM (128 units each) |
| **Training Speed** | ~30-60 seconds on CPU |
| **Generation Capacity** | 50–500 note compositions |
| **Output Format** | Playable `.mid` files |
| **Naming** | Auto-themed cosmic titles (Nebula Dreams, Black Hole Mystery, etc.) |
| **UI** | Space-themed, responsive, zero-framework |

---

## 🖥️ App Preview

![Dashboard Preview](./docs/images/dashboard-mockup.svg)
*Illustrative preview of the training and generation dashboard*

---

## ⚙️ How It Works

![Architecture Diagram](./docs/images/architecture.svg)
*From note corpus to downloadable MIDI — entirely on your machine*

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- ~500MB disk space (for TensorFlow)
- No internet required after installation

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/cosmic-harmony-composer.git
cd cosmic-harmony-composer

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open your browser to **http://localhost:5000** 🌌

---

## 🎼 How to Use

### Step 1: Train the Model
Click the **"Train Model"** button. The LSTM network will learn from a sample cosmic musical corpus in ~30-60 seconds.
Training Progress: ▓▓▓▓▓▓▓▓░░ 80% | Loss: 0.342
### Step 2: Generate a Symphony
1. Select the number of notes (50–500)
2. Click **"Generate Cosmic Symphony"**
3. Watch your original composition be created in real-time

### Step 3: Download & Play
Click **"Download MIDI File"** to save your unique composition. The file is automatically named after a cosmic theme.

---

## 🎵 Playing Your Compositions

| Platform | Tools | Notes |
|----------|-------|-------|
| **Windows** | Windows Media Player, GarageBand, DAWs | Direct MIDI support |
| **Mac** | GarageBand, QuickTime | Built-in MIDI player |
| **Linux** | Audacity, fluidsynth, VLC | Lightweight options |
| **Browser** | [Online Sequencer](https://onlinesequencer.net), [MusicXML](https://musicxml.com) | No installation needed |

### Convert to MP3 (Optional)
```bash
sudo apt-get install fluidsynth ffmpeg

fluidsynth -a alsa -m alsa_seq -F output.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 input.mid
ffmpeg -i output.wav -q:a 9 output.mp3
```

---

## 📁 Project Structure
cosmic-harmony-composer/
├── app.py                          # Flask backend & LSTM training
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                  # Web interface
├── static/
│   ├── css/style.css               # Space-themed styling
│   └── js/main.js                  # Interactive controls
├── models/                         # Saved LSTM models & mappings
├── generated_music/                # Output MIDI files
├── docs/
│   └── images/                     # README graphics
└── README.md                       # This file
---

## 🛠️ Tech Stack

**Backend:** Flask · TensorFlow/Keras (LSTM) · Music21 (MIDI)  
**Frontend:** HTML5 · CSS3 · Vanilla JavaScript (no frameworks)  
**Model:** 2-layer LSTM, 128 units each — optimal for small corpora

---

## 🎯 Customization

### Use Your Own MIDI Files

```python
# In app.py, find get_notes_from_sample_data()
def get_notes_from_sample_data():
    midi_files = glob("your_corpus/*.mid")  # Your MIDI collection
    return extract_notes(midi_files)
```

### Adjust Model Hyperparameters

```python
model = Sequential([
    LSTM(128, input_shape=(lookback, num_unique_notes), return_sequences=True),
    Dropout(0.2),
    LSTM(128, return_sequences=False),
    Dropout(0.2),
    Dense(num_unique_notes, activation='softmax')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy')
```

---

## 📊 Performance Notes

| Metric | Details |
|--------|---------|
| **Model Size** | ~2-5 MB (trained weights) |
| **Training Time** | 30–60 sec (CPU), 5–10 sec (GPU) |
| **Generation Time** | < 1 second per 100 notes |
| **Memory Usage** | ~150 MB during training, 50 MB idle |

> **Note:** TensorFlow is the largest dependency (~500MB+). On resource-constrained machines, training still completes in under a minute due to the small sample corpus.

---

## 🚀 Roadmap

- [ ] Web deployment (Heroku/Vercel with model caching)
- [ ] Advanced controls — tempo, key, instrument selection
- [ ] Multi-instrument polyphonic generation
- [ ] Audio visualization (waveform + spectral display)
- [ ] Export to MusicXML, MP3, WAV
- [ ] Community-contributed training corpus

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to your branch (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

---

## ⚠️ Troubleshooting

**`ModuleNotFoundError: No module named 'tensorflow'`**
```bash
pip install --upgrade tensorflow
```

**Port 5000 already in use**
```bash
python app.py --port 5001
```

**MIDI won't play** — Try [Online Sequencer](https://onlinesequencer.net), drag & drop your `.mid` file.

---

## 📄 License

Licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

Third-party: TensorFlow (Apache 2.0) · Flask (BSD 3-Clause) · Music21 (LGPL 3.0)

---

## 🌟 Show Your Support

If you find this project useful, please **⭐ Star** this repository!

---

<div align="center">

**Made with 🚀 and 🎵 for music lovers and AI enthusiasts**

</div>

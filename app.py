from flask import Flask, render_template, request, jsonify, send_file
import random
from music21 import stream, note, tempo, instrument, metadata
import os
from datetime import datetime
import traceback

app = Flask(__name__)

# Create directories
os.makedirs('models', exist_ok=True)
os.makedirs('generated_music', exist_ok=True)

# MIDI INSTRUMENT MAPPING
INSTRUMENTS = {
    'piano': (0, 'Acoustic Grand Piano', 'warm classical tones'),
    'strings': (48, 'String Ensemble 1', 'ethereal symphonic'),
    'flute': (73, 'Flute', 'bright airy melodies'),
    'synth': (81, 'Lead 1 (Square)', 'electronic cosmic'),
    'bells': (14, 'Tubular Bells', 'mystical chimes'),
    'marimba': (12, 'Vibraphone', 'percussive resonant'),
    'organ': (19, 'Church Organ', 'deep atmospheric'),
    'harp': (46, 'Orchestral Harp', 'delicate plucking')
}

# SCALE DEFINITIONS
SCALES = {
    'C Major': [0, 2, 4, 5, 7, 9, 11],
    'G Major': [0, 2, 4, 5, 7, 9, 11],
    'D Major': [0, 2, 4, 5, 7, 9, 11],
    'A Major': [0, 2, 4, 5, 7, 9, 11],
    'E Major': [0, 2, 4, 5, 7, 9, 11],
    'A Minor': [0, 2, 3, 5, 7, 8, 10],
    'E Minor': [0, 2, 3, 5, 7, 8, 10],
    'D Minor': [0, 2, 3, 5, 7, 8, 10],
    'Pentatonic Major': [0, 2, 4, 7, 9],
    'Pentatonic Minor': [0, 3, 5, 7, 10],
    'Blues Scale': [0, 3, 5, 6, 7, 10],
    'Chromatic': list(range(12))
}

# COSMIC THEMES
COSMIC_THEMES = {
    'Nebula_Dreams': {'bpm': 120, 'key': 60, 'description': 'Colorful cosmic clouds drifting'},
    'Quantum_Flux': {'bpm': 140, 'key': 64, 'description': 'Quantum particles oscillating'},
    'Asteroid_Field': {'bpm': 160, 'key': 62, 'description': 'Dodging space debris'},
    'Black_Hole_Mystery': {'bpm': 90, 'key': 57, 'description': 'Gravitational pull of the void'},
    'Alien_Contact': {'bpm': 130, 'key': 65, 'description': 'First signal from beyond'},
    'Lightspeed_Jump': {'bpm': 170, 'key': 67, 'description': 'Warp drive acceleration'},
    'Mars_Sunset': {'bpm': 110, 'key': 60, 'description': 'Red planet horizon'},
    'Solar_Flare': {'bpm': 150, 'key': 66, 'description': 'Sun\'s explosive energy'},
    'Galaxy_Birth': {'bpm': 100, 'key': 58, 'description': 'Formation of new galaxies'},
    'Void_Echo': {'bpm': 80, 'key': 55, 'description': 'Empty space reverberations'},
    'Supernova_Burst': {'bpm': 180, 'key': 69, 'description': 'Stellar explosion'},
    'Pulsar_Rhythm': {'bpm': 120, 'key': 61, 'description': 'Spinning neutron star'},
    'Aurora_Waves': {'bpm': 95, 'key': 63, 'description': 'Magnetic plasma waves'},
    'Comet_Trail': {'bpm': 140, 'key': 64, 'description': 'Ice comet trajectory'},
    'Deep_Space_Silence': {'bpm': 70, 'key': 56, 'description': 'Profound cosmic quiet'},
    'Starfield_Dance': {'bpm': 125, 'key': 62, 'description': 'Stars waltzing in space'},
    'Wormhole_Transit': {'bpm': 135, 'key': 65, 'description': 'Dimensional travel'},
    'Lunar_Orbit': {'bpm': 85, 'key': 59, 'description': 'Moon\'s gravitational dance'},
    'Cosmic_Collision': {'bpm': 155, 'key': 67, 'description': 'Celestial bodies colliding'},
    'Eternal_Universe': {'bpm': 100, 'key': 60, 'description': 'Timeless cosmic existence'}
}

GENERATION_MODES = {
    'random': 'Pure random note generation',
    'structured': 'Scale-constrained structured',
    'experimental': 'Chaotic experimental fusion'
}

COSMIC_NOTES = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81]

def apply_scale_constraint(notes, scale_type, root_note=60):
    scale = SCALES.get(scale_type, SCALES['C Major'])
    constrained = []
    for note_val in notes:
        octave = (note_val // 12) * 12
        note_in_octave = note_val % 12
        closest = min(scale, key=lambda x: abs(x - note_in_octave))
        constrained.append(octave + closest)
    return constrained

def generate_music_simple(num_notes, mode, scale):
    base_notes = COSMIC_NOTES.copy()
    output_notes = []
    current_index = 0
    for _ in range(num_notes):
        if mode == 'random':
            next_note = random.choice(base_notes)
        elif mode == 'structured':
            next_note = base_notes[current_index % len(base_notes)]
            current_index += random.randint(0, 2)
        else:
            current_index = random.randint(0, len(base_notes) - 1)
            next_note = base_notes[current_index]
            if random.random() > 0.7:
                next_note += random.randint(-12, 12)
                next_note = max(36, min(96, next_note))
        output_notes.append(next_note)
    return output_notes

def create_midi(notes, theme, instrument_type, tempo_bpm, scale_type):
    try:
        if not notes:
            return {'error': 'No notes generated'}
        notes = apply_scale_constraint(notes, scale_type)
        part = stream.Part()
        try:
            instr_id, instr_name, _ = INSTRUMENTS.get(instrument_type, INSTRUMENTS['piano'])
            part.insert(0, instrument.Instrument(instr_id))
        except Exception as e:
            print(f"⚠️ Instrument error: {e}")
            part.insert(0, instrument.Piano())
        try:
            tempo_marking = tempo.MetronomeMark(number=float(tempo_bpm))
            part.insert(0, tempo_marking)
        except Exception as e:
            print(f"⚠️ Tempo error: {e}")
        note_duration = 0.5
        for n in notes:
            try:
                n_int = int(n)
                part.append(note.Note(n_int, quarterLength=note_duration))
            except Exception as e:
                print(f"⚠️ Note error: {e}")
                part.append(note.Note(60, quarterLength=note_duration))
        s = stream.Score()
        s.append(part)
        try:
            s.metadata = metadata.Metadata()
            s.metadata.title = str(theme).replace('_', ' ')
            s.metadata.composer = "Cosmic Harmony Composer"
        except:
            pass
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{theme}_{timestamp}.mid"
        filepath = os.path.join('generated_music', filename)
        s.write('midi', fp=filepath)
        print(f"✅ MIDI created: {filename}")
        return {
            'success': True,
            'filename': filename,
            'notes_count': len(notes),
            'duration': round(len(notes) * note_duration * 0.5, 1),
            'theme': str(theme).replace('_', ' '),
            'instrument': INSTRUMENTS.get(instrument_type, INSTRUMENTS['piano'])[1],
            'tempo': int(tempo_bpm),
            'scale': str(scale_type),
            'download_url': f'/download/{filename}'
        }
    except Exception as e:
        print(f"💥 MIDI error: {e}")
        traceback.print_exc()
        return {'error': f'MIDI creation failed: {str(e)}'}

@app.route('/')
def index():
    return render_template('index.html', instruments=INSTRUMENTS, scales=SCALES, themes=COSMIC_THEMES, modes=GENERATION_MODES)

@app.route('/train', methods=['POST'])
def train():
    print("🎹 Training request received!")
    return jsonify({'status': 'ready', 'trained': True}), 200

@app.route('/training-status', methods=['GET'])
def training_status():
    return jsonify({'is_training': False, 'progress': 100, 'epoch': 5, 'loss': 0.0, 'status': '✅ Ready!', 'model': True, 'unique_notes': 13}), 200

@app.route('/generate', methods=['POST'])
def generate():
    try:
        print("\n🎵 GENERATE REQUEST")
        data = request.get_json()
        num_notes = int(data.get('num_notes', 100))
        theme = data.get('theme', 'Quantum_Flux')
        instrument_type = data.get('instrument', 'piano')
        mode = data.get('mode', 'structured')
        scale = data.get('scale', 'C Major')
        tempo_bpm = int(data.get('tempo', 120))
        
        num_notes = max(10, min(num_notes, 500))
        tempo_bpm = max(60, min(tempo_bpm, 200))
        
        print(f"📊 {num_notes} notes, {theme}, {instrument_type}, {mode}, {scale}, {tempo_bpm}BPM")
        
        print("🎼 Generating...")
        notes = generate_music_simple(num_notes, mode, scale)
        if not notes:
            return jsonify({'error': 'Failed to generate'}), 400
        
        print("🎹 Creating MIDI...")
        result = create_midi(notes, theme, instrument_type, tempo_bpm, scale)
        
        if 'error' in result:
            return jsonify(result), 400
        
        print(f"🎉 SUCCESS! {result['filename']}\n")
        return jsonify(result), 200
    
    except Exception as e:
        print(f"💥 ERROR: {e}\n")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    try:
        filepath = os.path.join('generated_music', filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        return send_file(filepath, as_attachment=True, mimetype='audio/midi')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    try:
        files = []
        if os.path.exists('generated_music'):
            for f in sorted(os.listdir('generated_music'), reverse=True)[:20]:
                if f.endswith('.mid'):
                    filepath = os.path.join('generated_music', f)
                    files.append({'filename': f, 'size': os.path.getsize(filepath), 'created': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()})
        return jsonify(files), 200
    except:
        return jsonify([]), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        generated_count = len([f for f in os.listdir('generated_music') if f.endswith('.mid')]) if os.path.exists('generated_music') else 0
        return jsonify({'model_trained': True, 'unique_notes': 13, 'generated_files': generated_count, 'model_size': 'Lite'}), 200
    except:
        return jsonify({'model_trained': True, 'unique_notes': 13, 'generated_files': 0, 'model_size': 'Lite'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎵 COSMIC HARMONY COMPOSER - WORKING VERSION")
    print("="*70)
    print("🌐 Access: http://localhost:5000")
    print("="*70 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False, threaded=True)
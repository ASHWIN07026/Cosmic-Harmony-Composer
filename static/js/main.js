// STATE MANAGEMENT
const state = {
    modelTrained: false,
    isTraining: false,
    lastResult: null,
    downloadHistory: []
};

// DOM ELEMENTS
const trainBtn = document.getElementById('train-btn');
const generateBtn = document.getElementById('generate-btn');
const themeSelect = document.getElementById('theme-select');
const instrumentSelect = document.getElementById('instrument-select');
const scaleSelect = document.getElementById('scale-select');
const modeSelect = document.getElementById('mode-select');
const tempoSlider = document.getElementById('tempo-slider');
const tempoValue = document.getElementById('tempo-value');
const notesSlider = document.getElementById('notes-slider');
const notesValue = document.getElementById('notes-value');
const resultSection = document.getElementById('result-section');
const downloadBtn = document.getElementById('download-btn');
const generateAgainBtn = document.getElementById('generate-again-btn');
const historyList = document.getElementById('history-list');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadStats();
    loadHistory();
    updateTempoBPM();
    updateNotesCount();
});

// EVENT LISTENERS
function setupEventListeners() {
    trainBtn.addEventListener('click', trainModel);
    generateBtn.addEventListener('click', generateMusic);
    downloadBtn.addEventListener('click', downloadMIDI);
    generateAgainBtn.addEventListener('click', resetForm);
    tempoSlider.addEventListener('input', updateTempoBPM);
    notesSlider.addEventListener('input', updateNotesCount);

    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            switchTab(e.target.dataset.tab);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter' && !state.isTraining) {
            generateMusic();
        }
        if (e.altKey && e.key === 't') {
            e.preventDefault();
            trainModel();
        }
    });
}

// TAB SWITCHING
function switchTab(tabName) {
    // Hide all tabs
    tabContents.forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from buttons
    tabBtns.forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Mark button as active
    event.target.classList.add('active');

    // Refresh stats when settings tab opened
    if (tabName === 'settings') {
        loadStats();
    }
    if (tabName === 'history') {
        loadHistory();
    }
}

// SLIDER UPDATES
function updateTempoBPM() {
    tempoValue.textContent = tempoSlider.value;
}

function updateNotesCount() {
    notesValue.textContent = notesSlider.value;
}

// TRAIN MODEL
async function trainModel() {
    if (state.isTraining) return;

    state.isTraining = true;
    trainBtn.disabled = true;
    trainBtn.textContent = '⏳ Training...';

    const trainStatus = document.getElementById('train-status');
    const progressFill = document.getElementById('progress-fill');
    const trainText = document.getElementById('train-text');

    try {
        const response = await fetch('/train', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) throw new Error('Training failed');

        // Poll for progress
        const pollInterval = setInterval(async () => {
            const statusResponse = await fetch('/training-status');
            const trainData = await statusResponse.json();

            progressFill.style.width = trainData.progress + '%';
            trainText.textContent = `${trainData.status} (Epoch ${trainData.epoch}/5)`;

            if (trainData.progress >= 100) {
                clearInterval(pollInterval);
                state.modelTrained = true;
                trainBtn.disabled = false;
                trainBtn.textContent = '✅ Model Trained!';
                generateBtn.disabled = false;
                
                // Pulse effect
                trainBtn.style.animation = 'pulse 0.5s ease-out';
                setTimeout(() => {
                    trainBtn.textContent = '🧠 Train Model';
                    trainBtn.style.animation = 'none';
                }, 500);

                loadStats();
                showNotification('Model trained successfully!', 'success');
            }
        }, 500);

    } catch (error) {
        console.error('Error:', error);
        trainText.textContent = '❌ Training failed: ' + error.message;
        showNotification('Training error: ' + error.message, 'error');
    } finally {
        state.isTraining = false;
        trainBtn.disabled = false;
        trainBtn.textContent = '🧠 Train Model';
    }
}

// GENERATE MUSIC
async function generateMusic() {
    if (!state.modelTrained) {
        showNotification('Please train the model first!', 'warning');
        return;
    }

    generateBtn.disabled = true;
    generateBtn.textContent = '⏳ Generating...';

    try {
        const generateData = {
            num_notes: parseInt(notesSlider.value),
            theme: themeSelect.value,
            instrument: instrumentSelect.value,
            scale: scaleSelect.value,
            mode: modeSelect.value,
            tempo: parseInt(tempoSlider.value)
        };

        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(generateData)
        });

        if (!response.ok) throw new Error('Generation failed');

        const result = await response.json();
        state.lastResult = result;

        // Display result
        displayResult(result);
        resultSection.style.display = 'block';
        resultSection.scrollIntoView({ behavior: 'smooth' });

        showNotification('✨ Music generated successfully!', 'success');
        loadHistory();

    } catch (error) {
        console.error('Error:', error);
        showNotification('Generation error: ' + error.message, 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = '✨ Generate Cosmic Symphony';
    }
}

// DISPLAY RESULT
function displayResult(result) {
    document.getElementById('result-theme').textContent = result.theme.replace(/_/g, ' ');
    document.getElementById('result-instrument').textContent = result.instrument;
    document.getElementById('result-scale').textContent = result.scale;
    document.getElementById('result-tempo').textContent = result.tempo;
    document.getElementById('result-duration').textContent = Math.ceil(result.duration);
    document.getElementById('result-notes').textContent = result.notes_count;
}

// DOWNLOAD MIDI
function downloadMIDI() {
    if (!state.lastResult) return;

    const filename = state.lastResult.filename;
    const link = document.createElement('a');
    link.href = `/download/${filename}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showNotification('📥 MIDI file downloaded!', 'success');
}

// RESET FORM
function resetForm() {
    notesSlider.value = 100;
    tempoSlider.value = 120;
    updateNotesCount();
    updateTempoBPM();
    resultSection.style.display = 'none';
}

// LOAD HISTORY
async function loadHistory() {
    try {
        const response = await fetch('/history');
        const files = await response.json();

        if (files.length === 0) {
            historyList.innerHTML = '<p class="empty-state">No compositions yet. Generate some music first!</p>';
            return;
        }

        historyList.innerHTML = files.map(file => `
            <div class="history-item">
                <div class="history-item-title">🎵 ${file.filename.split('_')[0].replace(/([A-Z])/g, ' $1')}</div>
                <div class="history-item-meta">
                    📁 ${(file.size / 1024).toFixed(1)} KB<br>
                    📅 ${new Date(file.created).toLocaleDateString()}
                </div>
                <div class="button-group">
                    <button class="btn btn-info" onclick="downloadFile('${file.filename}')">
                        📥 Download
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// LOAD STATS
async function loadStats() {
    try {
        const response = await fetch('/stats');
        const stats = await response.json();

        document.getElementById('stat-model').textContent = stats.model_trained ? '✅ Trained' : '❌ Not Trained';
        document.getElementById('stat-notes').textContent = stats.unique_notes;
        document.getElementById('stat-files').textContent = stats.generated_files;
        document.getElementById('stat-size').textContent = stats.model_size;
        
        // Update header badge
        document.getElementById('model-status').textContent = stats.model_trained ? '✅ Ready' : '⚠️ Train First';
        document.getElementById('files-count').textContent = `📁 ${stats.generated_files} Files`;

        if (stats.model_trained) {
            generateBtn.disabled = false;
            state.modelTrained = true;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// HELPER FUNCTIONS
function downloadFile(filename) {
    const link = document.createElement('a');
    link.href = `/download/${filename}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showNotification('📥 File downloaded!', 'success');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#00ff88' : type === 'error' ? '#ff4444' : '#0088ff'};
        color: #0a0e27;
        border-radius: 8px;
        font-weight: 700;
        z-index: 9999;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add styles for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
`;
document.head.appendChild(style);

// Load stats on page load
loadStats();
// app.js

// utilities: show/hide
const show = el => el.classList.remove('hidden');
const hide = el => el.classList.add('hidden');

// element refs & state
const grid = document.getElementById('grid');
const disclaimer = document.getElementById('disclaimer-section');
const hero = document.getElementById('hero');
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const chooseBtn = document.getElementById('chooseFileBtn');
const uploadBtn = document.getElementById('uploadBtn');
const imgPreview = document.getElementById('imgPreview');

const resultCon = document.getElementById('resultContainer');
const rawOutput = document.getElementById('rawOutput');
const translateBtn = document.getElementById('translateBtn');
const transOutput = document.getElementById('translatedOutput');
const ttsSection = document.getElementById('ttsSection');
const ttsBtn = document.getElementById('ttsBtn');
const ttsAudio = document.getElementById('ttsAudio');
const backBtn = document.getElementById('backBtn');
const langSelect = document.getElementById('langSelect');
const previewSection = document.getElementById('previewSection');
const outlinedImage = document.getElementById('outlinedImage');
const lineOutputs = document.getElementById('lineOutputs');
const loadingOverlay = document.getElementById('loadingOverlay');
const coordTooltip = document.getElementById('coord-tooltip');
const transTooltip = document.getElementById('trans-tooltip');
const detectedLangContainer = document.getElementById('detectedLangContainer');
const detectedLangOutput = document.getElementById('detectedLangOutput');

let selectedFile = null;




// Theme management

function initTheme() {
  let theme = null;

  // Check for the theme in the URL first.
  const urlParams = new URLSearchParams(window.location.search);
  const themeFromUrl = urlParams.get('theme');

  if (themeFromUrl === 'dark' || themeFromUrl === 'light') {
    theme = themeFromUrl;
    // If we get a theme from the URL, save it to this page's own localStorage.
    localStorage.setItem('theme', theme);
  }

  // If not in the URL, check this page's localStorage.
  if (!theme) {
    theme = localStorage.getItem('theme');
  }

  // If still no theme, fall back to the user's system preference.
  if (!theme) {
    theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  // Apply the final theme to the page.
  document.documentElement.setAttribute('data-theme', theme);
  updateThemeIcon(theme);
}

function toggleTheme() {
  const curr = document.documentElement.getAttribute('data-theme');
  const next = curr === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  const sun = 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z';
  const moon = 'M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z';
  document.querySelectorAll('#themeIcon path').forEach(path => {
    path.setAttribute('d', theme === 'dark' ? moon : sun)
  });
}

// expose toggleTheme globally for inline onclick
window.toggleTheme = toggleTheme;

//Model selection & drop-zone
grid.addEventListener('click', (e) => {
  // Check if a clickable section or its child was clicked
  if (e.target.closest('.clickable-section')) {
    hide(hero);
    hide(grid);
    show(dropZone);
    show(disclaimer); // Show the disclaimer section
    show(langSelectContainer); // Show the language selector
  }
});
// dragenter/dragover highlight
['dragenter', 'dragover'].forEach(evt =>
  dropZone.addEventListener(evt, e => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  })
);

// dragleave/drop & file-picker → prepareFiles
['dragleave', 'drop'].forEach(evt =>
  dropZone.addEventListener(evt, e => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.type === 'drop') prepareFiles(e.dataTransfer.files)
  })
);

chooseBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', () => prepareFiles(fileInput.files));

// Preview & submit 

function prepareFiles(files) {
  if (!files.length) return;
  selectedFile = files[0];
  imgPreview.src = URL.createObjectURL(selectedFile);
  imgPreview.onload = () => URL.revokeObjectURL(imgPreview.src);
  show(imgPreview);
  show(uploadBtn);
}
async function detectLanguage(text) {
  if (!text || !text.trim()) {
    hide(detectedLangContainer);
    return;
  }
  try {
    const res = await fetch('/api/detect-language', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });

    if (!res.ok) {
      throw new Error(`API error: ${res.status}`);
    }

    const data = await res.json();
    const confidence = (data.score * 100).toFixed(1);
    detectedLangOutput.textContent = `Auto-Detected: ${data.detectedLanguage} `;
    show(detectedLangContainer);

  } catch (err) {
    console.error("Language detection failed:", err);
    hide(detectedLangContainer);
  }
}

uploadBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  hide(uploadBtn);
  hide(imgPreview);
  hide(dropZone);
  show(loadingOverlay); // show loader here

  const form = new FormData();
  form.append('file', selectedFile);
  form.append('lang', langSelect.value);

  try {
    const res = await fetch('/api/ocr', { method: 'POST', body: form });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();


    rawOutput.textContent = data.text;
    lineOutputs.innerHTML = data.lines
      .map((l, i) => `<div class="line-box">${i + 1}: ${l}</div>`).join('');

    outlinedImage.src = data.image; // already fixed key
    show(outlinedImage);

    lineOutputs.innerHTML = data.lines.map((line, i) => {
      const coords = JSON.stringify(line.coordinates);
      const sanitizedText = line.text.replace(/"/g, '&quot;');

      return `<div class="line-box" data-coords='${coords}' data-text="${sanitizedText}">
                    <span class="original-text">${i + 1}: ${line.text}</span>
                    <span class="translated-text"></span>
                </div>`;
    }).join('');

   
    // This section now checks the dropdown and decides what to display.
    const selectedLangValue = langSelect.value;
    const selectedLangText = langSelect.options[langSelect.selectedIndex].text;

    if (selectedLangValue === "") {
      // If "Auto Detect" is selected, call the detection API
      await detectLanguage(data.text);
    } else {
      // If a specific language is selected, just display the user's choice
      detectedLangOutput.textContent = `Language: User Selected (${selectedLangText})`;
      show(detectedLangContainer);
    }
    

    show(previewSection);
    show(resultCon);
    // Always show the TTS section so the button is visible
    show(ttsSection);

  } catch (err) {
    alert('Upload failed: ' + err.message);
    show(dropZone);
  } finally {
    hide(loadingOverlay); // always hide overlay
    hide(langSelectContainer);
  }
});

// Image Zoom Modal Logic 
const zoomModal = document.getElementById('zoomModal');
if (zoomModal) {
  const outlinedImage = document.getElementById('outlinedImage'); // The small result image
  const zoomedInImage = document.getElementById('zoomedInImage'); // The large image in the modal
  const modalCloseBtn = document.querySelector('.modal-close-btn');

  // Open the modal when the result image is clicked
  outlinedImage.addEventListener('click', () => {
    if (outlinedImage.src) {
      zoomedInImage.src = outlinedImage.src;
      show(zoomModal);
    }
  });

  // Function to close the modal
  const closeModal = () => hide(zoomModal);

  // Close when the 'X' button is clicked
  modalCloseBtn.addEventListener('click', closeModal);

  // Close when the dark background area is clicked
  zoomModal.addEventListener('click', (e) => {
    if (e.target === zoomModal) {
      closeModal();
    }
  });
}

// Interactive Translations 

// The on-demand translation function remains the same
async function getLineTranslation(lineBox) {
  if (lineBox.dataset.translation) {
    return lineBox.dataset.translation;
  }
  const textToTranslate = lineBox.dataset.text;
  if (!textToTranslate) return null;

  lineBox.dataset.translation = 'Translating...';
  try {
    const res = await fetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: textToTranslate, target: 'en' })
    });
    if (!res.ok) throw new Error('API error');
    const { translatedText } = await res.json();
    lineBox.dataset.translation = translatedText;
    return translatedText;
  } catch (err) {
    delete lineBox.dataset.translation;
    return 'Translation failed';
  }
}


if (lineOutputs) {
  lineOutputs.addEventListener('mouseover', async e => {
    const lineBox = e.target.closest('.line-box');
    if (!lineBox) return;

    // Show coordinate tooltip
    if (coordTooltip && lineBox.dataset.coords) {
      const coords = JSON.parse(lineBox.dataset.coords);
      const formattedCoords = coords.map(p => `[${Math.round(p[0])}, ${Math.round(p[1])}]`).join(', ');
      coordTooltip.textContent = `Coords: ${formattedCoords}`;
      show(coordTooltip);
    }

    // Populate the translation span if it's empty
    const translatedSpan = lineBox.querySelector('.translated-text');
    if (translatedSpan && !translatedSpan.textContent) {
      translatedSpan.textContent = await getLineTranslation(lineBox);
    }
  });

  // Update coordinate tooltip position
  lineOutputs.addEventListener('mousemove', e => {
    if (coordTooltip) {
      coordTooltip.style.left = `${e.clientX + 15}px`;
      coordTooltip.style.top = `${e.clientY + 15}px`;
    }
  });

  // Hide coordinate tooltip on exit
  lineOutputs.addEventListener('mouseout', () => {
    if (coordTooltip) hide(coordTooltip);
  });
}
// Translate & TTS 

translateBtn.addEventListener('click', async () => {
  const res = await fetch('/api/translate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: rawOutput.textContent, target: 'en' })
  });
  const { translatedText } = await res.json();
  transOutput.textContent = translatedText;
  show(transOutput);
  show(document.querySelector('button[data-copy="#translatedOutput"]'));
  show(document.querySelector('button[data-download="#translatedOutput"]'));
});

ttsBtn.addEventListener('click', async () => {
  const textToSpeak = transOutput.textContent || rawOutput.textContent;
  if (!textToSpeak) {
    alert("No text to generate speech from.");
    return;
  }
  const res = await fetch('/api/tts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: textToSpeak })
  });
  if (!res.ok) {
    alert(`Error generating speech: ${res.statusText}`);
    return;
  }
  const blob = await res.blob();
  ttsAudio.src = URL.createObjectURL(blob);
  ttsAudio.play();
  show(ttsAudio);
});


//  Copy, Download & Back 

resultCon.addEventListener('click', e => {
  let btn;
  if (btn = e.target.closest('button[data-copy]')) {
    const txt = document.querySelector(btn.dataset.copy).textContent;
    navigator.clipboard.writeText(txt);
  }
  if (btn = e.target.closest('button[data-download]')) {
    const txt = document.querySelector(btn.dataset.download).textContent;
    const blob = new Blob([txt], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = btn.dataset.filename;
    a.click();
    URL.revokeObjectURL(url);
  }
});

backBtn.addEventListener('click', () => {
  hide(resultCon);
  hide(ttsSection);
  hide(transOutput);
  // Added this line to hide the language section when going back
  hide(detectedLangContainer);
  hide(document.getElementById('langSelectContainer')); // hide when going back
  rawOutput.textContent = '';
  transOutput.textContent = '';
  show(dropZone);
  hide(disclaimer);
});


// ─── Initialize ──────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', initTheme);
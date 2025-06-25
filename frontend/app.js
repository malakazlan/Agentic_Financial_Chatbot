// --- Tab Switching ---
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');
tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    tabs.forEach(t => t.classList.remove('active'));
    tabContents.forEach(tc => tc.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(tab.dataset.tab + '-section').classList.add('active');
  });
});

// --- Loading Indicator ---
function showLoading(show) {
  document.getElementById('loading').style.display = show ? 'flex' : 'none';
}

// --- Chat Logic ---
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatHistory = document.getElementById('chat-history');
let chatMessages = [];

function renderChat() {
  chatHistory.innerHTML = '';
  chatMessages.forEach(msg => {
    const div = document.createElement('div');
    div.className = 'chat-message ' + msg.role;
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = msg.text;
    div.appendChild(bubble);
    if (msg.image) {
      const img = document.createElement('img');
      img.src = msg.image;
      img.alt = 'Portfolio Plot';
      img.style.maxWidth = '100%';
      img.style.marginTop = '0.5rem';
      div.appendChild(img);
    }
    chatHistory.appendChild(div);
  });
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const userText = chatInput.value.trim();
  if (!userText) return;
  chatMessages.push({ role: 'user', text: userText });
  renderChat();
  chatInput.value = '';
  showLoading(true);
  try {
    const formData = new FormData();
    formData.append('user_input', userText);
    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    chatMessages.push({ role: 'bot', text: data.response, image: data.image });
    renderChat();
  } catch (err) {
    chatMessages.push({ role: 'bot', text: 'Error: Could not reach backend.' });
    renderChat();
  }
  showLoading(false);
});

// --- Document Analysis Logic ---
const uploadForm = document.getElementById('upload-form');
const pdfUpload = document.getElementById('pdf-upload');
const reportSummary = document.getElementById('report-summary');
const reportQueryForm = document.getElementById('report-query-form');
const reportQueryInput = document.getElementById('report-query-input');
const reportAnswer = document.getElementById('report-answer');

uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!pdfUpload.files.length) return;
  showLoading(true);
  reportSummary.textContent = '';
  reportAnswer.textContent = '';
  reportQueryForm.style.display = 'none';
  const formData = new FormData();
  formData.append('file', pdfUpload.files[0]);
  try {
    const res = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    reportSummary.textContent = data.summary;
    reportQueryForm.style.display = 'flex';
  } catch (err) {
    reportSummary.textContent = 'Error: Could not upload or process PDF.';
  }
  showLoading(false);
});

reportQueryForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const query = reportQueryInput.value.trim();
  if (!query) return;
  showLoading(true);
  reportAnswer.textContent = '';
  const formData = new FormData();
  formData.append('query', query);
  try {
    const res = await fetch('http://localhost:8000/report-query', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    reportAnswer.textContent = data.answer;
  } catch (err) {
    reportAnswer.textContent = 'Error: Could not query the report.';
  }
  showLoading(false);
}); 
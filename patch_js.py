import re

with open('static/js/prediction.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace top part
new_top = """document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    if (!form) return;
    
    const brandSelect = document.getElementById('brand');
    const modelSelect = document.getElementById('model');
    const processorSelect = document.getElementById('processor');
    const ramSelect = document.getElementById('ram');
    const storageSelect = document.getElementById('storage');
    const displaySelect = document.getElementById('display');
    const networkSelect = document.getElementById('network');
    
    const resultContainer = document.getElementById('result-container');
    const livePreviewPanel = document.getElementById('live-preview-panel');
    const predictBtn = document.getElementById('predict-btn');
    const saveBtn = document.getElementById('save-btn');
    const phoneSilhouette = document.getElementById('phone-silhouette');
    const brandIcon = document.getElementById('preview-brand-icon');
    let chartInstance = null;
    let currentPredictionData = null;

    // Brand Icons map
    const brandIcons = {
        'Apple': 'fa-brands fa-apple',
        'Samsung': 'fa-brands fa-android',
        'Google': 'fa-brands fa-google',
        'OnePlus': 'fa-brands fa-android',
        'Xiaomi': 'fa-brands fa-android',
        'Motorola': 'fa-brands fa-android'
    };

    // Live Preview update function
    function updateLivePreview(field, value, suffix = '') {
        const idMap = {
            'Display Type': 'Display_Type',
            'Battery Capacity': 'Battery_Capacity',
            'Fast Charging': 'Fast_Charging',
            'Rear Camera': 'Rear_Camera',
            'Current Market Price': 'Current_Market_Price'
        };
        
        const elemId = idMap[field] || field;
        const target = document.getElementById(\prev-\\);
        if (!target) return;

        const li = target.closest('li');
        
        if (value && String(value).trim() !== '') {
            const displayValue = suffix ? \\\\ : value;
            if (target.textContent !== displayValue) {
                target.textContent = displayValue;
                target.classList.remove('updated');
                void target.offsetWidth; // trigger reflow
                target.classList.add('updated');
            }
            li.classList.add('filled');
            phoneSilhouette.classList.add('active');
        } else {
            target.textContent = '--';
            li.classList.remove('filled');
        }
        
        if (field === 'Brand' && value) {
            brandIcon.className = brandIcons[value] || 'fa-solid fa-mobile-screen';
        }
    }

    // Attach listeners to inputs
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        const ev = input.tagName.toLowerCase() === 'select' ? 'change' : 'input';
        input.addEventListener(ev, (e) => {
            let suffix = '';
            if (input.name === 'RAM' || input.name === 'Storage') suffix = ' GB';
            if (input.name === 'Battery Capacity') suffix = ' mAh';
            if (input.name === 'Fast Charging') suffix = ' W';
            if (input.name === 'Rear Camera') suffix = ' MP';
            
            updateLivePreview(input.name, e.target.value, suffix);
        });
    });

    // Brand logic
    brandSelect.addEventListener('change', () => {
        const brand = brandSelect.value;
        const models = window.FULL_MAP[brand] || {};
        
        modelSelect.innerHTML = '<option value="" disabled selected>Select a model...</option>';
        Object.keys(models).forEach(mod => {
            const option = document.createElement('option');
            option.value = mod;
            option.textContent = mod;
            modelSelect.appendChild(option);
        });
        modelSelect.disabled = false;
        
        processorSelect.disabled = true; processorSelect.innerHTML = '<option value="" disabled selected>Select model first...</option>';
        ramSelect.disabled = true; ramSelect.innerHTML = '<option value="" disabled selected>...</option>';
        storageSelect.disabled = true; storageSelect.innerHTML = '<option value="" disabled selected>...</option>';
        displaySelect.disabled = true; displaySelect.innerHTML = '<option value="" disabled selected>...</option>';
        networkSelect.disabled = true; networkSelect.innerHTML = '<option value="" disabled selected>...</option>';
        
        updateLivePreview('Brand', brand);
        updateLivePreview('Model', '');
        updateLivePreview('Processor', '');
        updateLivePreview('RAM', '');
        updateLivePreview('Storage', '');
        updateLivePreview('Display Type', '');
    });

    // Model logic
    modelSelect.addEventListener('change', () => {
        const brand = brandSelect.value;
        const model = modelSelect.value;
        const data = window.FULL_MAP[brand][model];
        
        processorSelect.innerHTML = \<option value="\" selected>\</option>\;
        processorSelect.disabled = false;
        
        displaySelect.innerHTML = \<option value="\" selected>\</option>\;
        displaySelect.disabled = false;
        
        networkSelect.innerHTML = \<option value="\" selected>\</option>\;
        networkSelect.disabled = false;
        
        ramSelect.innerHTML = '<option value="" disabled selected>Select...</option>';
        data.RAM.forEach(r => {
            const option = document.createElement('option');
            option.value = r; option.textContent = \\ GB\;
            ramSelect.appendChild(option);
        });
        ramSelect.disabled = false;
        
        storageSelect.innerHTML = '<option value="" disabled selected>Select...</option>';
        data.Storage.forEach(s => {
            const option = document.createElement('option');
            option.value = s; option.textContent = \\ GB\;
            storageSelect.appendChild(option);
        });
        storageSelect.disabled = false;
        
        updateLivePreview('Model', model);
        updateLivePreview('Processor', data.Processor);
        updateLivePreview('Display Type', data['Display Type']);
        updateLivePreview('RAM', '');
        updateLivePreview('Storage', '');
    });

    // Form Submission
    form.addEventListener('submit', async (e) => {
"""

content = re.sub(r'document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{.*?// Form Submission\s*form\.addEventListener\(\'submit\', async \(e\) => \{', new_top, content, flags=re.DOTALL | re.MULTILINE)

with open('static/js/prediction.js', 'w', encoding='utf-8') as f:
    f.write(content)

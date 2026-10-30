document.addEventListener('DOMContentLoaded', () => {
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

    const brandIcons = {
        'Apple': 'fa-brands fa-apple',
        'Samsung': 'fa-brands fa-android',
        'Google': 'fa-brands fa-google',
        'OnePlus': 'fa-brands fa-android',
        'Xiaomi': 'fa-brands fa-android',
        'Motorola': 'fa-brands fa-android'
    };

    function updateLivePreview(field, value, suffix = '') {
        const idMap = {
            'Display Type': 'Display_Type',
            'Battery Capacity': 'Battery_Capacity',
            'Fast Charging': 'Fast_Charging',
            'Rear Camera': 'Rear_Camera',
            'Current Market Price': 'Current_Market_Price'
        };
        
        const elemId = idMap[field] || field;
        const target = document.getElementById(`prev-${elemId}`);
        if (!target) return;

        const li = target.closest('li');
        
        if (value && String(value).trim() !== '') {
            const displayValue = suffix ? `${value}${suffix}` : value;
            if (target.textContent !== displayValue) {
                target.textContent = displayValue;
                target.classList.remove('updated');
                void target.offsetWidth;
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

    modelSelect.addEventListener('change', () => {
        const brand = brandSelect.value;
        const model = modelSelect.value;
        const variants = window.FULL_MAP[brand][model];
        
        ramSelect.innerHTML = '<option value="" disabled selected>Select RAM...</option>';
        const uniqueRams = [...new Set(variants.map(v => v.RAM))];
        uniqueRams.forEach(r => {
            const option = document.createElement('option');
            option.value = r; option.textContent = `${r} GB`;
            ramSelect.appendChild(option);
        });
        ramSelect.disabled = false;
        
        storageSelect.innerHTML = '<option value="" disabled selected>Select RAM first...</option>';
        storageSelect.disabled = true;
        
        processorSelect.innerHTML = '<option value="" disabled selected>Auto-filled...</option>';
        processorSelect.disabled = true;
        displaySelect.innerHTML = '<option value="" disabled selected>Auto-filled...</option>';
        displaySelect.disabled = true;
        networkSelect.innerHTML = '<option value="" disabled selected>Auto-filled...</option>';
        networkSelect.disabled = true;
        
        updateLivePreview('Model', model);
        updateLivePreview('Processor', '');
        updateLivePreview('Display Type', '');
        updateLivePreview('Network', '');
        updateLivePreview('RAM', '');
        updateLivePreview('Storage', '');
    });

    ramSelect.addEventListener('change', () => {
        const brand = brandSelect.value;
        const model = modelSelect.value;
        const selectedRam = parseFloat(ramSelect.value);
        if(!model) return;
        
        const variants = window.FULL_MAP[brand][model];
        const validVariants = variants.filter(v => v.RAM === selectedRam);
        
        storageSelect.innerHTML = '<option value="" disabled selected>Select Storage...</option>';
        const uniqueStorages = [...new Set(validVariants.map(v => v.Storage))];
        uniqueStorages.forEach(s => {
            const option = document.createElement('option');
            option.value = s; option.textContent = `${s} GB`;
            storageSelect.appendChild(option);
        });
        storageSelect.disabled = false;
        
        processorSelect.innerHTML = '<option value="" disabled selected>Auto-filled...</option>';
        displaySelect.innerHTML = '<option value="" disabled selected>Auto-filled...</option>';
        networkSelect.innerHTML = '<option value="" disabled selected>Auto-filled...</option>';
        
        updateLivePreview('Storage', '');
        updateLivePreview('Processor', '');
    });
    
    storageSelect.addEventListener('change', () => {
        const brand = brandSelect.value;
        const model = modelSelect.value;
        const selectedRam = parseFloat(ramSelect.value);
        const selectedStorage = parseFloat(storageSelect.value);
        if(!model || !selectedRam) return;
        
        const variants = window.FULL_MAP[brand][model];
        const variant = variants.find(v => v.RAM === selectedRam && v.Storage === selectedStorage);
        
        if (variant) {
            processorSelect.innerHTML = `<option value="${variant.Processor}" selected>${variant.Processor}</option>`;
            processorSelect.disabled = false;
            displaySelect.innerHTML = `<option value="${variant['Display Type']}" selected>${variant['Display Type']}</option>`;
            displaySelect.disabled = false;
            networkSelect.innerHTML = `<option value="${variant.Network}" selected>${variant.Network}</option>`;
            networkSelect.disabled = false;
            
            updateLivePreview('Processor', variant.Processor);
            updateLivePreview('Display Type', variant['Display Type']);
            updateLivePreview('Network', variant.Network);
            // Storage and RAM updates are already handled by the generic input loop at the top
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        predictBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
        predictBtn.disabled = true;
        document.getElementById('full-screen-scanner').style.display = 'block';
        resultContainer.style.display = 'none';
        resultContainer.style.opacity = '0';

        try {
            const res = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await res.json();
            
            await new Promise(r => setTimeout(r, 1500));
            
            if (!res.ok) throw new Error(result.error || 'Prediction failed');
            
            document.getElementById('full-screen-scanner').style.display = 'none';
            livePreviewPanel.style.display = 'none';
            
            renderResult(data, result.prediction, result.alternatives);
            
        } catch (error) {
            console.error(error);
            document.getElementById('full-screen-scanner').style.display = 'none';
            alert("An error occurred during prediction.");
        } finally {
            predictBtn.innerHTML = 'Analyze Price <i class="fa-solid fa-wand-magic-sparkles"></i>';
            predictBtn.disabled = false;
        }
    });

    function renderResult(inputs, prediction, alternatives) {
        currentPredictionData = { ...inputs, ...prediction };
        
        saveBtn.innerHTML = '<i class="fa-regular fa-bookmark"></i> Save';
        saveBtn.disabled = false;
        
        const modelName = inputs.Model ? `${inputs.Brand} ${inputs.Model}` : inputs.Brand;
        document.getElementById('res-model').textContent = modelName;
        
        document.getElementById('res-fair-price').textContent = `₹${prediction['Predicted Fair Price'].toLocaleString()}`;
        document.getElementById('res-current-price').textContent = `₹${prediction['Current Price'].toLocaleString()}`;
        
        const badge = document.getElementById('res-badge');
        badge.textContent = prediction.Recommendation;
        
        if (prediction['Overpriced Percentage'] < -5) {
            badge.style.background = 'rgba(63, 93, 69, 0.1)';
            badge.style.color = 'var(--accent-secondary)'; 
        } else if (prediction['Overpriced Percentage'] < 15) {
            badge.style.background = 'rgba(217, 164, 65, 0.1)';
            badge.style.color = 'var(--accent-highlight)'; 
        } else {
            badge.style.background = 'rgba(155, 59, 50, 0.1)';
            badge.style.color = 'var(--danger)'; 
        }

        document.getElementById('res-confidence').textContent = `${prediction.Confidence}%`;

        renderChart(prediction['Current Price'], prediction['Predicted Fair Price']);

        const altContainer = document.getElementById('alternatives-grid');
        altContainer.innerHTML = '';
        if (alternatives && alternatives.length > 0) {
            altContainer.style.maxHeight = '450px';
            altContainer.style.overflowY = 'auto';
            altContainer.style.paddingRight = '8px';
            alternatives.forEach((alt, index) => {
                const isTopPick = index < 3;
                const borderStyle = isTopPick ? '2px solid var(--accent-primary)' : '1px solid var(--border-divider)';
                const glowStyle = isTopPick ? 'box-shadow: 0 4px 12px rgba(217, 164, 65, 0.15);' : '';
                const badgeHtml = isTopPick ? `<span style="display: inline-block; margin-left: 8px; background: rgba(217, 164, 65, 0.15); color: var(--accent-highlight); padding: 2px 8px; border-radius: 12px; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; vertical-align: middle;"><i class="fa-solid fa-star" style="font-size: 0.6rem; margin-right: 3px;"></i>Top Pick</span>` : '';
                
                altContainer.innerHTML += `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 1.25rem; border: ${borderStyle}; border-radius: 12px; background: var(--bg-color); transition: var(--transition-fast); ${glowStyle}">
                        <div>
                            <div style="display: flex; align-items: center; margin-bottom: 0.25rem;">
                                <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent-secondary); text-transform: uppercase; letter-spacing: 0.05em;">${alt.Brand}</span>
                                ${badgeHtml}
                            </div>
                            <h4 style="margin-bottom: 0.5rem; font-size: 1.1rem;">${alt.Model}</h4>
                            <ul style="font-size: 0.85rem; color: var(--text-secondary); padding-left: 1.25rem; list-style-type: square; line-height: 1.4;">
                                ${alt.Pros.map(p => `<li>${p}</li>`).join('')}
                            </ul>
                        </div>
                        <div style="text-align: right; background: var(--card-surface); padding: 1rem; border-radius: 8px; box-shadow: var(--shadow-sm); min-width: 120px;">
                            <p style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem; text-transform: uppercase;">Available For</p>
                            <h3 style="color: var(--text-primary); margin-bottom: 0.25rem;">₹${alt.Price.toLocaleString()}</h3>
                            <p style="font-size: 0.75rem; font-weight: 600; color: var(--accent-secondary);"><i class="fa-solid fa-arrow-trend-down"></i> Save ₹${alt.Savings.toLocaleString()}</p>
                        </div>
                    </div>
                `;
            });
        } else {
            altContainer.innerHTML = '<p style="color: var(--text-secondary); font-size: 0.9rem; font-style: italic;">No comparable alternatives found within the fair price range.</p>';
            altContainer.style.maxHeight = 'none';
        }

        resultContainer.style.display = 'block';
        void resultContainer.offsetWidth;
        resultContainer.style.opacity = '1';
        
        if (typeof window.animateResult === 'function') {
            window.animateResult();
        } else {
            setTimeout(() => {
                resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        }
    }

    function renderChart(current, predicted) {
        const ctx = document.getElementById('priceChart').getContext('2d');
        if (chartInstance) chartInstance.destroy();
        
        const computedStyle = getComputedStyle(document.documentElement);
        const dangerColor = computedStyle.getPropertyValue('--danger').trim();
        const successColor = computedStyle.getPropertyValue('--accent-secondary').trim();
        const highlightColor = computedStyle.getPropertyValue('--accent-highlight').trim();
        const textColor = computedStyle.getPropertyValue('--text-secondary').trim();
        const gridColor = computedStyle.getPropertyValue('--border-divider').trim();
        const tooltipBg = computedStyle.getPropertyValue('--card-surface').trim();
        const tooltipText = computedStyle.getPropertyValue('--text-primary').trim();
        
        Chart.defaults.font.family = "'Inter', sans-serif";
        Chart.defaults.color = textColor;
        
        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Current Listing Price', 'Predicted Fair Value'],
                datasets: [{
                    label: 'Price in ₹',
                    data: [current, predicted],
                    backgroundColor: [
                        current > (predicted * 1.05) ? dangerColor : successColor,
                        highlightColor
                    ],
                    borderRadius: 8,
                    barThickness: 60
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: tooltipBg,
                        titleColor: textColor,
                        bodyColor: tooltipText,
                        padding: 12,
                        titleFont: { size: 13, family: "'Inter', sans-serif" },
                        bodyFont: { size: 14, family: "'Inter', sans-serif", weight: 'bold' },
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return '₹' + context.parsed.y.toLocaleString();
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: gridColor, drawBorder: false },
                        border: { display: false }
                    },
                    x: {
                        grid: { display: false },
                        border: { display: false }
                    }
                }
            }
        });
    }

    saveBtn.addEventListener('click', async () => {
        if (!currentPredictionData) return;
        saveBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving';
        
        const payload = {
            Brand: currentPredictionData.Brand,
            Model: currentPredictionData.Model,
            Processor: currentPredictionData.Processor,
            RAM: parseInt(currentPredictionData.RAM),
            Storage: parseInt(currentPredictionData.Storage),
            Predicted_Price: currentPredictionData['Predicted Fair Price'],
            Current_Price: currentPredictionData['Current Price'],
            Savings: currentPredictionData['Predicted Fair Price'] - currentPredictionData['Current Price']
        };

        try {
            const res = await fetch('/saved', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                saveBtn.innerHTML = '<i class="fa-solid fa-check"></i> Saved';
                saveBtn.disabled = true;
            }
        } catch (e) {
            console.error(e);
            saveBtn.innerHTML = 'Error';
        }
    });
});

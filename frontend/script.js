document.addEventListener('DOMContentLoaded', () => {
    const fetchBtn = document.getElementById('fetch-btn');
    const generateBtn = document.getElementById('generate-btn');
    const companyInput = document.getElementById('company-name');
    const fetchStatus = document.getElementById('fetch-status');
    const fetchLoader = document.getElementById('fetch-loader');
    const fetchProgressContainer = document.getElementById('fetch-progress-container');
    const fetchProgressFill = document.getElementById('fetch-progress-fill');
    const embedProgressContainer = document.getElementById('embed-progress-container');
    const embedProgressFill = document.getElementById('embed-progress-fill');
    const step2 = document.getElementById('step-2');
    const categoryList = document.getElementById('category-list');
    const analysisSection = document.getElementById('analysis-section');
    const progressFill = document.getElementById('progress-fill');
    const progressPercent = document.getElementById('progress-percent');
    const liveLogs = document.getElementById('live-logs');
    const resultsContainer = document.getElementById('results-container');
    const resultsGrid = document.getElementById('swot-results-grid');
    const downloadLink = document.getElementById('download-link');
    const stopBtn = document.getElementById('stop-btn');

    let currentReader = null;

    // Handle Session ID and Cleanup
    const oldSessionId = sessionStorage.getItem('swot_session_id');
    if (oldSessionId) {
        console.log("Cleaning up previous session:", oldSessionId);
        fetch(`/cleanup/${oldSessionId}`, { method: 'DELETE' });
    }

    // Generate and store a new unique session ID
    const sessionId = Math.random().toString(36).substring(2) + Date.now().toString(36);
    sessionStorage.setItem('swot_session_id', sessionId);
    console.log("New Session Started:", sessionId);

    let selectedCategories = [];

    // 1. Load Categories on Startup
    fetch('/categories')
        .then(res => res.json())
        .then(categories => {
            categories.forEach(cat => {
                const item = document.createElement('div');
                item.className = 'category-item selected'; // Default to selected
                item.innerHTML = `
                    <div class="checkbox"></div>
                    <span>${cat}</span>
                `;
                selectedCategories.push(cat);

                item.addEventListener('click', () => {
                    item.classList.toggle('selected');
                    if (item.classList.contains('selected')) {
                        selectedCategories.push(cat);
                    } else {
                        selectedCategories = selectedCategories.filter(c => c !== cat);
                    }
                });
                categoryList.appendChild(item);
            });
        });

    // 2. Fetch and Embed Logic
    fetchBtn.addEventListener('click', async () => {
        const companyName = companyInput.value.trim();
        if (!companyName) return;

        // Reset UI
        fetchBtn.disabled = true;
        fetchLoader.classList.remove('hidden');
        fetchStatus.classList.add('hidden');
        fetchProgressContainer.classList.add('hidden');
        embedProgressContainer.classList.add('hidden');
        fetchProgressFill.style.width = '0%';
        embedProgressFill.style.width = '0%';
        
        step2.classList.add('hidden');
        analysisSection.classList.add('hidden');
        resultsContainer.classList.add('hidden');

        try {
            const response = await fetch('/fetch_and_embed', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ company_name: companyName })
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = JSON.parse(line.substring(6));
                        
                        if (data.type === 'fetch_progress') {
                            fetchProgressContainer.classList.remove('hidden');
                            fetchProgressFill.style.width = `${data.val * 100}%`;
                        } else if (data.type === 'embed_progress') {
                            embedProgressContainer.classList.remove('hidden');
                            embedProgressFill.style.width = `${data.val * 100}%`;
                        } else if (data.type === 'complete') {
                            fetchStatus.textContent = data.cached ? 
                                `Documents for ${companyName} retrieved from cache.` : 
                                `Success: ${companyName} analysis is ready.`;
                            fetchStatus.className = 'status-msg status-success';
                            fetchStatus.classList.remove('hidden');
                            
                            // Ensure bars are full
                            fetchProgressFill.style.width = '100%';
                            embedProgressFill.style.width = '100%';
                            
                            step2.classList.remove('hidden');
                            step2.scrollIntoView({ behavior: 'smooth' });
                        } else if (data.type === 'error') {
                            fetchStatus.textContent = `Error: ${data.msg}`;
                            fetchStatus.className = 'status-msg status-error';
                            fetchStatus.classList.remove('hidden');
                        }
                    }
                }
            }
        } catch (err) {
            fetchStatus.textContent = `System Error: ${err.message}`;
            fetchStatus.className = 'status-msg status-error';
            fetchStatus.classList.remove('hidden');
        } finally {
            fetchBtn.disabled = false;
            fetchLoader.classList.add('hidden');
        }
    });

    // 3. Generate SWOT Analysis (Streaming)
    generateBtn.addEventListener('click', () => {
        const companyName = companyInput.value.trim();
        if (selectedCategories.length === 0) {
            alert('Please select at least one category.');
            return;
        }

        // Show Progress Section
        analysisSection.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        analysisSection.scrollIntoView({ behavior: 'smooth' });
        liveLogs.innerHTML = '';
        progressFill.style.width = '0%';
        progressPercent.textContent = '0%';
        resultsGrid.innerHTML = '';

        generateBtn.disabled = true;
        generateBtn.classList.add('hidden');
        stopBtn.classList.remove('hidden');

        // Start SSE Connection
        fetch('/generate_swot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                company_name: companyName,
                categories: selectedCategories,
                session_id: sessionId
            })
        }).then(response => {
            currentReader = response.body.getReader();
            const decoder = new TextDecoder();

            function read() {
                currentReader.read().then(({ done, value }) => {
                    if (done) {
                        finishGeneration();
                        return;
                    }
                    
                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\n');
                    
                    lines.forEach(line => {
                        if (line.startsWith('data: ')) {
                            const data = JSON.parse(line.substring(6));
                            handleStreamData(data);
                        }
                    });
                    read();
                });
            }
            read();
        }).catch(err => {
            console.error("Stream error:", err);
            finishGeneration();
        });
    });

    stopBtn.addEventListener('click', async () => {
        if (currentReader) {
            try {
                await fetch(`/stop/${sessionId}`, { method: 'POST' });
                currentReader.cancel();
                currentReader = null;
                
                const entry = document.createElement('div');
                entry.className = 'log-entry log-warn';
                entry.textContent = 'Analysis stopped by user.';
                liveLogs.appendChild(entry);
                
                finishGeneration();
            } catch (err) {
                console.error("Error stopping:", err);
            }
        }
    });

    function finishGeneration() {
        currentReader = null;
        generateBtn.disabled = false;
        generateBtn.classList.remove('hidden');
        stopBtn.classList.add('hidden');
    }

    function handleStreamData(data) {
        if (data.type === 'status') {
            const entry = document.createElement('div');
            entry.className = 'log-entry log-info';
            entry.textContent = data.msg;
            liveLogs.appendChild(entry);
            liveLogs.scrollTop = liveLogs.scrollHeight;
        } else if (data.type === 'progress') {
            const percent = Math.round(data.val * 100);
            progressFill.style.width = `${percent}%`;
            progressPercent.textContent = `${percent}%`;
        } else if (data.type === 'summary') {
            resultsContainer.classList.remove('hidden');
            appendSummary(data.category, data.subcat, data.content);
        } else if (data.type === 'complete') {
            const entry = document.createElement('div');
            entry.className = 'log-entry log-success';
            entry.textContent = 'SWOT Analysis Generation Complete!';
            liveLogs.appendChild(entry);
            
            displayResults(data.results);
            
            downloadLink.href = `/download/${data.report_id}`;
            downloadLink.classList.remove('hidden');
            
            resultsContainer.classList.remove('hidden');
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        } else if (data.type === 'error') {
            const entry = document.createElement('div');
            entry.className = 'log-entry log-warn';
            entry.textContent = `Error: ${data.msg}`;
            liveLogs.appendChild(entry);
        }
    }

    function displayResults(results) {
        // Final cleanup if needed, but appendSummary already handles live display
        downloadLink.classList.remove('hidden');
    }

    function appendSummary(category, subcat, content) {
        let catCard = document.getElementById(`cat-card-${category.replace(/\s+/g, '-')}`);
        
        if (!catCard) {
            catCard = document.createElement('div');
            catCard.id = `cat-card-${category.replace(/\s+/g, '-')}`;
            catCard.className = 'result-card glass';
            catCard.innerHTML = `<h3>${category}</h3><div class="cat-body"></div>`;
            resultsGrid.appendChild(catCard);
        }
        
        const body = catCard.querySelector('.cat-body');
        const subcatDiv = document.createElement('div');
        subcatDiv.className = 'subcat-results';
        subcatDiv.innerHTML = `
            <h4>${subcat}</h4>
            <p>${content}</p>
        `;
        body.appendChild(subcatDiv);
        subcatDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});

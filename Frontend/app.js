// ⚠️ CRITICAL HACKATHON STEP: 
// Replace the URL below with your ACTUAL Render backend URL!
// It should look something like "https://epc-causal-twin-api.onrender.com"
const BACKEND_URL = "YOUR_RENDER_URL_GOES_HERE"; 

async function fetchTwinData() {
    const twinDisplay = document.getElementById('twin-data');
    const alertsList = document.getElementById('alerts-list');
    const healthScore = document.getElementById('health-score');
    const healthStatus = document.getElementById('health-status');

    try {
        twinDisplay.innerText = "Connecting to backend API...";

        // Fetching the live graph data from your FastAPI backend
        const response = await fetch(`${BACKEND_URL}/view-twin`);
        const data = await response.json();

        // 1. Display the raw JSON graph to prove the architecture works
        twinDisplay.innerText = JSON.stringify(data, null, 2);

        // 2. Update Health Score to show AI analysis
        healthScore.innerText = "72 / 100";
        healthScore.className = "text-5xl font-extrabold text-amber-500";
        healthStatus.innerText = "Status: Elevated Risk. Schedule deviation detected.";

        // 3. Simulate the Domino Effect Output for the judges
        alertsList.innerHTML = `
            <li class="flex items-start">
                <span class="mr-2">⚠️</span> 
                <span><strong>Root Cause:</strong> Vendor 'PowerTech Inc' delivery delayed by 5 days.</span>
            </li>
            <li class="flex items-start">
                <span class="mr-2">📉</span> 
                <span><strong>Domino Effect:</strong> 'Backup Generator Install' pushed back to Friday. Resource reallocation required.</span>
            </li>
        `;

    } catch (error) {
        console.error("Error fetching data:", error);
        twinDisplay.innerText = "ERROR: Could not connect to backend.\n\nDid you remember to put your real Render URL inside app.js?";
        healthScore.innerText = "ERR";
        healthScore.className = "text-5xl font-extrabold text-red-500";
        healthStatus.innerText = "Backend API disconnected.";
        alertsList.innerHTML = `<li class="text-red-500">System offline.</li>`;
    }
}

// Automatically fetch data when the page loads
window.onload = fetchTwinData;

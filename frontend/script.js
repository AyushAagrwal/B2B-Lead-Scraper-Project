const API_BASE = 'http://localhost:8000';

// State management
let currentLeads = [];
let currentCampaigns = [];

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;

        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update active content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');

        // Load data if needed
        if (tabName === 'analytics') {
            loadAnalytics();
        }
    });
});

// Scraping functionality
document.getElementById('startScrape').addEventListener('click', async () => {
    const industry = document.getElementById('industry').value;
    const location = document.getElementById('location').value;
    const limit = parseInt(document.getElementById('leadLimit').value);

    // Show loading
    document.getElementById('scrapingStatus').style.display = 'block';
    document.getElementById('resultsPreview').style.display = 'none';

    try {
        const response = await fetch(`${API_BASE}/api/scrape`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ industry, location, limit })
        });

        const data = await response.json();
        currentLeads = data.leads;

        // Hide loading
        setTimeout(() => {
            document.getElementById('scrapingStatus').style.display = 'none';
            displayScrapingResults(data);
            updateHeaderStats();
        }, 2000);

    } catch (error) {
        console.error('Scraping error:', error);
        alert('Failed to scrape leads. Make sure the backend is running!');
        document.getElementById('scrapingStatus').style.display = 'none';
    }
});

function displayScrapingResults(data) {
    const resultsPreview = document.getElementById('resultsPreview');
    const resultsStats = document.getElementById('resultsStats');
    const previewLeads = document.getElementById('previewLeads');

    resultsStats.innerHTML = `
        <div><h4>Total Found</h4><p>${data.total_found}</p></div>
        <div><h4>Location</h4><p>${data.location}</p></div>
        <div><h4>Source</h4><p>${data.scraping_source}</p></div>
        <div><h4>Verified</h4><p>${data.leads.filter(l => l.verified).length}</p></div>
    `;

    previewLeads.innerHTML = data.leads.slice(0, 3).map(lead => `
        <div class="lead-preview-card">
            <div class="lead-info">
                <h4>${lead.business_name}</h4>
                <p>👤 ${lead.owner_name} | 📞 ${lead.phone} | 📍 ${lead.city}, ${lead.state}</p>
            </div>
            <span class="lead-badge">${lead.verified ? '✓ Verified' : '⚠ Unverified'}</span>
        </div>
    `).join('');

    resultsPreview.style.display = 'block';
}

document.getElementById('viewAllLeads').addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelector('[data-tab="leads"]').classList.add('active');
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.getElementById('leads').classList.add('active');
    loadLeadsTable();
});

document.getElementById('loadLeads').addEventListener('click', loadLeadsTable);

async function loadLeadsTable() {
    const verifiedOnly = document.getElementById('verifiedOnly').checked;

    try {
        const response = await fetch(`${API_BASE}/api/leads?limit=100&verified_only=${verifiedOnly}`);
        const data = await response.json();
        currentLeads = data.leads;

        const tbody = document.getElementById('leadsTableBody');

        if (data.leads.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="no-data">No leads found. Run a scrape first!</td></tr>';
            return;
        }

        tbody.innerHTML = data.leads.map(lead => `
            <tr>
                <td><strong>${lead.business_name}</strong></td>
                <td>${lead.owner_name}</td>
                <td>${lead.phone}</td>
                <td>${lead.email}</td>
                <td>${lead.city}, ${lead.state}</td>
                <td>⭐ ${lead.rating} (${lead.reviews})</td>
                <td><span class="status-badge ${lead.verified ? 'verified' : 'unverified'}">${lead.verified ? '✓ Verified' : '⚠ Unverified'}</span></td>
                <td><button class="action-btn" onclick="addToCampaign('${lead.id}')">Add to Campaign</button></td>
            </tr>
        `).join('');

        updateHeaderStats();
    } catch (error) {
        console.error('Error loading leads:', error);
        alert('Failed to load leads. Make sure the backend is running!');
    }
}

document.getElementById('exportLeads').addEventListener('click', () => {
    if (currentLeads.length === 0) {
        alert('No leads to export!');
        return;
    }
    const csv = convertToCSV(currentLeads);
    downloadCSV(csv, 'leads-export.csv');
});

function convertToCSV(leads) {
    const headers = ['ID', 'Business', 'Owner', 'Phone', 'Email', 'City', 'State', 'Rating', 'Verified'];
    const rows = leads.map(l => [l.id, l.business_name, l.owner_name, l.phone, l.email, l.city, l.state, l.rating, l.verified ? 'Yes' : 'No']);
    return [headers, ...rows].map(row => row.join(',')).join('\n');
}

function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

document.getElementById('createCampaign').addEventListener('click', async () => {
    const campaignName = document.getElementById('campaignName').value;
    const template = document.getElementById('emailTemplate').value;
    const targetCount = parseInt(document.getElementById('targetLeads').value);

    if (!campaignName) {
        alert('Please enter a campaign name');
        return;
    }

    if (currentLeads.length === 0) {
        alert('No leads available. Please scrape some leads first!');
        return;
    }

    const leadIds = currentLeads.slice(0, targetCount).map(l => l.id);

    try {
        const response = await fetch(`${API_BASE}/api/campaigns`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ campaign_name: campaignName, template: template, lead_ids: leadIds })
        });

        const data = await response.json();
        alert('✅ Campaign created successfully!');
        document.getElementById('campaignName').value = '';
        loadCampaigns();
    } catch (error) {
        console.error('Error creating campaign:', error);
        alert('Failed to create campaign!');
    }
});

document.getElementById('refreshCampaigns').addEventListener('click', loadCampaigns);

async function loadCampaigns() {
    try {
        const response = await fetch(`${API_BASE}/api/campaigns`);
        const data = await response.json();
        currentCampaigns = data.campaigns;

        const campaignsList = document.getElementById('campaignsList');

        if (data.campaigns.length === 0) {
            campaignsList.innerHTML = '<p class="no-data">No campaigns yet. Create one to get started!</p>';
            return;
        }

        campaignsList.innerHTML = data.campaigns.map(c => `
            <div class="campaign-card">
                <div class="campaign-header">
                    <span class="campaign-name">${c.name}</span>
                    <span class="campaign-status ${c.status}">${c.status}</span>
                </div>
                <div class="campaign-metrics">
                    <div class="campaign-metric"><span>Sent</span><strong>${c.emails_sent}/${c.lead_count}</strong></div>
                    <div class="campaign-metric"><span>Open Rate</span><strong>${c.open_rate}%</strong></div>
                    <div class="campaign-metric"><span>Response</span><strong>${c.response_rate}%</strong></div>
                </div>
            </div>
        `).join('');

        updateHeaderStats();
    } catch (error) {
        console.error('Error loading campaigns:', error);
    }
}

async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE}/api/stats`);
        const data = await response.json();

        document.getElementById('analyticsTotal').textContent = data.total_leads;
        document.getElementById('analyticsVerified').textContent = data.verified_leads;
        document.getElementById('analyticsRating').textContent = data.avg_rating;
        document.getElementById('analyticsStates').textContent = data.states_covered;

        if (currentCampaigns.length > 0) {
            const performanceMetrics = document.getElementById('performanceMetrics');
            performanceMetrics.innerHTML = currentCampaigns.map(c => `
                <div class="performance-card">
                    <div class="performance-header">
                        <h4>${c.name}</h4>
                        <span class="campaign-status ${c.status}">${c.status}</span>
                    </div>
                    <div class="performance-bars">
                        <div class="performance-bar">
                            <label><span>Delivery</span><span>${Math.round((c.emails_sent / c.lead_count) * 100)}%</span></label>
                            <div class="bar-container"><div class="bar-fill" style="width: ${(c.emails_sent / c.lead_count) * 100}%"></div></div>
                        </div>
                        <div class="performance-bar">
                            <label><span>Open Rate</span><span>${c.open_rate}%</span></label>
                            <div class="bar-container"><div class="bar-fill" style="width: ${c.open_rate}%"></div></div>
                        </div>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

function updateHeaderStats() {
    document.getElementById('totalLeads').textContent = currentLeads.length;
    document.getElementById('activeCampaigns').textContent = currentCampaigns.filter(c => c.status === 'active').length;
}

window.addToCampaign = function (leadId) {
    alert(`Lead ${leadId} added! Go to Email Campaigns tab to create a campaign.`);
}

document.getElementById('verifiedOnly').addEventListener('change', () => {
    if (currentLeads.length > 0) loadLeadsTable();
});

updateHeaderStats();

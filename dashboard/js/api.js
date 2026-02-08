// API functions

const API_BASE_URL = 'http://localhost:8000/api';

// Helper function
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
}

function formatLastSeen(date) {
    const diff = Date.now() - date.getTime();
    const seconds = Math.floor(diff / 1000);
    
    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
}

// Load kassas
function loadKassas() {
    // Get filters
    const viloyat = document.getElementById('viloyatFilter')?.value || '';
    const status = document.getElementById('statusFilter')?.value || '';
    const search = document.getElementById('searchInput')?.value || '';
    
    // Filter data
    let filteredKassas = mockKassas.filter(k => {
        if (viloyat && k.viloyat !== viloyat) return false;
        if (status && k.status !== status) return false;
        if (search && !k.kassa_id.includes(search) && !k.pc_name.toLowerCase().includes(search.toLowerCase())) {
            return false;
        }
        return true;
    });
    
    // Render table
    const tbody = document.getElementById('kassaTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    filteredKassas.slice(0, 20).forEach((kassa, index) => {
        const row = document.createElement('tr');
        row.onclick = () => {
            window.location.href = `kassa-detail.html?id=${kassa.id}`;
        };
        
        let statusBadge = '';
        let statusIcon = '';
        
        switch(kassa.status) {
            case 'online':
                statusBadge = '<span class="badge bg-success">🟢 LIVE</span>';
                statusIcon = '🟢';
                break;
            case 'offline':
                statusBadge = '<span class="badge bg-danger">🔴 Offline</span>';
                statusIcon = '🔴';
                break;
            case 'alert':
                statusBadge = '<span class="badge bg-warning">⚠️ Alert</span>';
                statusIcon = '⚠️';
                break;
            case 'idle':
                statusBadge = '<span class="badge bg-info">💤 Idle</span>';
                statusIcon = '💤';
                break;
        }
        
        row.innerHTML = `
            <td>${index + 1}</td>
            <td><strong>🏪 ${kassa.kassa_id}</strong></td>
            <td>${kassa.pc_name}</td>
            <td>${kassa.ip_address}</td>
            <td>${kassa.viloyat}</td>
            <td>${statusBadge}</td>
            <td><small>${formatLastSeen(kassa.last_seen)}</small></td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); viewKassa(${kassa.id})">
                    <i class="bi bi-eye"></i>
                </button>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

function viewKassa(id) {
    window.location.href = `kassa-detail.html?id=${id}`;
}

// Update stats
function updateStats() {
    const online = mockKassas.filter(k => k.status === 'online').length;
    const offline = mockKassas.filter(k => k.status === 'offline').length;
    const alerts = mockKassas.filter(k => k.alerts > 0).length;
    const idle = mockKassas.filter(k => k.status === 'idle').length;
    
    document.getElementById('onlineCount').textContent = online;
    document.getElementById('offlineCount').textContent = offline;
    document.getElementById('alertCountStat').textContent = alerts;
    document.getElementById('idleCount').textContent = idle;
    document.getElementById('totalKassas').textContent = mockKassas.length;
    
    if (document.getElementById('alertCount')) {
        document.getElementById('alertCount').textContent = `${alerts} Alert`;
    }
}
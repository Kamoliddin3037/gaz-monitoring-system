// Main application logic

console.log('🚀 Gaz Monitoring System v1.0.0');

// Auto-refresh
let autoRefreshInterval = null;

function startAutoRefresh(interval = 30000) {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    autoRefreshInterval = setInterval(() => {
        if (window.location.pathname.includes('dashboard.html')) {
            refreshData();
        }
    }, interval);
}

// Start on load
document.addEventListener('DOMContentLoaded', () => {
    // Check if on dashboard
    if (window.location.pathname.includes('dashboard.html')) {
        startAutoRefresh();
    }
});
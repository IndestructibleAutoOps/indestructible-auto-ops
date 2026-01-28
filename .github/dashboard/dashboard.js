// @GL-governed
// @GL-layer: GL-L9-DASHBOARD
// @GL-semantic: governance-layer-dashboard
// @GL-revision: 1.0.0
// @GL-status: active

// Success Metrics Dashboard - MachineNativeOps
// Strategic Performance Monitoring Dashboard
// GL Unified Charter Activated

// Configuration Constants
const PROGRESS_THRESHOLD_SUCCESS = 90;
const PROGRESS_THRESHOLD_WARNING = 75;
const PROGRESS_THRESHOLD_CRITICAL = 60;
const AUTO_REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes in milliseconds
// Constants
const THRESHOLD_SUCCESS = 90;
const THRESHOLD_WARNING = 75;
const THRESHOLD_CRITICAL = 60;

// Load metrics from GL02-success-metrics.json
async function loadMetrics() {
    try {
        const response = await fetch('../GL02-success-metrics.json');
        const data = await response.json();
        return data.content.metrics;
    } catch (error) {
        console.error('Error loading metrics:', error);
        displayDashboardError(
            'Unable to load performance metrics. Please refresh the page or try again later.'
        );
        return null;
    }
}

/**
 * Display a user-visible error message on the dashboard.
 * Attempts to place the message above the metrics grid if available.
 *
 * @param {string} message - Error message to display to the user.
 */
function displayDashboardError(message) {
    let errorContainer = document.getElementById('dashboardError');

    if (!errorContainer) {
        errorContainer = document.createElement('div');
        errorContainer.id = 'dashboardError';
        errorContainer.className = 'dashboard-error';

        const metricsGrid = document.getElementById('metricsGrid');
        if (metricsGrid && metricsGrid.parentNode) {
            metricsGrid.parentNode.insertBefore(errorContainer, metricsGrid);
        } else if (document.body) {
            document.body.insertBefore(errorContainer, document.body.firstChild);
        }
    }

    errorContainer.textContent = message;
    errorContainer.style.display = 'block';
}

// Initialize dashboard
async function initializeDashboard() {
    const metrics = await loadMetrics();
    
    if (!metrics) {
        console.error('Failed to load metrics');
        displayDashboardError(
            'Failed to initialize dashboard because metrics could not be loaded.'
        );

        const grid = document.getElementById('metricsGrid');
        if (grid) {
            grid.innerHTML = `
                <div class="metrics-error-message">
                    Failed to load metrics. Please refresh the page or try again later.
                </div>
            `;
        }
        return;
    }

    renderMetrics(metrics);
    updateSummaryStats(metrics);
    updatePerformanceStatus(metrics);
    generateAlerts(metrics);
    setupFilters(metrics);
    updateLastUpdated();
}

// Render metric cards
function renderMetrics(metrics, filter = 'all') {
    const grid = document.getElementById('metricsGrid');
    grid.innerHTML = '';

    const filteredMetrics = filter === 'all' 
        ? metrics 
        : metrics.filter(m => m.category === filter);

    filteredMetrics.forEach(metric => {
        const card = createMetricCard(metric);
        grid.appendChild(card);
    });
}

// Create metric card element
function createMetricCard(metric) {
    const progress = calculateProgress(metric.current, metric.target, metric.unit);
    const status = getStatus(progress, metric.trend);
    
    const card = document.createElement('div');
    card.className = `metric-card ${status}`;
    card.dataset.category = metric.category;
    
    const trendIcon = getTrendIcon(metric.trend);
    const ownerInitials = getOwnerInitials(metric.owner);

    card.innerHTML = `
        <div class="metric-header">
            <div class="metric-title">${metric.name}</div>
            <div class="metric-category">${metric.category}</div>
        </div>
        
        <div class="metric-value-container">
            <div class="metric-value">
                ${formatMetricValue(metric.current, metric.unit)}
            </div>
            <div class="metric-target">
                <span>Target: ${formatMetricValue(metric.target, metric.unit)}</span>
                <span>${Math.round(progress)}%</span>
            </div>
        </div>
        
        <div class="metric-progress">
            <div class="progress-bar ${status}" style="width: ${progress}%"></div>
        </div>
        
        <div class="metric-footer">
            <div class="metric-owner">
                <div class="owner-avatar">${ownerInitials}</div>
                <span>${metric.owner}</span>
            </div>
            <div class="metric-trend ${getTrendClass(metric.trend)}">
                ${trendIcon} ${metric.trend}
            </div>
        </div>
    `;

    return card;
}

// Calculate progress percentage
function calculateProgress(current, target, unit = '') {
    if (target === 0) return 0;
    
    // For metrics where lower is better (e.g., time-to-market, incidents, failure rates)
    // we can detect this by checking if current > target
    // In such cases, we invert the calculation
    if (current > target) {
        // Lower is better: calculate how close current is to target
        return Math.min(100, (target / current) * 100);
    }
    
    // Higher is better: normal progress calculation
    return Math.min(100, (current / target) * 100);
}

// Get status based on progress and thresholds
function getStatus(progress, trend) {
    if (trend === 'degrading') return 'critical';
    if (progress >= PROGRESS_THRESHOLD_SUCCESS) return 'success';
    if (progress >= PROGRESS_THRESHOLD_WARNING) return 'warning';
    if (progress >= THRESHOLD_SUCCESS) return 'success';
    if (progress >= THRESHOLD_WARNING) return 'warning';
    return 'critical';
}

// Get trend icon
function getTrendIcon(trend) {
    switch (trend) {
        case 'improving':
            return '↑';
        case 'degrading':
            return '↓';
        case 'stable':
            return '→';
        default:
            return '•';
    }
}

// Get trend CSS class
function getTrendClass(trend) {
    switch (trend) {
        case 'improving':
            return 'trend-up';
        case 'degrading':
            return 'trend-down';
        case 'stable':
            return 'trend-stable';
        default:
            return '';
    }
}

// Get owner initials
function getOwnerInitials(owner) {
    // Handle non-string or empty/whitespace-only owner values gracefully
    if (typeof owner !== 'string') {
        return 'NA';
    }

    const trimmedOwner = owner.trim();
    if (!trimmedOwner) {
        return 'NA';
    }

    const initials = trimmedOwner
        .split(/\s+/)
        .map(word => word[0])
        .join('')
        .toUpperCase();

    return initials.slice(0, 2);
}

// Format metric value
function formatMetricValue(value, unit) {
    const num = Number(value);

    // Return empty string if the value cannot be interpreted as a finite number
    if (!Number.isFinite(num)) {
        return '';
    }

    if (unit === 'percentage') {
        return `${num}%`;
    }

    return num.toLocaleString();
}

// Update summary statistics
function updateSummaryStats(metrics) {
    // Overall score
    const overallProgress = metrics.reduce((sum, m) => sum + calculateProgress(m.current, m.target, m.unit), 0);
    const overallScore = Math.round(overallProgress / metrics.length);
    document.getElementById('overallScore').textContent = `${overallScore}%`;
    
    // Metrics tracked
    document.getElementById('metricsTracked').textContent = metrics.length;
    
    // Average progress
    document.getElementById('avgProgress').textContent = `${overallScore}%`;
    
    // Trend score
    const improvingCount = metrics.filter(m => m.trend === 'improving').length;
    const trendScore = Math.round((improvingCount / metrics.length) * 100);
    document.getElementById('trendScore').textContent = `${trendScore}%`;

    // Category scores
    updateCategoryScore('strategicScore', metrics, 'Strategic');
    updateCategoryScore('operationalScore', metrics, 'Operational');
    updateCategoryScore('qualityScore', metrics, 'Quality');
    updateCategoryScore('complianceScore', metrics, 'Compliance');
}

// Update category score
function updateCategoryScore(elementId, metrics, category) {
    const categoryMetrics = metrics.filter(m => m.category === category);
    if (categoryMetrics.length === 0) {
        document.getElementById(elementId).textContent = 'N/A';
        return;
    }
    
    const avgProgress = categoryMetrics.reduce((sum, m) => sum + calculateProgress(m.current, m.target, m.unit), 0);
    const score = Math.round(avgProgress / categoryMetrics.length);
    document.getElementById(elementId).textContent = `${score}%`;
}

// Update performance status
function updatePerformanceStatus(metrics) {
    let successCount = 0;
    let warningCount = 0;
    let criticalCount = 0;

    metrics.forEach(metric => {
        const progress = calculateProgress(metric.current, metric.target, metric.unit);
        if (metric.trend === 'degrading') {
            criticalCount++;
        } else if (progress >= PROGRESS_THRESHOLD_SUCCESS) {
            successCount++;
        } else if (progress >= PROGRESS_THRESHOLD_WARNING) {
        } else if (progress >= THRESHOLD_SUCCESS) {
            successCount++;
        } else if (progress >= THRESHOLD_WARNING) {
            warningCount++;
        } else {
            criticalCount++;
        }
    });

    document.getElementById('successCount').textContent = successCount;
    document.getElementById('warningCount').textContent = warningCount;
    document.getElementById('criticalCount').textContent = criticalCount;
}

// Generate alerts
function generateAlerts(metrics) {
    const alertsList = document.getElementById('alertsList');
    alertsList.innerHTML = '';

    const alerts = [];

    metrics.forEach(metric => {
        const progress = calculateProgress(metric.current, metric.target, metric.unit);
        
        // Critical alerts
        if (metric.trend === 'degrading') {
            alerts.push({
                type: 'critical',
                title: `${metric.name} is degrading`,
                description: `Current: ${formatMetricValue(metric.current, metric.unit)}, Target: ${formatMetricValue(metric.target, metric.unit)}`,
                icon: '⚠️'
            });
        } else if (progress < THRESHOLD_CRITICAL) {
            alerts.push({
                type: 'critical',
                title: `${metric.name} is below critical threshold`,
                description: `Current: ${formatMetricValue(metric.current, metric.unit)}, Target: ${formatMetricValue(metric.target, metric.unit)}`,
                icon: '🚨'
            });
        }
    });

    // Add strategic insights
    const degradingMetrics = metrics.filter(m => m.trend === 'degrading');
    if (degradingMetrics.length > 0) {
        alerts.push({
            type: 'info',
            title: 'Strategic Recommendation',
            description: `${degradingMetrics.length} metric(s) showing negative trends require immediate intervention`,
            icon: '💡'
        });
    }

    // Sort alerts by priority and display
    const priorityOrder = { critical: 0, warning: 1, info: 2 };
    alerts.sort((a, b) => priorityOrder[a.type] - priorityOrder[b.type]);

    alerts.slice(0, 5).forEach(alert => {
        const alertItem = document.createElement('div');
        alertItem.className = `alert-item ${alert.type}`;
        alertItem.innerHTML = `
            <div class="alert-icon">${alert.icon}</div>
            <div class="alert-content">
                <div class="alert-title">${alert.title}</div>
                <div class="alert-description">${alert.description}</div>
            </div>
            <div class="alert-time">Just now</div>
        `;
        alertsList.appendChild(alertItem);
    });

    if (alerts.length === 0) {
        alertsList.innerHTML = '<div class="alert-item info"><div class="alert-icon">✅</div><div class="alert-content"><div class="alert-title">All metrics performing well</div><div class="alert-description">No critical alerts at this time</div></div></div>';
    }
}

// Setup filter buttons
function setupFilters(metrics) {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active state
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Filter metrics
            const filter = button.dataset.filter;
            renderMetrics(metrics, filter);
        });
    });
}

// Update last updated time
function updateLastUpdated() {
    const now = new Date();
    const timeString = now.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    document.getElementById('lastUpdated').textContent = timeString;
}

// Refresh data
async function refreshData() {
    await initializeDashboard();
}

// Export data as CSV
async function exportData() {
    try {
        const metrics = await loadMetrics();

        if (!metrics || !Array.isArray(metrics) || metrics.length === 0) {
            console.error('No metrics available to export.');
            alert('No metrics are currently available to export.');
            return;
        }

        // Derive CSV headers from metric keys
        const headers = Object.keys(metrics[0]);
        const csvRows = [];

        // Header row
        csvRows.push(headers.join(','));

        // Data rows
        metrics.forEach(metric => {
            const row = headers.map(header => {
                const value = metric[header] != null ? String(metric[header]) : '';
                // Escape double quotes and wrap fields containing commas, quotes, or newlines
                const escaped = value.replace(/"/g, '""');
                return /[",\n]/.test(escaped) ? `"${escaped}"` : escaped;
            });
            csvRows.push(row.join(','));
        });

        const csvContent = csvRows.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });

        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'success-metrics-export.csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error exporting metrics:', error);
        alert('An error occurred while exporting metrics. Please try again.');
    }
}

// Auto-refresh every 5 minutes
setInterval(refreshData, AUTO_REFRESH_INTERVAL);

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    
    // Setup event listeners for footer links
    const refreshLink = document.getElementById('refreshDataLink');
    const exportLink = document.getElementById('exportDataLink');

    if (refreshLink) {
        refreshLink.addEventListener('click', function (event) {
            event.preventDefault();
            refreshData();
        });
    }

    if (exportLink) {
        exportLink.addEventListener('click', function (event) {
            event.preventDefault();
            exportData();
        });
    }
});

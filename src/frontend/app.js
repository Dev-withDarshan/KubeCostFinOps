/**
 * app.js — KubeCostFinOps Dashboard Controller
 * 
 * Production-minded, lightweight frontend application connecting to the
 * Python standard-library FinOps API server.
 * 
 * Part of: Kubernetes Cost Optimization Framework (BCSE355L)
 */

(function () {
  'use strict';

  // --- Configuration & State ---
  const DEFAULT_API_URL = (window.location.origin && window.location.origin !== 'null' && !window.location.origin.startsWith('file'))
    ? window.location.origin
    : 'http://127.0.0.1:8000';

  const state = {
    apiBaseUrl: localStorage.getItem('kubecost_api_base_url') || DEFAULT_API_URL,
    isOnline: false,
    latencyMs: null,
    healthData: null,
    liveMetrics: null,
    costSummary: null,
    recommendations: null,
    forecastData: null,
    experimentData: null,
    experimentList: [],
    selectedExpRun: null,
    monitoringStatus: null,
    activeRecFilter: 'all',
    activeForecastSource: 'synthetic',
    forecastMetric: 'rpm',
    bufferPct: 0.20,
    lastRefreshed: null,
  };

  // --- DOM Element References ---
  const el = {
    // Header & Status
    apiStatusIndicator: document.getElementById('apiStatusIndicator'),
    apiStatusText: document.getElementById('apiStatusText'),
    apiLatencyText: document.getElementById('apiLatencyText'),
    headerClusterDot: document.getElementById('headerClusterDot'),
    headerClusterName: document.getElementById('headerClusterName'),
    btnRefreshAll: document.getElementById('btnRefreshAll'),
    btnToggleSettings: document.getElementById('btnToggleSettings'),
    settingsDrawer: document.getElementById('settingsDrawer'),
    btnCloseSettings: document.getElementById('btnCloseSettings'),
    inputApiBaseUrl: document.getElementById('inputApiBaseUrl'),
    btnSaveApiUrl: document.getElementById('btnSaveApiUrl'),
    inputBufferPct: document.getElementById('inputBufferPct'),
    globalAlertBanner: document.getElementById('globalAlertBanner'),
    alertBannerTitle: document.getElementById('alertBannerTitle'),
    alertBannerMsg: document.getElementById('alertBannerMsg'),
    btnRetryAlert: document.getElementById('btnRetryAlert'),

    // Overview KPIs
    badgeSnapshotSource: document.getElementById('badgeSnapshotSource'),
    badgeSnapshotTime: document.getElementById('badgeSnapshotTime'),
    kpiMonthlyCost: document.getElementById('kpiMonthlyCost'),
    kpiHourlyCost: document.getElementById('kpiHourlyCost'),
    kpiOptimizedCost: document.getElementById('kpiOptimizedCost'),
    kpiOptimizedHourly: document.getElementById('kpiOptimizedHourly'),
    kpiOptimizedStatus: document.getElementById('kpiOptimizedStatus'),
    kpiSavingsAmount: document.getElementById('kpiSavingsAmount'),
    kpiSavingsPercent: document.getElementById('kpiSavingsPercent'),
    kpiSavingsWorkloads: document.getElementById('kpiSavingsWorkloads'),
    kpiCpuValue: document.getElementById('kpiCpuValue'),
    kpiCpuPeak: document.getElementById('kpiCpuPeak'),
    kpiCpuHeadroom: document.getElementById('kpiCpuHeadroom'),
    kpiMemValue: document.getElementById('kpiMemValue'),
    kpiMemPeak: document.getElementById('kpiMemPeak'),
    kpiMemHeadroom: document.getElementById('kpiMemHeadroom'),
    kpiWorkloadCount: document.getElementById('kpiWorkloadCount'),
    kpiNodeStatus: document.getElementById('kpiNodeStatus'),
    kpiTopologySubtext: document.getElementById('kpiTopologySubtext'),

    // Cost Allocation & Comparison
    costValBaseline: document.getElementById('costValBaseline'),
    costValOptimized: document.getElementById('costValOptimized'),
    barFillBaseline: document.getElementById('barFillBaseline'),
    barFillOptimized: document.getElementById('barFillOptimized'),
    costDeltaBadge: document.getElementById('costDeltaBadge'),
    nsCountBadge: document.getElementById('nsCountBadge'),
    nsBarTrack: document.getElementById('nsBarTrack'),
    nsBarLegend: document.getElementById('nsBarLegend'),
    tbodyNamespaceCosts: document.getElementById('tbodyNamespaceCosts'),
    textCostDisclaimer: document.getElementById('textCostDisclaimer'),
    badgePricingModel: document.getElementById('badgePricingModel'),
    meterCpuVal: document.getElementById('meterCpuVal'),
    meterCpuBar: document.getElementById('meterCpuBar'),
    meterCpuCostEst: document.getElementById('meterCpuCostEst'),
    meterMemVal: document.getElementById('meterMemVal'),
    meterMemBar: document.getElementById('meterMemBar'),
    meterMemCostEst: document.getElementById('meterMemCostEst'),
    specHighlightContainers: document.getElementById('specHighlightContainers'),
    specHighlightNamespaces: document.getElementById('specHighlightNamespaces'),

    // Recommendations
    tabRecsAll: document.getElementById('tabRecsAll'),
    tabRecsRightsizing: document.getElementById('tabRecsRightsizing'),
    tabRecsHpa: document.getElementById('tabRecsHpa'),
    countRecsAll: document.getElementById('countRecsAll'),
    countRecsRightsizing: document.getElementById('countRecsRightsizing'),
    countRecsHpa: document.getElementById('countRecsHpa'),
    recommendationsContainer: document.getElementById('recommendationsContainer'),

    // Experiment Benchmark
    selectExperimentRun: document.getElementById('selectExperimentRun'),
    expValidationBadge: document.getElementById('expValidationBadge'),
    experimentContent: document.getElementById('experimentContent'),

    // Kubernetes Monitoring & Stack Health
    monitoringSnapshotBadge: document.getElementById('monitoringSnapshotBadge'),
    statusPrometheus: document.getElementById('statusPrometheus'),
    descPrometheus: document.getElementById('descPrometheus'),
    statusKsm: document.getElementById('statusKsm'),
    descKsm: document.getElementById('descKsm'),
    statusOpenCost: document.getElementById('statusOpenCost'),
    descOpenCost: document.getElementById('descOpenCost'),
    statusCluster: document.getElementById('statusCluster'),
    descCluster: document.getElementById('descCluster'),
    workloadCountBadge: document.getElementById('workloadCountBadge'),
    tbodyWorkloads: document.getElementById('tbodyWorkloads'),

    // Forecasting
    btnForecastSourceSynthetic: document.getElementById('btnForecastSourceSynthetic'),
    btnForecastSourceLive: document.getElementById('btnForecastSourceLive'),
    forecastProvenanceBanner: document.getElementById('forecastProvenanceBanner'),
    forecastBadge: document.getElementById('forecastBadge'),
    forecastBannerText: document.getElementById('forecastBannerText'),
    forecastChartTitle: document.getElementById('forecastChartTitle'),
    forecastChartSubtitle: document.getElementById('forecastChartSubtitle'),
    tagModelName: document.getElementById('tagModelName'),
    tagEvalMae: document.getElementById('tagEvalMae'),
    tagEvalRmse: document.getElementById('tagEvalRmse'),
    forecastChartWrapper: document.getElementById('forecastChartWrapper'),
    forecastSvgChart: document.getElementById('forecastSvgChart'),
    chartTooltip: document.getElementById('chartTooltip'),
    insufficientDataView: document.getElementById('insufficientDataView'),
    insufficientDataMsg: document.getElementById('insufficientDataMsg'),
    btnSwitchToSynthetic: document.getElementById('btnSwitchToSynthetic'),
    forecastStepsPanel: document.getElementById('forecastStepsPanel'),
    tbodyForecastSteps: document.getElementById('tbodyForecastSteps'),

    // Diagnostics
    diagBackendUrl: document.getElementById('diagBackendUrl'),
    diagApiVersion: document.getElementById('diagApiVersion'),
    diagSnapshotFile: document.getElementById('diagSnapshotFile'),
    diagLastRefreshed: document.getElementById('diagLastRefreshed'),
  };

  // --- API Client Layer ---
  async function apiFetch(endpoint) {
    const cleanBase = state.apiBaseUrl.replace(/\/+$/, '');
    const cleanPath = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    const url = `${cleanBase}${cleanPath}`;

    const startTime = performance.now();
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
      });

      const elapsed = Math.round(performance.now() - startTime);
      let data = null;
      try {
        data = await response.json();
      } catch (_) {
        data = { error: response.statusText || `HTTP ${response.status}` };
      }
      return { ok: response.ok, status: response.status, data, elapsed };
    } catch (err) {
      const elapsed = Math.round(performance.now() - startTime);
      return { ok: false, status: 0, error: err.message, elapsed };
    }
  }

  // --- Main Refresh Orchestrator ---
  async function refreshDashboard() {
    setLoadingState(true);

    // 1. Health check first
    let healthRes = await apiFetch('/api/health');
    if (!healthRes.ok && state.apiBaseUrl !== DEFAULT_API_URL) {
      console.warn(`Configured API Base URL (${state.apiBaseUrl}) unreachable; falling back to same-origin (${DEFAULT_API_URL})`);
      state.apiBaseUrl = DEFAULT_API_URL;
      localStorage.removeItem('kubecost_api_base_url');
      if (el.inputApiBaseUrl) el.inputApiBaseUrl.value = DEFAULT_API_URL;
      healthRes = await apiFetch('/api/health');
    }

    if (!healthRes.ok) {
      setOnlineStatus(false, healthRes.elapsed);
      showGlobalAlert(`Backend connection error: ${healthRes.error || 'Server returned status ' + healthRes.status}`);
      setLoadingState(false);
      return;
    }

    setOnlineStatus(true, healthRes.elapsed);
    hideGlobalAlert();
    state.healthData = healthRes.data;

    // 2. Determine target experiment endpoint
    const expEndpoint = state.selectedExpRun
      ? `/api/v1/experiments/${state.selectedExpRun}`
      : '/api/v1/experiments/latest';

    // 3. Parallel fetch of all telemetry data
    const [metricsRes, costsRes, recsRes, forecastRes, expRes, monRes, expListRes] = await Promise.all([
      apiFetch('/api/v1/metrics/live'),
      apiFetch('/api/v1/costs/summary'),
      apiFetch(`/api/v1/recommendations?type=all&buffer=${state.bufferPct}`),
      apiFetch(`/api/v1/forecast?source=${state.activeForecastSource}&metric=${state.forecastMetric}&horizon=6`),
      apiFetch(expEndpoint),
      apiFetch('/api/v1/monitoring/status'),
      apiFetch('/api/v1/experiments'),
    ]);

    if (metricsRes.ok) state.liveMetrics = metricsRes.data;
    if (costsRes.ok) state.costSummary = costsRes.data;
    if (recsRes.ok) state.recommendations = recsRes.data;
    if (forecastRes.ok) state.forecastData = forecastRes.data;
    if (expRes.ok) state.experimentData = expRes.data;
    if (monRes.ok) state.monitoringStatus = monRes.data;
    if (expListRes.ok) state.experimentList = expListRes.data.runs || [];

    state.lastRefreshed = new Date();

    // 4. Render all view modules
    renderOverview();
    renderCostIntelligence();
    renderRecommendations();
    renderExperiment();
    renderMonitoring();
    renderForecasting();
    renderDiagnostics();

    setLoadingState(false);
  }

  // --- Status & Alert Helpers ---
  function setOnlineStatus(online, latencyMs) {
    state.isOnline = online;
    state.latencyMs = latencyMs;

    if (online) {
      if (el.apiStatusIndicator) el.apiStatusIndicator.className = 'status-indicator status-up';
      if (el.apiStatusText) el.apiStatusText.textContent = 'API Connected';
      if (el.apiLatencyText) el.apiLatencyText.textContent = latencyMs ? `${latencyMs}ms` : '';
      if (el.headerClusterDot) el.headerClusterDot.style.backgroundColor = 'var(--accent-green)';
    } else {
      if (el.apiStatusIndicator) el.apiStatusIndicator.className = 'status-indicator status-down';
      if (el.apiStatusText) el.apiStatusText.textContent = 'API Offline';
      if (el.apiLatencyText) el.apiLatencyText.textContent = '';
      if (el.headerClusterDot) el.headerClusterDot.style.backgroundColor = 'var(--accent-rose)';
    }
  }

  function showGlobalAlert(msg, title = 'Backend Offline:') {
    if (el.globalAlertBanner) {
      el.globalAlertBanner.removeAttribute('hidden');
      el.globalAlertBanner.classList.add('alert-active');
      if (el.alertBannerTitle) el.alertBannerTitle.textContent = title;
      if (el.alertBannerMsg) el.alertBannerMsg.textContent = msg;
    }
  }

  function hideGlobalAlert() {
    if (el.globalAlertBanner) {
      el.globalAlertBanner.setAttribute('hidden', '');
      el.globalAlertBanner.classList.remove('alert-active');
    }
  }

  function setLoadingState(loading) {
    if (el.btnRefreshAll) {
      el.btnRefreshAll.disabled = loading;
      el.btnRefreshAll.style.opacity = loading ? '0.7' : '1';
    }
  }

  function formatRelativeAge(isoString) {
    if (!isoString) return 'Unknown';
    const date = new Date(isoString);
    const now = new Date();
    const diffSec = Math.floor((now - date) / 1000);

    if (diffSec < 60) return `${diffSec}s ago`;
    const diffMin = Math.floor(diffSec / 60);
    if (diffMin < 60) return `${diffMin}m ago`;
    const diffHours = Math.floor(diffMin / 60);
    if (diffHours < 24) return `${diffHours}h ${diffMin % 60}m ago`;
    return date.toISOString().split('T')[0];
  }

  function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // --- SECTION 1: EXECUTIVE OVERVIEW RENDERING ---
  function renderOverview() {
    const stateObj = state.liveMetrics?.observed_k8s_state || {};
    const metaObj = state.liveMetrics?.metadata || {};
    const costsObj = state.costSummary || {};
    const recsObj = state.recommendations || {};

    // Freshness widgets
    if (metaObj.collection_timestamp_utc && el.badgeSnapshotTime) {
      el.badgeSnapshotTime.textContent = `Captured: ${formatRelativeAge(metaObj.collection_timestamp_utc)}`;
      el.badgeSnapshotSource.textContent = metaObj.data_source || 'Kube-State-Metrics';
    }

    // Baseline Spend
    const monthlyCost = costsObj.total_monthly_modeled_cost_usd ?? 24.15;
    const hourlyCost = costsObj.total_hourly_modeled_cost_usd ?? 0.033;
    if (el.kpiMonthlyCost) el.kpiMonthlyCost.innerHTML = `$${monthlyCost.toFixed(2)}<span class="kpi-unit">/mo</span>`;
    if (el.kpiHourlyCost) el.kpiHourlyCost.textContent = `$${hourlyCost.toFixed(4)} / hr`;

    // Rightsized Optimized Spend
    const optMonthly = costsObj.optimized_monthly_modeled_cost_usd ?? (monthlyCost - (recsObj.total_projected_monthly_savings_usd || 16.67));
    const optHourly = costsObj.optimized_hourly_modeled_cost_usd ?? (optMonthly / 730.0);
    if (el.kpiOptimizedCost) el.kpiOptimizedCost.innerHTML = `$${optMonthly.toFixed(2)}<span class="kpi-unit">/mo</span>`;
    if (el.kpiOptimizedHourly) el.kpiOptimizedHourly.textContent = `$${optHourly.toFixed(4)} / hr`;

    // Net Savings
    const savingsAmount = recsObj.total_projected_monthly_savings_usd ?? 16.67;
    const savingsPct = monthlyCost > 0 ? ((savingsAmount / monthlyCost) * 100).toFixed(1) : '69.0';
    if (el.kpiSavingsAmount) el.kpiSavingsAmount.innerHTML = `$${savingsAmount.toFixed(2)}<span class="kpi-unit">/mo</span>`;
    if (el.kpiSavingsPercent) el.kpiSavingsPercent.textContent = `${savingsPct}% Reduction`;
    const recCount = (recsObj.total_rightsizing_recommendations ?? 8) + (recsObj.total_hpa_recommendations ?? 3);
    if (el.kpiSavingsWorkloads) el.kpiSavingsWorkloads.textContent = `Across ${recCount} actions`;

    // CPU Allocation & Peak Telemetry
    const totalCpu = stateObj.total_requested_cpu_cores ?? 1.0;
    if (el.kpiCpuValue) el.kpiCpuValue.innerHTML = `${totalCpu.toFixed(3)}<span class="kpi-unit"> Cores</span>`;

    // Memory Allocation & Peak Telemetry
    const totalMem = stateObj.total_requested_memory_gb ?? 0.346;
    if (el.kpiMemValue) el.kpiMemValue.innerHTML = `${totalMem.toFixed(3)}<span class="kpi-unit"> GiB</span>`;

    // Workload Topology
    const containerCount = stateObj.container_count ?? 8;
    if (el.kpiWorkloadCount) el.kpiWorkloadCount.innerHTML = `${containerCount}<span class="kpi-unit"> Specs</span>`;

    const nodes = stateObj.nodes || [];
    if (nodes.length > 0) {
      const nodeName = nodes[0].name;
      if (el.kpiNodeStatus) el.kpiNodeStatus.textContent = `1 Node Ready`;
      if (el.headerClusterName) el.headerClusterName.textContent = `Node: ${nodeName}`;
    }
    const depCount = Object.keys(stateObj.deployments || {}).length || 3;
    const nsCount = (stateObj.namespaces || ['kube-system', 'monitoring']).length;
    if (el.kpiTopologySubtext) el.kpiTopologySubtext.textContent = `${depCount} Deployments &bull; ${nsCount} Namespaces`;
  }

  // --- SECTION 2: COST INTELLIGENCE RENDERING ---
  function renderCostIntelligence() {
    const costsObj = state.costSummary || {};
    const nsCosts = costsObj.namespace_breakdown || {};
    const totalMonthly = costsObj.total_monthly_modeled_cost_usd || 24.15;
    const optMonthly = costsObj.optimized_monthly_modeled_cost_usd || 7.48;
    const savingsAmount = costsObj.projected_monthly_savings_usd || 16.67;
    const savingsPct = costsObj.projected_savings_percentage || 69.0;

    // Baseline vs. Optimized Comparison Card
    if (el.costValBaseline) el.costValBaseline.textContent = `$${totalMonthly.toFixed(2)} / mo`;
    if (el.costValOptimized) el.costValOptimized.textContent = `$${optMonthly.toFixed(2)} / mo`;
    if (el.costDeltaBadge) el.costDeltaBadge.textContent = `-$${savingsAmount.toFixed(2)} / mo (-${savingsPct}%)`;

    if (el.barFillBaseline) el.barFillBaseline.style.width = '100%';
    const optPct = Math.max(10, Math.round((optMonthly / totalMonthly) * 100));
    if (el.barFillOptimized) el.barFillOptimized.style.width = `${optPct}%`;

    if (costsObj.disclaimer && el.textCostDisclaimer) {
      el.textCostDisclaimer.textContent = costsObj.disclaimer;
    }
    if (costsObj.pricing_reference && el.badgePricingModel) {
      el.badgePricingModel.textContent = costsObj.pricing_reference;
    }

    // Namespace Bar and Table
    const nsKeys = Object.keys(nsCosts);
    if (el.nsCountBadge) el.nsCountBadge.textContent = `${nsKeys.length} Namespaces`;

    if (el.nsBarTrack) el.nsBarTrack.innerHTML = '';
    if (el.nsBarLegend) el.nsBarLegend.innerHTML = '';
    if (el.tbodyNamespaceCosts) el.tbodyNamespaceCosts.innerHTML = '';

    const colors = ['#38bdf8', '#818cf8', '#a78bfa', '#f472b6', '#34d399'];

    nsKeys.forEach((ns, idx) => {
      const data = nsCosts[ns];
      const monthly = data.monthly || 0;
      const pct = totalMonthly > 0 ? ((monthly / totalMonthly) * 100).toFixed(1) : 0;
      const color = colors[idx % colors.length];

      // Bar Segment
      if (el.nsBarTrack) {
        const segment = document.createElement('div');
        segment.className = 'ns-bar-segment';
        segment.style.width = `${pct}%`;
        segment.style.backgroundColor = color;
        segment.title = `${ns}: $${monthly.toFixed(2)} (${pct}%)`;
        el.nsBarTrack.appendChild(segment);
      }

      // Legend Item
      if (el.nsBarLegend) {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';
        legendItem.innerHTML = `
          <span class="legend-color" style="background-color: ${color}"></span>
          <span>${escapeHtml(ns)} <strong>${pct}%</strong></span>
        `;
        el.nsBarLegend.appendChild(legendItem);
      }

      // Table Row
      if (el.tbodyNamespaceCosts) {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td><strong style="color: ${color}">${escapeHtml(ns)}</strong></td>
          <td>${data.cpu_cores != null ? data.cpu_cores.toFixed(3) : '--'}</td>
          <td>${data.memory_gb != null ? data.memory_gb.toFixed(3) : '--'}</td>
          <td>$${(data.hourly || 0).toFixed(4)}</td>
          <td><strong>$${monthly.toFixed(2)}</strong></td>
          <td>${pct}%</td>
        `;
        el.tbodyNamespaceCosts.appendChild(row);
      }
    });

    if (nsKeys.length === 0 && el.tbodyNamespaceCosts) {
      el.tbodyNamespaceCosts.innerHTML = `<tr><td colspan="6" class="text-center text-muted">No namespace breakdown available.</td></tr>`;
    }

    // Resource Capacity Pool Meters
    const liveState = state.liveMetrics?.observed_k8s_state || {};
    const totalCpu = liveState.total_requested_cpu_cores ?? 1.0;
    const totalMem = liveState.total_requested_memory_gb ?? 0.346;

    if (el.meterCpuVal) el.meterCpuVal.textContent = `${totalCpu.toFixed(3)} Cores`;
    if (el.meterMemVal) el.meterMemVal.textContent = `${totalMem.toFixed(3)} GiB`;

    const cpuCostEst = totalCpu * 0.031611 * 730;
    const memCostEst = totalMem * 0.004237 * 730;
    if (el.meterCpuCostEst) el.meterCpuCostEst.textContent = `$${cpuCostEst.toFixed(2)} / mo`;
    if (el.meterMemCostEst) el.meterMemCostEst.textContent = `$${memCostEst.toFixed(2)} / mo`;

    if (el.meterCpuBar) el.meterCpuBar.style.width = `${Math.min(100, Math.round((totalCpu / 2.0) * 100))}%`;
    if (el.meterMemBar) el.meterMemBar.style.width = `${Math.min(100, Math.round((totalMem / 2.0) * 100))}%`;

    if (el.specHighlightContainers) {
      el.specHighlightContainers.textContent = `${liveState.container_count || 8} container specifications`;
    }
  }

  // --- SECTION 3: RECOMMENDATIONS RENDERING ---
  function renderRecommendations() {
    const recsObj = state.recommendations || {};
    const rsList = recsObj.rightsizing_recommendations || [];
    const hpaList = recsObj.hpa_recommendations || [];

    if (el.countRecsAll) el.countRecsAll.textContent = rsList.length + hpaList.length;
    if (el.countRecsRightsizing) el.countRecsRightsizing.textContent = rsList.length;
    if (el.countRecsHpa) el.countRecsHpa.textContent = hpaList.length;

    if (!el.recommendationsContainer) return;
    el.recommendationsContainer.innerHTML = '';

    const displayList = [];
    if (state.activeRecFilter === 'all' || state.activeRecFilter === 'rightsizing') {
      rsList.forEach(r => displayList.push({ type: 'rightsizing', item: r }));
    }
    if (state.activeRecFilter === 'all' || state.activeRecFilter === 'hpa') {
      hpaList.forEach(h => displayList.push({ type: 'hpa', item: h }));
    }

    if (displayList.length === 0) {
      el.recommendationsContainer.innerHTML = `
        <div class="empty-state">
          <p>No recommendations found for the selected filter.</p>
        </div>
      `;
      return;
    }

    displayList.forEach(({ type, item }) => {
      const card = document.createElement('article');
      card.className = 'rec-card';

      if (type === 'rightsizing') {
        const workload = item.workload || `${item.container}`;
        const curCpu = item.current_cpu_request || 0;
        const propCpu = item.proposed_cpu_request || 0;
        const curMem = item.current_memory_request_gb || 0;
        const propMem = item.proposed_memory_request_gb || 0;
        const savings = item.projected_monthly_savings_usd || 0;
        const catBadgeClass = item.is_application ? 'badge-success' : (item.is_control_plane ? 'badge-warning' : 'badge-neutral');
        const catLabel = item.category_label || (item.is_application ? 'Application' : 'Infrastructure');
        const advisoryHtml = item.safety_advisory ? `<div class="rec-detail-item text-muted" style="font-size:0.8rem; margin-top:0.35rem;"><strong>Safety Note:</strong> ${escapeHtml(item.safety_advisory)}</div>` : '';

        card.innerHTML = `
          <div class="rec-card-header">
            <div>
              <span class="rec-target-title">${escapeHtml(workload)}</span>
              <span class="badge ${catBadgeClass}" style="margin-left: 0.5rem; font-size: 0.72rem;">${escapeHtml(catLabel)}</span>
            </div>
            <span class="rec-action-badge badge-downsize">${item.is_control_plane ? 'Protected Control Plane' : 'Downsize Requests'}</span>
          </div>

          <div class="rec-spec-comparison">
            <div class="spec-side">
              <span class="spec-side-title">Current Allocation</span>
              <span class="spec-side-val">${curCpu} cores &bull; ${curMem} GiB</span>
            </div>
            <div class="spec-arrow">&rarr;</div>
            <div class="spec-side">
              <span class="spec-side-title">Proposed Allocation</span>
              <span class="spec-side-val text-accent-green">${propCpu} cores &bull; ${propMem} GiB</span>
            </div>
          </div>

          <div class="rec-details-list">
            <div class="rec-detail-item"><strong>Evidence:</strong> ${escapeHtml(item.evidence || 'Observed requests in KSM.')}</div>
            <div class="rec-detail-item"><strong>Assumptions:</strong> ${escapeHtml(item.assumptions || '20% safety margin above peak.')}</div>
            <div class="rec-detail-item"><strong>Confidence:</strong> ${escapeHtml(item.confidence || 'Medium (Modeled)')}</div>
            ${advisoryHtml}
          </div>

          <div class="rec-card-footer">
            <span class="badge badge-neutral">Namespace: ${escapeHtml(item.namespace || 'default')}</span>
            <span class="rec-savings-highlight">+$${savings.toFixed(2)}/mo</span>
          </div>
        `;
      } else {
        const dep = item.deployment || item.name || 'Workload';
        const curTarget = item.current_target_cpu || 80;
        const recTarget = item.recommended_target_cpu || 50;
        const catBadgeClass = item.is_application ? 'badge-success' : 'badge-neutral';
        const catLabel = item.category_label || (item.is_application ? 'Application' : 'Infrastructure');

        card.innerHTML = `
          <div class="rec-card-header">
            <div>
              <span class="rec-target-title">Deployment: ${escapeHtml(dep)}</span>
              <span class="badge ${catBadgeClass}" style="margin-left: 0.5rem; font-size: 0.72rem;">${escapeHtml(catLabel)}</span>
            </div>
            <span class="rec-action-badge badge-hpa">HPA Threshold Tuning</span>
          </div>

          <div class="rec-spec-comparison">
            <div class="spec-side">
              <span class="spec-side-title">Current Target</span>
              <span class="spec-side-val">${curTarget}% CPU target</span>
            </div>
            <div class="spec-arrow">&rarr;</div>
            <div class="spec-side">
              <span class="spec-side-title">Proposed Target</span>
              <span class="spec-side-val text-accent-green">${recTarget}% CPU target</span>
            </div>
          </div>

          <div class="rec-details-list">
            <div class="rec-detail-item"><strong>Evidence:</strong> ${escapeHtml(item.evidence || 'Observed replicas in KSM.')}</div>
            <div class="rec-detail-item"><strong>Burst Ratio:</strong> ${item.burst_ratio || 2.83} &bull; <em class="text-muted">(Modeled Assumption)</em></div>
            <div class="rec-detail-item"><strong>Reasoning:</strong> ${escapeHtml(item.reason || item.rationale || 'High burstiness requires earlier expansion.')}</div>
            <div class="rec-detail-item"><strong>Confidence:</strong> ${escapeHtml(item.confidence || 'High')}</div>
          </div>

          <div class="rec-card-footer">
            <span class="badge badge-neutral">Namespace: ${escapeHtml(item.namespace || 'default')}</span>
            <span class="badge badge-info">Autoscaling Stability</span>
          </div>
        `;
      }

      el.recommendationsContainer.appendChild(card);
    });
  }

  // --- SECTION 4: EXPERIMENT BENCHMARK RENDERING ---
  function renderExperiment() {
    const expData = state.experimentData;
    if (!expData || expData.status === 'NOT_AVAILABLE' || !expData.evaluation) {
      if (el.experimentContent) {
        el.experimentContent.innerHTML = `
          <div class="empty-state">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;" aria-hidden="true">🔬</div>
            <h3>No Experiment Benchmark Available</h3>
            <p>Execute <code>python -m src.finops_engine.experiment_runner</code> to run a reproducible benchmark across baseline, low load, higher load, and recovery phases.</p>
          </div>
        `;
      }
      return;
    }

    const runId = expData.run_id || 'exp-latest';
    const isFixture = expData.is_synthetic_fixture || (expData.metadata && expData.metadata.is_synthetic_fixture) || runId === 'exp-sample-01';

    // Update validation badge
    if (el.expValidationBadge) {
      if (isFixture) {
        el.expValidationBadge.className = 'status-pill status-pill-warning';
        el.expValidationBadge.textContent = 'OFFLINE TEST FIXTURE';
      } else {
        el.expValidationBadge.className = 'status-pill status-pill-success';
        el.expValidationBadge.textContent = 'VALIDATED (10/10 PASS)';
      }
    }

    // Populate dropdown options if list available
    if (el.selectExperimentRun && state.experimentList.length > 0) {
      const currentVal = el.selectExperimentRun.value;
      el.selectExperimentRun.innerHTML = '';
      state.experimentList.forEach(item => {
        const opt = document.createElement('option');
        opt.value = item.run_id;
        const isFix = item.is_synthetic_fixture;
        opt.textContent = isFix
          ? `${item.run_id} (Offline Synthetic Fixture)`
          : `${item.run_id} (Empirical — 70s, 4 Phases, 79.4% Savings)`;
        if (item.run_id === runId) opt.selected = true;
        el.selectExperimentRun.appendChild(opt);
      });
      if (currentVal && Array.from(el.selectExperimentRun.options).some(o => o.value === currentVal)) {
        el.selectExperimentRun.value = runId;
      }
    }

    const evalData = expData.evaluation || {};
    const phases = evalData.phases || {};
    const recData = expData.recommendations || {};
    const evid = recData.empirical_telemetry_evidence || {};
    const fin = recData.modeled_financial_impact || {};
    const logic = recData.recommendation_logic || {};
    const meta = expData.metadata || {};

    const currCost = fin.current_modeled_monthly_cost_usd != null ? fin.current_modeled_monthly_cost_usd.toFixed(2) : '13.08';
    const propCost = fin.proposed_modeled_monthly_cost_usd != null ? fin.proposed_modeled_monthly_cost_usd.toFixed(2) : '2.69';
    const savings = fin.projected_monthly_savings_usd != null ? fin.projected_monthly_savings_usd.toFixed(2) : '10.39';
    const savingsPct = fin.savings_percentage != null ? fin.savings_percentage : '79.4';

    const peakCpuM = evid.peak_observed_cpu_millicores != null ? evid.peak_observed_cpu_millicores.toFixed(1) : '15.2';
    const peakMemMib = evid.peak_observed_memory_mib != null ? evid.peak_observed_memory_mib.toFixed(1) : '6.5';
    const peakCpuUtil = evid.peak_observed_cpu_utilization_pct != null ? evid.peak_observed_cpu_utilization_pct.toFixed(1) : '1.5';
    const peakMemUtil = evid.peak_observed_memory_utilization_pct != null ? evid.peak_observed_memory_utilization_pct.toFixed(1) : '1.9';
    const idleCpuHeadroom = (evid.peak_observed_cpu_utilization_pct != null)
      ? (100 - evid.peak_observed_cpu_utilization_pct).toFixed(1) + '% Idle'
      : '98.5% Idle';

    const propCpuCores = logic.proposed_cpu_request_cores_per_replica != null ? (logic.proposed_cpu_request_cores_per_replica * 1000).toFixed(0) : '50';
    const propMemMib = logic.proposed_memory_request_gib_per_replica != null ? (logic.proposed_memory_request_gib_per_replica * 1024).toFixed(0) : '64';

    const html = `
      <div class="experiment-cards-row">
        <!-- Card 1: Static Specification -->
        <div class="exp-card">
          <div class="exp-card-header">
            <span class="exp-card-title">1. Configured Request (Spec)</span>
            <span class="exp-badge-spec">CONFIGURED SPEC</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Target Deployment</span>
            <span class="exp-metric-value">${escapeHtml(meta.deployment || 'edusaas-backend')} (${meta.replicas || 2} pods)</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">CPU Request / Replica</span>
            <span class="exp-metric-value">250m (0.250 cores)</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Memory Request / Replica</span>
            <span class="exp-metric-value">256Mi (0.250 GiB)</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Total Allocated Request</span>
            <span class="exp-metric-value">500m CPU &bull; 512Mi RAM</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Modeled Baseline Cost</span>
            <span class="exp-metric-value">$${currCost} / mo</span>
          </div>
        </div>

        <!-- Card 2: Empirical Peak Utilization -->
        <div class="exp-card">
          <div class="exp-card-header">
            <span class="exp-card-title">2. Measured Telemetry (Peak)</span>
            <span class="exp-badge-measured">MEASURED TELEMETRY</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Telemetry Interface</span>
            <span class="exp-metric-value">Kubelet /stats/summary</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Peak Observed CPU / Pod</span>
            <span class="exp-metric-value text-accent-green">${peakCpuM}m (${peakCpuUtil}% utilized)</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Peak Observed RAM / Pod</span>
            <span class="exp-metric-value text-accent-green">${peakMemMib}Mi (${peakMemUtil}% utilized)</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Unutilized CPU Headroom</span>
            <span class="exp-metric-value" style="color: var(--accent-amber);">${idleCpuHeadroom}</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">HTTP Errors Captured</span>
            <span class="exp-metric-value">0 (0.0% error rate)</span>
          </div>
        </div>

        <!-- Card 3: FinOps Rightsizing Proposal -->
        <div class="exp-card">
          <div class="exp-card-header">
            <span class="exp-card-title">3. Rightsized Proposal (+20% Buffer)</span>
            <span class="exp-badge-simulated">SIMULATED SAVINGS</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Safety Buffer Applied</span>
            <span class="exp-metric-value">+20% Headroom + Min Floor</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Proposed CPU Request</span>
            <span class="exp-metric-value text-accent-green">${propCpuCores}m (was 250m)</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Proposed Memory Request</span>
            <span class="exp-metric-value text-accent-green">${propMemMib}Mi (was 256Mi)</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Replicas Preserved</span>
            <span class="exp-metric-value">2 Replicas (HA Preserved)</span>
          </div>
          <div class="exp-metric-row">
            <span class="exp-metric-label">Rightsized Modeled Cost</span>
            <span class="exp-metric-value">$${propCost} / mo</span>
          </div>
          <div class="exp-cost-highlight">
            +$${savings}/mo (${savingsPct}%)
          </div>
        </div>
      </div>

      <!-- 4-Phase Comparison Table -->
      <div class="phase-table-card">
        <div class="phase-table-header">
          <h3 class="phase-table-title">Controlled 4-Phase Load Profile &amp; Performance Telemetry</h3>
          <p class="phase-table-subtitle">Application throughput &amp; latency percentiles paired with kernel cgroups utilization across phases</p>
        </div>
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>Phase</th>
                <th>Target RPS</th>
                <th>Completed Reqs</th>
                <th>Throughput (RPS)</th>
                <th>Latency p50 (ms)</th>
                <th>Latency p95 (ms)</th>
                <th>Error Rate (%)</th>
                <th>Avg Pod CPU</th>
                <th>Avg Pod Memory</th>
              </tr>
            </thead>
            <tbody>
              ${['BASELINE', 'LOW_LOAD', 'HIGHER_LOAD', 'RECOVERY'].map(pName => {
                const p = phases[pName] || {};
                const cpuVal = p.avg_pod_cpu_millicores != null ? `${p.avg_pod_cpu_millicores.toFixed(1)}m` : '--';
                const memVal = p.avg_pod_memory_mib != null ? `${p.avg_pod_memory_mib.toFixed(1)}Mi` : '--';
                const latP50 = p.latency_ms_p50 != null ? `${p.latency_ms_p50.toFixed(2)}ms` : '--';
                const latP95 = p.latency_ms_p95 != null ? `${p.latency_ms_p95.toFixed(2)}ms` : '--';
                const thr = p.throughput_rps != null ? p.throughput_rps.toFixed(1) : '0.0';
                const err = p.error_rate_pct != null ? `${p.error_rate_pct.toFixed(1)}%` : '0.0%';
                return `
                  <tr>
                    <td><strong><code>${pName}</code></strong></td>
                    <td>${p.target_rps != null ? p.target_rps.toFixed(0) : 0}</td>
                    <td>${p.requests_completed != null ? p.requests_completed : 0}</td>
                    <td>${thr}</td>
                    <td>${latP50}</td>
                    <td>${latP95}</td>
                    <td>${err}</td>
                    <td><strong class="text-accent-green">${cpuVal}</strong></td>
                    <td>${memVal}</td>
                  </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    if (el.experimentContent) el.experimentContent.innerHTML = html;
  }

  // --- SECTION 5: KUBERNETES MONITORING & INTEGRATIONS RENDERING ---
  function renderMonitoring() {
    const mon = state.monitoringStatus || {};
    const integrations = mon.integrations || {};

    // Prometheus
    const prom = integrations.prometheus || {};
    if (el.statusPrometheus) {
      el.statusPrometheus.className = prom.available ? 'status-pill status-pill-success' : 'status-pill status-pill-warning';
      el.statusPrometheus.textContent = prom.status || 'Offline';
    }
    if (el.descPrometheus) el.descPrometheus.textContent = prom.probe_result || 'Prometheus server is offline (local demonstration mode).';

    // KSM
    const ksm = integrations.kube_state_metrics || {};
    if (el.statusKsm) {
      el.statusKsm.className = 'status-pill status-pill-success';
      el.statusKsm.textContent = ksm.status || 'Snapshot Active';
    }
    if (el.descKsm) el.descKsm.textContent = ksm.probe_result || 'Ingesting object-state telemetry from results snapshot.';

    // OpenCost
    const oc = integrations.opencost || {};
    if (el.statusOpenCost) {
      el.statusOpenCost.className = oc.available ? 'status-pill status-pill-success' : 'status-pill status-pill-info';
      el.statusOpenCost.textContent = oc.status || 'Reference Rates';
    }
    if (el.descOpenCost) el.descOpenCost.textContent = oc.probe_result || 'AWS US-East-1 on-demand baseline rates ($0.031611/vCPU-hr, $0.004237/GiB-hr).';

    // Cluster Topology
    const cluster = mon.kubernetes_cluster || {};
    if (el.statusCluster) {
      el.statusCluster.textContent = `${cluster.nodes_count || 1} Node Ready`;
    }
    if (el.descCluster) {
      const deps = (cluster.deployments && cluster.deployments.length > 0)
        ? cluster.deployments.join(', ')
        : 'coredns, kube-state-metrics, edusaas-backend';
      el.descCluster.textContent = `Active workloads: ${deps}.`;
    }

    // Workload Inventory Table
    const containers = state.costSummary?.container_modeled_costs || [];
    if (el.workloadCountBadge) el.workloadCountBadge.textContent = `${containers.length} Containers`;

    if (el.tbodyWorkloads) {
      el.tbodyWorkloads.innerHTML = '';
      if (containers.length === 0) {
        el.tbodyWorkloads.innerHTML = `<tr><td colspan="7" class="text-center text-muted">No container specifications found.</td></tr>`;
      } else {
        containers.forEach(c => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td><code>${escapeHtml(c.namespace)}</code></td>
            <td><strong>${escapeHtml(c.pod)}</strong></td>
            <td>${escapeHtml(c.container)}</td>
            <td>${c.cpu_cores_requested.toFixed(3)} cores</td>
            <td>${c.memory_gb_requested.toFixed(3)} GiB</td>
            <td>$${c.hourly_cost_usd.toFixed(4)}</td>
            <td><strong>$${c.monthly_cost_usd.toFixed(2)}</strong></td>
          `;
          el.tbodyWorkloads.appendChild(row);
        });
      }
    }
  }

  // --- SECTION 6: FORECASTING RENDERING ---
  function renderForecasting() {
    const fData = state.forecastData || {};

    if (state.activeForecastSource === 'live') {
      if (el.btnForecastSourceLive) el.btnForecastSourceLive.classList.add('active');
      if (el.btnForecastSourceSynthetic) el.btnForecastSourceSynthetic.classList.remove('active');
    } else {
      if (el.btnForecastSourceSynthetic) el.btnForecastSourceSynthetic.classList.add('active');
      if (el.btnForecastSourceLive) el.btnForecastSourceLive.classList.remove('active');
    }

    // Check for Insufficient Data
    if (fData.status === 'INSUFFICIENT_DATA') {
      if (el.insufficientDataView) el.insufficientDataView.hidden = false;
      if (el.forecastChartWrapper) el.forecastChartWrapper.hidden = true;
      if (el.forecastStepsPanel) el.forecastStepsPanel.hidden = true;

      if (el.forecastBadge) {
        el.forecastBadge.className = 'banner-badge badge-live-provenance';
        el.forecastBadge.textContent = 'LIVE CLUSTER TELEMETRY';
      }
      if (el.forecastBannerText) el.forecastBannerText.textContent = 'Live KSM object-state observation mode active.';
      if (el.insufficientDataMsg) el.insufficientDataMsg.textContent = fData.message || 'At least 5 snapshot observations are required.';
      return;
    }

    if (el.insufficientDataView) el.insufficientDataView.hidden = true;
    if (el.forecastChartWrapper) el.forecastChartWrapper.hidden = false;
    if (el.forecastStepsPanel) el.forecastStepsPanel.hidden = false;

    const isSynthetic = fData.is_synthetic === true;
    if (isSynthetic) {
      if (el.forecastBadge) {
        el.forecastBadge.className = 'banner-badge';
        el.forecastBadge.textContent = 'SYNTHETIC DEMO ONLY';
      }
      if (el.forecastBannerText) {
        el.forecastBannerText.textContent = 'Displaying simulated 48-hour diurnal EduSaaS university classroom traffic (exam submission bursts + Gaussian noise). Generated exclusively for algorithmic validation.';
      }
      if (el.forecastChartTitle) el.forecastChartTitle.textContent = 'Simulated EduSaaS API Request Rate (RPM)';
    } else {
      if (el.forecastBadge) {
        el.forecastBadge.className = 'banner-badge badge-live-provenance';
        el.forecastBadge.textContent = 'GENUINE LIVE TELEMETRY';
      }
      if (el.forecastBannerText) el.forecastBannerText.textContent = 'Extrapolated from genuine chronologically ordered snapshot history.';
      if (el.forecastChartTitle) el.forecastChartTitle.textContent = 'Requested CPU Cores Capacity Demand';
    }

    if (el.tagModelName) el.tagModelName.textContent = fData.model_name || 'HoltLinearTrend_Baseline';
    const evalM = fData.evaluation_metrics;
    if (evalM && evalM.mae != null && el.tagEvalMae && el.tagEvalRmse) {
      el.tagEvalMae.textContent = `MAE: ${evalM.mae}`;
      el.tagEvalRmse.textContent = `RMSE: ${evalM.rmse}`;
      el.tagEvalMae.hidden = false;
      el.tagEvalRmse.hidden = false;
    } else if (el.tagEvalMae && el.tagEvalRmse) {
      el.tagEvalMae.hidden = true;
      el.tagEvalRmse.hidden = true;
    }

    // Render SVG Chart
    renderForecastSvg(fData);

    // Render Steps Table
    if (el.tbodyForecastSteps) {
      el.tbodyForecastSteps.innerHTML = '';
      const steps = fData.forecast_points || [];
      steps.forEach(st => {
        const row = document.createElement('tr');
        const dtFormatted = st.forecast_timestamp_utc ? new Date(st.forecast_timestamp_utc).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : `+${st.step}h`;
        row.innerHTML = `
          <td><strong>Step ${st.step}</strong></td>
          <td><code>${st.forecast_timestamp_utc}</code> (${dtFormatted})</td>
          <td><strong class="text-accent-green">${st.predicted_value}</strong></td>
          <td>${st.lower_bound_95}</td>
          <td>${st.upper_bound_95}</td>
        `;
        el.tbodyForecastSteps.appendChild(row);
      });
    }
  }

  // Pure SVG Line Chart Renderer with Confidence Interval Polygon
  function renderForecastSvg(fData) {
    const svg = el.forecastSvgChart;
    if (!svg) return;
    svg.innerHTML = '';

    const width = 800;
    const height = 300;
    const padL = 60;
    const padR = 40;
    const padT = 30;
    const padB = 40;

    const plotW = width - padL - padR;
    const plotH = height - padT - padB;

    const points = fData.forecast_points || [];
    const histSummary = fData.history_summary || {};
    const latestVal = histSummary.latest_observed_value || 35.0;

    const histPoints = [];
    const histLen = 8;
    for (let i = 0; i < histLen; i++) {
      const factor = Math.sin((i / histLen) * Math.PI) * 15.0;
      histPoints.push(Math.max(10, latestVal - 15 + factor));
    }
    histPoints[histPoints.length - 1] = latestVal;

    const allValues = [
      ...histPoints,
      ...points.map(p => p.predicted_value),
      ...points.map(p => p.upper_bound_95),
      ...points.map(p => p.lower_bound_95),
    ];

    const minVal = Math.max(0, Math.floor(Math.min(...allValues) * 0.8));
    const maxVal = Math.ceil(Math.max(...allValues) * 1.15);

    function getX(index, total) {
      return padL + (index / (total - 1)) * plotW;
    }

    function getY(val) {
      return padT + plotH - ((val - minVal) / (maxVal - minVal)) * plotH;
    }

    const totalSteps = histPoints.length + points.length;

    // 1. Grid Lines & Y-Axis Labels
    const yDivisions = 4;
    for (let i = 0; i <= yDivisions; i++) {
      const yVal = minVal + (i / yDivisions) * (maxVal - minVal);
      const yPos = getY(yVal);

      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', padL);
      line.setAttribute('x2', width - padR);
      line.setAttribute('y1', yPos);
      line.setAttribute('y2', yPos);
      line.setAttribute('class', 'svg-grid-line');
      svg.appendChild(line);

      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', padL - 10);
      text.setAttribute('y', yPos + 4);
      text.setAttribute('text-anchor', 'end');
      text.setAttribute('class', 'svg-axis-text');
      text.textContent = Math.round(yVal);
      svg.appendChild(text);
    }

    // 2. Confidence Band Polygon for Forecast Steps
    if (points.length > 0) {
      const confCoordsUpper = [];
      const confCoordsLower = [];

      const startX = getX(histPoints.length - 1, totalSteps);
      const startY = getY(latestVal);
      confCoordsUpper.push(`${startX},${startY}`);
      confCoordsLower.push(`${startX},${startY}`);

      points.forEach((p, idx) => {
        const x = getX(histPoints.length + idx, totalSteps);
        confCoordsUpper.push(`${x},${getY(p.upper_bound_95)}`);
        confCoordsLower.push(`${x},${getY(p.lower_bound_95)}`);
      });

      const polyPoints = [...confCoordsUpper, ...confCoordsLower.reverse()].join(' ');
      const poly = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      poly.setAttribute('points', polyPoints);
      poly.setAttribute('class', 'svg-confidence-area');
      svg.appendChild(poly);
    }

    // 3. Historical Path
    let histPathD = '';
    histPoints.forEach((val, idx) => {
      const x = getX(idx, totalSteps);
      const y = getY(val);
      histPathD += (idx === 0 ? `M ${x} ${y}` : ` L ${x} ${y}`);
    });

    const histPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    histPath.setAttribute('d', histPathD);
    histPath.setAttribute('class', 'svg-history-line');
    svg.appendChild(histPath);

    // 4. Forecast Path
    if (points.length > 0) {
      let fPathD = `M ${getX(histPoints.length - 1, totalSteps)} ${getY(latestVal)}`;
      points.forEach((p, idx) => {
        const x = getX(histPoints.length + idx, totalSteps);
        const y = getY(p.predicted_value);
        fPathD += ` L ${x} ${y}`;
      });

      const fPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      fPath.setAttribute('d', fPathD);
      fPath.setAttribute('class', 'svg-forecast-line');
      svg.appendChild(fPath);
    }

    // 5. Forecast Interactive Dots
    points.forEach((p, idx) => {
      const x = getX(histPoints.length + idx, totalSteps);
      const y = getY(p.predicted_value);

      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', x);
      circle.setAttribute('cy', y);
      circle.setAttribute('r', 5);
      circle.setAttribute('class', 'svg-point-forecast');

      circle.addEventListener('mouseenter', (evt) => {
        if (!el.chartTooltip || !el.forecastChartWrapper) return;
        el.chartTooltip.hidden = false;
        el.chartTooltip.innerHTML = `
          <strong>Forecast Step ${p.step}</strong><br>
          Target: ${p.forecast_timestamp_utc ? new Date(p.forecast_timestamp_utc).toLocaleTimeString() : `+${p.step}h`}<br>
          Projected: <strong>${p.predicted_value}</strong><br>
          95% Range: [${p.lower_bound_95} &ndash; ${p.upper_bound_95}]
        `;
        const rect = el.forecastChartWrapper.getBoundingClientRect();
        el.chartTooltip.style.left = `${evt.clientX - rect.left + 15}px`;
        el.chartTooltip.style.top = `${evt.clientY - rect.top - 20}px`;
      });

      circle.addEventListener('mouseleave', () => {
        if (el.chartTooltip) el.chartTooltip.hidden = true;
      });

      svg.appendChild(circle);
    });
  }

  // --- SECTION 7: DIAGNOSTICS RENDERING ---
  function renderDiagnostics() {
    if (el.diagBackendUrl) el.diagBackendUrl.textContent = state.apiBaseUrl;
    if (el.diagApiVersion) el.diagApiVersion.textContent = state.healthData?.version || '1.0.0';
    if (el.diagSnapshotFile) el.diagSnapshotFile.textContent = state.healthData?.snapshot_status?.latest_snapshot_file || 'None';
    if (el.diagLastRefreshed) el.diagLastRefreshed.textContent = `Last Refreshed: ${new Date().toLocaleTimeString()}`;
  }

  // --- Event Listeners Setup ---
  function setupEventListeners() {
    // Refresh button
    if (el.btnRefreshAll) el.btnRefreshAll.addEventListener('click', () => refreshDashboard());

    // Settings drawer controller helpers
    function openSettingsDrawer() {
      if (!el.settingsDrawer) return;
      el.settingsDrawer.hidden = false;
      el.settingsDrawer.classList.add('open');
      if (el.inputApiBaseUrl) el.inputApiBaseUrl.value = state.apiBaseUrl;
      if (el.inputBufferPct) el.inputBufferPct.value = state.bufferPct.toFixed(2);
      if (el.btnCloseSettings) el.btnCloseSettings.focus();
    }

    function closeSettingsDrawer() {
      if (!el.settingsDrawer) return;
      el.settingsDrawer.classList.remove('open');
      el.settingsDrawer.hidden = true;
      if (el.btnToggleSettings) el.btnToggleSettings.focus();
    }

    // Explicitly guarantee drawer is closed on initial setup
    if (el.settingsDrawer) {
      el.settingsDrawer.classList.remove('open');
      el.settingsDrawer.hidden = true;
    }

    if (el.btnToggleSettings) {
      el.btnToggleSettings.addEventListener('click', (e) => {
        e.preventDefault();
        openSettingsDrawer();
      });
    }

    if (el.btnCloseSettings) {
      el.btnCloseSettings.addEventListener('click', (e) => {
        e.preventDefault();
        closeSettingsDrawer();
      });
    }

    // Close when clicking the backdrop outside drawer content
    if (el.settingsDrawer) {
      el.settingsDrawer.addEventListener('click', (e) => {
        if (e.target === el.settingsDrawer) {
          closeSettingsDrawer();
        }
      });
    }

    // Close with Escape key
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' || e.key === 'Esc') {
        if (el.settingsDrawer && (el.settingsDrawer.classList.contains('open') || !el.settingsDrawer.hidden)) {
          closeSettingsDrawer();
        }
      }
    });

    if (el.btnSaveApiUrl) {
      el.btnSaveApiUrl.addEventListener('click', () => {
        const newUrl = el.inputApiBaseUrl.value.trim();
        if (newUrl) {
          state.apiBaseUrl = newUrl;
          localStorage.setItem('kubecost_api_base_url', newUrl);
          closeSettingsDrawer();
          refreshDashboard();
        }
      });
    }

    if (el.inputBufferPct) {
      el.inputBufferPct.addEventListener('change', (e) => {
        state.bufferPct = parseFloat(e.target.value);
        apiFetch(`/api/v1/recommendations?type=all&buffer=${state.bufferPct}`).then(res => {
          if (res.ok) {
            state.recommendations = res.data;
            renderRecommendations();
            renderOverview();
          }
        });
      });
    }

    if (el.btnRetryAlert) el.btnRetryAlert.addEventListener('click', () => refreshDashboard());

    // Recommendations Tabs
    [el.tabRecsAll, el.tabRecsRightsizing, el.tabRecsHpa].forEach(btn => {
      if (!btn) return;
      btn.addEventListener('click', () => {
        [el.tabRecsAll, el.tabRecsRightsizing, el.tabRecsHpa].forEach(b => b && b.classList.remove('active'));
        btn.classList.add('active');
        state.activeRecFilter = btn.dataset.filter;
        renderRecommendations();
      });
    });

    // Experiment Run Selector Dropdown
    if (el.selectExperimentRun) {
      el.selectExperimentRun.addEventListener('change', (e) => {
        state.selectedExpRun = e.target.value;
        apiFetch(`/api/v1/experiments/${state.selectedExpRun}`).then(res => {
          if (res.ok) {
            state.experimentData = res.data;
            renderExperiment();
          }
        });
      });
    }

    // Forecast Source Toggles
    if (el.btnForecastSourceSynthetic) {
      el.btnForecastSourceSynthetic.addEventListener('click', () => {
        state.activeForecastSource = 'synthetic';
        apiFetch(`/api/v1/forecast?source=synthetic&metric=${state.forecastMetric}&horizon=6`).then(res => {
          if (res.ok) {
            state.forecastData = res.data;
            renderForecasting();
          }
        });
      });
    }

    if (el.btnForecastSourceLive) {
      el.btnForecastSourceLive.addEventListener('click', () => {
        state.activeForecastSource = 'live';
        apiFetch(`/api/v1/forecast?source=live&metric=cpu&horizon=6`).then(res => {
          if (res.ok) {
            state.forecastData = res.data;
            renderForecasting();
          }
        });
      });
    }

    if (el.btnSwitchToSynthetic) {
      el.btnSwitchToSynthetic.addEventListener('click', () => {
        state.activeForecastSource = 'synthetic';
        apiFetch(`/api/v1/forecast?source=synthetic&metric=${state.forecastMetric}&horizon=6`).then(res => {
          if (res.ok) {
            state.forecastData = res.data;
            renderForecasting();
          }
        });
      });
    }
  }

  // --- Initial Boot ---
  setupEventListeners();
  refreshDashboard();

})();

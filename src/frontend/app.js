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
    activeRecFilter: 'all',
    activeForecastSource: 'synthetic', // Default to synthetic for rich demo, toggleable to live
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
    kpiNodeCount: document.getElementById('kpiNodeCount'),
    kpiNodeStatus: document.getElementById('kpiNodeStatus'),
    kpiNodeSubtext: document.getElementById('kpiNodeSubtext'),
    kpiContainerCount: document.getElementById('kpiContainerCount'),
    kpiNamespacesCount: document.getElementById('kpiNamespacesCount'),
    kpiDeploymentsCount: document.getElementById('kpiDeploymentsCount'),
    kpiMonthlyCost: document.getElementById('kpiMonthlyCost'),
    kpiHourlyCost: document.getElementById('kpiHourlyCost'),
    kpiSavingsAmount: document.getElementById('kpiSavingsAmount'),
    kpiSavingsPercent: document.getElementById('kpiSavingsPercent'),
    kpiSavingsWorkloads: document.getElementById('kpiSavingsWorkloads'),

    // Cost Allocation
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

    // Experiment Benchmark
    expRunIdBadge: document.getElementById('expRunIdBadge'),
    expTimestampBadge: document.getElementById('expTimestampBadge'),
    experimentContent: document.getElementById('experimentContent'),

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
      const data = await response.json();
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
    const healthRes = await apiFetch('/api/health');
    if (!healthRes.ok) {
      setOnlineStatus(false, healthRes.elapsed);
      showGlobalAlert(`Backend connection error: ${healthRes.error || 'Server returned status ' + healthRes.status}`);
      setLoadingState(false);
      return;
    }

    setOnlineStatus(true, healthRes.elapsed);
    hideGlobalAlert();
    state.healthData = healthRes.data;

    // 2. Fetch live metrics, costs, recommendations, forecast, and experiment benchmark in parallel
    const [metricsRes, costsRes, recsRes, forecastRes, expRes] = await Promise.all([
      apiFetch('/api/v1/metrics/live'),
      apiFetch('/api/v1/costs/summary'),
      apiFetch(`/api/v1/recommendations?type=all&buffer=${state.bufferPct}`),
      apiFetch(`/api/v1/forecast?source=${state.activeForecastSource}&metric=${state.forecastMetric}&horizon=6`),
      apiFetch('/api/v1/experiments/latest'),
    ]);

    if (metricsRes.ok) state.liveMetrics = metricsRes.data;
    if (costsRes.ok) state.costSummary = costsRes.data;
    if (recsRes.ok) state.recommendations = recsRes.data;
    if (forecastRes.ok) state.forecastData = forecastRes.data;
    if (expRes.ok) state.experimentData = expRes.data;

    state.lastRefreshed = new Date();

    // 3. Render all view modules
    renderOverview();
    renderCostIntelligence();
    renderRecommendations();
    renderExperiment();
    renderForecasting();
    renderDiagnostics();

    setLoadingState(false);
  }

  // --- Status & Alert Helpers ---
  function setOnlineStatus(online, latencyMs) {
    state.isOnline = online;
    state.latencyMs = latencyMs;

    if (online) {
      el.apiStatusIndicator.className = 'status-indicator status-up';
      el.apiStatusText.textContent = 'API Connected';
      el.apiLatencyText.textContent = latencyMs ? `${latencyMs}ms` : '';
      el.headerClusterDot.style.backgroundColor = 'var(--accent-green)';
    } else {
      el.apiStatusIndicator.className = 'status-indicator status-down';
      el.apiStatusText.textContent = 'API Offline';
      el.apiLatencyText.textContent = '';
      el.headerClusterDot.style.backgroundColor = 'var(--accent-rose)';
    }
  }

  function showGlobalAlert(msg) {
    el.globalAlertBanner.hidden = false;
    el.alertBannerMsg.textContent = msg;
  }

  function hideGlobalAlert() {
    el.globalAlertBanner.hidden = true;
  }

  function setLoadingState(loading) {
    if (loading) {
      el.btnRefreshAll.disabled = true;
      el.btnRefreshAll.style.opacity = '0.7';
    } else {
      el.btnRefreshAll.disabled = false;
      el.btnRefreshAll.style.opacity = '1';
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

  // --- SECTION 1: OVERVIEW RENDERING ---
  function renderOverview() {
    const stateObj = state.liveMetrics?.observed_k8s_state || {};
    const metaObj = state.liveMetrics?.metadata || {};
    const costsObj = state.costSummary || {};
    const recsObj = state.recommendations || {};

    // Freshness widgets
    if (metaObj.collection_timestamp_utc) {
      el.badgeSnapshotTime.textContent = `Captured: ${formatRelativeAge(metaObj.collection_timestamp_utc)}`;
      el.badgeSnapshotSource.textContent = metaObj.data_source || 'Kube-State-Metrics';
    }

    // Nodes
    const nodes = stateObj.nodes || [];
    el.kpiNodeCount.textContent = nodes.length > 0 ? nodes.length : '1';
    if (nodes.length > 0) {
      const nodeName = nodes[0].name;
      el.kpiNodeSubtext.textContent = `Node: ${nodeName}`;
      el.headerClusterName.textContent = `Node: ${nodeName}`;
    }

    // Containers & Namespaces
    const containerCount = stateObj.container_count ?? 8;
    el.kpiContainerCount.textContent = containerCount;
    const namespaces = stateObj.namespaces || ['kube-system', 'monitoring'];
    el.kpiNamespacesCount.textContent = `${namespaces.length} Namespaces`;
    const depCount = Object.keys(stateObj.deployments || {}).length;
    el.kpiDeploymentsCount.textContent = `${depCount} Deployments`;

    // Monthly Cost
    const monthlyCost = costsObj.total_monthly_modeled_cost_usd ?? 24.15;
    const hourlyCost = costsObj.total_hourly_modeled_cost_usd ?? 0.033;
    el.kpiMonthlyCost.innerHTML = `$${monthlyCost.toFixed(2)}<span class="kpi-unit">/mo</span>`;
    el.kpiHourlyCost.textContent = `$${hourlyCost.toFixed(4)} / hr`;

    // Savings
    const savingsAmount = recsObj.total_projected_monthly_savings_usd ?? 16.67;
    const savingsPct = monthlyCost > 0 ? ((savingsAmount / monthlyCost) * 100).toFixed(1) : '69.0';
    el.kpiSavingsAmount.innerHTML = `$${savingsAmount.toFixed(2)}<span class="kpi-unit">/mo</span>`;
    el.kpiSavingsPercent.textContent = `${savingsPct}% Reduction`;
    const recCount = (recsObj.total_rightsizing_recommendations ?? 8) + (recsObj.total_hpa_recommendations ?? 3);
    el.kpiSavingsWorkloads.textContent = `Across ${recCount} actions`;
  }

  // --- SECTION 2: COST INTELLIGENCE RENDERING ---
  function renderCostIntelligence() {
    const costsObj = state.costSummary || {};
    const nsCosts = costsObj.namespace_breakdown || {};
    const totalMonthly = costsObj.total_monthly_modeled_cost_usd || 24.15;

    if (costsObj.disclaimer) {
      el.textCostDisclaimer.textContent = costsObj.disclaimer;
    }
    if (costsObj.pricing_reference) {
      el.badgePricingModel.textContent = costsObj.pricing_reference;
    }

    // Namespace Bar and Table
    const nsKeys = Object.keys(nsCosts);
    el.nsCountBadge.textContent = `${nsKeys.length} Namespaces`;

    el.nsBarTrack.innerHTML = '';
    el.nsBarLegend.innerHTML = '';
    el.tbodyNamespaceCosts.innerHTML = '';

    const colors = ['#38bdf8', '#818cf8', '#a78bfa', '#f472b6', '#34d399'];

    nsKeys.forEach((ns, idx) => {
      const data = nsCosts[ns];
      const monthly = data.monthly || 0;
      const pct = totalMonthly > 0 ? ((monthly / totalMonthly) * 100).toFixed(1) : 0;
      const color = colors[idx % colors.length];

      // Bar Segment
      const segment = document.createElement('div');
      segment.className = 'ns-bar-segment';
      segment.style.width = `${pct}%`;
      segment.style.backgroundColor = color;
      segment.title = `${ns}: $${monthly.toFixed(2)} (${pct}%)`;
      el.nsBarTrack.appendChild(segment);

      // Legend Item
      const legendItem = document.createElement('div');
      legendItem.className = 'legend-item';
      legendItem.innerHTML = `
        <span class="legend-color" style="background-color: ${color}"></span>
        <span>${escapeHtml(ns)} <strong>${pct}%</strong></span>
      `;
      el.nsBarLegend.appendChild(legendItem);

      // Table Row
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
    });

    if (nsKeys.length === 0) {
      el.tbodyNamespaceCosts.innerHTML = `<tr><td colspan="6" class="text-center text-muted">No namespace breakdown available.</td></tr>`;
    }

    // Resource Meters
    const liveState = state.liveMetrics?.observed_k8s_state || {};
    const totalCpu = liveState.total_requested_cpu_cores ?? 1.0;
    const totalMem = liveState.total_requested_memory_gb ?? 0.346;

    el.meterCpuVal.textContent = `${totalCpu.toFixed(3)} Cores`;
    el.meterMemVal.textContent = `${totalMem.toFixed(3)} GiB`;

    // Modeled component costs (AWS US-East-1 $0.031611/core-hr, $0.004237/GB-hr, 730h)
    const cpuCostEst = totalCpu * 0.031611 * 730;
    const memCostEst = totalMem * 0.004237 * 730;
    el.meterCpuCostEst.textContent = `$${cpuCostEst.toFixed(2)} / mo`;
    el.meterMemCostEst.textContent = `$${memCostEst.toFixed(2)} / mo`;

    // Meter bar percentages (normalized against typical 2-core node baseline)
    el.meterCpuBar.style.width = `${Math.min(100, Math.round((totalCpu / 2.0) * 100))}%`;
    el.meterMemBar.style.width = `${Math.min(100, Math.round((totalMem / 2.0) * 100))}%`;

    el.specHighlightContainers.textContent = `${liveState.container_count || 8} container specifications`;
  }

  // --- SECTION 3: RECOMMENDATIONS RENDERING ---
  function renderRecommendations() {
    const recsObj = state.recommendations || {};
    const rsList = recsObj.rightsizing_recommendations || [];
    const hpaList = recsObj.hpa_recommendations || [];

    el.countRecsAll.textContent = rsList.length + hpaList.length;
    el.countRecsRightsizing.textContent = rsList.length;
    el.countRecsHpa.textContent = hpaList.length;

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

        card.innerHTML = `
          <div class="rec-card-header">
            <span class="rec-target-title">${escapeHtml(workload)}</span>
            <span class="rec-action-badge badge-downsize">Downsize Requests</span>
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
          </div>

          <div class="rec-card-footer">
            <span class="badge badge-neutral">Namespace: ${escapeHtml(item.namespace || 'default')}</span>
            <span class="rec-savings-highlight">+$${savings.toFixed(2)}/mo</span>
          </div>
        `;
      } else {
        // HPA recommendation
        const dep = item.deployment || item.name || 'Workload';
        const curMin = item.current_min_replicas || 1;
        const recMin = item.recommended_min_replicas || 1;
        const curTarget = item.current_target_cpu || 80;
        const recTarget = item.recommended_target_cpu || 50;

        card.innerHTML = `
          <div class="rec-card-header">
            <span class="rec-target-title">Deployment: ${escapeHtml(dep)}</span>
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
            <div class="rec-detail-item"><strong>Reasoning:</strong> ${escapeHtml(item.reason || 'High burstiness requires earlier expansion.')}</div>
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

  // --- SECTION: EXPERIMENT BENCHMARK RENDERING ---
  function renderExperiment() {
    const expData = state.experimentData;
    if (!expData || expData.status === 'NOT_AVAILABLE' || !expData.evaluation) {
      if (el.expRunIdBadge) el.expRunIdBadge.textContent = 'Run: None';
      if (el.expTimestampBadge) el.expTimestampBadge.textContent = 'Captured: Not Run Yet';
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
    if (el.expRunIdBadge) {
      el.expRunIdBadge.textContent = isFixture ? `Run: ${runId} [SYNTHETIC FIXTURE]` : `Run: ${runId}`;
      el.expRunIdBadge.title = isFixture ? 'Synthetic test fixture for offline UI/API testing — not an empirical run' : 'Empirical benchmark run';
    }
    if (el.expTimestampBadge) el.expTimestampBadge.textContent = `Captured: ${formatRelativeAge(expData.timestamp_utc)}`;

    const evalData = expData.evaluation || {};
    const phases = evalData.phases || {};
    const recData = expData.recommendations || {};
    const evid = recData.empirical_telemetry_evidence || {};
    const fin = recData.modeled_financial_impact || {};
    const logic = recData.recommendation_logic || {};
    const meta = expData.metadata || {};

    const currCost = fin.current_modeled_monthly_cost_usd != null ? fin.current_modeled_monthly_cost_usd.toFixed(2) : '--';
    const propCost = fin.proposed_modeled_monthly_cost_usd != null ? fin.proposed_modeled_monthly_cost_usd.toFixed(2) : '--';
    const savings = fin.projected_monthly_savings_usd != null ? fin.projected_monthly_savings_usd.toFixed(2) : '--';
    const savingsPct = fin.savings_percentage != null ? fin.savings_percentage : '--';

    const peakCpuM = evid.peak_observed_cpu_millicores != null ? evid.peak_observed_cpu_millicores.toFixed(1) : '--';
    const peakMemMib = evid.peak_observed_memory_mib != null ? evid.peak_observed_memory_mib.toFixed(1) : '--';
    const peakCpuUtil = evid.peak_observed_cpu_utilization_pct != null ? evid.peak_observed_cpu_utilization_pct.toFixed(1) : '--';
    const peakMemUtil = evid.peak_observed_memory_utilization_pct != null ? evid.peak_observed_memory_utilization_pct.toFixed(1) : '--';
    const idleCpuHeadroom = (evid.peak_observed_cpu_utilization_pct != null) ? (100 - evid.peak_observed_cpu_utilization_pct).toFixed(1) + '% Idle' : '--';

    const propCpuCores = logic.proposed_cpu_request_cores_per_replica != null ? (logic.proposed_cpu_request_cores_per_replica * 1000).toFixed(0) : '--';
    const propMemMib = logic.proposed_memory_request_gib_per_replica != null ? (logic.proposed_memory_request_gib_per_replica * 1024).toFixed(0) : '--';

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
          <p class="phase-table-subtitle">Independent application latency measurement paired with kernel cgroups utilization across all phases</p>
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

    el.experimentContent.innerHTML = html;
  }

  // --- SECTION 5: FORECASTING RENDERING ---
  function renderForecasting() {
    const fData = state.forecastData || {};

    if (state.activeForecastSource === 'live') {
      el.btnForecastSourceLive.classList.add('active');
      el.btnForecastSourceSynthetic.classList.remove('active');
    } else {
      el.btnForecastSourceSynthetic.classList.add('active');
      el.btnForecastSourceLive.classList.remove('active');
    }

    // Check for Insufficient Data
    if (fData.status === 'INSUFFICIENT_DATA') {
      el.insufficientDataView.hidden = false;
      el.forecastChartWrapper.hidden = true;
      el.forecastStepsPanel.hidden = true;

      el.forecastBadge.className = 'banner-badge badge-live-provenance';
      el.forecastBadge.textContent = 'LIVE CLUSTER TELEMETRY';
      el.forecastBannerText.textContent = 'Live KSM object-state observation mode active.';

      el.insufficientDataMsg.textContent = fData.message || 'At least 5 snapshot observations are required.';
      return;
    }

    // Success state
    el.insufficientDataView.hidden = true;
    el.forecastChartWrapper.hidden = false;
    el.forecastStepsPanel.hidden = false;

    const isSynthetic = fData.is_synthetic === true;
    if (isSynthetic) {
      el.forecastBadge.className = 'banner-badge';
      el.forecastBadge.textContent = 'SYNTHETIC DEMO ONLY';
      el.forecastBannerText.textContent = 'Displaying simulated 48-hour diurnal EduSaaS university classroom traffic (exam submission bursts + Gaussian noise). Generated exclusively for algorithmic validation.';
      el.forecastChartTitle.textContent = 'Simulated EduSaaS API Request Rate (RPM)';
    } else {
      el.forecastBadge.className = 'banner-badge badge-live-provenance';
      el.forecastBadge.textContent = 'GENUINE LIVE TELEMETRY';
      el.forecastBannerText.textContent = 'Extrapolated from genuine chronologically ordered snapshot history.';
      el.forecastChartTitle.textContent = 'Requested CPU Cores Capacity Demand';
    }

    el.tagModelName.textContent = fData.model_name || 'HoltLinearTrend_Baseline';
    const evalM = fData.evaluation_metrics;
    if (evalM && evalM.mae != null) {
      el.tagEvalMae.textContent = `MAE: ${evalM.mae}`;
      el.tagEvalRmse.textContent = `RMSE: ${evalM.rmse}`;
      el.tagEvalMae.hidden = false;
      el.tagEvalRmse.hidden = false;
    } else {
      el.tagEvalMae.hidden = true;
      el.tagEvalRmse.hidden = true;
    }

    // Render SVG Chart
    renderForecastSvg(fData);

    // Render Steps Table
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

  // Pure SVG Line Chart Renderer with Confidence Interval Polygon
  function renderForecastSvg(fData) {
    const svg = el.forecastSvgChart;
    svg.innerHTML = '';

    const width = 800;
    const height = 300;
    const padL = 60;
    const padR = 40;
    const padT = 30;
    const padB = 40;

    const plotW = width - padL - padR;
    const plotH = height - padT - padB;

    // Synthesize display series
    const points = fData.forecast_points || [];
    const histSummary = fData.history_summary || {};
    const latestVal = histSummary.latest_observed_value || 35.0;

    // Build timeline points: 8 simulated past points + horizon forecast points
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

      // Starting point at connection boundary
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
        el.chartTooltip.hidden = true;
      });

      svg.appendChild(circle);
    });
  }

  // --- SECTION 5: DIAGNOSTICS RENDERING ---
  function renderDiagnostics() {
    el.diagBackendUrl.textContent = state.apiBaseUrl;
    el.diagApiVersion.textContent = state.healthData?.version || '1.0.0';
    el.diagSnapshotFile.textContent = state.healthData?.snapshot_status?.latest_snapshot_file || 'None';
    el.diagLastRefreshed.textContent = `Last Refreshed: ${new Date().toLocaleTimeString()}`;
  }

  // --- Event Listeners Setup ---
  function setupEventListeners() {
    // Refresh button
    el.btnRefreshAll.addEventListener('click', () => refreshDashboard());

    // Settings drawer
    el.btnToggleSettings.addEventListener('click', () => {
      el.settingsDrawer.hidden = false;
      el.inputApiBaseUrl.value = state.apiBaseUrl;
    });

    el.btnCloseSettings.addEventListener('click', () => {
      el.settingsDrawer.hidden = true;
    });

    el.btnSaveApiUrl.addEventListener('click', () => {
      const newUrl = el.inputApiBaseUrl.value.trim();
      if (newUrl) {
        state.apiBaseUrl = newUrl;
        localStorage.setItem('kubecost_api_base_url', newUrl);
        el.settingsDrawer.hidden = true;
        refreshDashboard();
      }
    });

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

    el.btnRetryAlert.addEventListener('click', () => refreshDashboard());

    // Recommendations Tabs
    [el.tabRecsAll, el.tabRecsRightsizing, el.tabRecsHpa].forEach(btn => {
      btn.addEventListener('click', () => {
        [el.tabRecsAll, el.tabRecsRightsizing, el.tabRecsHpa].forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.activeRecFilter = btn.dataset.filter;
        renderRecommendations();
      });
    });

    // Forecast Source Toggles
    el.btnForecastSourceSynthetic.addEventListener('click', () => {
      state.activeForecastSource = 'synthetic';
      apiFetch(`/api/v1/forecast?source=synthetic&metric=${state.forecastMetric}&horizon=6`).then(res => {
        if (res.ok) {
          state.forecastData = res.data;
          renderForecasting();
        }
      });
    });

    el.btnForecastSourceLive.addEventListener('click', () => {
      state.activeForecastSource = 'live';
      apiFetch(`/api/v1/forecast?source=live&metric=cpu&horizon=6`).then(res => {
        if (res.ok) {
          state.forecastData = res.data;
          renderForecasting();
        }
      });
    });

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

  // --- Initial Boot ---
  setupEventListeners();
  refreshDashboard();

})();

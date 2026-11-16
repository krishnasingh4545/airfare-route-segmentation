/**
 * AEROMATRIX Cockpit Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  // Mode / View Switcher
  const viewBtns = document.querySelectorAll(".nav-tab-btn");
  const viewPanels = document.querySelectorAll(".view-panel");

  viewBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetView = btn.getAttribute("data-view");
      viewBtns.forEach(b => b.classList.remove("active"));
      viewPanels.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const activePanel = document.getElementById(targetView);
      if (activePanel) {
        activePanel.classList.add("active");
      }
    });
  });

  // Search Form
  const searchForm = document.getElementById("cockpitSearchForm");
  if (searchForm) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      executeCockpitScan();
    });
  }

  // Airport Swap Button
  const btnSwap = document.getElementById("btnSwapAtc");
  if (btnSwap) {
    btnSwap.addEventListener("click", () => {
      const fromSel = document.getElementById("fromCity");
      const toSel = document.getElementById("toCity");
      if (fromSel && toSel) {
        const temp = fromSel.value;
        fromSel.value = toSel.value;
        toSel.value = temp;

        btnSwap.style.transform = "rotate(180deg)";
        setTimeout(() => { btnSwap.style.transform = "none"; }, 300);

        executeCockpitScan();
      }
    });
  }

  // Quick Vector Presets
  document.querySelectorAll(".preset-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      const from = pill.getAttribute("data-from");
      const to = pill.getAttribute("data-to");
      const fromSel = document.getElementById("fromCity");
      const toSel = document.getElementById("toCity");

      if (fromSel && toSel) {
        fromSel.value = from;
        toSel.value = to;
        executeCockpitScan();
      }
    });
  });

  // PCA Route Filter
  const pcaFilter = document.getElementById("pcaRouteFilter");
  if (pcaFilter) {
    pcaFilter.addEventListener("input", (e) => {
      const query = (e.target.value || "").trim().toLowerCase();
      if (window.MODEL_METRICS && window.MODEL_METRICS.pca_points) {
        let pts = window.MODEL_METRICS.pca_points;
        if (query) {
          pts = pts.filter(p => p.route.toLowerCase().includes(query));
        }
        renderPcaScatter(pts, window.CURRENT_ACTIVE_ROUTE || "");
      }
    });
  }

  // Initialize with initial data
  if (window.INITIAL_DATA) {
    window.CURRENT_ACTIVE_ROUTE = window.INITIAL_DATA.route;
    updateCockpitUI(window.INITIAL_DATA);
  }

  if (window.MODEL_METRICS) {
    renderEvaluationHub(window.MODEL_METRICS);
  }
});

function executeCockpitScan() {
  const fromCity = document.getElementById("fromCity").value;
  const toCity = document.getElementById("toCity").value;
  const departDate = document.getElementById("departDate").value;
  const travelClass = document.getElementById("travelClass").value;

  const btn = document.querySelector(".btn-execute-analysis");
  const origHtml = btn.innerHTML;
  btn.innerHTML = `<span>⏳ Scanning Corridors...</span>`;
  btn.disabled = true;

  const url = `/api/predict?from=${encodeURIComponent(fromCity)}&to=${encodeURIComponent(toCity)}&depart=${encodeURIComponent(departDate)}&class=${encodeURIComponent(travelClass)}`;

  fetch(url)
    .then(res => res.json())
    .then(data => {
      window.CURRENT_ACTIVE_ROUTE = data.route;
      updateCockpitUI(data);
    })
    .catch(err => {
      console.error("Telemetry query failed:", err);
    })
    .finally(() => {
      btn.innerHTML = origHtml;
      btn.disabled = false;
    });
}

function updateCockpitUI(data) {
  // 1. Route IATA Callout
  const calloutIata = document.getElementById("calloutIata");
  if (calloutIata) {
    calloutIata.innerHTML = `<span>${data.origin_code}</span> <span class="flight-arrow">➔</span> <span>${data.destination_code}</span>`;
  }

  const calloutCities = document.getElementById("calloutCities");
  if (calloutCities) {
    calloutCities.textContent = `${data.origin} (${data.origin_airport}) to ${data.destination} (${data.destination_airport})`;
  }

  // 2. Verdict Badge
  const verdictBadge = document.getElementById("verdictBadge");
  if (verdictBadge) {
    verdictBadge.className = `signal-badge-cockpit ${data.verdict_badge}`;
    const icon = data.verdict_badge === "book-now" ? "⚡" : (data.verdict_badge === "wait" ? "⏳" : "👁");
    verdictBadge.innerHTML = `<span>${icon}</span> ${data.verdict}`;
  }

  // 3. Telemetry Cells
  const statFare = document.getElementById("statFare");
  if (statFare) statFare.textContent = `₹${data.estimated_fare.toLocaleString()}`;

  const statConfidence = document.getElementById("statConfidence");
  if (statConfidence) statConfidence.textContent = `${data.confidence_score}%`;

  const statSurge = document.getElementById("statSurge");
  if (statSurge) statSurge.textContent = `${data.cluster_info.surge_ratio}x`;

  const statDays = document.getElementById("statDays");
  if (statDays) statDays.textContent = `${data.days_left} Days`;

  // 4. Percentile Gauge Pin
  const gaugePin = document.getElementById("gaugePin");
  if (gaugePin) {
    gaugePin.style.left = `${data.percentile_rank}%`;
  }

  const medianVal = document.getElementById("medianVal");
  if (medianVal) medianVal.textContent = `MEDIAN BENCHMARK: ₹${data.price_benchmarks.median.toLocaleString()}`;

  const p10Val = document.getElementById("p10Val");
  if (p10Val) p10Val.textContent = `P10 (Floor): ₹${data.price_benchmarks.p10.toLocaleString()}`;

  const p90Val = document.getElementById("p90Val");
  if (p90Val) p90Val.textContent = `P90 (Peak): ₹${data.price_benchmarks.p90.toLocaleString()}`;

  // 5. Financial Advantage Callout
  const advantageMsg = document.getElementById("advantageMsg");
  if (advantageMsg) {
    advantageMsg.textContent = `Financial Protection Active: Booking now avoids up to ₹${data.potential_savings_inr.toLocaleString()} in departure-week surge escalation.`;
  }

  const advantagePill = document.getElementById("advantagePill");
  if (advantagePill) {
    advantagePill.textContent = `Save ${data.savings_pct}% vs Peak`;
  }

  // 6. Booking Yield Curve
  if (data.curve_data) {
    renderBookingCurve(data.curve_data, data.estimated_fare);
  }

  // 7. PCA Map Spotlight
  if (window.MODEL_METRICS && window.MODEL_METRICS.pca_points) {
    renderPcaScatter(window.MODEL_METRICS.pca_points, data.route);
  }
}

function renderEvaluationHub(metrics) {
  if (metrics.k_eval_sweep) {
    renderElbowChart(metrics.k_eval_sweep);
    renderSilhouetteChart(metrics.k_eval_sweep);
  }
  if (metrics.distance_comparison) {
    renderDistanceComparison(metrics.distance_comparison);
  }
  if (metrics.pca_points) {
    renderPcaScatter(metrics.pca_points, window.CURRENT_ACTIVE_ROUTE || "");
  }
}

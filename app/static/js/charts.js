/**
 * AEROMATRIX Telemetry Visualizer (Clean Light Theme)
 * High-precision light analytics charts
 */

let bookingCurveChart = null;
let pcaScatterChart = null;
let elbowChart = null;
let silhouetteChart = null;
let distanceMetricChart = null;

function renderBookingCurve(curveData, currentFare) {
  const ctx = document.getElementById("bookingCurveCanvas");
  if (!ctx) return;

  const days = curveData.days.slice().reverse();
  const prices = curveData.prices.slice().reverse();

  if (bookingCurveChart) {
    bookingCurveChart.destroy();
  }

  const chartCtx = ctx.getContext("2d");
  const gradient = chartCtx.createLinearGradient(0, 0, 0, 320);
  gradient.addColorStop(0, "rgba(37, 99, 235, 0.22)");
  gradient.addColorStop(0.6, "rgba(37, 99, 235, 0.05)");
  gradient.addColorStop(1, "rgba(255, 255, 255, 0.0)");

  bookingCurveChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: days.map(d => `${d}d out`),
      datasets: [
        {
          label: "Yield Trajectory (INR)",
          data: prices,
          borderColor: "#2563eb",
          borderWidth: 2.8,
          backgroundColor: gradient,
          fill: true,
          tension: 0.35,
          pointRadius: 4.5,
          pointHoverRadius: 8,
          pointBackgroundColor: "#2563eb",
          pointBorderColor: "#ffffff",
          pointBorderWidth: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#0f172a",
          padding: 10,
          cornerRadius: 8,
          titleFont: { family: 'JetBrains Mono', size: 12 },
          bodyFont: { family: 'JetBrains Mono', size: 13, weight: 'bold' },
          callbacks: {
            label: function(context) {
              return `  Median Fare: ₹${context.raw.toLocaleString()}`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(226, 232, 240, 0.7)" },
          ticks: { color: "#64748b", font: { family: 'JetBrains Mono', size: 11, weight: '600' } }
        },
        y: {
          grid: { color: "rgba(226, 232, 240, 0.7)" },
          ticks: {
            color: "#64748b",
            font: { family: 'JetBrains Mono', size: 11, weight: '600' },
            callback: function(value) {
              return "₹" + (value >= 1000 ? (value/1000).toFixed(0) + "k" : value);
            }
          }
        }
      }
    }
  });
}

function renderPcaScatter(pcaPoints, activeRoute = "") {
  const ctx = document.getElementById("pcaScatterCanvas");
  if (!ctx) return;

  if (pcaScatterChart) {
    pcaScatterChart.destroy();
  }

  const clusterColors = ["#f59e0b", "#6366f1", "#10b981", "#0284c7"];
  const clusterNames = [
    "Cross-Country Domestic Trunk",
    "Ultra-Long-Haul Intercontinental",
    "Short-Haul Regional Shuttles",
    "Regional International Gateway"
  ];

  const datasets = [];

  for (let c = 0; c < 4; c++) {
    const clusterPts = pcaPoints.filter(p => p.cluster === c);
    datasets.push({
      label: `C${c}: ${clusterNames[c]}`,
      data: clusterPts.map(p => ({
        x: p.pc1,
        y: p.pc2,
        route: p.route,
        mean_price: p.mean_price,
        avg_dur: p.avg_duration,
        surge: p.surge_ratio
      })),
      backgroundColor: clusterColors[c],
      borderColor: "#ffffff",
      borderWidth: 2,
      pointRadius: function(ctx) {
        if (!ctx.raw) return 6;
        return (activeRoute && ctx.raw.route.toLowerCase().includes(activeRoute.toLowerCase())) ? 13 : 6.5;
      },
      pointHoverRadius: 10
    });
  }

  pcaScatterChart = new Chart(ctx, {
    type: "scatter",
    data: { datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: { color: "#334155", font: { family: 'JetBrains Mono', size: 11, weight: '600' }, boxWidth: 12 }
        },
        tooltip: {
          backgroundColor: "#0f172a",
          padding: 12,
          cornerRadius: 8,
          titleFont: { family: 'JetBrains Mono', size: 12 },
          bodyFont: { family: 'JetBrains Mono', size: 12 },
          callbacks: {
            label: function(ctx) {
              const r = ctx.raw;
              return [
                `Corridor: ${r.route}`,
                `PC1: ${r.x.toFixed(2)}, PC2: ${r.y.toFixed(2)}`,
                `Mean Fare: ₹${Math.round(r.mean_price).toLocaleString()}`,
                `Duration: ${r.avg_dur}h | Surge: ${r.surge.toFixed(2)}x`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          title: { display: true, text: "Principal Component 1 (Fare Scale & Distance - 68.1% Var)", color: "#475569", font: { family: 'JetBrains Mono', weight: 'bold' } },
          grid: { color: "rgba(226, 232, 240, 0.7)" },
          ticks: { color: "#64748b", font: { family: 'JetBrains Mono', weight: '600' } }
        },
        y: {
          title: { display: true, text: "Principal Component 2 (Direct Density vs Volatility - 11.1% Var)", color: "#475569", font: { family: 'JetBrains Mono', weight: 'bold' } },
          grid: { color: "rgba(226, 232, 240, 0.7)" },
          ticks: { color: "#64748b", font: { family: 'JetBrains Mono', weight: '600' } }
        }
      }
    }
  });
}

function renderElbowChart(kSweep) {
  const ctx = document.getElementById("elbowCurveCanvas");
  if (!ctx) return;

  if (elbowChart) {
    elbowChart.destroy();
  }

  elbowChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: kSweep.map(d => `K=${d.k}`),
      datasets: [{
        label: "WCSS (Inertia)",
        data: kSweep.map(d => d.wcss),
        borderColor: "#2563eb",
        borderWidth: 2.5,
        backgroundColor: "rgba(37, 99, 235, 0.08)",
        fill: true,
        tension: 0.25,
        pointRadius: 6,
        pointBackgroundColor: function(ctx) {
          return ctx.dataIndex === 2 ? "#dc2626" : "#2563eb";
        },
        pointBorderColor: "#ffffff",
        pointBorderWidth: 2.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#0f172a",
          padding: 10,
          cornerRadius: 8,
          callbacks: {
            afterLabel: function(ctx) {
              if (ctx.dataIndex === 2) return "★ Optimal Defensible Elbow (K=4)";
            }
          }
        }
      },
      scales: {
        x: { grid: { color: "rgba(226, 232, 240, 0.7)" }, ticks: { color: "#64748b", font: { family: 'JetBrains Mono', weight: '600' } } },
        y: { grid: { color: "rgba(226, 232, 240, 0.7)" }, ticks: { color: "#64748b", font: { family: 'JetBrains Mono', weight: '600' } } }
      }
    }
  });
}

function renderSilhouetteChart(kSweep) {
  const ctx = document.getElementById("silhouetteCanvas");
  if (!ctx) return;

  if (silhouetteChart) {
    silhouetteChart.destroy();
  }

  silhouetteChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: kSweep.map(d => `K=${d.k}`),
      datasets: [
        {
          label: "Silhouette Score",
          data: kSweep.map(d => d.silhouette),
          backgroundColor: kSweep.map(d => d.k === 4 ? "#059669" : "#cbd5e1"),
          borderRadius: 6
        },
        {
          label: "Davies-Bouldin (Lower is better)",
          data: kSweep.map(d => d.davies_bouldin),
          backgroundColor: "#f59e0b",
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#334155", font: { family: 'JetBrains Mono', size: 11, weight: '600' } } },
        tooltip: {
          backgroundColor: "#0f172a",
          padding: 10,
          cornerRadius: 8
        }
      },
      scales: {
        x: { grid: { color: "rgba(226, 232, 240, 0.7)" }, ticks: { color: "#64748b", font: { family: 'JetBrains Mono', weight: '600' } } },
        y: { grid: { color: "rgba(226, 232, 240, 0.7)" }, ticks: { color: "#64748b", font: { family: 'JetBrains Mono', weight: '600' } } }
      }
    }
  });
}

function renderDistanceComparison(distanceData) {
  const ctx = document.getElementById("distanceCompCanvas");
  if (!ctx) return;

  if (distanceMetricChart) {
    distanceMetricChart.destroy();
  }

  const eucItems = distanceData.filter(d => d.algorithm.includes("Euclidean"));
  const manItems = distanceData.filter(d => d.algorithm.includes("Manhattan"));

  distanceMetricChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: eucItems.map(d => `K=${d.k}`),
      datasets: [
        {
          label: "Euclidean L2 Silhouette",
          data: eucItems.map(d => d.silhouette_euclidean),
          backgroundColor: "#3b82f6",
          borderRadius: 6
        },
        {
          label: "Manhattan L1 Silhouette",
          data: manItems.map(d => d.silhouette_manhattan),
          backgroundColor: "#059669",
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#334155", font: { family: 'JetBrains Mono', size: 11, weight: '600' } } },
        tooltip: {
          backgroundColor: "#0f172a",
          padding: 10,
          cornerRadius: 8
        }
      },
      scales: {
        x: { grid: { color: "rgba(226, 232, 240, 0.7)" }, ticks: { color: "#64748b", font: { family: 'JetBrains Mono', weight: '600' } } },
        y: { grid: { color: "rgba(226, 232, 240, 0.7)" }, ticks: { color: "#64748b", font: { family: 'JetBrains Mono', weight: '600' } }, min: 0, max: 0.7 }
      }
    }
  });
}

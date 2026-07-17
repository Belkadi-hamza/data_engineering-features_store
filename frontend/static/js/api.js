const API_BASE = "http://127.0.0.1:8000";

async function apiRequest(path, options = {}) {
  const init = {
    method: options.method || "GET",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  };

  if (options.body !== undefined) {
    init.body = JSON.stringify(options.body);
  }

  const response = await fetch(`${API_BASE}${path}`, init);
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `${response.status} ${response.statusText}`);
  }

  return response.json();
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = value ?? "";
  }
}

function setValue(id, value) {
  const el = document.getElementById(id);
  if (el) {
    el.value = value ?? "";
  }
}

function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "-";
  }
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(Number(value));
}

function parseClientId(input) {
  const id = Number(input.trim());
  if (!Number.isInteger(id) || id <= 0) {
    throw new Error("Please enter a valid client ID.");
  }
  return id;
}

function showError(message) {
  alert(message);
}

async function loadHealthData() {
  try {
    const data = await apiRequest("/health");
    setText("dashboard-mongo-status", data.status === "OK" ? "Connected" : "Offline");
    setText("dashboard-model-status", data.model_loaded ? "Loaded" : "Not loaded");
    setText("dashboard-customer-count", data.mongodb_documents ?? "-");
    setText("dashboard-api-status", data.status ?? "Unknown");

    setText("monitor-mongo-status", data.status === "OK" ? "Connected" : "Offline");
    setText("monitor-feature-status", data.status === "OK" ? "Healthy" : "Degraded");
    setText("monitor-model-status", data.model_loaded ? "Loaded" : "Not loaded");
    setText("monitor-api-status", data.status ?? "Unknown");
  } catch (error) {
    showError(`Health check failed: ${error.message}`);
  }
}

async function fetchCustomer(clientId) {
  return apiRequest(`/customer/${clientId}`);
}

async function searchCustomerPage() {
  try {
    const input = document.getElementById("customer-search-input");
    const clientId = parseClientId(input.value);
    const customer = await fetchCustomer(clientId);

    setText("customer-id", customer.CLIENTNUM);
    setText("customer-age", customer.Customer_Age);

    setText("customer-credit-limit", formatCurrency(customer.Credit_Limit));
    setText("customer-revolving-balance", formatCurrency(customer.Total_Revolving_Bal));
    setText("customer-open-to-buy", formatCurrency(customer.Avg_Open_To_Buy));
    setText("customer-utilization", `${customer.Avg_Utilization_Ratio ?? "-"}`);

    setText("customer-transactions", customer.Total_Trans_Ct ?? "-");
    setText("customer-total-amount", formatCurrency(customer.Total_Trans_Amt));
    setText("customer-months-book", customer.Months_on_book ?? "-");
    setText("customer-relations", customer.Total_Relationship_Count ?? "-");
    setText("customer-contacts", customer.Contacts_Count_12_mon ?? "-");
    setText("customer-inactive-months", customer.Months_Inactive_12_mon ?? "-");
  } catch (error) {
    showError(error.message);
  }
}

async function runPredictionPage() {
  try {
    const input = document.getElementById("prediction-client-id");
    const clientId = parseClientId(input.value);
    const result = await apiRequest(`/prediction/${clientId}`, { method: "POST" });

    setValue("prediction-client-id", result.client_id);
    setText("prediction-client-display", result.client_id);
    setText("prediction-label", result.label);
    setText("prediction-probability", `${result.probability}%`);
    setText("prediction-percent", `${result.probability}%`);
    setText("prediction-status", result.prediction === 1 ? "High risk of churn" : "Low risk of churn");

    const riskChip = document.getElementById("prediction-risk-chip");
    if (riskChip) {
      const riskClass = result.prediction === 1 ? "risk-high" : "risk-low";
      riskChip.className = `risk-chip ${riskClass}`;
      riskChip.textContent = result.prediction === 1 ? "High Risk" : "Low Risk";
    }

    const chartBar = document.getElementById("prediction-chart-bar");
    if (chartBar) {
      const width = Math.min(Math.max(result.probability, 0), 100);
      chartBar.style.width = `${width}%`;
      chartBar.dataset.value = `${width}%`;
    }

    const chartLabel = document.getElementById("prediction-probability-label");
    if (chartLabel) {
      chartLabel.textContent = `Probability ${result.probability}%`;
    }
  } catch (error) {
    showError(error.message);
  }
}

async function findTransactionCustomer() {
  try {
    const input = document.getElementById("transaction-search-input");
    const clientId = parseClientId(input.value);
    const customer = await fetchCustomer(clientId);

    setText("transaction-client-id-display", customer.CLIENTNUM);
    setText("transaction-total-transactions", customer.Total_Trans_Ct ?? "-");
    setText("transaction-total-amount", formatCurrency(customer.Total_Trans_Amt));
    setText("transaction-utilization", `${customer.Avg_Utilization_Ratio ?? "-"}`);
    setValue("transaction-client-id", customer.CLIENTNUM);
  } catch (error) {
    showError(error.message);
  }
}

async function addTransaction(event) {
  try {
    event.preventDefault();
    const clientId = parseClientId(document.getElementById("transaction-client-id").value);
    const amount = Number(document.getElementById("transaction-amount").value);
    if (Number.isNaN(amount)) {
      throw new Error("Please enter a valid transaction amount.");
    }

    const result = await apiRequest("/transaction/", {
      method: "POST",
      body: {
        client_id: clientId,
        amount,
      },
    });

    setText("transaction-client-id-display", result.CLIENTNUM);
    setText("transaction-total-transactions", result.Total_Trans_Ct ?? "-");
    setText("transaction-total-amount", formatCurrency(result.Total_Trans_Amt));
    setText("transaction-utilization", `${result.Avg_Utilization_Ratio ?? "-"}`);
    setText("update-count", result.Total_Trans_Ct ?? "-");
    setText("update-amount", formatCurrency(result.Total_Trans_Amt));
    setText("update-utilization", `${result.Avg_Utilization_Ratio ?? "-"}`);
  } catch (error) {
    showError(error.message);
  }
}

async function syncNow() {
  try {
    const result = await apiRequest("/sync/", { method: "POST" });
    setText("sync-status-message", result.message || "Synchronization finished.");
    setText("sync-progress-text", "Sync completed");
    setText("sync-progress-value", "100%");
    const progressBar = document.getElementById("sync-progress-bar");
    if (progressBar) {
      progressBar.style.width = "100%";
    }
  } catch (error) {
    showError(error.message);
  }
}

function initDashboard() {
  const refreshButton = document.getElementById("dashboard-refresh-button");
  if (refreshButton) {
    refreshButton.addEventListener("click", loadHealthData);
    loadHealthData();
  }
}

function initCustomer() {
  const searchButton = document.getElementById("customer-search-button");
  if (searchButton) {
    searchButton.addEventListener("click", searchCustomerPage);
  }
}

function initPrediction() {
  const predictionButton = document.getElementById("prediction-run-button");
  if (predictionButton) {
    predictionButton.addEventListener("click", runPredictionPage);
  }
}

async function runSimulationPage() {
  try {
    const clientId = parseClientId(document.getElementById("simulation-client-id").value);
    const numInput = document.getElementById("simulation-number-input");
    const numberOfTransactions = Number(numInput.value);

    const result = await apiRequest("/transaction/simulate", {
      method: "POST",
      body: {
        client_id: clientId,
        number_of_transactions: numberOfTransactions,
      },
    });

    setText("simulation-total-amount", formatCurrency(result.customer.Total_Trans_Amt));
    setText("simulation-total-transactions", result.customer.Total_Trans_Ct ?? "-");
    setText("simulation-utilization", `${result.customer.Avg_Utilization_Ratio ?? "-"}`);

    const timelineList = document.getElementById("simulation-timeline-list");
    if (timelineList) {
      timelineList.innerHTML = result.transactions
        .map(
          (txn) => `
            <div class="timeline-item">
              <span class="timeline-step">${txn.transaction}</span>
              <div>
                <p>Transaction ${txn.transaction}</p>
                <small>${formatCurrency(txn.amount)} · Utilization ${txn.utilization}</small>
              </div>
            </div>
          `,
        )
        .join("");
    }

    const progress = document.getElementById("simulation-progress-fill");
    const progressPercent = document.getElementById("simulation-progress-percent");
    if (progress && progressPercent) {
      const filled = Math.min(Math.max(numberOfTransactions / 50, 0), 1) * 100;
      progress.style.width = `${filled}%`;
      progressPercent.textContent = `${Math.round(filled)}%`;
    }
  } catch (error) {
    showError(error.message);
  }
}

function initTransactions() {
  const searchButton = document.getElementById("transaction-search-button");
  if (searchButton) {
    searchButton.addEventListener("click", findTransactionCustomer);
  }

  const transactionForm = document.querySelector(".transaction-form");
  if (transactionForm) {
    transactionForm.addEventListener("submit", addTransaction);
  }
}

function initSimulation() {
  const simulationButton = document.getElementById("simulation-run-button");
  if (simulationButton) {
    simulationButton.addEventListener("click", runSimulationPage);
  }

  const rangeInput = document.getElementById("simulation-number-input");
  const rangeValue = document.getElementById("simulation-range-value");
  if (rangeInput && rangeValue) {
    rangeInput.addEventListener("input", () => {
      rangeValue.textContent = `${rangeInput.value} transactions`;
    });
  }
}

function initSync() {
  const syncButton = document.getElementById("sync-now-button");
  if (syncButton) {
    syncButton.addEventListener("click", syncNow);
  }
}

function initMonitoring() {
  const refreshButton = document.getElementById("monitor-refresh-button");
  if (refreshButton) {
    refreshButton.addEventListener("click", loadHealthData);
    loadHealthData();
  }
}

function initApp() {
  initDashboard();
  initCustomer();
  initPrediction();
  initTransactions();
  initSimulation();
  initSync();
  initMonitoring();
}

document.addEventListener("DOMContentLoaded", initApp);

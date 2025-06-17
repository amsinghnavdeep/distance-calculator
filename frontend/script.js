async function calculate() {
  const source = document.getElementById("source").value;
  const destination = document.getElementById("destination").value;
  const resultEl = document.getElementById("result");
  const errorEl = document.getElementById("error");

  resultEl.textContent = "";
  errorEl.textContent = "";

  try {
    const res = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, destination }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "API error");
    }

    const data = await res.json();
    resultEl.innerHTML = `
      <strong>From:</strong> ${data.source}<br>
      <strong>To:</strong> ${data.destination}<br>
      <strong>Distance:</strong> ${data.distance_km} km (${data.distance_miles} miles)
    `;
    loadHistory();
  } catch (err) {
    errorEl.textContent = err.message;
  }
}

async function loadHistory() {
  const res = await fetch("/history");
  const data = await res.json();
  const list = document.getElementById("history-list");
  list.innerHTML = "";
  data.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.source} → ${item.destination}: ${item.distance_km} km`;
    list.appendChild(li);
  });
}

loadHistory();

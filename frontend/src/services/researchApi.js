// ```javascript
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function apiRequest(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data?.detail || "API request failed.");
  }

  return data;
}

export async function researchTopic(topic) {
  const response = await fetch(`${API_BASE_URL}/research`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ topic: topic.trim() }),
  });

  const data = await response.json();

  if (!response.ok || data.success === false) {
    throw new Error(
      data?.detail?.[0]?.msg ||
      data?.error ||
      "Research request failed."
    );
  }

  return data;
}

export async function getSavedReports() {
  return apiRequest("/reports");
}

export async function getSavedReport(filename) {
  return apiRequest(`/reports/${encodeURIComponent(filename)}`);
}

export async function getSimilarTopics(topic) {
  return apiRequest(`/similar-topics?topic=${encodeURIComponent(topic)}`);
}

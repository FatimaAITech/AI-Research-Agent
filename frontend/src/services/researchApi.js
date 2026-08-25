const API_BASE_URL = "http://127.0.0.1:8000";

export async function researchTopic(topic) {
  const response = await fetch(`${API_BASE_URL}/research`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      topic: topic.trim(),
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data?.detail?.[0]?.msg ||
      data?.error ||
      "Research request failed."
    );
  }

  return data;
}
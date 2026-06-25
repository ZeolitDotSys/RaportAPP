const API_BASE_URL = "";

const form = document.querySelector("#reportForm");
const clearBtn = document.querySelector("#clearBtn");
const result = document.querySelector("#result");
const resultTitle = document.querySelector("#resultTitle");
const reportImage = document.querySelector("#reportImage");
const downloadLink = document.querySelector("#downloadLink");

function formToPayload(formElement) {
  const data = new FormData(formElement);

  return {
    weather: data.get("weather")?.trim() || "-",
    operator: data.get("operator")?.trim() || "",
    inspection: data.get("inspection")?.trim() || "",
    company: data.get("company")?.trim() || "",
    city: data.get("city")?.trim() || "",
    street: data.get("street")?.trim() || "",
    start_manhole: data.get("start_manhole")?.trim() || "",
    end_manhole: data.get("end_manhole")?.trim() || "",
    distance: Number(data.get("distance")),
    level_difference: Number(data.get("level_difference")),
    filming_date: data.get("filming_date")?.trim() || "",
    diameter: data.get("diameter")?.trim() || "",
  };
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const submitButton = form.querySelector("button[type='submit']");
  const originalText = submitButton.textContent;
  submitButton.textContent = "Se generează...";
  submitButton.disabled = true;

  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-report`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formToPayload(form)),
    });

    if (!response.ok) {
      throw new Error("Raportul nu a putut fi generat.");
    }

    const payload = await response.json();
    const imageUrl = `${API_BASE_URL}${payload.image_url}`;

    resultTitle.textContent = `Tronson ${payload.start_manhole || "START"} → ${payload.end_manhole || "STOP"}`;
    reportImage.src = imageUrl;
    downloadLink.href = imageUrl;
    downloadLink.download = payload.filename;
    result.classList.remove("hidden");
    result.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    alert(error.message);
  } finally {
    submitButton.textContent = originalText;
    submitButton.disabled = false;
  }
});

clearBtn.addEventListener("click", () => {
  form.reset();
  result.classList.add("hidden");
});

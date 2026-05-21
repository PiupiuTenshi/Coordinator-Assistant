const API_BASE = localStorage.getItem("apiBase") || "http://127.0.0.1:8000/api";

const state = {
  location: null,
  lastResult: null,
  lastRequest: null,
};

const form = document.querySelector("#symptomForm");
const discomfort = document.querySelector("#discomfort");
const painValue = document.querySelector("#painValue");
const locationButton = document.querySelector("#locationButton");
const locationStatus = document.querySelector("#locationStatus");
const submitButton = document.querySelector("#submitButton");
const resultBand = document.querySelector("#resultBand");
const triageBanner = document.querySelector("#triageBanner");
const triageTitle = document.querySelector("#triageTitle");
const triageMessage = document.querySelector("#triageMessage");
const adviceList = document.querySelector("#adviceList");
const symptomPills = document.querySelector("#symptomPills");
const specialtyList = document.querySelector("#specialtyList");
const doctorList = document.querySelector("#doctorList");
const doctorSection = document.querySelector("#doctorSection");
const hospitalList = document.querySelector("#hospitalList");
const hospitalMap = document.querySelector("#hospitalMap");
const mapCaption = document.querySelector("#mapCaption");
const disclaimer = document.querySelector("#disclaimer");
const feedbackStatus = document.querySelector("#feedbackStatus");

const TRIAGE_TEXT = {
  SELF_CARE: "Theo dõi tại nhà",
  BOOK_APPOINTMENT: "Nên đặt lịch khám",
  URGENT_CARE: "Nên đi khám sớm",
  EMERGENCY: "Cần cấp cứu ngay",
};

const TRIAGE_CLASS = {
  SELF_CARE: "self-care",
  BOOK_APPOINTMENT: "book-appointment",
  URGENT_CARE: "urgent-care",
  EMERGENCY: "emergency",
};

discomfort.addEventListener("input", () => {
  painValue.value = discomfort.value;
});

locationButton.addEventListener("click", () => {
  if (!navigator.geolocation) {
    locationStatus.textContent = "Trình duyệt không hỗ trợ định vị";
    return;
  }
  locationStatus.textContent = "Đang lấy vị trí...";
  navigator.geolocation.getCurrentPosition(
    (position) => {
      state.location = {
        lat: Number(position.coords.latitude.toFixed(6)),
        lng: Number(position.coords.longitude.toFixed(6)),
      };
      locationStatus.textContent = `Đã có vị trí: ${state.location.lat}, ${state.location.lng}`;
    },
    () => {
      locationStatus.textContent = "Không lấy được vị trí";
    },
    { enableHighAccuracy: true, timeout: 8000 }
  );
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = buildPayload();
  state.lastRequest = payload;
  submitButton.disabled = true;
  submitButton.textContent = "Đang kiểm tra...";

  try {
    const response = await fetch(`${API_BASE}/symptom/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error(`API lỗi ${response.status}`);
    }
    const result = await response.json();
    state.lastResult = result;
    renderResult(result);
  } catch (error) {
    renderError(error);
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = '<span aria-hidden="true">✓</span> Kiểm tra nhanh';
  }
});

document.querySelectorAll("[data-feedback]").forEach((button) => {
  button.addEventListener("click", async () => {
    if (!state.lastResult) {
      return;
    }
    const rating = button.getAttribute("data-feedback");
    feedbackStatus.textContent = "Đang gửi...";
    try {
      await fetch(`${API_BASE}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: getSessionId(),
          rating,
          triage_label: state.lastResult.triage_label,
        }),
      });
      feedbackStatus.textContent = "Đã nhận phản hồi";
    } catch {
      feedbackStatus.textContent = "Chưa gửi được phản hồi";
    }
  });
});

function buildPayload() {
  const data = new FormData(form);
  return {
    age: Number(data.get("age")),
    gender: String(data.get("gender") || "unknown"),
    patient_type: String(data.get("patient_type") || "first_visit"),
    symptom_text: String(data.get("symptom_text") || "").trim(),
    duration: String(data.get("duration") || "").trim(),
    discomfort_level: Number(data.get("discomfort_level") || 5),
    risk_groups: data.getAll("risk_groups").map(String),
    dangerous_symptoms: data.getAll("dangerous_symptoms").map(String),
    location: state.location,
    consent: Boolean(data.get("consent")),
  };
}

function renderResult(result) {
  resultBand.classList.remove("hidden");
  triageBanner.className = `triage-banner ${TRIAGE_CLASS[result.triage_label] || ""}`;
  triageTitle.textContent = TRIAGE_TEXT[result.triage_label] || result.triage_label;
  triageMessage.textContent = result.message;
  disclaimer.textContent = result.disclaimer;

  adviceList.replaceChildren(...result.temporary_advice.map((item) => el("li", item)));
  renderPills(symptomPills, result.recognized_symptoms);
  renderSpecialties(result.specialty_recommendations || []);
  renderDoctors(result.doctor_recommendations || []);
  renderHospitals(result.nearest_hospitals || []);
  feedbackStatus.textContent = "";
  resultBand.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderError(error) {
  resultBand.classList.remove("hidden");
  triageBanner.className = "triage-banner emergency";
  triageTitle.textContent = "Chưa kết nối được API";
  triageMessage.textContent = `${error.message}. Kiểm tra backend ở ${API_BASE}.`;
  adviceList.replaceChildren(el("li", "Chạy: uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"));
  symptomPills.replaceChildren();
  specialtyList.replaceChildren();
  doctorList.replaceChildren();
  hospitalList.replaceChildren();
  hospitalMap.replaceChildren();
  mapCaption.textContent = "";
  disclaimer.textContent = "";
}

function renderPills(container, items) {
  container.replaceChildren();
  if (!items.length) {
    container.append(el("p", "Chưa nhận diện được triệu chứng từ từ điển hiện tại."));
    return;
  }
  items.forEach((item) => {
    const pill = el("span", item);
    pill.className = "pill";
    container.append(pill);
  });
}

function renderSpecialties(items) {
  specialtyList.replaceChildren();
  items.forEach((item) => {
    const article = itemBlock();
    article.append(el("strong", item.department));
    article.append(el("p", `${item.reason} · Độ tin cậy ${Math.round(item.confidence * 100)}%`));
    specialtyList.append(article);
  });
}

function renderDoctors(items) {
  doctorList.replaceChildren();
  doctorSection.style.display = items.length ? "" : "none";
  items.forEach((doctor) => {
    const article = itemBlock();
    article.append(el("strong", doctor.name));
    article.append(el("p", `${doctor.degree} · ${doctor.specialty} · ${doctor.hospital_name}`));
    const actions = div("item-actions");
    if (doctor.next_available_slot) {
      const button = el("button", `Đặt ${formatSlot(doctor.next_available_slot)}`);
      button.type = "button";
      button.addEventListener("click", () => bookAppointment(doctor));
      actions.append(button);
    }
    article.append(actions);
    doctorList.append(article);
  });
}

function renderHospitals(items) {
  hospitalList.replaceChildren();
  if (!items.length) {
    hospitalList.append(el("p", "Chưa có bệnh viện phù hợp."));
    hospitalMap.replaceChildren();
    mapCaption.textContent = "Chưa có dữ liệu sơ đồ nội viện.";
    return;
  }

  items.forEach((hospital, index) => {
    const article = itemBlock();
    const distance = hospital.distance_km == null ? "" : ` · ${hospital.distance_km} km`;
    article.append(el("strong", `${hospital.name}${distance}`));
    article.append(el("p", hospital.address));
    const meta = div("hospital-meta");
    meta.append(
      el("span", hospital.has_emergency ? "Có cấp cứu 24/7" : "Không có cấp cứu"),
      el("span", `Giờ làm việc: ${hospital.opening_hours || "Đang cập nhật"}`)
    );
    article.append(meta);
    const actions = div("item-actions");
    const showMap = el("button", "Chỉ đường tới khoa");
    showMap.type = "button";
    showMap.addEventListener("click", () => showIndoorMap(hospital, showMap));
    const call = el("a", "Gọi bệnh viện");
    call.href = `tel:${hospital.phone.replace(/\s/g, "")}`;
    actions.append(showMap, call);
    article.append(actions);
    hospitalList.append(article);
    if (index === 0) {
      showIndoorMap(hospital, showMap);
    }
  });
}

function showIndoorMap(hospital, activeButton) {
  hospitalMap.replaceChildren(buildIndoorSvg(hospital));
  const route = hospital.department_route;
  if (route) {
    mapCaption.textContent = `${hospital.name} · ${route.department} · ${route.building}, ${route.floor}, phòng ${route.room} · khoảng ${route.estimated_walk_minutes} phút đi bộ`;
  } else {
    mapCaption.textContent = `${hospital.name} · Chưa có sơ đồ khoa phù hợp`;
  }
  document.querySelectorAll(".map-button-active").forEach((button) => {
    button.classList.remove("map-button-active");
  });
  if (activeButton) {
    activeButton.classList.add("map-button-active");
  }
}

function buildIndoorSvg(hospital) {
  const route = hospital.department_route || {
    department: "Khoa tiếp nhận",
    room: "",
    map_points: [
      [10, 82],
      [42, 70],
      [72, 42],
    ],
    steps: ["Vào sảnh chính", "Đến quầy hướng dẫn"],
  };
  const points = route.map_points;
  const polyline = points.map(([x, y]) => `${x},${y}`).join(" ");
  const start = points[0];
  const end = points[points.length - 1];
  const wrapper = document.createElement("div");
  const steps = route.steps.map((step, index) => `<li>${index + 1}. ${escapeHtml(step)}</li>`).join("");
  wrapper.innerHTML = `
    <svg viewBox="0 0 100 100" aria-hidden="true">
      <rect x="4" y="8" width="92" height="84" rx="4" fill="#ffffff" stroke="#d8e0e7" />
      <rect x="14" y="18" width="28" height="24" rx="3" fill="#e6f5f3" stroke="#bddbd7" />
      <text x="28" y="32" text-anchor="middle" font-size="4.5" fill="#0b5f59">Tòa A</text>
      <rect x="58" y="18" width="28" height="24" rx="3" fill="#eef2ff" stroke="#c7d2fe" />
      <text x="72" y="32" text-anchor="middle" font-size="4.5" fill="#1d4ed8">Tòa B/C</text>
      <rect x="18" y="58" width="64" height="24" rx="3" fill="#f5f8fa" stroke="#d8e0e7" />
      <text x="50" y="72" text-anchor="middle" font-size="4.5" fill="#5d6876">Sảnh chính</text>
      <polyline points="${polyline}" fill="none" stroke="#c2412f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
      <circle cx="${start[0]}" cy="${start[1]}" r="3.2" fill="#15803d" />
      <text x="${start[0] + 4}" y="${start[1] + 1}" font-size="4" fill="#15803d">Cổng</text>
      <circle cx="${end[0]}" cy="${end[1]}" r="3.6" fill="#c2412f" />
      <text x="${Math.max(8, end[0] - 18)}" y="${Math.max(10, end[1] - 5)}" font-size="4" fill="#c2412f">${escapeHtml(route.department)}</text>
    </svg>
    <ol class="indoor-steps">${steps}</ol>
  `;
  return wrapper;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function bookAppointment(doctor) {
  const request = state.lastRequest;
  if (!request || !doctor.next_available_slot) {
    return;
  }
  const payload = {
    patient_type: request.patient_type,
    doctor_id: doctor.id,
    specialty: doctor.specialty,
    hospital_id: doctor.hospital_id,
    appointment_time: doctor.next_available_slot,
    symptom_summary: request.symptom_text,
    consent: request.consent,
  };
  const response = await fetch(`${API_BASE}/appointments/book`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const result = await response.json();
  window.alert(`Mã lịch hẹn: ${result.appointment_code}\nTrạng thái: ${result.status}`);
}

function itemBlock() {
  return document.querySelector("#itemTemplate").content.firstElementChild.cloneNode(true);
}

function el(tag, text) {
  const node = document.createElement(tag);
  node.textContent = text;
  return node;
}

function div(className) {
  const node = document.createElement("div");
  node.className = className;
  return node;
}

function formatSlot(value) {
  try {
    return new Intl.DateTimeFormat("vi-VN", {
      dateStyle: "short",
      timeStyle: "short",
    }).format(new Date(value));
  } catch {
    return value;
  }
}

function getSessionId() {
  const existing = localStorage.getItem("sessionId");
  if (existing) {
    return existing;
  }
  const value = crypto.randomUUID ? crypto.randomUUID() : String(Date.now());
  localStorage.setItem("sessionId", value);
  return value;
}

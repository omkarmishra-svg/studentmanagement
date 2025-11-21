const API_BASE = "/api/students";

async function fetchJSON(url, opts = {}) {
  const res = await fetch(url, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw err;
  }
  return res.json();
}

// Helper function to format marks
function formatMarks(m1, m2, m3, m4, m5) {
  return `${m1 || 0}, ${m2 || 0}, ${m3 || 0}, ${m4 || 0}, ${m5 || 0}`;
}

// Helper function to get grade badge HTML
function getGradeBadge(grade) {
  return `<span class="grade-badge grade-${grade}">${grade}</span>`;
}

// Helper function to show result message
function showResult(element, message, isError = false) {
  element.innerHTML = message;
  element.className = isError ? "error" : "success";
  element.style.display = "block";
  
  // Auto-hide after 5 seconds for success messages
  if (!isError) {
    setTimeout(() => {
      element.style.display = "none";
      element.innerHTML = "";
      element.className = "";
    }, 5000);
  }
}

/* ---------- index.html behavior ---------- */
async function loadAll() {
  const tbody = document.querySelector("#studentsTable tbody");
  if (!tbody) return;
  
  tbody.innerHTML = `<tr><td colspan="8" class="loading">Loading students...</td></tr>`;
  
  try {
    const students = await fetchJSON(API_BASE);
    
    if (students.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" class="empty-state">No students found. <a href="add.html" style="color: var(--accent-primary);">Add your first student</a>!</td></tr>`;
      return;
    }
    
    tbody.innerHTML = "";
    students.forEach((s) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${s.roll}</strong></td>
        <td>${s.name || "-"}</td>
        <td>${s.age || "-"}</td>
        <td>${s.branch || "-"}</td>
        <td style="font-size: 0.9rem;">${formatMarks(s.mark1, s.mark2, s.mark3, s.mark4, s.mark5)}</td>
        <td class="percentage">${Number(s.percentage || 0).toFixed(2)}%</td>
        <td>${getGradeBadge(s.grade || "F")}</td>
        <td>
          <a href="edit.html?roll=${s.roll}">✏️ Edit</a>
          <a href="#" onclick="deleteStudent(${s.roll});return false;">🗑️ Delete</a>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="8" class="error">❌ Error: ${e.error || e.message}</td></tr>`;
  }
}

async function deleteStudent(roll) {
  if (!confirm(`Are you sure you want to delete student with Roll No. ${roll}?`)) return;
  
  try {
    await fetchJSON(`${API_BASE}/${roll}`, { method: "DELETE" });
    showResult(document.getElementById("countArea"), `✅ Student ${roll} deleted successfully!`, false);
    setTimeout(() => {
      document.getElementById("countArea").innerHTML = "";
    }, 3000);
    loadAll();
  } catch (e) {
    alert(`❌ Error: ${e.error || e.message}`);
  }
}

async function sortedLoad() {
  const tbody = document.querySelector("#studentsTable tbody");
  if (!tbody) return;
  
  tbody.innerHTML = `<tr><td colspan="8" class="loading">Sorting students...</td></tr>`;
  
  try {
    const students = await fetchJSON(`${API_BASE}/sorted`);
    
    if (students.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" class="empty-state">No students found.</td></tr>`;
      return;
    }
    
    tbody.innerHTML = "";
    students.forEach((s, i) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${s.roll}</strong> <span style="color: var(--accent-primary); font-size: 0.8rem;">#${i + 1}</span></td>
        <td>${s.name || "-"}</td>
        <td>${s.age || "-"}</td>
        <td>${s.branch || "-"}</td>
        <td style="font-size: 0.9rem;">${formatMarks(s.mark1, s.mark2, s.mark3, s.mark4, s.mark5)}</td>
        <td class="percentage">${Number(s.percentage || 0).toFixed(2)}%</td>
        <td>${getGradeBadge(s.grade || "F")}</td>
        <td>
          <a href="edit.html?roll=${s.roll}">✏️ Edit</a>
          <a href="#" onclick="deleteStudent(${s.roll});return false;">🗑️ Delete</a>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="8" class="error">❌ Error: ${e.error || e.message}</td></tr>`;
  }
}

async function showCount() {
  const countArea = document.getElementById("countArea");
  if (!countArea) return;
  
  countArea.innerHTML = `<span class="loading">Counting...</span>`;
  
  try {
    const res = await fetchJSON(`${API_BASE}/count`);
    countArea.innerHTML = `📊 <strong>Total Students:</strong> ${res.count}`;
    countArea.style.display = "block";
  } catch (e) {
    countArea.innerHTML = `❌ Error: ${e.error || e.message}`;
    countArea.className = "error";
  }
}

async function addDummyData() {
  if (!confirm("This will add 10 sample students to the database. Continue?")) return;
  
  const countArea = document.getElementById("countArea");
  const dummyBtn = document.getElementById("dummyBtn");
  
  if (!dummyBtn) return;
  
  dummyBtn.disabled = true;
  dummyBtn.textContent = "⏳ Adding...";
  
  if (countArea) {
    countArea.innerHTML = `<span class="loading">Adding dummy data...</span>`;
    countArea.style.display = "block";
  }
  
  try {
    const res = await fetchJSON(`${API_BASE}/dummy`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    
    if (countArea) {
      countArea.innerHTML = `✅ ${res.message || "Dummy data added successfully!"}`;
      countArea.className = "success";
    }
    
    // Reload the table
    setTimeout(() => {
      loadAll();
      if (countArea) {
        countArea.innerHTML = "";
      }
    }, 2000);
  } catch (e) {
    if (countArea) {
      countArea.innerHTML = `❌ Error: ${e.error || e.message}`;
      countArea.className = "error";
    }
    alert(`Error: ${e.error || e.message}`);
  } finally {
    dummyBtn.disabled = false;
    dummyBtn.textContent = "🎲 Add Dummy Data";
  }
}

/* ---------- add.html behavior ---------- */
async function handleAddForm(e) {
  e.preventDefault();
  const form = e.target;
  const resultDiv = document.getElementById("result");
  const submitBtn = form.querySelector('button[type="submit"]');
  
  // Disable button during submission
  submitBtn.disabled = true;
  submitBtn.textContent = "⏳ Adding...";
  resultDiv.innerHTML = "";
  
  const data = Object.fromEntries(new FormData(form).entries());
  
  // Convert numeric fields
  for (const k of ["roll", "age", "mark1", "mark2", "mark3", "mark4", "mark5"]) {
    if (data[k] === undefined || data[k] === "") {
      if (k === "roll") {
        showResult(resultDiv, "❌ Roll number is required!", true);
        submitBtn.disabled = false;
        submitBtn.textContent = "✨ Add Student";
        return;
      }
      delete data[k];
    } else {
      data[k] = Number(data[k]);
    }
  }
  
  try {
    await fetchJSON(API_BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    
    showResult(resultDiv, "✅ Student added successfully! Redirecting...", false);
    form.reset();
    
    // Redirect after 1.5 seconds
    setTimeout(() => {
      window.location.href = "index.html";
    }, 1500);
  } catch (err) {
    showResult(resultDiv, `❌ Error: ${err.error || err.message}`, true);
    submitBtn.disabled = false;
    submitBtn.textContent = "✨ Add Student";
  }
}

/* ---------- edit.html behavior ---------- */
function getQueryParams() {
  return Object.fromEntries(new URLSearchParams(location.search));
}

async function loadEditForm() {
  const params = getQueryParams();
  const resultDiv = document.getElementById("result");
  
  if (!params.roll) {
    showResult(resultDiv, "❌ No roll number specified in URL.", true);
    return;
  }
  
  resultDiv.innerHTML = `<span class="loading">Loading student data...</span>`;
  
  try {
    const s = await fetchJSON(`${API_BASE}/${params.roll}`);
    const form = document.getElementById("editForm");
    
    form.roll.value = s.roll;
    form.name.value = s.name || "";
    form.age.value = s.age || "";
    form.branch.value = s.branch || "";
    form.mark1.value = s.mark1 || "";
    form.mark2.value = s.mark2 || "";
    form.mark3.value = s.mark3 || "";
    form.mark4.value = s.mark4 || "";
    form.mark5.value = s.mark5 || "";
    
    resultDiv.innerHTML = "";
  } catch (e) {
    showResult(resultDiv, `❌ Error: ${e.error || e.message}`, true);
  }
}

async function handleEditForm(e) {
  e.preventDefault();
  const form = e.target;
  const resultDiv = document.getElementById("result");
  const submitBtn = form.querySelector('button[type="submit"]');
  const roll = form.roll.value;
  
  // Disable button during submission
  submitBtn.disabled = true;
  submitBtn.textContent = "⏳ Saving...";
  resultDiv.innerHTML = "";
  
  const payload = {
    name: form.name.value || "",
    age: form.age.value ? Number(form.age.value) : 0,
    branch: form.branch.value || "",
    mark1: form.mark1.value ? Number(form.mark1.value) : 0,
    mark2: form.mark2.value ? Number(form.mark2.value) : 0,
    mark3: form.mark3.value ? Number(form.mark3.value) : 0,
    mark4: form.mark4.value ? Number(form.mark4.value) : 0,
    mark5: form.mark5.value ? Number(form.mark5.value) : 0,
  };

  try {
    await fetchJSON(`${API_BASE}/${roll}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    
    showResult(resultDiv, "✅ Student updated successfully! Redirecting...", false);
    
    // Redirect after 1.5 seconds
    setTimeout(() => {
      window.location.href = "index.html";
    }, 1500);
  } catch (e) {
    showResult(resultDiv, `❌ Error: ${e.error || e.message}`, true);
    submitBtn.disabled = false;
    submitBtn.textContent = "💾 Save Changes";
  }
}

/* ---------- wire up events on page load ---------- */
document.addEventListener("DOMContentLoaded", () => {
  // Index page
  if (document.querySelector("#studentsTable")) {
    const refreshBtn = document.getElementById("refreshBtn");
    const sortBtn = document.getElementById("sortBtn");
    const countBtn = document.getElementById("countBtn");
    const dummyBtn = document.getElementById("dummyBtn");
    
    if (refreshBtn) {
      refreshBtn.addEventListener("click", loadAll);
    }
    if (sortBtn) {
      sortBtn.addEventListener("click", sortedLoad);
    }
    if (countBtn) {
      countBtn.addEventListener("click", showCount);
    }
    if (dummyBtn) {
      dummyBtn.addEventListener("click", addDummyData);
    }
    
    loadAll();
  }

  // Add form
  const addForm = document.getElementById("addForm");
  if (addForm) {
    addForm.addEventListener("submit", handleAddForm);
  }

  // Edit form
  const editForm = document.getElementById("editForm");
  if (editForm) {
    loadEditForm();
    editForm.addEventListener("submit", handleEditForm);
  }
});

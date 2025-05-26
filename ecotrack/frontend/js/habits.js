const API_URL = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");

if (!token) {
  alert("No estás autenticado. Serás redirigido al login.");
  window.location.href = "index.html";
}

const habitForm = document.getElementById("habit-form");
const habitIdInput = document.getElementById("habit-id");
const habitNameInput = document.getElementById("habit-name");
const habitFrequencySelect = document.getElementById("habit-frequency");
const habitSubmitBtn = document.getElementById("habit-submit-btn");
const habitList = document.getElementById("habit-list");
const logoutBtn = document.getElementById("logout-btn");

logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "index.html";
});

async function fetchHabits() {
  try {
    const res = await fetch(API_URL + "/habits", {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) throw new Error("Error al cargar hábitos");
    const habits = await res.json();
    renderHabits(habits);
  } catch (err) {
    alert(err.message);
    if (err.message.includes("401")) {
      localStorage.removeItem("token");
      window.location.href = "index.html";
    }
  }
}

function renderHabits(habits) {
  habitList.innerHTML = "";
  if (habits.length === 0) {
    habitList.innerHTML = "<li>No tienes hábitos registrados.</li>";
    return;
  }
  habits.forEach(habit => {
    const li = document.createElement("li");

    // Span para nombre del hábito
    const nameSpan = document.createElement("span");
    nameSpan.textContent = habit.name;

    // Span para frecuencia, con clase de color
    const freqSpan = document.createElement("span");
    freqSpan.textContent = habit.frequency;
    freqSpan.className = `habit-frequency frequency-${habit.frequency}`;

    li.appendChild(nameSpan);
    li.appendChild(freqSpan);

    // Botón editar
    const editBtn = document.createElement("button");
    editBtn.textContent = "Editar";
    editBtn.className = "edit";
    editBtn.onclick = () => fillFormForEdit(habit);
    li.appendChild(editBtn);

    // Botón eliminar
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Eliminar";
    deleteBtn.className = "delete";
    deleteBtn.onclick = () => deleteHabit(habit.id);
    li.appendChild(deleteBtn);

    habitList.appendChild(li);
  });
}

function fillFormForEdit(habit) {
  habitIdInput.value = habit.id;
  habitNameInput.value = habit.name;
  habitFrequencySelect.value = habit.frequency;
  habitSubmitBtn.textContent = "Actualizar hábito";
}

habitForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = habitIdInput.value;
  const name = habitNameInput.value.trim();
  const frequency = habitFrequencySelect.value;

  if (!name || !frequency) {
    alert("Completa todos los campos.");
    return;
  }

  const method = id ? "PUT" : "POST";
  const url = id ? `${API_URL}/habits/${id}` : `${API_URL}/habits`;
  const body = JSON.stringify({ name, frequency });

  try {
    const res = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || "Error al guardar hábito");
    }
    habitForm.reset();
    habitIdInput.value = "";
    habitSubmitBtn.textContent = "Agregar hábito";
    fetchHabits();
  } catch (err) {
    alert(err.message);
  }
});

async function deleteHabit(id) {
  if (!confirm("¿Seguro que quieres eliminar este hábito?")) return;
  try {
    const res = await fetch(`${API_URL}/habits/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || "Error al eliminar hábito");
    }
    fetchHabits();
  } catch (err) {
    alert(err.message);
  }
}

// Al cargar la página, traemos los hábitos
fetchHabits();

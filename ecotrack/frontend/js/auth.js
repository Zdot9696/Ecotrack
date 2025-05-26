const API_URL = "http://127.0.0.1:8000"; 

const formTitle = document.getElementById("form-title");
const authForm = document.getElementById("auth-form");
const toggleLink = document.getElementById("toggle-link");
const submitBtn = document.getElementById("submit-btn");
const errorMsg = document.getElementById("error-msg");

let isLogin = true; // Estado: true para login, false para registro

toggleLink.addEventListener("click", () => {
  isLogin = !isLogin;
  if (isLogin) {
    formTitle.textContent = "Iniciar Sesión";
    submitBtn.textContent = "Entrar";
    toggleLink.textContent = "¿No tienes cuenta? Regístrate";
  } else {
    formTitle.textContent = "Registro";
    submitBtn.textContent = "Registrarse";
    toggleLink.textContent = "¿Ya tienes cuenta? Inicia sesión";
  }
  errorMsg.textContent = "";
  authForm.reset();
});

authForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorMsg.textContent = "";

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    errorMsg.textContent = "Por favor ingresa email y contraseña";
    return;
  }

  const endpoint = isLogin ? "/login" : "/register";
  const method = "POST";

  try {
    const res = await fetch(API_URL + endpoint, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      errorMsg.textContent = data.detail || "Error en la solicitud";
      return;
    }

    if (isLogin) {
      // Guardar token y redirigir a dashboard
      localStorage.setItem("token", data.access_token);
      window.location.href = "dashboard.html";
    } else {
      alert("Registro exitoso! Ahora inicia sesión.");
      isLogin = true;
      formTitle.textContent = "Iniciar Sesión";
      submitBtn.textContent = "Entrar";
      toggleLink.textContent = "¿No tienes cuenta? Regístrate";
      authForm.reset();
    }
  } catch (err) {
    errorMsg.textContent = "Error de red. Intenta de nuevo.";
    console.error(err);
  }
});

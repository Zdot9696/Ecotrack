async function cargarConsejos() {
  const lista = document.getElementById("consejos-lista");
  lista.innerHTML = "<p>Cargando consejos...</p>";

  try {
    const res = await fetch("http://127.0.0.1:8000/consejos");
    const data = await res.json();

    lista.innerHTML = "";

    const consejosArray = data.consejos?.consejos || [];

    consejosArray.forEach((c, index) => {
      const card = document.createElement("div");
      card.className = "consejo-card";

      const content = document.createElement("div");
      content.innerHTML = `<span>${index + 1}.</span> ${c.tip}`;

      card.appendChild(content);
      lista.appendChild(card);
    });

  } catch (error) {
    lista.innerHTML = "<p>Error al cargar los consejos.</p>";
    console.error(error);
  }
}

window.onload = () => {
  cargarConsejos();
};

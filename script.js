// Bo'limlarni almashtirish
const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".panel");

function show(id) {
  tabs.forEach(t => t.classList.toggle("active", t.dataset.tab === id));
  panels.forEach(p => p.classList.toggle("active", p.id === id));
}
tabs.forEach(t => t.addEventListener("click", () => show(t.dataset.tab)));

// Xabarni Telegram botga yuborish
const form = document.getElementById("form");
const status = document.getElementById("status");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = form.querySelector("button");
  btn.disabled = true;
  status.textContent = "Yuborilmoqda...";
  try {
    const res = await fetch("/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });
    const data = await res.json();
    if (data.ok) {
      status.textContent = "Xabaringiz yuborildi. Rahmat!";
      form.reset();
    } else {
      status.textContent = data.error || "Xatolik yuz berdi.";
    }
  } catch {
    status.textContent = "Server bilan aloqa yo'q. Dastur ishlayotganini tekshiring.";
  }
  btn.disabled = false;
});

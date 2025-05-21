document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/list_foods")
    .then(response => response.json())
    .then(data => {
      const list = document.getElementById("food-list");

      if (data.length === 0) {
        list.innerHTML = "<p>Hiç yemek bulunamadı.</p>";
        return;
      }

      data.forEach(food => {
        const card = document.createElement("div");
        card.className = "food-card";
        card.innerHTML = `
          <h3>${food.food_name}</h3>
          <p>Stok: ${food.stock}</p>
          <p>Fiyat: ${food.price}₺</p>
          <p>Mesafe: ${food.distance} km</p>
        `;
        list.appendChild(card);
      });
    })
    .catch(error => {
      console.error("Yemekleri çekerken hata:", error);
    });
});

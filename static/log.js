document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const mail = document.getElementById("mail").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/owners/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ mail, password }),
    });
    window.location.href = "/home"; // gibi bir yönlendirme


    const data = await response.json();

    if (response.ok) {
        alert("Giriş başarılı!");
        // yönlendirme eklenebilir
    } else {
        document.getElementById("error-message").textContent = data.detail || "Giriş başarısız!";
    }
});

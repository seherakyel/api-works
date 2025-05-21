document.getElementById('registerForm').addEventListener('submit', async function(event) {
  event.preventDefault();

  const formData = new FormData(this);
  const formObj = {};
  formData.forEach((value, key) => {
    formObj[key] = value;
  });

  try {
    const response = await fetch('/users/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formObj),
    });

    const data = await response.json();

    const messageEl = document.getElementById('registerError');

    if (response.ok) {
      messageEl.style.color = "green";
      messageEl.innerText = data.message;
      setTimeout(() => {
        window.location.href = '/login';
      }, 1500);
    } else {
      messageEl.style.color = "red";
      messageEl.innerText = data.detail || "Kayıt başarısız.";
    }

  } catch (error) {
    document.getElementById('registerError').style.color = "red";
    document.getElementById('registerError').innerText = "Bir hata oluştu. Lütfen tekrar deneyin.";
    console.error('JS Kayıt Hatası:', error);
  }
});

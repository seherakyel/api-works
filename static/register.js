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
    const errorTextEl = document.getElementById('errorText');

    if (response.ok) {
      messageEl.style.display = 'flex';
      messageEl.style.backgroundColor = 'rgba(40, 167, 69, 0.1)';
      messageEl.style.borderLeftColor = '#28a745';
      errorTextEl.style.color = '#28a745';
      errorTextEl.innerText = data.message || "Kayıt başarılı! İşletme giriş sayfasına yönlendiriliyorsunuz...";
      
      setTimeout(() => {
        window.location.href = '/user/login';
      }, 1500);
    } else {
      messageEl.style.display = 'flex';
      errorTextEl.innerText = data.detail || "Kayıt başarısız.";
    }

  } catch (error) {
    const messageEl = document.getElementById('registerError');
    const errorTextEl = document.getElementById('errorText');
    
    messageEl.style.display = 'flex';
    errorTextEl.innerText = "Bir hata oluştu. Lütfen tekrar deneyin.";
    console.error('JS Kayıt Hatası:', error);
  }
});

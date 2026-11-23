// ===== Popup ต้อนรับ: เด้งครั้งแรก แล้วจำว่าเลือกภาษาแล้ว =====
(function () {
    const popup = document.getElementById('welcomePopup');
    if (!popup) return;

    let saved = null;
    try { saved = localStorage.getItem('siteLang'); } catch (e) {}
    if (saved) { popup.classList.add('popup-hidden'); return; }

    popup.querySelectorAll('.popup-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            try { localStorage.setItem('siteLang', btn.dataset.lang); } catch (e) {}
            popup.classList.add('popup-hidden');
        });
    });
})();

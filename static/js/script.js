// ===== Dark Mode =====
function toggleDarkMode() {
    const isDark = document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDark ? 'on' : 'off');
    const iconSpan = document.getElementById('darkModeIcon');
    if (iconSpan) {
        iconSpan.innerHTML = isDark
            ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91l-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-7c-4.14 0-7.5 3.36-7.5 7.5s3.36 7.5 7.5 7.5 7.5-3.36 7.5-7.5-3.36-7.5-7.5-7.5zm.5 13.05h-1V15h1v1.55zm5.2 0l-1.79-1.79 1.41-1.41 1.79 1.79-1.41 1.41zM11 19v3h2v-3h-2z"/></svg>' // Sun
            : '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/></svg>'; // Moon
    }
}

// ===== On page load: restore dark mode preference =====
document.addEventListener('DOMContentLoaded', () => {
    const pref = localStorage.getItem('darkMode');
    const isDark = pref === 'on';
    if (isDark) {
        document.body.classList.add('dark-mode');
    }
    const iconSpan = document.getElementById('darkModeIcon');
    if (iconSpan) {
        iconSpan.innerHTML = isDark
            ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91l-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-7c-4.14 0-7.5 3.36-7.5 7.5s3.36 7.5 7.5 7.5 7.5-3.36 7.5-7.5-3.36-7.5-7.5-7.5zm.5 13.05h-1V15h1v1.55zm5.2 0l-1.79-1.79 1.41-1.41 1.79 1.79-1.41 1.41zM11 19v3h2v-3h-2z"/></svg>' // Sun
            : '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/></svg>'; // Moon
    }

    // ===== Animate progress circles =====
    document.querySelectorAll('.progress-circle').forEach(el => {
        const pct = parseInt(el.dataset.progress || 0, 10);
        const circle = el.querySelector('circle.progress');
        if (circle) {
            const circumference = 345;
            circle.style.strokeDashoffset = circumference - (circumference * pct / 100);
        }
        const text = el.querySelector('.progress-text h2');
        if (text) text.textContent = pct + '%';
    });
});

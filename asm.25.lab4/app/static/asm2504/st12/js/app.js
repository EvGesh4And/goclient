document.addEventListener('click', (e) => {
    const btn = e.target.closest('form button.btn.danger, a.btn.danger')
    if (btn) {
        if (!confirm('Удалить запись?')) {
            e.preventDefault()
        }
    }
})


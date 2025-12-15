document.addEventListener('DOMContentLoaded', function() {
    flatpickr('input[type="date"]', {
        dateFormat: "d.m.Y",
        locale: "ru"
    });

    console.log("Modern UI scripts loaded ✅");
});
// Navbar Scroll Effect
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 20) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Advanced mode toggle
const toggleAdvanced = document.getElementById('toggle-advanced');
const advancedFields = document.getElementById('advanced-fields');
const advancedPreviews = document.querySelectorAll('.advanced-preview');

if (toggleAdvanced && advancedFields) {
    toggleAdvanced.addEventListener('click', () => {
        if (advancedFields.style.display === 'block') {
            advancedFields.style.display = 'none';
            toggleAdvanced.innerText = 'Show';
            advancedPreviews.forEach(el => el.style.display = 'none');
        } else {
            advancedFields.style.display = 'block';
            toggleAdvanced.innerText = 'Hide';
            advancedPreviews.forEach(el => el.style.display = 'flex');
        }
    });
}

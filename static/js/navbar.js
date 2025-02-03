document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const lightIcon = document.getElementById('lightIcon');
    const darkIcon = document.getElementById('darkIcon');

    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
        document.documentElement.classList.add('dark');
        lightIcon.classList.add('hidden');
        darkIcon.classList.remove('hidden');
    } else {
        document.documentElement.classList.remove('dark');
        lightIcon.classList.remove('hidden');
        darkIcon.classList.add('hidden');
    }

    // Toggle theme on button click
    themeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        const isDarkMode = document.documentElement.classList.contains('dark');

        if (isDarkMode) {
            localStorage.setItem('theme', 'dark');
            lightIcon.classList.add('hidden');
            darkIcon.classList.remove('hidden');
        } else {
            localStorage.setItem('theme', 'light');
            lightIcon.classList.remove('hidden');
            darkIcon.classList.add('hidden');
        }
    });
});

// Search bar 
const searchBtn = document.getElementById('search-btn');
const fullScreenSearch = document.getElementById('full-screen-search');
const closeBtn = document.getElementById('close-btn');

// Open fullscreen search
searchBtn.addEventListener('click', () => {
    fullScreenSearch.classList.remove('opacity-0', 'invisible');
    fullScreenSearch.classList.add('opacity-100', 'visible');
});

// Close fullscreen search
closeBtn.addEventListener('click', () => {
    fullScreenSearch.classList.remove('opacity-100', 'visible');
    fullScreenSearch.classList.add('opacity-0', 'invisible');
});


const menuBtn = document.getElementById('menu-btn');
const closeMenu = document.getElementById('close-menu');
const menu = document.getElementById('menu');

// Open menu
menuBtn.addEventListener('click', () => {
    menu.classList.remove('-translate-x-full');
});

// Close menu
closeMenu.addEventListener('click', () => {
    menu.classList.add('-translate-x-full');
});


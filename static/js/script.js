const GENRE_MAP = {
    28: "Боевик", 12: "Приключения", 16: "Мультфильм", 35: "Комедия",
    80: "Криминал", 99: "Документальный", 18: "Драма", 10751: "Семейный",
    14: "Фэнтези", 36: "История", 27: "Ужасы", 10402: "Музыка",
    9648: "Детектив", 10749: "Мелодрама", 878: "Фантастика",
    10770: "ТВ-фильм", 53: "Триллер", 10752: "Военный", 37: "Вестерн"
};

let allFilms = [];
let currentFilm = null;

async function loadFilms(){
    try{
        const response = await fetch('/films');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        const data = await response.json();
        allFilms = data.results || data;

        if(allFilms.length === 0){
            showError('Фильм не найден');
            return;
        }

        renderPosterStrip(allFilms);
        displayFilm(allFilms[0]);
    } catch(error){
        console.error('Ошибка загрузки: ', error);
        showError(`Не удалось загрузить фильмы: ${error.message}`);
    }
}

function displayFilm(film){
    currentFilm = film;
    const posterUrl = film.poster_path ? `https://image.tmdb.org/t/p/w500${film.poster_path}`: 'https://via.placeholder.com/300x450/333/888?text=Нет+постера';
    document.getElementById('filmPoster').src = posterUrl;

    document.getElementById('filmTitle').textContent = film.title || 'Без названия';
    document.getElementById('filmOriginalTitle').textContent = film.original_title || '';
    document.getElementById('filmOverview').textContent = film.overview || 'Описание отсутствует';

    document.getElementById('tmdbLink').href =
        `https://www.themoviedb.org/movie/${film.id}`;

        
    const ratingEl = document.getElementById('filmRating');
    if(ratingEl){
        ratingEl.textContent = film.vote_average ? film.vote_average.toFixed(1): 'N/A';
    }
        
    const yearEl = document.getElementById('filmYear');
    if(yearEl){
        const year = film.release_date ? film.release_date.slice(0, 4): '';
        yearEl.textContent = year ? `Год: ${year}` : '';
    }

    const genresEl = document.getElementById('filmGenres');
    if(genresEl){
        if(film.genre_ids && film.genre_ids.length > 0){
            const genresName = film.genre_ids.slice(0, 3).map(id => GENRE_MAP[id]||'Неизвестно').join(', ');
            genresEl.textContent = genresName;
        } else{
            genresEl.textContent = 'Жанры не указаны';
        }
    }

    document.querySelectorAll('.poster-placeholder').forEach(el => {
        const isActive = el.dataset.filmId == film.id;
        el.classList.toggle('active', isActive);
        
        if (isActive) {
            el.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        }
    });
}

function renderPosterStrip(films) {
    const strip = document.querySelector('.poster-strip');
    if (!strip) return;
    strip.innerHTML = '';

    films.forEach(film => {
        const posterUrl = film.poster_path
            ? `https://image.tmdb.org/t/p/w200${film.poster_path}`
            : 'https://via.placeholder.com/120x180/333/888?text=?';

        const div = document.createElement('div');
        div.className = 'poster-placeholder mr-3 ml-3';
        div.dataset.filmId = film.id;
        div.style.backgroundImage = `url(${posterUrl})`;

        div.addEventListener('click', () => displayFilm(film));
        strip.appendChild(div);
    });
}

// ===== КНОПКА «КРУТИТЬ ЗАНОВО» =====
function reroll() {
    if (allFilms.length === 0) return;
    // Выбираем случайный фильм, не совпадающий с текущим
    let next;
    do {
        next = allFilms[Math.floor(Math.random() * allFilms.length)];
    } while (allFilms.length > 1 && next.id === currentFilm?.id);
    displayFilm(next);
}

// ===== ПОХОЖИЕ ФИЛЬМЫ =====
async function loadSimilar() {
    if (!currentFilm) return;
    try {
        const response = await fetch(`/similar/${currentFilm.id}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        const similar = data.results || data;

        if (similar.length === 0) {
            alert('Похожих фильмов не найдено');
            return;
        }

        // Заменяем текущий список на похожие
        allFilms = similar;
        displayFilm(similar[0]);
        renderPosterStrip(similar);

    } catch (error) {
        console.error('Ошибка загрузки похожих:', error);
        alert(`Не удалось загрузить похожие: ${error.message}`);
    }
}

// ===== ОШИБКА =====
function showError(message) {
    document.getElementById('filmTitle').textContent = 'Ошибка';
    document.getElementById('filmOverview').textContent = message;
}

// ===== СТАРТ =====
document.addEventListener('DOMContentLoaded', () => {
    loadFilms();

    const rerollBtn = document.getElementById('rerollBtn');
    if (rerollBtn) rerollBtn.addEventListener('click', reroll);

    const similarBtn = document.querySelector('.btn-outline-light');
    if (similarBtn && similarBtn.textContent.includes('Похожие')) {
        similarBtn.addEventListener('click', loadSimilar);
    }
});
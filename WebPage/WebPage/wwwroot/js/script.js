// script.js
// Two datasets:
// suggestionData is a small array of strings for autocomplete
// bigData is a large array of objects for full search on Enter

const suggestionData = [
    'Search Result',
    'Another Result',
    'Example Result',
    'More Results',
    'Extra One',
    'Another Extra'
    // … small list of key terms
];

const bigData = [
    { icon: '🌐', title: 'Search Result', desc: 'Lorem ipsum dolor sit amet' },
    { icon: '🔗', title: 'Another Result', desc: 'Consectetur adipiscing elit' },
    { icon: '📁', title: 'Example Result', desc: 'Sed do eiusmod tempor' },
    { icon: '🔍', title: 'More Results', desc: 'Incididunt ut labore et dolore' }
    // … potentially thousands of full objects
];

const input = document.getElementById('searchInput');
const suggBox = document.getElementById('suggestions');
const resultsContainer = document.getElementById('results');
let activeIndex = -1;

// Highlight helper
function highlight(text, term) {
    if (!term) return text;
    const re = new RegExp(`(${term.replace(/[-\\/\\^$*+?.()|[\]{}]/g,'\\$&')})`, 'gi');
    return text.replace(re, '<mark>$1</mark>');
}

// Render small suggestions list
function renderSmallSuggestions(list, query) {
    if (!list.length) return suggBox.classList.add('d-none');
    suggBox.innerHTML = list.map((item, i) =>
        `<div class="suggestion-item${i === activeIndex ? ' active' : ''}" data-index="${i}">` +
        highlight(item, query) +
        `</div>`
    ).join('');
    suggBox.classList.remove('d-none');
}

// Render full results from bigData
function renderBigResults(list, query) {
    if (!list.length) {
        resultsContainer.innerHTML = '<p class="no-results">No results found.</p>';
        return;
    }
    resultsContainer.innerHTML = list.map(item => `
    <div class="result-item">
      <div class="result-icon">${item.icon}</div>
      <div>
        <p class="result-title">${highlight(item.title, query)}</p>
        <p class="result-desc">${highlight(item.desc, query)}</p>
      </div>
    </div>
  `).join('');
}

// Perform search and render (shared logic)
function performSearch(term) {
    const q = term.trim().toLowerCase();
    const results = bigData.filter(d =>
        d.title.toLowerCase().includes(q) ||
        d.desc.toLowerCase().includes(q)
    );
    renderBigResults(results, q);
}

// Handle input for suggestions (small list)
input.addEventListener('input', e => {
    const q = e.target.value.trim().toLowerCase();
    activeIndex = -1;
    if (!q) {
        // show top 4 suggestions when input is empty
        renderSmallSuggestions(suggestionData.slice(0, 4), '');
        return;
    }
    const matches = suggestionData.filter(s => s.toLowerCase().includes(q));
    renderSmallSuggestions(matches.slice(0, 4), q);
});

// Handle key navigation and Enter
input.addEventListener('keydown', e => {
    const items = suggBox.querySelectorAll('.suggestion-item');
    const q = input.value.trim().toLowerCase();

    if (e.key === 'ArrowDown' && items.length) {
        e.preventDefault();
        activeIndex = Math.min(activeIndex + 1, items.length - 1);
        renderSmallSuggestions(Array.from(items).map(i => i.textContent), q);
    } else if (e.key === 'ArrowUp' && items.length) {
        e.preventDefault();
        activeIndex = Math.max(activeIndex - 1, 0);
        renderSmallSuggestions(Array.from(items).map(i => i.textContent), q);
    } else if (e.key === 'Enter') {
        e.preventDefault();
        suggBox.classList.add('d-none');
        // If suggestion selected, fill input and render results
        if (activeIndex > -1 && items[activeIndex]) {
            const selected = items[activeIndex].textContent;
            input.value = selected;
            performSearch(selected);
        } else {
            performSearch(input.value);
        }
    }
});

// Handle mouse click on suggestion
suggBox.addEventListener('click', e => {
    const item = e.target.closest('.suggestion-item');
    if (item) {
        const selected = item.textContent;
        input.value = selected;
        suggBox.classList.add('d-none');
        performSearch(selected);
    }
});

// Hide suggestions when clicking outside
document.addEventListener('click', e => {
    if (!input.contains(e.target) && !suggBox.contains(e.target)) {
        suggBox.classList.add('d-none');
    }
});

// Initial load: show the first 4 results
document.addEventListener('DOMContentLoaded', () => {
    // Render corresponding bigData results
    const initialSuggestions = suggestionData.slice(0, 4);
    const initialResults = bigData.filter(d => initialSuggestions.includes(d.title));
    renderBigResults(initialResults, '');
});

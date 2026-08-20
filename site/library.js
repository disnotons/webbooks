(() => {
  const state = { books: [] };
  const $ = (id) => document.getElementById(id);

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('webbook-theme', theme);
  }

  function initTheme() {
    const saved = localStorage.getItem('webbook-theme');
    const systemDark = matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(saved || (systemDark ? 'dark' : 'light'));
    $('themeToggle').addEventListener('click', () => {
      applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
    });
  }

  function text(value) {
    return value == null ? '' : String(value);
  }

  function render(books) {
    const container = $('librarySections');
    container.replaceChildren();

    if (!books.length) {
      $('libraryStatus').textContent = state.books.length
        ? '검색 조건에 맞는 웹북이 없습니다.'
        : '아직 발행된 웹북이 없습니다.';
      return;
    }

    $('libraryStatus').textContent = `웹북 ${books.length}권`;
    const groups = new Map();
    for (const book of books) {
      const category = text(book.category) || '기타';
      if (!groups.has(category)) groups.set(category, []);
      groups.get(category).push(book);
    }

    for (const [category, items] of groups) {
      const section = document.createElement('section');
      section.className = 'library-section';
      const heading = document.createElement('h2');
      heading.textContent = category;
      section.appendChild(heading);

      const grid = document.createElement('div');
      grid.className = 'book-grid';
      for (const book of items) {
        const card = document.createElement('a');
        card.className = 'book-card';
        card.href = book.url;

        const meta = document.createElement('div');
        meta.className = 'book-card-meta';
        const series = text(book.series || book.collection);
        if (series) {
          const badge = document.createElement('span');
          badge.className = 'badge';
          badge.textContent = series;
          meta.appendChild(badge);
        }
        const count = document.createElement('span');
        count.className = 'muted';
        count.textContent = `${book.chapter_count}편`;
        meta.appendChild(count);

        const title = document.createElement('h3');
        title.textContent = text(book.title);

        const desc = document.createElement('p');
        desc.textContent = text(book.description) || '웹북 읽기';

        card.append(meta, title, desc);
        grid.appendChild(card);
      }
      section.appendChild(grid);
      container.appendChild(section);
    }
  }

  async function main() {
    initTheme();
    try {
      const response = await fetch('catalog.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      state.books = await response.json();
      render(state.books);
    } catch (error) {
      console.error(error);
      $('libraryStatus').textContent = '웹북 목록을 불러오지 못했습니다.';
    }

    $('librarySearch').addEventListener('input', (event) => {
      const q = event.target.value.trim().toLowerCase();
      if (!q) return render(state.books);
      render(state.books.filter((book) => {
        const haystack = [
          book.title, book.category, book.collection, book.series, book.description
        ].map(text).join(' ').toLowerCase();
        return haystack.includes(q);
      }));
    });
  }

  main();
})();

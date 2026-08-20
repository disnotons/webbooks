(() => {
  const $ = (id) => document.getElementById(id);
  const state = { book: null, currentIndex: 0 };

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

  function showToast(message) {
    const toast = $('toast');
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => toast.classList.remove('show'), 1800);
  }

  function chapterKey(chapter) {
    return String(chapter.id || chapter.file || chapter.index);
  }

  function renderToc(filter = '') {
    const toc = $('toc');
    toc.replaceChildren();
    const q = filter.trim().toLowerCase();

    state.book.chapters.forEach((chapter, index) => {
      const label = `${chapter.id || ''} ${chapter.title || ''}`.trim();
      if (q && !label.toLowerCase().includes(q)) return;
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'toc-item';
      if (index === state.currentIndex) button.classList.add('active');
      button.dataset.index = index;
      button.textContent = label;
      button.addEventListener('click', () => loadChapter(index, true));
      toc.appendChild(button);
    });
  }

  function markdownToHtml(markdown) {
    if (window.marked?.parse) {
      window.marked.setOptions({ gfm: true, breaks: false });
      return window.marked.parse(markdown);
    }
    const escaped = markdown
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;');
    return `<pre>${escaped}</pre>`;
  }

  function updateNav() {
    const prev = $('prevChapter');
    const next = $('nextChapter');
    prev.disabled = state.currentIndex <= 0;
    next.disabled = state.currentIndex >= state.book.chapters.length - 1;
  }

  function updateUrl(chapter) {
    const url = new URL(location.href);
    url.searchParams.set('chapter', chapterKey(chapter));
    history.replaceState(null, '', url);
  }

  async function loadChapter(index, pushToUrl = true) {
    const chapter = state.book.chapters[index];
    if (!chapter) return;
    state.currentIndex = index;
    renderToc($('tocSearch').value);
    updateNav();

    $('chapterMeta').textContent = `${index + 1} / ${state.book.chapters.length}`;
    $('chapterContent').innerHTML = '<p>본문을 불러오는 중입니다.</p>';

    try {
      const response = await fetch(chapter.content_url, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const markdown = await response.text();
      $('chapterContent').innerHTML = markdownToHtml(markdown);
      document.title = `${chapter.title} · ${state.book.title}`;
      if (pushToUrl) updateUrl(chapter);
      window.scrollTo({ top: 0, behavior: 'auto' });
      const active = document.querySelector('.toc-item.active');
      active?.scrollIntoView({ block: 'nearest' });
      $('tocPanel').classList.remove('open');
    } catch (error) {
      console.error(error);
      $('chapterContent').innerHTML = '<p>본문을 불러오지 못했습니다.</p>';
    }
  }

  async function shareCurrent() {
    const chapter = state.book.chapters[state.currentIndex];
    const data = {
      title: `${chapter.title} · ${state.book.title}`,
      text: chapter.title,
      url: location.href,
    };
    if (navigator.share) {
      try {
        await navigator.share(data);
        return;
      } catch (error) {
        if (error?.name === 'AbortError') return;
      }
    }
    try {
      await navigator.clipboard.writeText(location.href);
      showToast('현재 주소를 복사했습니다.');
    } catch {
      showToast('주소 복사를 사용할 수 없습니다.');
    }
  }

  function initProgress() {
    const progress = $('readingProgress');
    const topButton = $('topButton');
    const update = () => {
      const root = document.documentElement;
      const max = root.scrollHeight - root.clientHeight;
      const ratio = max > 0 ? root.scrollTop / max : 0;
      progress.style.transform = `scaleX(${Math.min(1, Math.max(0, ratio))})`;
      topButton.classList.toggle('visible', root.scrollTop > 600);
    };
    addEventListener('scroll', update, { passive: true });
    addEventListener('resize', update);
    update();
    topButton.addEventListener('click', () => scrollTo({ top: 0, behavior: 'smooth' }));
  }

  async function main() {
    initTheme();
    initProgress();

    try {
      const response = await fetch('book.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      state.book = await response.json();
    } catch (error) {
      console.error(error);
      $('bookTitle').textContent = '웹북 정보를 불러오지 못했습니다.';
      $('chapterContent').innerHTML = '<p>웹북 정보를 확인할 수 없습니다.</p>';
      return;
    }

    $('libraryLink').href = state.book.library_url || './';
    $('bookTitle').textContent = state.book.title;
    $('bookCategory').textContent = [state.book.category, state.book.series]
      .filter(Boolean).join(' · ');
    $('bookDescription').textContent = state.book.description || '';

    $('tocSearch').addEventListener('input', (event) => renderToc(event.target.value));
    $('prevChapter').addEventListener('click', () => loadChapter(state.currentIndex - 1, true));
    $('nextChapter').addEventListener('click', () => loadChapter(state.currentIndex + 1, true));
    $('shareButton').addEventListener('click', shareCurrent);
    $('menuToggle').addEventListener('click', () => $('tocPanel').classList.toggle('open'));

    const requested = new URLSearchParams(location.search).get('chapter');
    const found = requested
      ? state.book.chapters.findIndex((chapter) =>
          chapterKey(chapter) === requested || chapter.file === requested)
      : 0;
    await loadChapter(found >= 0 ? found : 0, Boolean(requested));
  }

  main();
})();

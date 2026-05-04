// OPUS — interaction layer
// Handles: contents drawer, keyboard nav (g, j, k, /), ASCII pre detection,
// active TOC highlighting on scroll.

(function () {
  'use strict';

  // --- Contents drawer ---------------------------------------------------

  const drawer = document.getElementById('toc-drawer');
  const backdrop = document.getElementById('toc-backdrop');
  const toggle = document.getElementById('toc-toggle');
  const closeBtn = document.getElementById('toc-close');

  function openDrawer() {
    drawer?.classList.add('open');
    backdrop?.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeDrawer() {
    drawer?.classList.remove('open');
    backdrop?.classList.remove('open');
    document.body.style.overflow = '';
  }

  toggle?.addEventListener('click', openDrawer);
  closeBtn?.addEventListener('click', closeDrawer);
  backdrop?.addEventListener('click', closeDrawer);

  // --- Keyboard navigation -----------------------------------------------
  // g  → open contents drawer
  // j  → next chapter
  // k  → previous chapter
  // i  → return to index
  // Esc → close drawer

  document.addEventListener('keydown', (e) => {
    // Ignore when typing into a form field
    const tag = (e.target?.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || e.target?.isContentEditable) return;

    if (e.key === 'Escape') {
      closeDrawer();
      return;
    }
    if (e.metaKey || e.ctrlKey || e.altKey) return;

    switch (e.key.toLowerCase()) {
      case 'g':
      case 't':
        e.preventDefault();
        if (drawer?.classList.contains('open')) closeDrawer();
        else openDrawer();
        break;
      case 'j': {
        const next = document.querySelector('a.nav-next-link');
        if (next) { e.preventDefault(); window.location = next.href; }
        break;
      }
      case 'k': {
        const prev = document.querySelector('a.nav-prev-link');
        if (prev) { e.preventDefault(); window.location = prev.href; }
        break;
      }
      case 'i': {
        e.preventDefault();
        window.location = 'index.html';
        break;
      }
    }
  });

  // --- Active section highlighting in side TOC ---------------------------

  const articleToc = document.querySelector('.article-toc');
  if (articleToc) {
    const links = Array.from(articleToc.querySelectorAll('a[href^="#"]'));
    const targets = links
      .map((a) => {
        const id = decodeURIComponent(a.getAttribute('href').slice(1));
        return document.getElementById(id);
      })
      .filter(Boolean);

    if (targets.length) {
      const observer = new IntersectionObserver(
        (entries) => {
          // Find the entry currently most "active" (top-most that is visible).
          const visible = entries
            .filter((e) => e.isIntersecting)
            .sort((a, b) => a.target.getBoundingClientRect().top - b.target.getBoundingClientRect().top);
          if (!visible.length) return;
          const id = visible[0].target.id;
          links.forEach((a) => a.classList.remove('is-current-section'));
          const matchingLink = articleToc.querySelector(`a[href="#${CSS.escape(id)}"]`);
          matchingLink?.classList.add('is-current-section');
        },
        { rootMargin: '-80px 0px -70% 0px', threshold: 0 }
      );
      targets.forEach((t) => observer.observe(t));
    }
  }

  // --- ASCII art detection in pre blocks ---------------------------------
  // If a <pre> contains box-drawing characters, mark it so CSS can tighten
  // letter-spacing and disable ligatures, preserving alignment.

  const ASCII_BOX_CHARS = /[─│┌┐└┘├┤┬┴┼━┃┏┓┗┛╔╗╚╝╠╣╦╩╬▲▼◀▶◆●◯]/;
  document.querySelectorAll('pre').forEach((pre) => {
    const text = pre.textContent || '';
    if (ASCII_BOX_CHARS.test(text)) {
      pre.classList.add('ascii');
    }
  });

  // --- External links open in new tab ------------------------------------

  document.querySelectorAll('a[href^="http"]').forEach((a) => {
    if (!a.href.includes(window.location.host)) {
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
    }
  });

  // --- Persist drawer scroll across navigation ---------------------------

  if (drawer) {
    const scrollKey = 'opus-toc-scroll';
    const restoreScroll = () => {
      const saved = sessionStorage.getItem(scrollKey);
      if (saved) drawer.scrollTop = parseInt(saved, 10) || 0;
    };
    drawer.addEventListener('scroll', () => {
      sessionStorage.setItem(scrollKey, String(drawer.scrollTop));
    });
    // Restore when drawer is opened
    toggle?.addEventListener('click', () => setTimeout(restoreScroll, 50));
  }

  // --- Highlight current chapter in drawer TOC ---------------------------

  const currentChapter = document.body.dataset.chapter;
  if (currentChapter) {
    const link = drawer?.querySelector(`a[data-chapter="${currentChapter}"]`);
    link?.classList.add('is-current');
    // Scroll into view if needed when drawer opens
    toggle?.addEventListener('click', () => {
      setTimeout(() => link?.scrollIntoView({ block: 'nearest' }), 50);
    });
  }
})();

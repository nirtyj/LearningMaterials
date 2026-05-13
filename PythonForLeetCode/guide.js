(function () {
    const SIDEBAR_OUTLINE = [
        {
            group: 'Foundations',
            items: [
                { href: 'compilation.html', label: 'Compilation & Execution' },
                { href: 'variables.html',   label: 'Variables & Memory' },
                { href: 'complexity.html',  label: 'Time Complexity' },
            ],
        },
        {
            group: 'Data Structures',
            items: [
                { href: 'list.html',    label: 'List / Array' },
                { href: 'dict.html',    label: 'Dict / HashMap' },
                { href: 'set.html',     label: 'Set / HashSet' },
                { href: 'stack.html',   label: 'Stack' },
                { href: 'queue.html',   label: 'Queue / Deque' },
                { href: 'heap.html',    label: 'Heap / Priority Queue' },
                { href: 'string.html',  label: 'String' },
                { href: 'counter.html', label: 'DefaultDict / Counter' },
            ],
        },
        {
            group: 'Object-Oriented',
            items: [
                { href: 'classes.html', label: 'Classes, Nodes & OOP' },
            ],
        },
        {
            group: 'Patterns & Reference',
            items: [
                { href: 'algorithms.html',             label: 'Algorithm Patterns' },
                { href: 'power-features.html',         label: 'Python Power Features' },
                { href: 'python-builtins.html',        label: 'Python Builtins' },
                { href: 'gotchas.html',                label: 'Common Gotchas' },
                { href: 'cheatsheet-by-operation.html', label: 'Methods by Operation' },
            ],
        },
    ];

    const HOME_HREF = 'index.html';

    function currentPage() {
        const file = (location.pathname.split('/').pop() || HOME_HREF).toLowerCase();
        return file === '' ? HOME_HREF : file;
    }

    function escapeHtml(str) {
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function buildSidebarMarkup(activeHref, subItems) {
        const header = `
            <div class="sidebar-header">
                <a href="${HOME_HREF}" style="text-decoration:none;">
                    <h1>🐍 LC</h1>
                    <div class="sidebar-subtitle">Python for LeetCode</div>
                </a>
            </div>`;

        const groupsHtml = SIDEBAR_OUTLINE.map(group => {
            const itemsHtml = group.items.map(item => {
                const isActive = item.href === activeHref;
                const itemClasses = ['nav-item'];
                if (isActive) itemClasses.push('expanded');
                const linkClasses = ['nav-link'];
                if (isActive) linkClasses.push('active');

                let subnavHtml = '';
                if (isActive && subItems && subItems.length) {
                    subnavHtml = '<ul class="subnav">' + subItems.map(s =>
                        `<li><a href="#${s.id}" class="sub-link">${escapeHtml(s.label)}</a></li>`
                    ).join('') + '</ul>';
                }

                return `
                    <li class="${itemClasses.join(' ')}" data-section="${item.href}">
                        <a href="${item.href}" class="${linkClasses.join(' ')}">${escapeHtml(item.label)}</a>
                        ${subnavHtml}
                    </li>`;
            }).join('');

            return `
                <div class="sidebar-group">${escapeHtml(group.group)}</div>
                <ul class="nav-list">${itemsHtml}</ul>`;
        }).join('');

        return header + '<nav>' + groupsHtml + '</nav>';
    }

    function collectSubItems() {
        const headings = Array.from(document.querySelectorAll('.content h2[id], .content h3[id]'));
        return headings.map(h => {
            const raw = h.textContent.trim();
            const cleaned = raw.replace(/^[\p{Emoji}\p{Emoji_Presentation}\p{Extended_Pictographic}\u{FE0F}\u{20E3}\d#️⃣\s]+/u, '').trim();
            return { id: h.id, label: cleaned || raw };
        }).filter(item => item.id);
    }

    function init() {
        const sidebar = document.querySelector('.sidebar');
        if (!sidebar) return;

        const subItems = collectSubItems();
        sidebar.innerHTML = buildSidebarMarkup(currentPage(), subItems);

        const body = document.body;
        const toggle = document.querySelector('.nav-toggle');
        const backdrop = document.querySelector('.sidebar-backdrop');
        const content = document.querySelector('.content');
        const navLinks = Array.from(document.querySelectorAll('.sidebar .nav-link'));
        const subLinks = Array.from(document.querySelectorAll('.sidebar .sub-link'));

        const isMobile = () => window.matchMedia('(max-width: 768px)').matches;
        const closeNav = () => {
            body.classList.remove('nav-open');
            if (toggle) toggle.setAttribute('aria-expanded', 'false');
        };

        if (toggle) {
            toggle.addEventListener('click', () => {
                const open = body.classList.toggle('nav-open');
                toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            });
        }
        if (backdrop) backdrop.addEventListener('click', closeNav);

        [...navLinks, ...subLinks].forEach(link => {
            link.addEventListener('click', () => {
                if (isMobile()) closeNav();
            });
        });

        if (subItems.length === 0) return;

        const headings = subItems
            .map(item => document.getElementById(item.id))
            .filter(Boolean);
        const visible = new Set();

        const setActive = (id) => {
            subLinks.forEach(link => {
                link.classList.toggle('active', link.getAttribute('href') === '#' + id);
            });
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) visible.add(entry.target);
                else visible.delete(entry.target);
            });
            if (visible.size) {
                const top = [...visible].sort(
                    (a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top
                )[0];
                setActive(top.id);
            }
        }, {
            root: isMobile() ? null : content,
            rootMargin: '-15% 0px -70% 0px',
            threshold: 0,
        });

        headings.forEach(h => observer.observe(h));
        if (headings.length) setActive(headings[0].id);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

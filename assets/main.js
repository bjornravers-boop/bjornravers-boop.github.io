// UllieMoeke Productions: small enhancements. Every page still works without this file.
(() => {
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
  };

  // Theme: follow the system unless the visitor picked one.
  const saved = store.get('theme');
  if (saved) root.dataset.theme = saved;
  const toggle = document.querySelector('.theme-toggle');
  if (toggle) {
    const isDark = () => root.dataset.theme
      ? root.dataset.theme === 'dark'
      : matchMedia('(prefers-color-scheme: dark)').matches;
    const paint = () => {
      toggle.innerHTML = isDark()
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
      toggle.setAttribute('aria-label', isDark() ? 'Switch to light mode' : 'Switch to dark mode');
    };
    toggle.addEventListener('click', () => {
      root.dataset.theme = isDark() ? 'light' : 'dark';
      store.set('theme', root.dataset.theme);
      paint();
    });
    paint();
  }

  // Nav background once the page scrolls; reading progress bar on policy pages.
  const nav = document.querySelector('.nav');
  const bar = document.querySelector('.progress');
  const onScroll = () => {
    nav?.classList.toggle('scrolled', scrollY > 12);
    if (bar) {
      const max = document.documentElement.scrollHeight - innerHeight;
      bar.style.transform = `scaleX(${max > 0 ? Math.min(scrollY / max, 1) : 0})`;
    }
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Hero headline: animate letter by letter, keeping words together.
  const h1 = document.querySelector('[data-split]');
  if (h1 && !reduced) {
    let i = 0;
    const html = [];
    for (const node of [...h1.childNodes]) {
      const isSpan = node.nodeType === 1;
      const words = node.textContent.split(/(\s+)/);
      const cls = isSpan ? node.className : '';
      for (const w of words) {
        if (!w) continue;
        if (/^\s+$/.test(w)) { html.push(' '); continue; }
        if (isSpan) { // gradient text: animate whole words, background-clip breaks on transformed children
          html.push(`<span class="word char ${cls}" style="animation-delay:${(0.15 + i * 0.035).toFixed(3)}s">${w}</span>`);
          i += w.length;
          continue;
        }
        const chars = [...w].map(c => `<span class="char" style="animation-delay:${(0.15 + i++ * 0.035).toFixed(3)}s">${c}</span>`).join('');
        html.push(`<span class="word ${cls}">${chars}</span>`);
      }
    }
    h1.setAttribute('aria-label', h1.textContent.trim().replace(/\s+/g, ' '));
    h1.innerHTML = html.join('');
    h1.querySelectorAll('.word').forEach(w => w.setAttribute('aria-hidden', 'true'));
  }

  // Reveal on scroll.
  const io = new IntersectionObserver(entries => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  if (reduced) return;
  const fine = matchMedia('(pointer: fine)').matches;

  // Floating hero icons drift away from the pointer a little.
  const floats = document.querySelectorAll('.float-icon');
  if (floats.length && fine) {
    addEventListener('pointermove', e => {
      const x = e.clientX / innerWidth - 0.5, y = e.clientY / innerHeight - 0.5;
      floats.forEach((f, n) => {
        const depth = (n + 1) * 14;
        f.style.transform = `translate(${-x * depth}px, ${-y * depth}px)`;
      });
    }, { passive: true });
  }

  // 3D tilt for the phone mockups.
  if (fine) {
    document.querySelectorAll('.app-visual').forEach(v => {
      const phone = v.querySelector('.phone');
      v.addEventListener('pointermove', e => {
        const r = v.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        phone.style.transform = `rotateY(${x * 18}deg) rotateX(${-y * 14}deg) translateZ(0)`;
      });
      v.addEventListener('pointerleave', () => { phone.style.transform = ''; });
    });
  }

  // Spotlight that follows the pointer on the promise cards.
  document.querySelectorAll('.card').forEach(c => {
    c.addEventListener('pointermove', e => {
      const r = c.getBoundingClientRect();
      c.style.setProperty('--mx', `${e.clientX - r.left}px`);
      c.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });
})();

// Digital cookies: an in-page collectible, the same idea as in the apps. Runs with reduced motion too,
// just without the crumbs flying around.
(() => {
  const btn = document.querySelector('.cookie-btn');
  const out = document.querySelector('.cookie-count');
  if (!btn) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let count = 0;
  try { count = +localStorage.getItem('cookies') || 0; } catch { /* private mode */ }
  const lines = ['Grandma approves.', 'Still warm.', 'Crumbs everywhere. Worth it.', 'No calories. Literally.', 'You have excellent taste.'];
  const show = fresh => {
    if (!count) return;
    out.textContent = `${count} digital cookie${count === 1 ? '' : 's'} collected${fresh ? ' · ' + lines[count % lines.length] : ''}`;
  };
  show(false);
  btn.addEventListener('click', e => {
    count++;
    try { localStorage.setItem('cookies', count); } catch { /* private mode */ }
    show(true);
    if (reduced) return;
    const r = btn.getBoundingClientRect();
    const cx = e.clientX || r.left + r.width / 2, cy = e.clientY || r.top + r.height / 2;
    for (let i = 0; i < 14; i++) {
      const c = document.createElement('span');
      c.className = 'crumb';
      c.textContent = i % 4 ? '🍪' : '✨';
      document.body.appendChild(c);
      const a = Math.random() * Math.PI * 2, d = 90 + Math.random() * 160;
      c.animate([
        { transform: `translate(${cx - 14}px, ${cy - 14}px) scale(.4) rotate(0deg)`, opacity: 1 },
        { transform: `translate(${cx - 14 + Math.cos(a) * d}px, ${cy - 14 + Math.sin(a) * d - 60}px) scale(1) rotate(${(Math.random() - .5) * 540}deg)`, opacity: 1, offset: .6 },
        { transform: `translate(${cx - 14 + Math.cos(a) * d * 1.2}px, ${cy + 120 + Math.random() * 120}px) scale(.8) rotate(${(Math.random() - .5) * 720}deg)`, opacity: 0 },
      ], { duration: 1300 + Math.random() * 500, easing: 'cubic-bezier(.2,.7,.3,1)' }).onfinish = () => c.remove();
    }
  });
})();

import Reveal from 'reveal.js';
import Markdown from 'reveal.js/plugin/markdown';
import Highlight from 'reveal.js/plugin/highlight';
import Notes from 'reveal.js/plugin/notes';
import 'reveal.js/reveal.css';
import 'reveal.js/theme/black.css';
import 'reveal.js/plugin/highlight/monokai.css';
import './slides.css';

export function startDeck(markdown) {
  // Embed the Markdown at build time so the published deck needs no fetch.
  const template = document.createElement('script');
  template.type = 'text/template';
  template.textContent = markdown;
  document.querySelector('[data-markdown]').append(template);

  const deck = new Reveal({
    hash: true,
    slideNumber: 'c/t',
    transition: 'slide',
    plugins: [Markdown, Highlight, Notes],
  });

  return deck.initialize();
}

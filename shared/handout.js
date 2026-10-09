import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { Marked, walkTokens } from 'marked';
import QRCode from 'qrcode';

// Replaces `<!-- handout: ./FILE.md -->` in an HTML entry with the rendered
// Markdown. Every `##` section gets a grid of QR codes for its external links,
// so participants can open them on a phone straight from the projector or
// a laptop screen.
const PLACEHOLDER = /<!--\s*handout:\s*(\S+)\s*-->/;
const EXTERNAL = /^https?:\/\//;

const escapeHtml = (text) =>
  text.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

const slugify = (text) =>
  text
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');

const displayUrl = (url) => url.replace(EXTERNAL, '').replace(/^www\./, '').replace(/\/$/, '');

const marked = new Marked({
  renderer: {
    link({ href, title, tokens }) {
      const text = this.parser.parseInline(tokens);
      const titleAttr = title ? ` title="${escapeHtml(title)}"` : '';
      const target = EXTERNAL.test(href) ? ' target="_blank" rel="noopener"' : '';
      return `<a href="${escapeHtml(href)}"${titleAttr}${target}>${text}</a>`;
    },
  },
});

async function qrSvg(url) {
  const svg = await QRCode.toString(url, {
    type: 'svg',
    margin: 2,
    errorCorrectionLevel: 'M',
    color: { dark: '#000000', light: '#ffffff' },
  });
  return svg.replace('<svg ', '<svg aria-hidden="true" ');
}

async function qrCard(url, label) {
  return `<a class="qr-card" href="${escapeHtml(url)}" target="_blank" rel="noopener">
  ${await qrSvg(url)}
  <span class="qr-label">${escapeHtml(label)}</span>
  <span class="qr-url">${escapeHtml(displayUrl(url))}</span>
</a>`;
}

function externalLinks(tokens) {
  const links = new Map();
  walkTokens(tokens, (token) => {
    if (token.type === 'link' && EXTERNAL.test(token.href) && !links.has(token.href)) {
      links.set(token.href, token.text.replace(/[*_`]/g, ''));
    }
  });
  return links;
}

function splitSections(tokens) {
  const intro = [];
  const sections = [];
  let title = '';
  for (const token of tokens) {
    if (token.type === 'heading' && token.depth === 1) {
      title = token.text;
    } else if (token.type === 'heading' && token.depth === 2) {
      sections.push({ heading: token, tokens: [] });
    } else {
      (sections.at(-1)?.tokens ?? intro).push(token);
    }
  }
  return { title, intro, sections };
}

export async function renderHandout(markdown, { pageUrl } = {}) {
  const { title, intro, sections } = splitSections(marked.lexer(markdown));

  const rendered = await Promise.all(
    sections.map(async ({ heading, tokens }) => {
      const id = slugify(heading.text);
      const cards = await Promise.all(
        [...externalLinks(tokens)].map(([url, label]) => qrCard(url, label)),
      );
      const qrGrid = cards.length
        ? `<div class="qr-grid" aria-label="Povezave s QR-kodami">${cards.join('\n')}</div>`
        : '';
      return {
        id,
        heading: marked.parseInline(heading.text),
        html: `<section id="${id}">
<h2><a class="anchor" href="#${id}">${marked.parseInline(heading.text)}</a></h2>
${marked.parser(tokens)}
${qrGrid}
</section>`,
      };
    }),
  );

  const pageQr = pageUrl
    ? `<a class="qr-card page-qr" href="${escapeHtml(pageUrl)}">
  ${await qrSvg(pageUrl)}
  <span class="qr-label">Odpri na telefonu</span>
  <span class="qr-url">${escapeHtml(displayUrl(pageUrl))}</span>
</a>`
    : '';

  const toc = rendered.map(({ id, heading }) => `<li><a href="#${id}">${heading}</a></li>`).join('\n');

  return `<header>
<div class="intro">
<h1>${marked.parseInline(title)}</h1>
${marked.parser(intro)}
</div>
${pageQr}
</header>
<nav class="toc" aria-label="Vaje"><ol>${toc}</ol></nav>
${rendered.map(({ html }) => html).join('\n')}`;
}

export function handout({ siteUrl = process.env.SITE_URL } = {}) {
  let root;
  let server;
  const sources = new Set();

  return {
    name: 'handout',
    configResolved(config) {
      root = config.root;
    },
    configureServer(devServer) {
      server = devServer;
    },
    async transformIndexHtml(html, ctx) {
      const match = html.match(PLACEHOLDER);
      if (!match) return html;

      const dir = path.dirname(ctx.filename);
      const source = path.resolve(dir, match[1]);
      sources.add(source);
      server?.watcher.add(source);

      const pageUrl = siteUrl
        ? new URL(`${path.relative(root, dir).split(path.sep).join('/')}/`, siteUrl.replace(/\/?$/, '/')).href
        : undefined;
      const body = await renderHandout(await readFile(source, 'utf8'), { pageUrl });
      return html.replace(match[0], () => body);
    },
    handleHotUpdate({ file, server: devServer }) {
      if (sources.has(file)) {
        devServer.ws.send({ type: 'full-reload' });
        return [];
      }
    },
  };
}

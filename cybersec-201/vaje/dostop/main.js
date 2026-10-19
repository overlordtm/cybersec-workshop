import bundle from './credentials.json';
import { decryptCredential } from './crypto.js';

const $ = (id) => document.getElementById(id);
let credential = null;
let attempt = 0;

function reset() {
  attempt++;
  credential = null;
  $('result').hidden = true;
  $('hosted').hidden = true;
  $('wireguard').hidden = true;
  $('username').textContent = '';
  $('login-password').value = '';
  $('login-password').type = 'password';
  $('show-password').textContent = 'Pokaži geslo';
  $('show-password').setAttribute('aria-pressed', 'false');
  $('claim-code').value = '';
  $('claim-code').type = 'password';
  $('show-code').textContent = 'Pokaži kodo';
  $('show-code').setAttribute('aria-pressed', 'false');
  $('install-config').textContent = '';
  $('unlock').disabled = false;
  $('status').textContent = '';
}

function toggle(input, button, subject) {
  const visible = $(input).type === 'password';
  $(input).type = visible ? 'text' : 'password';
  $(button).textContent = `${visible ? 'Skrij' : 'Pokaži'} ${subject}`;
  $(button).setAttribute('aria-pressed', String(visible));
}

$('show-code').addEventListener('click', () => toggle('claim-code', 'show-code', 'kodo'));
$('show-password').addEventListener('click', () => toggle('login-password', 'show-password', 'geslo'));
$('lock').addEventListener('click', () => { reset(); $('claim-code').focus(); });
window.addEventListener('pagehide', reset);
window.addEventListener('pageshow', (event) => { if (event.persisted) reset(); });

$('unlock-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const code = $('claim-code').value;
  reset();
  const current = attempt;
  if (!crypto.subtle) {
    $('status').textContent = 'Za prevzem odpri to stran prek HTTPS v sodobnem brskalniku.';
    return;
  }
  $('unlock').disabled = true;
  $('status').textContent = 'Odpiram tvoj dostop …';
  try {
    const payload = await decryptCredential(bundle, code);
    if (current !== attempt) return;
    credential = payload;
    $('username').textContent = payload.user;
    const hosted = payload.access === 'kali';
    $('access-kind').textContent = hosted ? 'KALI V BRSKALNIKU' : 'LASTNA KALI VM / WIREGUARD';
    $('hosted').hidden = !hosted;
    $('wireguard').hidden = hosted;
    if (hosted) $('login-password').value = payload.password;
    else $('install-config').textContent = `sudo install -d -m 700 /etc/wireguard\nsudo install -m 600 ${payload.user}.conf /etc/wireguard/acme.conf`;
    $('result').hidden = false;
    $('status').textContent = 'Dostop je pripravljen.';
    $('result-title').focus();
  } catch {
    if (current === attempt) $('status').textContent = Object.keys(bundle.entries).length
      ? 'Dostopa ni mogoče odpreti. Preveri kodo ali se obrni na izvajalca.'
      : 'Dostopi še niso objavljeni. Obrni se na izvajalca.';
  } finally {
    if (current === attempt) $('unlock').disabled = false;
  }
});

$('copy-password').addEventListener('click', async () => {
  if (credential?.access !== 'kali') return;
  try {
    await navigator.clipboard.writeText(credential.password);
    $('status').textContent = 'Geslo je kopirano v odložišče.';
  } catch {
    $('status').textContent = 'Kopiranje ni uspelo. Pokaži geslo in ga prekopiraj ročno.';
  }
});

$('download-config').addEventListener('click', () => {
  if (credential?.access !== 'wireguard') return;
  const url = URL.createObjectURL(new Blob([credential.config], { type: 'text/plain;charset=utf-8' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = `${credential.user}.conf`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

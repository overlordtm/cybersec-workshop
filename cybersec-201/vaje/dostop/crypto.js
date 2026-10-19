// Format shared with infra/export-credentials.py. No network or storage access here.
const encoder = new TextEncoder();
const decode = (value) => Uint8Array.from(atob(value), (c) => c.charCodeAt(0));

export function normalizeCode(code) {
  return code.toUpperCase().replace(/[\s-]/g, '');
}

export async function decryptCredential(bundle, code) {
  if (bundle.version !== 2 || bundle.iterations !== 600000) {
    throw new Error('Unsupported credential bundle');
  }
  const token = encoder.encode(normalizeCode(code));
  const material = await crypto.subtle.importKey('raw', token, 'PBKDF2', false, ['deriveBits', 'deriveKey']);
  const lookupKey = await crypto.subtle.deriveBits(
    { name: 'PBKDF2', hash: 'SHA-256', salt: decode(bundle.lookupSalt), iterations: bundle.iterations },
    material, 256,
  );
  const digest = new Uint8Array(await crypto.subtle.digest('SHA-256', lookupKey));
  const id = Array.from(digest, (n) => n.toString(16).padStart(2, '0')).join('');
  const entry = bundle.entries[id];
  if (!entry) throw new Error('Unknown code');
  const key = await crypto.subtle.deriveKey(
    { name: 'PBKDF2', hash: 'SHA-256', salt: decode(entry.salt), iterations: bundle.iterations },
    material, { name: 'AES-GCM', length: 256 }, false, ['decrypt'],
  );
  const decrypted = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: decode(entry.iv), additionalData: encoder.encode(`cybersec-201-access-v2:${id}`) },
    key, decode(entry.ciphertext),
  );
  const payload = JSON.parse(new TextDecoder().decode(decrypted));
  if (payload.version !== 1 || !/^udelezenec[12]\d{2}$/.test(payload.user)
      || !['kali', 'wireguard'].includes(payload.access)) throw new Error('Invalid credential');
  return payload;
}

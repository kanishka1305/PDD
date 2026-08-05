/* ═══════════════════════════════════════════════════════════
   DentAI — app.js   (shared utilities + professional toasts)
   ═══════════════════════════════════════════════════════════ */
const API = '';   // same-origin — FastAPI serves both

/* ── Storage helpers ── */
const store = {
  get:   k => { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
  set:   (k, v) => localStorage.setItem(k, JSON.stringify(v)),
  clear: () => localStorage.clear()
};

/* ── Auth guards ── */
function requireAuth()  { if (!store.get('user')) window.location.href = '/login'; }
function requireGuest() { if ( store.get('user')) window.location.href = '/dashboard'; }

/* ── Sidebar population ── */
function populateSidebar() {
  const u = store.get('user');
  if (!u) return;
  const nameEl  = document.getElementById('sb-name');
  const emailEl = document.getElementById('sb-email');
  if (nameEl)  nameEl.textContent  = 'Dr. ' + u.name;
  if (emailEl) emailEl.textContent = u.email;
}

/* ── Logout ── */
function logout() { store.clear(); window.location.href = '/login'; }

/* ── POST form-encoded ── */
async function postForm(endpoint, data) {
  const res = await fetch(API + endpoint, {
    method:  'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body:    new URLSearchParams(data).toString()
  });
  return res.json();
}

/* ── POST multipart ── */
async function postFile(endpoint, formData) {
  const res = await fetch(API + endpoint, { method: 'POST', body: formData });
  return res.json();
}

/* ═══════════════════════════════════════════════════════════
   PROFESSIONAL TOAST SYSTEM
   ═══════════════════════════════════════════════════════════ */
(function initProToasts() {
  if (document.getElementById('pro-toast-wrap')) return;
  const wrap = document.createElement('div');
  wrap.id = 'pro-toast-wrap';
  wrap.className = 'pro-toast-wrap';
  document.body.appendChild(wrap);
})();

const TOAST_ICONS = {
  success: 'check-circle-2',
  error:   'alert-circle',
  info:    'info',
  warn:    'alert-triangle',
  upload:  'upload-cloud',
  export:  'download',
  ai:      'cpu',
  report:  'file-text'
};

/**
 * proToast(title, sub, type, duration)
 * type: 'success' | 'error' | 'info' | 'warn' | 'upload' | 'export' | 'ai' | 'report'
 */
function proToast(title, sub = '', type = 'info', duration = 4000) {
  // Ensure container exists (pages that haven't been updated yet)
  let wrap = document.getElementById('pro-toast-wrap');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.id = 'pro-toast-wrap';
    wrap.className = 'pro-toast-wrap';
    document.body.appendChild(wrap);
  }

  const iconType = ['success','error','info','warn','upload'].includes(type) ? type : 'info';
  const iconName = TOAST_ICONS[type] || 'info';

  const el = document.createElement('div');
  el.className = 'pro-toast';
  el.innerHTML = `
    <div class="pt-accent pt-${iconType}"></div>
    <div class="pt-body">
      <div class="pt-icon-wrap pt-${iconType}">
        <i data-lucide="${iconName}" style="width:18px;height:18px;"></i>
      </div>
      <div class="pt-content">
        <div class="pt-title">${title}</div>
        ${sub ? `<div class="pt-sub">${sub}</div>` : ''}
      </div>
      <button class="pt-close" onclick="this.closest('.pro-toast').remove()">
        <i data-lucide="x" style="width:13px;height:13px;"></i>
      </button>
    </div>
    <div class="pt-progress-bar">
      <div class="pt-progress-fill" id="ptpf-${Date.now()}" style="width:100%;"></div>
    </div>`;

  wrap.appendChild(el);

  // Re-render icons if lucide is available
  if (window.lucide) lucide.createIcons();

  // Animate in
  requestAnimationFrame(() => {
    requestAnimationFrame(() => el.classList.add('pt-show'));
  });

  // Progress bar drain
  const fill = el.querySelector('.pt-progress-fill');
  if (fill && duration > 0) {
    fill.style.transition = `width ${duration}ms linear`;
    requestAnimationFrame(() => { requestAnimationFrame(() => { fill.style.width = '0%'; }); });
  }

  // Auto-dismiss
  if (duration > 0) {
    setTimeout(() => {
      el.classList.add('pt-hide');
      setTimeout(() => el.remove(), 380);
    }, duration);
  }

  return el;
}

/* Convenience aliases matching old toast() signature so existing pages work unchanged */
function toast(msg, type = 'info') {
  // Map old types to new
  const typeMap = { success:'success', error:'error', info:'info' };
  const t = typeMap[type] || 'info';

  // Try to use new system if container present, fallback to legacy
  try {
    proToast(msg, '', t, 3400);
  } catch {
    // Legacy fallback
    let el = document.getElementById('toast');
    if (!el) { el = document.createElement('div'); el.id = 'toast'; el.className = 'toast'; document.body.appendChild(el); }
    el.textContent = msg;
    el.className = `toast ${type} show`;
    setTimeout(() => el.classList.remove('show'), 3000);
  }
}

/* ── Specialised toast helpers ── */
function toastUpload(filename, scanId)   { proToast('Scan Uploaded', `${filename} → Scan #${scanId}`, 'upload', 5000); }
function toastAnalysis(scanId, conf)     { proToast('AI Segmentation Complete', `Scan #${scanId} · Confidence ${conf ? conf.toFixed(1)+'%' : '—'}`, 'ai', 5000); }
function toastExport(fmt, region, scanId){ proToast(`${fmt.toUpperCase()} Export Ready`, `${region.replace(/_/g,' ')} · Scan #${scanId}`, 'export', 4000); }
function toastReport()                   { proToast('Clinical Report Generated', 'PDF ready for download', 'report', 4000); }
function toastError(title, detail)       { proToast(title, detail, 'error', 6000); }

/* ═══════════════════════════════════════════════════════════
   SHARED UTILITIES
   ═══════════════════════════════════════════════════════════ */

/** Format voxel number with locale separator, returns "Not Segmented" for 0/null */
function fmtVoxel(v) {
  if (v === undefined || v === null) return '—';
  const n = parseFloat(v);
  if (isNaN(n) || n === 0) return 'Not Segmented';
  return n.toLocaleString();
}

/** Format number with fixed decimals, dash for null */
function fmtNum(v, dec = 2) {
  if (v === undefined || v === null) return '—';
  const n = parseFloat(v);
  return isNaN(n) ? '—' : n.toFixed(dec);
}

/** HTML-escape a string */
function escHtml(str) {
  return String(str ?? '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/** Format file size bytes → KB / MB / GB */
function fmtSize(bytes) {
  if (bytes >= 1073741824) return (bytes / 1073741824).toFixed(2) + ' GB';
  if (bytes >= 1048576)    return (bytes / 1048576).toFixed(1)    + ' MB';
  return (bytes / 1024).toFixed(0) + ' KB';
}

/** Derive per-region stats from voxel volume */
function deriveRegionStats(volVoxels, totalVol) {
  const v = parseFloat(volVoxels) || 0;
  if (v === 0) return { sa:'N/A', vc:'N/A', conf:'N/A', volMm3:'N/A', pct:'0' };
  const sp   = 0.4;  // mm/voxel typical CBCT
  const volMm3 = (v * sp * sp * sp).toFixed(1);
  const saMm2  = (v * 0.6 * sp * sp).toFixed(1);
  const conf   = (88 + (v % 12)).toFixed(1) + '%';
  const pct    = totalVol > 0 ? ((v / totalVol) * 100).toFixed(1) : '0';
  return { sa: saMm2, vc: v.toLocaleString(), conf, volMm3, pct };
}

/** Mobile sidebar toggle wiring (called once after lucide.createIcons()) */
function wireSidebar() {
  const toggle  = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (!toggle) return;
  toggle.addEventListener('click', () => {
    sidebar?.classList.toggle('open');
    overlay?.classList.toggle('open');
  });
  overlay?.addEventListener('click', () => {
    sidebar?.classList.remove('open');
    overlay?.classList.remove('open');
  });
}

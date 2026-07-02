// =============================================
// HMS Pro - Supabase Configuration & Core JS
// =============================================
const SUPABASE_URL = 'https://rqbnveuekmnlohqfjlia.supabase.co';
const SUPABASE_KEY = 'sb_publishable_Fh1N1Z_OEMK37_kOxIMDgw_dv6BOW41';

let supabaseClient = null;

function getSupabase() {
    if (!supabaseClient) {
        supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    }
    return supabaseClient;
}

// =============================================
// DARK / LIGHT MODE
// =============================================
function initTheme() {
    const saved = localStorage.getItem('hms_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeBtn(saved);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('hms_theme', next);
    updateThemeBtn(next);
}

function updateThemeBtn(theme) {
    const btn = document.getElementById('themeToggleBtn');
    if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// =============================================
// TOAST NOTIFICATIONS
// =============================================
function showToast(msg, type = 'success') {
    // Remove existing toast if any
    const existing = document.querySelector('.hms-toast');
    if (existing) existing.remove();

    const t = document.createElement('div');
    t.className = 'hms-toast';
    t.innerHTML = msg;

    const colors = {
        success: 'linear-gradient(135deg,#10b981,#059669)',
        error:   'linear-gradient(135deg,#ef4444,#dc2626)',
        info:    'linear-gradient(135deg,#6366f1,#8b5cf6)',
        warning: 'linear-gradient(135deg,#f59e0b,#d97706)'
    };

    Object.assign(t.style, {
        position: 'fixed',
        bottom: '2rem',
        right: '2rem',
        background: colors[type] || colors.info,
        color: 'white',
        padding: '1rem 1.5rem',
        borderRadius: '12px',
        fontWeight: '600',
        zIndex: '99999',
        boxShadow: '0 8px 32px rgba(0,0,0,0.35)',
        fontFamily: 'Outfit, sans-serif',
        fontSize: '0.95rem',
        animation: 'toastIn 0.3s ease',
        maxWidth: '320px'
    });
    document.body.appendChild(t);
    setTimeout(() => {
        t.style.animation = 'toastOut 0.3s ease forwards';
        setTimeout(() => t.remove(), 300);
    }, 3500);
}

// Inject toast keyframes once
(function injectToastCSS() {
    if (document.getElementById('hms-toast-css')) return;
    const s = document.createElement('style');
    s.id = 'hms-toast-css';
    s.textContent = `
        @keyframes toastIn  { from { opacity:0; transform: translateY(20px); } to { opacity:1; transform: translateY(0); } }
        @keyframes toastOut { from { opacity:1; transform: translateY(0); }    to { opacity:0; transform: translateY(20px); } }
    `;
    document.head.appendChild(s);
})();

// =============================================
// LOADING SKELETON HELPERS
// =============================================
function showSkeletonRows(tbodyId, cols = 5, rows = 4) {
    const tbody = document.getElementById(tbodyId);
    if (!tbody) return;
    tbody.innerHTML = Array.from({ length: rows }, () =>
        `<tr class="skeleton-row">${Array.from({ length: cols }, () =>
            `<td><div class="skeleton-cell"></div></td>`
        ).join('')}</tr>`
    ).join('');
}

function showSkeletonStat(cardId) {
    const el = document.getElementById(cardId);
    if (el) el.innerHTML = `<div class="skeleton-cell" style="width:80px;height:2.2rem;border-radius:8px;margin:0.5rem 0;"></div>`;
}

// =============================================
// ERROR DISPLAY HELPER
// =============================================
function showError(containerId, message = 'Data load nahi hua. Internet connection check karein aur page reload karein.') {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = `
        <div class="error-state">
            <div class="error-icon">⚠️</div>
            <h4>Kuch Masla Aaya!</h4>
            <p>${message}</p>
            <button class="btn-secondary small" onclick="location.reload()">🔄 Dobara Koshish</button>
        </div>`;
}

// =============================================
// SUPABASE DATA FUNCTIONS
// =============================================

/** Fetch patients from Supabase */
async function fetchPatients(limit = 10) {
    const db = getSupabase();
    const { data, error } = await db
        .from('patients')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(limit);
    if (error) throw error;
    return data;
}

/** Fetch appointments from Supabase */
async function fetchAppointments({ date, department, status, search } = {}) {
    const db = getSupabase();
    let query = db.from('appointments').select('*').order('date').order('time');
    if (date)       query = query.eq('date', date);
    if (department) query = query.ilike('department', `%${department}%`);
    if (status)     query = query.eq('status', status);
    if (search)     query = query.ilike('patient_name', `%${search}%`);
    const { data, error } = await query;
    if (error) throw error;
    return data;
}

/** Insert new patient */
async function insertPatient(patientData) {
    const db = getSupabase();
    const { data, error } = await db.from('patients').insert([patientData]).select();
    if (error) throw error;
    return data[0];
}

/** Insert new appointment */
async function insertAppointment(aptData) {
    const db = getSupabase();
    const { data, error } = await db.from('appointments').insert([aptData]).select();
    if (error) throw error;
    return data[0];
}

/** Fetch dashboard stats */
async function fetchDashboardStats() {
    const db = getSupabase();
    const today = new Date().toISOString().split('T')[0];

    const [patientsRes, todayAptRes, admittedRes] = await Promise.all([
        db.from('patients').select('id', { count: 'exact', head: true }),
        db.from('appointments').select('id', { count: 'exact', head: true }).eq('date', today),
        db.from('patients').select('id', { count: 'exact', head: true }).eq('status', 'admitted')
    ]);

    if (patientsRes.error) throw patientsRes.error;
    if (todayAptRes.error) throw todayAptRes.error;

    return {
        totalPatients:    patientsRes.count  || 0,
        todayAppointments: todayAptRes.count || 0,
        admittedPatients:  admittedRes.count || 0
    };
}

/** Fetch medical records by patient_id */
async function fetchMedicalRecords(patientId) {
    const db = getSupabase();
    const { data, error } = await db.from('medical_records')
        .select('*')
        .eq('patient_id', patientId)
        .order('date', { ascending: false });
    if (error) throw error;
    return data;
}

/** Insert new medical record */
async function insertMedicalRecord(recordData) {
    const db = getSupabase();
    const { data, error } = await db.from('medical_records').insert([recordData]).select();
    if (error) throw error;
    return data[0];
}

/** Insert new insurance request */
async function insertInsuranceRequest(requestData) {
    const db = getSupabase();
    console.log("Submitting insurance request:", requestData);
    const { data, error } = await db.from('insurance_requests').insert([requestData]).select();
    if (error) throw error;
    return data[0];
}

/** Insert new international service request */
async function insertInternationalRequest(requestData) {
    const db = getSupabase();
    console.log("Submitting international request:", requestData);
    const { data, error } = await db.from('international_requests').insert([requestData]).select();
    if (error) throw error;
    return data[0];
}

/** Subscribe to realtime changes */
function subscribeRealtime(table, callback) {
    const db = getSupabase();
    return db.channel(`realtime-${table}`)
        .on('postgres_changes', { event: '*', schema: 'public', table }, callback)
        .subscribe();
}

// =============================================
// MOBILE MENU HELPERS
// =============================================
function closeAllMobileMenuOverlays(breakpoint) {
    if (window.innerWidth <= breakpoint) return;

    document.querySelectorAll('.mobile-menu-overlay.active').forEach(overlay => {
        overlay.classList.remove('active');
    });
}

// =============================================
// APP INIT
// =============================================
document.addEventListener('DOMContentLoaded', () => {
    initTheme();

    // Theme toggle button click
    const themeBtn = document.getElementById('themeToggleBtn');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    // Dynamic sidebar hamburger toggle injection for dashboards
    const dashHeader = document.querySelector('.dashboard-header');
    if (dashHeader && !document.getElementById('hamburgerBtn')) {
        const hamburgerBtn = document.createElement('button');
        hamburgerBtn.id = 'hamburgerBtn';
        hamburgerBtn.innerHTML = '☰';
        hamburgerBtn.setAttribute('aria-label', 'Toggle Sidebar Menu');
        dashHeader.insertBefore(hamburgerBtn, dashHeader.firstChild);
    }

    // Mobile sidebar toggle
    const hamburger = document.getElementById('hamburgerBtn');
    const sidebar   = document.querySelector('.sidebar');
    if (hamburger && sidebar) {
        hamburger.addEventListener('click', () => sidebar.classList.toggle('sidebar-open'));
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768 && sidebar.classList.contains('sidebar-open')) {
                if (!sidebar.contains(e.target) && e.target !== hamburger) {
                    sidebar.classList.remove('sidebar-open');
                }
            }
        });
    }

    // Dynamic mobile navigation menu for secondary pages (.glass-nav)
    const glassNav = document.querySelector('.glass-nav');
    if (glassNav) {
        // Create hamburger button if it doesn't exist
        if (!glassNav.querySelector('.glass-hamburger')) {
            const hamburgerBtn = document.createElement('button');
            hamburgerBtn.className = 'glass-hamburger';
            hamburgerBtn.innerHTML = '☰';
            hamburgerBtn.setAttribute('aria-label', 'Toggle Navigation Menu');
            
            // Insert before the last button if possible, or append
            const actionBtn = glassNav.querySelector('.btn-primary');
            if (actionBtn) {
                glassNav.insertBefore(hamburgerBtn, actionBtn);
            } else {
                glassNav.appendChild(hamburgerBtn);
            }

            // Create mobile overlay
            const overlay = document.createElement('div');
            overlay.className = 'mobile-menu-overlay';
            
            const closeBtn = document.createElement('button');
            closeBtn.className = 'close-btn';
            closeBtn.innerHTML = '&times;';
            overlay.appendChild(closeBtn);

            const menuLinksContainer = document.createElement('div');
            menuLinksContainer.className = 'mobile-menu-links';

            // Extract links from .nav-links
            const originalNavLinks = glassNav.querySelector('.nav-links');
            if (originalNavLinks) {
                // We'll iterate through children
                Array.from(originalNavLinks.children).forEach(child => {
                    if (child.tagName === 'A') {
                        const linkCopy = child.cloneNode(true);
                        menuLinksContainer.appendChild(linkCopy);
                    } else if (child.classList.contains('dropdown')) {
                        const dropBtn = child.querySelector('.dropbtn');
                        const subLinks = child.querySelectorAll('.dropdown-content a');
                        if (!dropBtn || subLinks.length === 0) return;

                        const title = document.createElement('div');
                        title.className = 'mobile-menu-group-title';
                        title.textContent = dropBtn.textContent.replace(/[▾▾]/g, '').trim();
                        menuLinksContainer.appendChild(title);

                        const subContainer = document.createElement('div');
                        subContainer.className = 'mobile-submenu';
                        subLinks.forEach(sub => {
                            subContainer.appendChild(sub.cloneNode(true));
                        });
                        menuLinksContainer.appendChild(subContainer);
                    }
                });

                // Add Portal/Staff Login links for mobile viewports
                const accountTitle = document.createElement('div');
                accountTitle.className = 'mobile-menu-group-title';
                accountTitle.textContent = 'Account';
                menuLinksContainer.appendChild(accountTitle);

                const accountSub = document.createElement('div');
                accountSub.className = 'mobile-submenu';

                const patLogin = document.createElement('a');
                patLogin.href = 'patient-login.html';
                patLogin.textContent = 'Patient Portal Login';
                accountSub.appendChild(patLogin);

                const staffLogin = document.createElement('a');
                staffLogin.href = 'dashboard.html';
                staffLogin.textContent = 'Staff / Admin Login';
                accountSub.appendChild(staffLogin);

                menuLinksContainer.appendChild(accountSub);
            }

            overlay.appendChild(menuLinksContainer);
            document.body.appendChild(overlay);

            // Toggle events
            hamburgerBtn.addEventListener('click', () => {
                overlay.classList.add('active');
            });

            closeBtn.addEventListener('click', () => {
                overlay.classList.remove('active');
            });

            // Close overlay on link click
            overlay.addEventListener('click', (e) => {
                if (e.target.tagName === 'A') {
                    overlay.classList.remove('active');
                }
            });
        }
    }

    window.addEventListener('resize', () => closeAllMobileMenuOverlays(992));

    console.log('HMS Pro - Initialized ✅');
});

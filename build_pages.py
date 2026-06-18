import os

pages = {
    'billing-insurance.html': {
        'title': 'Billing & Insurance',
        'heading': 'Billing & Insurance',
        'subheading': 'Easy and transparent billing. Verify your insurance or make secure online payments.',
        'custom_css': '''
        .content-container { max-width: 900px; margin: 0 auto 4rem auto; padding: 0 5%; }
        .card { background: rgba(20, 22, 33, 0.6); backdrop-filter: blur(12px); border: 1px solid var(--glass-border); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; }
        .card h2 { font-size: 1.5rem; margin-bottom: 1rem; color: #efeff1; }
        .form-group { margin-bottom: 1.5rem; text-align: left; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; color: var(--text-muted); }
        .form-control { width: 100%; padding: 0.8rem 1rem; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); color: #fff; font-family: 'Outfit'; }
        .btn-submit { background: var(--accent-primary, #6366f1); color: #fff;  padding: 0.9rem 2rem; border-radius: 12px; border: none; font-size: 1rem; cursor: pointer; transition: 0.3s; font-weight: 600; width: 100%; }
        .btn-submit:hover { background: #4f46e5; }
        .insurance-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem; }
        .insurance-item { padding: 1.5rem; text-align: center; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); font-weight: 600; }
        ''',
        'custom_js': '''
        <script>
            async function submitInsurance(e) {
                e.preventDefault();
                const btn = e.target.querySelector('button');
                btn.innerHTML = 'Submitting...';
                
                const data = {
                    patient_name: document.getElementById('name').value,
                    policy_number: document.getElementById('policy').value,
                    provider: document.getElementById('provider').value
                };
                
                try {
                    await insertInsuranceRequest(data);
                    showToast('Insurance verification request submitted successfully!');
                    e.target.reset();
                } catch (err) {
                    showToast('Failed to submit: ' + err.message, 'error');
                } finally {
                    btn.innerHTML = 'Verify Insurance';
                }
            }
        </script>
        ''',
        'content': '''
        <div class="content-container">
            <div class="card">
                <h2>Accepted Insurance Providers</h2>
                <p style="color: var(--text-muted)">HMS Pro accepts most major national and international healthcare plans.</p>
                <div class="insurance-grid">
                    <div class="insurance-item">State Life Insurance</div>
                    <div class="insurance-item">Jubilee Life</div>
                    <div class="insurance-item">Allianz Care</div>
                    <div class="insurance-item">Bupa Global</div>
                    <div class="insurance-item">Cigna Healthcare</div>
                    <div class="insurance-item">Aetna International</div>
                </div>
            </div>

            <div class="card">
                <h2>Verify Your Insurance</h2>
                <form onsubmit="submitInsurance(event)">
                    <div class="form-group">
                        <label>Patient Full Name</label>
                        <input type="text" id="name" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label>Policy Number</label>
                        <input type="text" id="policy" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label>Insurance Provider</label>
                        <select id="provider" class="form-control" required>
                            <option value="">Select a Provider</option>
                            <option value="State Life">State Life</option>
                            <option value="Jubilee Life">Jubilee Life</option>
                            <option value="Allianz">Allianz</option>
                            <option value="Bupa">Bupa</option>
                            <option value="Cigna">Cigna</option>
                            <option value="Other">Other (We will contact you)</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-submit">Verify Insurance</button>
                </form>
            </div>
        </div>
        '''
    },
    'international-services.html': {
        'title': 'International Services',
        'heading': 'Global Patient Services',
        'subheading': 'World-class care, wherever you call home. We provide comprehensive support for our international patients.',
        'custom_css': '''
        .content-container { max-width: 1000px; margin: 0 auto 4rem auto; padding: 0 5%; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        .card { background: rgba(20, 22, 33, 0.6); backdrop-filter: blur(12px); border: 1px solid var(--glass-border); border-radius: 20px; padding: 2.5rem; }
        .card h2 { font-size: 1.5rem; margin-bottom: 1rem; color: #efeff1; }
        .service-list { list-style: none; padding: 0; }
        .service-list li { margin-bottom: 1rem; color: var(--text-muted); display: flex; align-items: start; gap: 0.75rem; }
        .service-list li span { font-size: 1.25rem; }
        .form-group { margin-bottom: 1.5rem; text-align: left; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; color: var(--text-muted); }
        .form-control { width: 100%; padding: 0.8rem 1rem; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); color: #fff; font-family: 'Outfit'; }
        .btn-submit { background: var(--accent-primary, #6366f1); color: #fff;  padding: 0.9rem 2rem; border-radius: 12px; border: none; font-size: 1rem; cursor: pointer; transition: 0.3s; font-weight: 600; width: 100%; }
        .btn-submit:hover { background: #4f46e5; }
        @media (max-width: 768px) { .content-container { grid-template-columns: 1fr; } }
        ''',
        'custom_js': '''
        <script>
            async function submitInternational(e) {
                e.preventDefault();
                const btn = e.target.querySelector('button');
                btn.innerHTML = 'Submitting...';
                
                const getSelectedServices = () => {
                    const checkboxes = document.querySelectorAll('input[name="services"]:checked');
                    let vals = [];
                    checkboxes.forEach((cb) => {
                        vals.push(cb.value);
                    });
                    return vals.join(', ');
                };
                
                const data = {
                    patient_name: document.getElementById('name').value,
                    country: document.getElementById('country').value,
                    email: document.getElementById('email').value,
                    services: getSelectedServices(),
                    notes: document.getElementById('notes').value
                };
                
                try {
                    await insertInternationalRequest(data);
                    showToast('International service request submitted successfully!');
                    e.target.reset();
                } catch (err) {
                    showToast('Failed to submit: ' + err.message, 'error');
                } finally {
                    btn.innerHTML = 'Request Assistance';
                }
            }
        </script>
        ''',
        'content': '''
        <div class="content-container">
            <div class="card">
                <h2>Our Premium Services</h2>
                <p style="color: var(--text-muted); margin-bottom: 1.5rem;">Traveling for medical care can be daunting. Let our dedicated International Patient Services team handle the details so you can focus on your health.</p>
                <ul class="service-list">
                    <li><span>🌐</span> <div><strong>Visa & Travel Assistance</strong><br>Medical visa letters and coordination with embassies.</div></li>
                    <li><span>🏨</span> <div><strong>Concierge & Accommodation</strong><br>VIP suites and partnerships with luxury hotels.</div></li>
                    <li><span>🗣️</span> <div><strong>Language Interpreters</strong><br>Free interpreters for Arabic, Mandarin, Spanish, and French.</div></li>
                    <li><span>✈️</span> <div><strong>Airport Transfers</strong><br>Complimentary pickup from the international airport.</div></li>
                    <li><span>💵</span> <div><strong>Financial Counseling</strong><br>Transparent estimates and international insurance coordination.</div></li>
                </ul>
            </div>

            <div class="card">
                <h2>Request Assistance</h2>
                <form onsubmit="submitInternational(event)">
                    <div class="form-group">
                        <label>Patient Full Name</label>
                        <input type="text" id="name" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label>Country of Residence</label>
                        <input type="text" id="country" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label>Email Address</label>
                        <input type="email" id="email" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label>Required Services (Check all that apply)</label>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">
                            <label><input type="checkbox" name="services" value="Visa Letter"> Visa Letter</label><br>
                            <label><input type="checkbox" name="services" value="Interpreter"> Interpreter</label><br>
                            <label><input type="checkbox" name="services" value="Accommodation"> Accommodation Booking</label><br>
                            <label><input type="checkbox" name="services" value="Airport Transfer"> Airport Transfer</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Additional Notes</label>
                        <textarea id="notes" class="form-control" rows="3" style="resize: vertical;"></textarea>
                    </div>
                    <button type="submit" class="btn-submit">Request Assistance</button>
                </form>
            </div>
        </div>
        '''
    },
    'patient-visitor-guide.html': {
        'title': 'Patient & Visitor Guide',
        'heading': 'Patient & Visitor Guide',
        'subheading': 'Everything you need to know before visiting HMS Pro.',
        'custom_css': '''
        .content-container { max-width: 900px; margin: 0 auto 4rem auto; padding: 0 5%; display: grid; gap: 1.5rem; }
        .card { background: rgba(20, 22, 33, 0.6); backdrop-filter: blur(12px); border: 1px solid var(--glass-border); border-radius: 20px; padding: 2rem; display: flex; align-items: start; gap: 1.5rem; }
        .card .icon { font-size: 2.5rem; }
        .card h2 { font-size: 1.4rem; margin-bottom: 0.5rem; color: #efeff1; }
        .card p { color: var(--text-muted); line-height: 1.6; }
        ''',
        'custom_js': '',
        'content': '''
        <div class="content-container">
            <div class="card">
                <div class="icon">🕒</div>
                <div>
                    <h2>Visiting Hours</h2>
                    <p><b>General Wards:</b> 10:00 AM - 12:00 PM and 4:00 PM - 7:00 PM.<br>
                    <b>ICU / CCU:</b> 11:00 AM - 12:00 PM and 5:00 PM - 6:00 PM. (Strictly one visitor per patient during these times).<br>
                    Please respect the resting times of our patients.</p>
                </div>
            </div>
            
            <div class="card">
                <div class="icon">🚗</div>
                <div>
                    <h2>Parking Options</h2>
                    <p>We offer secure, multi-level parking open 24/7. Valet parking is available at the main entrance. Wheelchair assistance can be requested directly from the parking attendants.</p>
                </div>
            </div>
            
            <div class="card">
                <div class="icon">☕</div>
                <div>
                    <h2>Cafeteria & Dining</h2>
                    <p>The **HMS Cafeteria** on the ground floor offers a wide selection of hot meals, snacks, and beverages (Open 7:00 AM - 10:00 PM). Coffee shops are located in the main lobby and the out-patient consulting area.</p>
                </div>
            </div>
            
            <div class="card">
                <div class="icon">📶</div>
                <div>
                    <h2>Wi-Fi & Connectivity</h2>
                    <p>Complimentary high-speed Wi-Fi is available throughout the hospital. Select the "HMS-Guest" network and accept the terms to connect instantly.</p>
                </div>
            </div>
        </div>
        '''
    },
    'patient-login.html': {
        'title': 'Patient Portal Login',
        'heading': 'Patient Portal Login',
        'subheading': 'Access your medical records, appointments, and test results securely.',
        'custom_css': '''
        .content-container { max-width: 500px; margin: 0 auto 4rem auto; padding: 0 5%; }
        .card { background: rgba(20, 22, 33, 0.6); backdrop-filter: blur(12px); border: 1px solid var(--glass-border); border-radius: 20px; padding: 2.5rem; text-align: center; }
        .card h2 { font-size: 1.5rem; margin-bottom: 1.5rem; color: #efeff1; }
        .form-group { margin-bottom: 1.5rem; text-align: left; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; color: var(--text-muted); }
        .form-control { width: 100%; padding: 0.8rem 1rem; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); color: #fff; font-family: 'Outfit'; }
        .form-control:focus { outline: none; border-color: var(--accent-primary, #6366f1); box-shadow: 0 0 10px rgba(99, 102, 241, 0.2); }
        .btn-submit { background: linear-gradient(135deg, var(--accent-primary, #6366f1), var(--accent-secondary, #0ea5e9)); color: #fff; padding: 0.9rem 2rem; border-radius: 12px; border: none; font-size: 1rem; cursor: pointer; transition: 0.3s; font-weight: 600; width: 100%; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3); margin-top: 1rem; }
        .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5); }
        .forgot-link { display: block; margin-top: 1.5rem; color: var(--accent-secondary, #0ea5e9); font-size: 0.9rem; text-decoration: none; }
        .forgot-link:hover { text-decoration: underline; }
        ''',
        'custom_js': '''
        <script>
            function loginPatient(e) {
                e.preventDefault();
                const btn = e.target.querySelector('button');
                btn.innerHTML = 'Logging in...';
                
                setTimeout(() => {
                    showToast('Login successful. Redirecting to dashboard...', 'success');
                    setTimeout(() => {
                        window.location.href = 'patient-dashboard.html';
                    }, 1000);
                }, 1000);
            }
        </script>
        ''',
        'content': '''
        <div class="content-container">
            <div class="card">
                <h2>Welcome Back</h2>
                <form onsubmit="loginPatient(event)">
                    <div class="form-group">
                        <label>Email Address or MRN</label>
                        <input type="text" class="form-control" required placeholder="Enter your email or MRN">
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" class="form-control" required placeholder="Enter your password">
                    </div>
                    <button type="submit" class="btn-submit">Login</button>
                    <a href="#" class="forgot-link">Forgot your password?</a>
                </form>
            </div>
        </div>
        '''
    },
    'diseases-conditions.html': {
        'title': 'Diseases & Conditions',
        'heading': 'Health Library: Diseases & Conditions',
        'subheading': 'A comprehensive A-Z reference guide to medical conditions, symptoms, and treatments.',
        'custom_css': '''
        .content-container { max-width: 1000px; margin: 0 auto 4rem auto; padding: 0 5%; }
        .search-box { display: flex; gap: 1rem; margin-bottom: 2rem; }
        .form-control { flex: 1; padding: 1rem 1.5rem; border-radius: 100px; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); color: #fff; font-family: 'Outfit'; font-size: 1rem; }
        .disease-list { display: grid; gap: 1rem; }
        .disease-card { background: rgba(20, 22, 33, 0.6); border: 1px solid var(--glass-border); border-radius: 16px; padding: 1.5rem; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: 0.3s; }
        .disease-card:hover { background: rgba(255, 255, 255, 0.05); transform: translateY(-3px); }
        .disease-card h3 { font-size: 1.1rem; color: #efeff1; margin-bottom: 0.3rem; }
        .disease-card p { font-size: 0.9rem; color: var(--text-muted); }
        .alphabet { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 2rem; justify-content: center; }
        .alphabet span { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.05); border-radius: 8px; cursor: pointer; font-weight: 600; transition: 0.3s; }
        .alphabet span:hover { background: var(--accent-primary, #6366f1); }
        ''',
        'custom_js': '''
        <script>
            function filterDiseases() {
                const search = document.getElementById('search').value.toLowerCase();
                const cards = document.querySelectorAll('.disease-card');
                cards.forEach(card => {
                    const title = card.querySelector('h3').innerText.toLowerCase();
                    if (title.includes(search)) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            }
        </script>
        ''',
        'content': '''
        <div class="content-container">
            <div class="alphabet">
                <span>A</span><span>B</span><span>C</span><span>D</span><span>E</span><span>F</span><span>G</span><span>H</span><span>I</span><span>J</span><span>K</span><span>L</span><span>M</span><span>N</span><span>O</span><span>P</span><span>Q</span><span>R</span><span>S</span><span>T</span><span>U</span><span>V</span><span>W</span><span>X</span><span>Y</span><span>Z</span>
            </div>
            <div class="search-box">
                <input type="text" id="search" class="form-control" placeholder="Search for a disease or condition..." onkeyup="filterDiseases()">
            </div>
            
            <div class="disease-list">
                <div class="disease-card">
                    <div>
                        <h3>Arrhythmia (Heart Rhythm Disorders)</h3>
                        <p>Cardiology · Irregular heartbeat conditions</p>
                    </div>
                    <div style="color: var(--accent-primary);">→</div>
                </div>
                <div class="disease-card">
                    <div>
                        <h3>Asthma</h3>
                        <p>Pulmonology · Airways inflammation causing difficulty in breathing</p>
                    </div>
                    <div style="color: var(--accent-primary);">→</div>
                </div>
                <div class="disease-card">
                    <div>
                        <h3>Coronary Artery Disease (CAD)</h3>
                        <p>Cardiology · Plaque buildup in the walls of the arteries</p>
                    </div>
                    <div style="color: var(--accent-primary);">→</div>
                </div>
                <div class="disease-card">
                    <div>
                        <h3>Diabetes (Type 1 & Type 2)</h3>
                        <p>Endocrinology · Conditions that affect how your body uses blood sugar</p>
                    </div>
                    <div style="color: var(--accent-primary);">→</div>
                </div>
                <div class="disease-card">
                    <div>
                        <h3>Epilepsy</h3>
                        <p>Neurology · Central nervous system disorder causing seizures</p>
                    </div>
                    <div style="color: var(--accent-primary);">→</div>
                </div>
                <div class="disease-card">
                    <div>
                        <h3>Osteoarthritis</h3>
                        <p>Orthopedics · Wear-and-tear damage to joint cartilage</p>
                    </div>
                    <div style="color: var(--accent-primary);">→</div>
                </div>
                <div class="disease-card">
                    <div>
                        <h3>Stroke</h3>
                        <p>Neurology · Emergency condition where blood supply to brain is interrupted</p>
                    </div>
                    <div style="color: var(--accent-primary);">→</div>
                </div>
            </div>
        </div>
        '''
    }
}

base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - HMS Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <style>
        .page-header {{ padding: 4rem 5% 2rem 5%; text-align: center; }}
        .page-header h1 {{ font-size: 2.5rem; margin-bottom: 1rem; }}
        .page-header p {{ color: var(--text-muted); max-width: 600px; margin: 0 auto; line-height: 1.6; font-size: 1.1rem; }}
        {custom_css}
    </style>
</head>
<body>
    <div class="background-elements">
        <div class="blob purple-blob"></div>
        <div class="blob blue-blob"></div>
    </div>
    <div class="top-bar">
        <div class="top-bar-content">
            <div class="top-bar-left">
                <span><span style="color:#ef4444;">🚨</span> Emergency: 111-911-911</span>
                <span class="hide-mobile">|</span>
                <span class="hide-mobile">📍 Find a Location</span>
            </div>
            <div class="top-bar-right">
                <a href="patient-login.html">Patient Portal Login</a>
                <a href="dashboard.html" class="staff-login">Staff/Admin Login</a>
            </div>
        </div>
    </div>
    <nav class="glass-nav">
        <div class="logo"><span class="logo-icon">🏥</span> HMS <span>Pro</span></div>
        <div class="nav-links">
            <a href="index.html">Home</a>
            <div class="dropdown">
                <a href="#about" class="dropbtn">About Us ▾</a>
                <div class="dropdown-content">
                    <a href="vision-mission.html">Vision & Mission</a>
                    <a href="leadership.html">Leadership</a>
                    <a href="accreditations.html">Accreditations</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="#services" class="dropbtn active">Patient Services ▾</a>
                <div class="dropdown-content">
                    <a href="find-doctor.html">Find a Doctor</a>
                    <a href="request-appointment.html">Book Appointment</a>
                    <a href="admission-guidelines.html">Admission Guidelines</a>
                    <a href="welfare-support.html">Welfare & Support</a>
                    <a href="billing-insurance.html">Billing & Insurance</a>
                    <a href="international-services.html">International Services</a>
                    <a href="patient-visitor-guide.html">Patient & Visitor Guide</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="#departments" class="dropbtn">Departments ▾</a>
                <div class="dropdown-content">
                    <a href="dept-cardiology.html">Cardiology</a>
                    <a href="dept-neurology.html">Neurology</a>
                    <a href="dept-pediatrics.html">Pediatrics</a>
                    <a href="dept-orthopedics.html">Orthopedics</a>
                </div>
            </div>
            <div class="dropdown">
                <a href="#health" class="dropbtn">Health Library ▾</a>
                <div class="dropdown-content">
                    <a href="diseases-conditions.html">Diseases & Conditions</a>
                    <a href="#">Symptoms Checker</a>
                    <a href="#">Tests & Procedures</a>
                    <a href="#">Drugs & Supplements</a>
                </div>
            </div>
            <a href="clinical-labs.html">Clinical Labs</a>
        </div>
        <button class="btn-primary" onclick="window.location.href='request-appointment.html'">Book Appointment</button>
    </nav>

    <div class="page-header">
        <h1>{heading}</h1>
        <p>{subheading}</p>
    </div>

    {content}

    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="app.js"></script>
    {custom_js}
</body>
</html>
"""

dir_path = r"c:\Users\Star\Desktop\Hospital-management-system"

for filename, data in pages.items():
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        html_code = base_template.format(**data)
        f.write(html_code)
    print(f"Created {filename}")

replacements = {
    '<a href=\"#\">Billing &amp; Insurance</a>': '<a href=\"billing-insurance.html\">Billing &amp; Insurance</a>',
    '<a href=\"#\">International Services</a>': '<a href=\"international-services.html\">International Services</a>',
    '<a href=\"#\">Patient &amp; Visitor Guide</a>': '<a href=\"patient-visitor-guide.html\">Patient &amp; Visitor Guide</a>',
    '<a href=\"#\">Diseases &amp; Conditions</a>': '<a href=\"diseases-conditions.html\">Diseases &amp; Conditions</a>',
    '<a href=\"#\">International Patients</a>': '<a href=\"international-services.html\">International Patients</a>',
    '<a href=\"#\">Billing & Insurance</a>': '<a href=\"billing-insurance.html\">Billing & Insurance</a>',
    '<a href=\"#\">Patient & Visitor Guide</a>': '<a href=\"patient-visitor-guide.html\">Patient & Visitor Guide</a>',
    '<a href=\"#\">Diseases & Conditions</a>': '<a href=\"diseases-conditions.html\">Diseases & Conditions</a>',
    '<a href=\"#\">Patient Portal Login</a>': '<a href=\"patient-login.html\">Patient Portal Login</a>'
}

html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

for file in html_files:
    file_path = os.path.join(dir_path, file)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated links in {file}')


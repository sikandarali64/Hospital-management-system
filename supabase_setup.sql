-- =============================================
-- HMS Pro - Supabase Database Setup Script
-- =============================================
-- Supabase Dashboard > SQL Editor mein yeh poora script paste karein aur "Run" dabayein

-- 1. PATIENTS TABLE
CREATE TABLE IF NOT EXISTS patients (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    dob             DATE NOT NULL,
    gender          TEXT NOT NULL CHECK (gender IN ('male', 'female', 'other')),
    phone           TEXT NOT NULL,
    address         TEXT,
    department      TEXT NOT NULL,
    doctor          TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'waiting' CHECK (status IN ('admitted', 'waiting', 'discharged')),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 2. APPOINTMENTS TABLE
CREATE TABLE IF NOT EXISTS appointments (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_name    TEXT NOT NULL,
    doctor          TEXT NOT NULL,
    department      TEXT NOT NULL DEFAULT 'General',
    date            DATE NOT NULL,
    time            TEXT NOT NULL,
    reason          TEXT,
    status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('confirmed', 'pending', 'cancelled')),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Enable Row Level Security (RLS) - Public read/write for demo
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;

-- Allow all operations for demo (anon key)
DROP POLICY IF EXISTS "Allow all for patients" ON patients;
CREATE POLICY "Allow all for patients"      ON patients      FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for appointments" ON appointments;
CREATE POLICY "Allow all for appointments"  ON appointments  FOR ALL USING (true) WITH CHECK (true);

-- 4. Enable Realtime on both tables
-- Supabase Dashboard > Database > Replication > Tables mein "patients" aur "appointments" enable karein
-- YA yeh command chalayein (Note: Peli baar chalane ke baad isko comment out kar dein warna error aayega)
-- ALTER PUBLICATION supabase_realtime ADD TABLE patients;
-- ALTER PUBLICATION supabase_realtime ADD TABLE appointments;

-- 5. Sample Data (Optional - Test ke liye)
-- (Agar data bar bar insert ho raha ho, toh aap in lines ko comment kar sakte hain)
INSERT INTO patients (first_name, last_name, dob, gender, phone, address, department, doctor, status)
VALUES
    ('Ali', 'Khan',    '1990-05-15', 'male',   '0300-1234567', 'Lahore, Pakistan',   'cardiology',   'Dr. Sarah Smith',   'admitted'),
    ('Fatima', 'Malik','1985-08-22', 'female', '0321-9876543', 'Karachi, Pakistan',  'neurology',    'Dr. Michael Chen',  'waiting'),
    ('Usman', 'Ahmed', '2000-01-10', 'male',   '0333-5555555', 'Islamabad, Pakistan','pediatrics',   'Dr. Emily Davis',   'discharged'),
    ('Sara', 'Baig',   '1978-11-03', 'female', '0311-2223333', 'Rawalpindi, Pakistan','orthopedics', 'Dr. James Wilson',  'admitted');

INSERT INTO appointments (patient_name, doctor, department, date, time, reason, status)
VALUES
    ('Ali Khan',    'Dr. Sarah Smith',  'Cardiology',   CURRENT_DATE, '09:00', 'Routine Checkup',      'confirmed'),
    ('Fatima Malik','Dr. Michael Chen', 'Neurology',    CURRENT_DATE, '10:30', 'Neurology Consultation','pending'),
    ('Usman Ahmed', 'Dr. Emily Davis',  'Pediatrics',   CURRENT_DATE, '11:15', 'Pediatric Vaccination', 'confirmed'),
    ('Sara Baig',   'Dr. James Wilson', 'Orthopedics',  CURRENT_DATE, '14:00', 'Orthopedic Follow-up',  'confirmed');


-- 6. MEDICAL RECORDS TABLE
CREATE TABLE IF NOT EXISTS medical_records (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_id      UUID REFERENCES patients(id) ON DELETE CASCADE,
    date            DATE NOT NULL,
    doctor_name     TEXT NOT NULL,
    diagnosis       TEXT NOT NULL,
    prescription    TEXT,
    notes           TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE medical_records ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow all for medical_records" ON medical_records;
CREATE POLICY "Allow all for medical_records" ON medical_records FOR ALL USING (true) WITH CHECK (true);

-- ALTER PUBLICATION supabase_realtime ADD TABLE medical_records;

-- DONE! Tables ready hain.
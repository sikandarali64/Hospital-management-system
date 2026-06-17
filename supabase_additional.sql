-- =============================================
-- HMS Pro - Additional Tables (Insurance & International)
-- =============================================

-- 7. INSURANCE REQUESTS TABLE
CREATE TABLE IF NOT EXISTS insurance_requests (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_name    TEXT NOT NULL,
    policy_number   TEXT NOT NULL,
    provider        TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'rejected')),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE insurance_requests ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for insurance_requests" ON insurance_requests;
CREATE POLICY "Allow all for insurance_requests" ON insurance_requests FOR ALL USING (true) WITH CHECK (true);
         
-- 8. INTERNATIONAL REQUESTS TABLE
CREATE TABLE IF NOT EXISTS international_requests (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_name    TEXT NOT NULL,
    country         TEXT NOT NULL,
    email           TEXT NOT NULL,
    services        TEXT NOT NULL, -- e.g., "Interpreter, Visa Assistance"
    notes           TEXT,
    status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'contacted', 'resolved')),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE international_requests ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all for international_requests" ON international_requests;
CREATE POLICY "Allow all for international_requests" ON international_requests FOR ALL USING (true) WITH CHECK (true);

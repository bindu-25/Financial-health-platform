-- PostgreSQL Schema for Financial Health Platform

-- Drop tables if exist (for fresh install)
DROP TABLE IF EXISTS recommendations CASCADE;
DROP TABLE IF EXISTS forecasts CASCADE;
DROP TABLE IF EXISTS credit_scores CASCADE;
DROP TABLE IF EXISTS financial_records CASCADE;
DROP TABLE IF EXISTS smes CASCADE;

-- SMEs Table
CREATE TABLE smes (
    id SERIAL PRIMARY KEY,
    business_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    registration_number VARCHAR(100) UNIQUE,
    gst_number VARCHAR(50),
    email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial Records Table
CREATE TABLE financial_records (
    id SERIAL PRIMARY KEY,
    sme_id INTEGER NOT NULL REFERENCES smes(id) ON DELETE CASCADE,
    period VARCHAR(7) NOT NULL,
    
    -- P&L Items
    total_revenue NUMERIC(15,2) DEFAULT 0,
    total_cogs NUMERIC(15,2) DEFAULT 0,
    gross_profit NUMERIC(15,2) DEFAULT 0,
    operating_expenses NUMERIC(15,2) DEFAULT 0,
    ebitda NUMERIC(15,2) DEFAULT 0,
    net_profit NUMERIC(15,2) DEFAULT 0,
    
    -- Margins
    gross_margin NUMERIC(5,2),
    operating_margin NUMERIC(5,2),
    net_profit_margin NUMERIC(5,2),
    
    -- Cash Flow
    cash_inflow NUMERIC(15,2) DEFAULT 0,
    cash_outflow NUMERIC(15,2) DEFAULT 0,
    net_cash_flow NUMERIC(15,2) DEFAULT 0,
    ending_cash_balance NUMERIC(15,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(sme_id, period)
);

-- Credit Scores Table
CREATE TABLE credit_scores (
    id SERIAL PRIMARY KEY,
    sme_id INTEGER NOT NULL REFERENCES smes(id) ON DELETE CASCADE,
    period VARCHAR(7) NOT NULL,
    
    credit_score NUMERIC(5,2) NOT NULL,
    credit_rating VARCHAR(5),
    
    -- Component Scores
    profitability_score NUMERIC(5,2),
    liquidity_score NUMERIC(5,2),
    leverage_score NUMERIC(5,2),
    efficiency_score NUMERIC(5,2),
    growth_score NUMERIC(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(sme_id, period)
);

-- Forecasts Table
CREATE TABLE forecasts (
    id SERIAL PRIMARY KEY,
    sme_id INTEGER NOT NULL REFERENCES smes(id) ON DELETE CASCADE,
    forecast_period VARCHAR(7) NOT NULL,
    
    forecast_revenue NUMERIC(15,2),
    lower_bound NUMERIC(15,2),
    upper_bound NUMERIC(15,2),
    forecast_method VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(sme_id, forecast_period)
);

-- Recommendations Table
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    sme_id INTEGER NOT NULL REFERENCES smes(id) ON DELETE CASCADE,
    
    category VARCHAR(50),
    recommendation_text TEXT,
    priority VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_financial_records_sme_id ON financial_records(sme_id);
CREATE INDEX idx_financial_records_period ON financial_records(period);
CREATE INDEX idx_credit_scores_sme_id ON credit_scores(sme_id);
CREATE INDEX idx_forecasts_sme_id ON forecasts(sme_id);
CREATE INDEX idx_recommendations_sme_id ON recommendations(sme_id);

-- Sample data (optional)
INSERT INTO smes (business_name, industry, registration_number, gst_number, email, phone)
VALUES ('Demo Electronics Retail', 'Retail Electronics', 'REG001', 'GST001', 'demo@example.com', '+91-9999999999');

COMMENT ON TABLE smes IS 'Small and Medium Enterprises master data';
COMMENT ON TABLE financial_records IS 'Monthly financial statements';
COMMENT ON TABLE credit_scores IS 'Credit scoring history';
COMMENT ON TABLE forecasts IS 'Revenue forecasts';
COMMENT ON TABLE recommendations IS 'AI-generated recommendations';
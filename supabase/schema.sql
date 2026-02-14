-- Weddingfinder Venues Schema
-- Supabase URL: https://gqlprwursgbgkfkwzkyb.supabase.co

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Venues Table
CREATE TABLE IF NOT EXISTS venues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    city TEXT,
    region TEXT,
    price_min INTEGER,
    price_max INTEGER,
    capacity_min INTEGER,
    capacity_max INTEGER,
    description TEXT,
    style_tags TEXT[] DEFAULT '{}',
    amenities TEXT[] DEFAULT '{}',
    image_urls TEXT[] DEFAULT '{}',
    website_url TEXT,
    phone TEXT,
    email TEXT,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_venues_city ON venues(city);
CREATE INDEX IF NOT EXISTS idx_venues_region ON venues(region);
CREATE INDEX IF NOT EXISTS idx_venues_price_min ON venues(price_min);
CREATE INDEX IF NOT EXISTS idx_venues_price_max ON venues(price_max);
CREATE INDEX IF NOT EXISTS idx_venues_capacity_min ON venues(capacity_min);
CREATE INDEX IF NOT EXISTS idx_venues_capacity_max ON venues(capacity_max);
CREATE INDEX IF NOT EXISTS idx_venues_is_premium ON venues(is_premium);
CREATE INDEX IF NOT EXISTS idx_venues_style_tags ON venues USING GIN(style_tags);
CREATE INDEX IF NOT EXISTS idx_venues_amenities ON venues USING GIN(amenities);

-- Full-text search index on name and description
CREATE INDEX IF NOT EXISTS idx_venues_search ON venues 
    USING gin(to_tsvector('dutch', name || ' ' || COALESCE(description, '')));

-- Trigger for auto-updating updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_venues_updated_at
    BEFORE UPDATE ON venues
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- RLS POLICIES
-- ============================================

-- Enable RLS on venues table
ALTER TABLE venues ENABLE ROW LEVEL SECURITY;

-- Policy: Public read access (anyone can read venues)
CREATE POLICY "Allow public read access"
    ON venues
    FOR SELECT
    USING (true);

-- Policy: Admin write access (only authenticated admins can write)
CREATE POLICY "Allow admin insert access"
    ON venues
    FOR INSERT
    WITH CHECK (
        auth.role() = 'authenticated' AND
        (auth.jwt() ->> 'role') = 'admin'
    );

CREATE POLICY "Allow admin update access"
    ON venues
    FOR UPDATE
    USING (
        auth.role() = 'authenticated' AND
        (auth.jwt() ->> 'role') = 'admin'
    )
    WITH CHECK (
        auth.role() = 'authenticated' AND
        (auth.jwt() ->> 'role') = 'admin'
    );

CREATE POLICY "Allow admin delete access"
    ON venues
    FOR DELETE
    USING (
        auth.role() = 'authenticated' AND
        (auth.jwt() ->> 'role') = 'admin'
    );

-- ============================================
-- HELPER FUNCTIONS
-- ============================================

-- Function to generate slug from name
CREATE OR REPLACE FUNCTION generate_slug(name TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN lower(
        regexp_replace(
            regexp_replace(name, '[^a-zA-Z0-9\s]', '', 'g'),
            '\s+', '-', 'g'
        )
    );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to search venues by text
CREATE OR REPLACE FUNCTION search_venues(search_query TEXT)
RETURNS SETOF venues AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM venues
    WHERE to_tsvector('dutch', name || ' ' || COALESCE(description, '')) 
          @@ plainto_tsquery('dutch', search_query)
    ORDER BY ts_rank(
        to_tsvector('dutch', name || ' ' || COALESCE(description, '')),
        plainto_tsquery('dutch', search_query)
    ) DESC;
END;
$$ LANGUAGE plpgsql STABLE;

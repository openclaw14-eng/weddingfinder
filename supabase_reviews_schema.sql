-- ============================================================================
-- Weddingfinder App - Vendor Reviews Schema
-- ============================================================================
-- This schema creates a reviews table for wedding venues with proper
-- indexing and Row Level Security policies for the Supabase backend.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. CREATE TABLE
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.reviews (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id        UUID NOT NULL,
    user_id         UUID NOT NULL,
    rating          INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text     TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    verified        BOOLEAN DEFAULT FALSE,
    
    -- Foreign key constraints (adjust references based on your actual schema)
    CONSTRAINT fk_venue 
        FOREIGN KEY (venue_id) 
        REFERENCES public.venues(id) 
        ON DELETE CASCADE,
    
    CONSTRAINT fk_user 
        FOREIGN KEY (user_id) 
        REFERENCES auth.users(id) 
        ON DELETE CASCADE
);

-- Add table comment for documentation
COMMENT ON TABLE public.reviews IS 'User reviews and ratings for wedding venues';

-- ----------------------------------------------------------------------------
-- 2. CREATE INDEXES FOR EFFICIENT QUERYING
-- ----------------------------------------------------------------------------

-- Index for fetching reviews by venue (most common query pattern)
CREATE INDEX IF NOT EXISTS idx_reviews_venue_id 
    ON public.reviews(venue_id);

-- Index for fetching reviews by user
CREATE INDEX IF NOT EXISTS idx_reviews_user_id 
    ON public.reviews(user_id);

-- Composite index for venue reviews sorted by date (recent first)
CREATE INDEX IF NOT EXISTS idx_reviews_venue_created 
    ON public.reviews(venue_id, created_at DESC);

-- Index for filtering verified reviews
CREATE INDEX IF NOT EXISTS idx_reviews_verified 
    ON public.reviews(verified) 
    WHERE verified = TRUE;

-- Index for rating-based queries (e.g., "show 5-star reviews")
CREATE INDEX IF NOT EXISTS idx_reviews_rating 
    ON public.reviews(rating);

-- GIN index for full-text search on review text (if needed)
CREATE INDEX IF NOT EXISTS idx_reviews_text_search 
    ON public.reviews USING gin(to_tsvector('english', review_text));

-- ----------------------------------------------------------------------------
-- 3. ENABLE ROW LEVEL SECURITY
-- ----------------------------------------------------------------------------

ALTER TABLE public.reviews ENABLE ROW LEVEL SECURITY;

-- ----------------------------------------------------------------------------
-- 4. RLS POLICIES
-- ----------------------------------------------------------------------------

-- Policy: Allow anyone to read reviews (public read access)
CREATE POLICY "Reviews are viewable by everyone"
    ON public.reviews
    FOR SELECT
    USING (true);

-- Policy: Allow authenticated users to insert their own reviews
CREATE POLICY "Users can create their own reviews"
    ON public.reviews
    FOR INSERT
    WITH CHECK (
        auth.uid() = user_id
    );

-- Policy: Allow users to update only their own reviews
CREATE POLICY "Users can update their own reviews"
    ON public.reviews
    FOR UPDATE
    USING (
        auth.uid() = user_id
    )
    WITH CHECK (
        auth.uid() = user_id
    );

-- Policy: Allow users to delete only their own reviews
CREATE POLICY "Users can delete their own reviews"
    ON public.reviews
    FOR DELETE
    USING (
        auth.uid() = user_id
    );

-- Policy: Allow admins to manage all reviews (optional - requires admin check)
-- Uncomment if you have an admins table or role-based access
-- CREATE POLICY "Admins can manage all reviews"
--     ON public.reviews
--     FOR ALL
--     USING (
--         EXISTS (
--             SELECT 1 FROM public.admins 
--             WHERE admins.user_id = auth.uid()
--         )
--     );

-- ----------------------------------------------------------------------------
-- 5. TRIGGERS (Optional but recommended)
-- ----------------------------------------------------------------------------

-- Trigger to auto-update a venue's average rating when a review is added/modified
-- This requires a venues table with an avg_rating column

-- Function to update venue average rating
CREATE OR REPLACE FUNCTION update_venue_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE public.venues
    SET avg_rating = (
        SELECT ROUND(AVG(rating)::numeric, 2)
        FROM public.reviews
        WHERE venue_id = COALESCE(NEW.venue_id, OLD.venue_id)
    ),
    review_count = (
        SELECT COUNT(*)
        FROM public.reviews
        WHERE venue_id = COALESCE(NEW.venue_id, OLD.venue_id)
    )
    WHERE id = COALESCE(NEW.venue_id, OLD.venue_id);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for insert/update/delete on reviews
DROP TRIGGER IF EXISTS trg_update_venue_rating ON public.reviews;
CREATE TRIGGER trg_update_venue_rating
    AFTER INSERT OR UPDATE OR DELETE ON public.reviews
    FOR EACH ROW
    EXECUTE FUNCTION update_venue_rating();

-- ----------------------------------------------------------------------------
-- 6. USEFUL VIEWS
-- ----------------------------------------------------------------------------

-- View: Venue rating summary
CREATE OR REPLACE VIEW public.venue_rating_summary AS
SELECT 
    venue_id,
    COUNT(*) as total_reviews,
    AVG(rating)::numeric(3,2) as average_rating,
    COUNT(*) FILTER (WHERE rating = 5) as five_star_count,
    COUNT(*) FILTER (WHERE rating = 4) as four_star_count,
    COUNT(*) FILTER (WHERE rating = 3) as three_star_count,
    COUNT(*) FILTER (WHERE rating = 2) as two_star_count,
    COUNT(*) FILTER (WHERE rating = 1) as one_star_count,
    COUNT(*) FILTER (WHERE verified = TRUE) as verified_reviews_count
FROM public.reviews
GROUP BY venue_id;

-- ----------------------------------------------------------------------------
-- 7. USAGE EXAMPLES
-- ----------------------------------------------------------------------------
/*
-- Insert a new review
INSERT INTO public.reviews (venue_id, user_id, rating, review_text)
VALUES (
    'uuid-of-venue',
    auth.uid(),
    5,
    'Amazing venue! Perfect for our wedding.'
);

-- Get all reviews for a venue (most recent first)
SELECT * FROM public.reviews 
WHERE venue_id = 'uuid-of-venue'
ORDER BY created_at DESC;

-- Get average rating for a venue
SELECT AVG(rating) FROM public.reviews 
WHERE venue_id = 'uuid-of-venue';

-- Get verified reviews only
SELECT * FROM public.reviews 
WHERE venue_id = 'uuid-of-venue' AND verified = TRUE;

-- Get venue rating summary
SELECT * FROM public.venue_rating_summary 
WHERE venue_id = 'uuid-of-venue';
*/

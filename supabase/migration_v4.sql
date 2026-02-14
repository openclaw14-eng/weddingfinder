-- Migration V4: Full Production Schema
-- 1. Create a proper auth-linked favorites table if not exists
CREATE TABLE IF NOT EXISTS public.user_favorites (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_session_id TEXT NOT NULL, -- To support guest faves first
    vendor_id UUID REFERENCES public.vendors(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(user_session_id, vendor_id)
);

-- 2. Add structural columns for high-end filtering
ALTER TABLE public.vendors ADD COLUMN IF NOT EXISTS capacity_min INTEGER DEFAULT 0;
ALTER TABLE public.vendors ADD COLUMN IF NOT EXISTS capacity_max INTEGER DEFAULT 250;
ALTER TABLE public.vendors ADD COLUMN IF NOT EXISTS price_indicator TEXT; -- €, €€, €€€, €€€€
ALTER TABLE public.vendors ADD COLUMN IF NOT EXISTS category_type TEXT DEFAULT 'venue'; -- venue, photo, music
ALTER TABLE public.vendors ADD COLUMN IF NOT EXISTS vibe_tags TEXT[]; -- ['classic', 'industrial', 'modern']
ALTER TABLE public.vendors ADD COLUMN IF NOT EXISTS amenities TEXT[]; -- ['overnight', 'catering', 'parking']

-- 3. Enable RLS
ALTER TABLE public.user_favorites ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow anonymous favorites" ON public.user_favorites 
FOR ALL USING (true) WITH CHECK (true);

-- 4. Sample update for the new filter engine
UPDATE public.vendors SET capacity_max = 300, price_indicator = '€€€', category_type = 'venue' WHERE capacity_max IS NULL;

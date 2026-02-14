-- Create favorites table
CREATE TABLE IF NOT EXISTS public.favorites (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID DEFAULT auth.uid(), -- Placeholder for future auth
    vendor_id UUID REFERENCES public.vendors(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(user_id, vendor_id) -- Prevent double favoriting for same user
);

-- Enable RLS
ALTER TABLE public.favorites ENABLE ROW LEVEL SECURITY;

-- Allow public read/write for now (Prototype stage)
CREATE POLICY "Public access to favorites" ON public.favorites 
FOR ALL USING (true) WITH CHECK (true);

-- Add 'vibe' and 'usp' columns to vendors if they don't exist
ALTER TABLE public.vendors ADD COLUMN IF NOT EXISTS vibes text[];
ALTER TABLE public.vendors ADD COLUMN IF NOT EXISTS usps text[];
ALTER TABLE public.vendors ADD COLUMN IF NOT EXISTS rating numeric(2,1) DEFAULT 4.8;

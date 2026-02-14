-- Weddingfinder Venues Seed Data
-- 5 test venues for development

INSERT INTO venues (
    name,
    slug,
    city,
    region,
    price_min,
    price_max,
    capacity_min,
    capacity_max,
    description,
    style_tags,
    amenities,
    image_urls,
    website_url,
    phone,
    email,
    is_premium
) VALUES 
-- Venue 1: Kasteel de Hooge Vuursche
(
    'Kasteel de Hooge Vuursche',
    'kasteel-de-hooge-vuursche',
    'Baarn',
    'Utrecht',
    8500,
    15000,
    50,
    200,
    'Een sprookjesachtig kasteel gelegen in een prachtig bosrijke omgeving. Perfect voor een romantische bruiloft met een klassieke uitstraling. Het kasteel biedt diverse zalen en een prachtige tuin voor buitenfeesten.',
    ARRAY['klassiek', 'romantisch', 'kasteel', 'landelijk', 'elegant'],
    ARRAY['parking', 'wifi', 'terras', 'tuin', 'kleedkamers', 'airco', 'eigen catering'],
    ARRAY[
        'https://images.unsplash.com/photo-1519225421980-5cb7e4c912f2?w=800',
        'https://images.unsplash.com/photo-1519741497674-611481863552?w=800'
    ],
    'https://www.kasteeldehoogevuursche.nl',
    '+31 35 542 1234',
    'info@kasteeldehoogevuursche.nl',
    true
),

-- Venue 2: The Loft Amsterdam
(
    'The Loft Amsterdam',
    'the-loft-amsterdam',
    'Amsterdam',
    'Noord-Holland',
    4500,
    8000,
    30,
    120,
    'Een industriële urban loft in hartje Amsterdam met een moderne, minimalistische uitstraling. Grote ramen zorgen voor fantastisch daglicht. Ideaal voor stedelijke bruiloften met een trendy karakter.',
    ARRAY['modern', 'industrieel', 'urban', 'minimalistisch', 'stedelijk'],
    ARRAY['wifi', 'parking', 'rolstoeltoegankelijk', 'eigen drank', 'dj booth'],
    ARRAY[
        'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?w=800',
        'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=800'
    ],
    'https://www.theloftamsterdam.nl',
    '+31 20 123 4567',
    'info@theloftamsterdam.nl',
    false
),

-- Venue 3: Landgoed Groenendaal
(
    'Landgoed Groenendaal',
    'landgoed-groenendaal',
    'Heemstede',
    'Noord-Holland',
    6000,
    12000,
    40,
    180,
    'Een charmant landgoed met een prachtige orangerie en uitgestrekte tuinen. De perfecte locatie voor een romantische buitenbruiloft met een landelijke en natuurlijke sfeer.',
    ARRAY['landelijk', 'romantisch', 'natuurlijk', 'buiten', 'tuin'],
    ARRAY['parking', 'wifi', 'terras', 'tuin', 'tent mogelijk', 'kleedkamers', 'kindvriendelijk'],
    ARRAY[
        'https://images.unsplash.com/photo-1510076857177-4ba7a50f6103?w=800',
        'https://images.unsplash.com/photo-1460978812857-470ed1c77af0?w=800'
    ],
    'https://www.landgoedgroenendaal.nl',
    '+31 23 512 3456',
    'info@landgoedgroenendaal.nl',
    true
),

-- Venue 4: Beachclub Zandvoort
(
    'Beachclub Zandvoort',
    'beachclub-zandvoort',
    'Zandvoort',
    'Noord-Holland',
    3500,
    7000,
    25,
    150,
    'Een relaxed beachclub aan het strand van Zandvoort. Ideaal voor een informele, zomerse bruiloft met je voeten in het zand. Prachtige zonsondergangen en een laid-back sfeer.',
    ARRAY['strand', 'informeel', 'zomer', 'relaxed', 'buiten'],
    ARRAY['parking', 'wifi', 'terras', 'strand', 'bbq mogelijk', 'eigen drank'],
    ARRAY[
        'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800',
        'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800'
    ],
    'https://www.beachclubzandvoort.nl',
    '+31 23 571 2345',
    'info@beachclubzandvoort.nl',
    false
),

-- Venue 5: De Fabrique Utrecht
(
    'De Fabrique Utrecht',
    'de-fabrique-utrecht',
    'Utrecht',
    'Utrecht',
    5500,
    11000,
    50,
    300,
    'Een voormalige fabriekshal omgetoverd tot een industriële evenementenlocatie. Ruime, flexibele zalen met een rauwe, authentieke uitstraling. Perfect voor grotere bruiloften met een urban industrieel thema.',
    ARRAY['industrieel', 'urban', 'modern', 'ruim', 'flexibel'],
    ARRAY['parking', 'wifi', 'rolstoeltoegankelijk', 'eigen catering', 'eigen drank', 'geluidssysteem', 'lichtinstallatie'],
    ARRAY[
        'https://images.unsplash.com/photo-1510074377623-8cf13fb86c08?w=800',
        'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=800'
    ],
    'https://www.defabrique.nl',
    '+31 30 234 5678',
    'info@defabrique.nl',
    true
);

-- Update sequences if needed
SELECT setval('venues_id_seq', (SELECT MAX(id) FROM venues));

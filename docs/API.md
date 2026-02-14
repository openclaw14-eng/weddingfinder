# Weddingfinder API Documentation

## Supabase Configuration

- **URL**: `https://gqlprwursgbgkfkwzkyb.supabase.co`
- **Client Library**: `lib/supabase.js`

## Database Schema

### Table: `venues`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `name` | TEXT | UNIQUE, NOT NULL | Venue name |
| `slug` | TEXT | UNIQUE, NOT NULL | URL-friendly identifier |
| `city` | TEXT | | City name |
| `region` | TEXT | | Province/region |
| `price_min` | INTEGER | | Minimum price (EUR) |
| `price_max` | INTEGER | | Maximum price (EUR) |
| `capacity_min` | INTEGER | | Minimum guest capacity |
| `capacity_max` | INTEGER | | Maximum guest capacity |
| `description` | TEXT | | Full venue description |
| `style_tags` | TEXT[] | DEFAULT '{}' | Style categories (e.g., 'modern', 'romantisch') |
| `amenities` | TEXT[] | DEFAULT '{}' | Available amenities |
| `image_urls` | TEXT[] | DEFAULT '{}' | Array of image URLs |
| `website_url` | TEXT | | Official website |
| `phone` | TEXT | | Contact phone |
| `email` | TEXT | | Contact email |
| `is_premium` | BOOLEAN | DEFAULT FALSE | Premium listing flag |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMPTZ | DEFAULT NOW() | Last update timestamp |

## RLS Policies

| Operation | Policy | Access |
|-----------|--------|--------|
| SELECT | `Allow public read access` | ✅ Everyone |
| INSERT | `Allow admin insert access` | 🔒 Admin only |
| UPDATE | `Allow admin update access` | 🔒 Admin only |
| DELETE | `Allow admin delete access` | 🔒 Admin only |

## JavaScript API

### Public Queries (No Auth Required)

```javascript
import { 
  getVenues, 
  getVenueById, 
  getVenueBySlug, 
  searchVenues,
  getCities,
  getRegions,
  getStyleTags,
  getAmenities 
} from './lib/supabase.js';

// Get all venues
const { data, error } = await getVenues();

// Get venues with filters
const { data } = await getVenues({
  city: 'Amsterdam',
  price_max: 10000,
  style_tags: ['modern'],
}, { limit: 20 });

// Get single venue
const { data: venue } = await getVenueBySlug('kasteel-de-hooge-vuursche');

// Full-text search
const { data: results } = await searchVenues('kasteel romantisch');

// Get filter options
const { data: cities } = await getCities();
const { data: regions } = await getRegions();
const { data: styles } = await getStyleTags();
const { data: amenities } = await getAmenities();
```

### Admin Operations (Requires Admin JWT)

```javascript
import { 
  createVenue, 
  updateVenue, 
  deleteVenue,
  createVenueAsAdmin 
} from './lib/supabase.js';

// Create venue
const { data, error } = await createVenue({
  name: 'My New Venue',
  city: 'Rotterdam',
  price_min: 5000,
  style_tags: ['industrieel', 'modern'],
});

// Update venue
await updateVenue('uuid-hier', { 
  price_max: 15000,
  is_premium: true 
});

// Delete venue
await deleteVenue('uuid-hier');

// Server-side admin (with service key)
await createVenueAsAdmin({ ...venueData });
```

## Filter Options

### Available Filters

| Filter | Type | Example |
|--------|------|---------|
| `city` | string | `'Amsterdam'` |
| `region` | string | `'Noord-Holland'` |
| `price_min` | number | `5000` |
| `price_max` | number | `15000` |
| `capacity_min` | number | `50` |
| `capacity_max` | number | `200` |
| `style_tags` | string[] | `['modern', 'romantisch']` |
| `amenities` | string[] | `['parking', 'wifi']` |
| `is_premium` | boolean | `true` |
| `search` | string | `'kasteel tuin'` |

### Query Options

| Option | Default | Description |
|--------|---------|-------------|
| `limit` | 50 | Max results per page |
| `offset` | 0 | Pagination offset |
| `orderBy` | 'created_at' | Sort column |
| `ascending` | false | Sort direction |

## SQL Setup

```bash
# Run schema
psql $SUPABASE_URL -f supabase/schema.sql

# Seed test data
psql $SUPABASE_URL -f supabase/seed.sql
```

## Database Functions

### `search_venues(search_query TEXT)`
Full-text Dutch search on name and description.

```sql
SELECT * FROM search_venues('kasteel romantisch');
```

### `generate_slug(name TEXT)`
Auto-generate URL slug from name.

```sql
SELECT generate_slug('My Wedding Venue'); -- Returns 'my-wedding-venue'
```

## Environment Variables

```bash
# Client-side (public)
NEXT_PUBLIC_SUPABASE_URL=https://gqlprwursgbgkfkwzkyb.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Server-side (private)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## Error Handling

```javascript
const { data, error } = await getVenues();

if (error) {
  console.error('Supabase error:', error.message);
  // Handle error
}
```

## Indexes

- `idx_venues_city` - City filtering
- `idx_venues_region` - Region filtering
- `idx_venues_price_min/max` - Price range queries
- `idx_venues_capacity_min/max` - Capacity queries
- `idx_venues_is_premium` - Premium filtering
- `idx_venues_style_tags` - GIN index for array contains
- `idx_venues_amenities` - GIN index for array contains
- `idx_venues_search` - Full-text search

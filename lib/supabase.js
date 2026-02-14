import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://gqlprwursgbgkfkwzkyb.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

// Types for Weddingfinder venues

/**
 * @typedef {Object} Venue
 * @property {string} id - UUID
 * @property {string} name - Venue name
 * @property {string} slug - URL-friendly slug
 * @property {string|null} city - City name
 * @property {string|null} region - Region/province
 * @property {number|null} price_min - Minimum price
 * @property {number|null} price_max - Maximum price
 * @property {number|null} capacity_min - Minimum capacity
 * @property {number|null} capacity_max - Maximum capacity
 * @property {string|null} description - Venue description
 * @property {string[]} style_tags - Style tags (e.g., 'modern', 'romantisch')
 * @property {string[]} amenities - Available amenities
 * @property {string[]} image_urls - Array of image URLs
 * @property {string|null} website_url - Website URL
 * @property {string|null} phone - Phone number
 * @property {string|null} email - Contact email
 * @property {boolean} is_premium - Premium listing status
 * @property {string} created_at - ISO timestamp
 * @property {string} updated_at - ISO timestamp
 */

/**
 * @typedef {Object} VenueFilters
 * @property {string} [city] - Filter by city
 * @property {string} [region] - Filter by region
 * @property {number} [price_min] - Minimum price filter
 * @property {number} [price_max] - Maximum price filter
 * @property {number} [capacity_min] - Minimum capacity filter
 * @property {number} [capacity_max] - Maximum capacity filter
 * @property {string[]} [style_tags] - Filter by style tags
 * @property {string[]} [amenities] - Filter by amenities
 * @property {boolean} [is_premium] - Filter by premium status
 * @property {string} [search] - Text search query
 */

/**
 * @typedef {Object} VenueCreate
 * @property {string} name - Required: Venue name
 * @property {string} [slug] - Optional: will be auto-generated from name
 * @property {string} [city]
 * @property {string} [region]
 * @property {number} [price_min]
 * @property {number} [price_max]
 * @property {number} [capacity_min]
 * @property {number} [capacity_max]
 * @property {string} [description]
 * @property {string[]} [style_tags]
 * @property {string[]} [amenities]
 * @property {string[]} [image_urls]
 * @property {string} [website_url]
 * @property {string} [phone]
 * @property {string} [email]
 * @property {boolean} [is_premium]
 */

/**
 * @typedef {Object} VenueUpdate
 * @property {string} [name]
 * @property {string} [slug]
 * @property {string} [city]
 * @property {string} [region]
 * @property {number} [price_min]
 * @property {number} [price_max]
 * @property {number} [capacity_min]
 * @property {number} [capacity_max]
 * @property {string} [description]
 * @property {string[]} [style_tags]
 * @property {string[]} [amenities]
 * @property {string[]} [image_urls]
 * @property {string} [website_url]
 * @property {string} [phone]
 * @property {string} [email]
 * @property {boolean} [is_premium]
 */

// Create Supabase clients

/** @type {import('@supabase/supabase-js').SupabaseClient} */
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  },
});

/** Admin client with service role (server-side only) */
/** @type {import('@supabase/supabase-js').SupabaseClient|null} */
export const supabaseAdmin = supabaseServiceKey 
  ? createClient(supabaseUrl, supabaseServiceKey)
  : null;

// ============================================
// VENUE QUERIES
// ============================================

/**
 * Get all venues with optional filters
 * @param {VenueFilters} filters
 * @param {Object} options
 * @param {number} [options.limit=50]
 * @param {number} [options.offset=0]
 * @param {string} [options.orderBy='created_at']
 * @param {boolean} [options.ascending=false]
 * @returns {Promise<{data: Venue[]|null, error: Error|null}>}
 */
export async function getVenues(filters = {}, options = {}) {
  const {
    limit = 50,
    offset = 0,
    orderBy = 'created_at',
    ascending = false,
  } = options;

  let query = supabase
    .from('venues')
    .select('*');

  // Apply filters
  if (filters.city) {
    query = query.eq('city', filters.city);
  }
  if (filters.region) {
    query = query.eq('region', filters.region);
  }
  if (filters.price_min !== undefined) {
    query = query.gte('price_min', filters.price_min);
  }
  if (filters.price_max !== undefined) {
    query = query.lte('price_max', filters.price_max);
  }
  if (filters.capacity_min !== undefined) {
    query = query.gte('capacity_min', filters.capacity_min);
  }
  if (filters.capacity_max !== undefined) {
    query = query.lte('capacity_max', filters.capacity_max);
  }
  if (filters.is_premium !== undefined) {
    query = query.eq('is_premium', filters.is_premium);
  }
  if (filters.style_tags?.length > 0) {
    query = query.contains('style_tags', filters.style_tags);
  }
  if (filters.amenities?.length > 0) {
    query = query.contains('amenities', filters.amenities);
  }

  // Text search
  if (filters.search) {
    query = query.or(`name.ilike.%${filters.search}%,description.ilike.%${filters.search}%`);
  }

  // Apply pagination and ordering
  query = query
    .order(orderBy, { ascending })
    .range(offset, offset + limit - 1);

  return await query;
}

/**
 * Get a single venue by ID
 * @param {string} id
 * @returns {Promise<{data: Venue|null, error: Error|null}>}
 */
export async function getVenueById(id) {
  return await supabase
    .from('venues')
    .select('*')
    .eq('id', id)
    .single();
}

/**
 * Get a single venue by slug
 * @param {string} slug
 * @returns {Promise<{data: Venue|null, error: Error|null}>}
 */
export async function getVenueBySlug(slug) {
  return await supabase
    .from('venues')
    .select('*')
    .eq('slug', slug)
    .single();
}

/**
 * Search venues using full-text search
 * @param {string} searchQuery
 * @returns {Promise<{data: Venue[]|null, error: Error|null}>}
 */
export async function searchVenues(searchQuery) {
  return await supabase
    .rpc('search_venues', { search_query: searchQuery });
}

/**
 * Get all unique cities
 * @returns {Promise<{data: string[]|null, error: Error|null}>}
 */
export async function getCities() {
  const { data, error } = await supabase
    .from('venues')
    .select('city')
    .not('city', 'is', null);
  
  if (error) return { data: null, error };
  
  const cities = [...new Set(data.map(v => v.city))].sort();
  return { data: cities, error: null };
}

/**
 * Get all unique regions
 * @returns {Promise<{data: string[]|null, error: Error|null}>}
 */
export async function getRegions() {
  const { data, error } = await supabase
    .from('venues')
    .select('region')
    .not('region', 'is', null);
  
  if (error) return { data: null, error };
  
  const regions = [...new Set(data.map(v => v.region))].sort();
  return { data: regions, error: null };
}

/**
 * Get all unique style tags
 * @returns {Promise<{data: string[]|null, error: Error|null}>}
 */
export async function getStyleTags() {
  const { data, error } = await supabase
    .from('venues')
    .select('style_tags');
  
  if (error) return { data: null, error };
  
  const allTags = data.flatMap(v => v.style_tags || []);
  const uniqueTags = [...new Set(allTags)].sort();
  return { data: uniqueTags, error: null };
}

/**
 * Get all unique amenities
 * @returns {Promise<{data: string[]|null, error: Error|null}>}
 */
export async function getAmenities() {
  const { data, error } = await supabase
    .from('venues')
    .select('amenities');
  
  if (error) return { data: null, error };
  
  const allAmenities = data.flatMap(v => v.amenities || []);
  const uniqueAmenities = [...new Set(allAmenities)].sort();
  return { data: uniqueAmenities, error: null };
}

// ============================================
// ADMIN OPERATIONS (require admin auth)
// ============================================

/**
 * Create a new venue (admin only)
 * @param {VenueCreate} venueData
 * @returns {Promise<{data: Venue|null, error: Error|null}>}
 */
export async function createVenue(venueData) {
  // Auto-generate slug if not provided
  if (!venueData.slug && venueData.name) {
    venueData.slug = venueData.name
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .replace(/\s+/g, '-');
  }

  return await supabase
    .from('venues')
    .insert(venueData)
    .select()
    .single();
}

/**
 * Update a venue (admin only)
 * @param {string} id
 * @param {VenueUpdate} venueData
 * @returns {Promise<{data: Venue|null, error: Error|null}>}
 */
export async function updateVenue(id, venueData) {
  return await supabase
    .from('venues')
    .update(venueData)
    .eq('id', id)
    .select()
    .single();
}

/**
 * Delete a venue (admin only)
 * @param {string} id
 * @returns {Promise<{data: null, error: Error|null}>}
 */
export async function deleteVenue(id) {
  return await supabase
    .from('venues')
    .delete()
    .eq('id', id);
}

/**
 * Create venue using admin service role (server-side only)
 * @param {VenueCreate} venueData
 * @returns {Promise<{data: Venue|null, error: Error|null}>}
 */
export async function createVenueAsAdmin(venueData) {
  if (!supabaseAdmin) {
    return { data: null, error: new Error('Admin client not configured') };
  }

  if (!venueData.slug && venueData.name) {
    venueData.slug = venueData.name
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .replace(/\s+/g, '-');
  }

  return await supabaseAdmin
    .from('venues')
    .insert(venueData)
    .select()
    .single();
}

// Wedding Venue Types and Mock Data

const WEDDING_TYPES = {
  HISTORIC: 'Historic',
  MODERN: 'Modern',
  RUSTIC: 'Rustic',
  LUXURY: 'Luxury',
  NATURE: 'Nature',
  URBAN: 'Urban',
  BEACH: 'Beach',
  CASTLE: 'Castle'
};

const VENUE_CAPACITY = {
  INTIMATE: { min: 10, max: 50, label: 'Intiem (10-50)' },
  MEDIUM: { min: 50, max: 100, label: 'Middel (50-100)' },
  LARGE: { min: 100, max: 200, label: 'Groot (100-200)' },
  GRAND: { min: 200, max: 500, label: 'Groots (200+)' }
};

const MOCK_VENUES = [
  {
    id: 1,
    name: 'Kasteel de Haar',
    location: 'Utrecht',
    type: 'Castle',
    capacity: { min: 50, max: 200 },
    priceRange: { min: 5000, max: 15000 },
    rating: 4.8,
    reviews: 127,
    image: 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800',
    description: 'Een betoverend kasteel met sprookjesachtige tuinen, perfect voor een klassieke bruiloft.',
    amenities: ['Tuin', 'Parkeergelegenheid', 'Catering', 'Bruidsuite'],
    featured: true
  },
  {
    id: 2,
    name: 'Trouwlocatie De Vrede',
    location: 'Amsterdam',
    type: 'Historic',
    capacity: { min: 30, max: 120 },
    priceRange: { min: 3500, max: 8000 },
    rating: 4.6,
    reviews: 89,
    image: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800',
    description: 'Een historisch pand in hartje Amsterdam met authentieke details en moderne faciliteiten.',
    amenities: ['Stadscentrum', 'Catering', 'DJ mogelijk', 'Terras'],
    featured: true
  },
  {
    id: 3,
    name: 'Beachclub Zonsondergang',
    location: 'Scheveningen',
    type: 'Beach',
    capacity: { min: 20, max: 150 },
    priceRange: { min: 2500, max: 6000 },
    rating: 4.7,
    reviews: 156,
    image: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800',
    description: 'Romantische strandbruiloften met de zonsondergang als decor.',
    amenities: ['Strand', 'Zeezicht', 'BBQ', 'Vuurkorven'],
    featured: false
  },
  {
    id: 4,
    name: 'Landgoed Groenveld',
    location: 'Laren',
    type: 'Nature',
    capacity: { min: 40, max: 180 },
    priceRange: { min: 4000, max: 10000 },
    rating: 4.9,
    reviews: 203,
    image: 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800',
    description: 'Prachtig landgoed omgeven door weelderige tuinen en oude bomen.',
    amenities: ['Tuin', 'Bos', 'Kapel', 'Overnachting'],
    featured: true
  },
  {
    id: 5,
    name: 'The Loft Downtown',
    location: 'Rotterdam',
    type: 'Urban',
    capacity: { min: 25, max: 80 },
    priceRange: { min: 2000, max: 4500 },
    rating: 4.5,
    reviews: 67,
    image: 'https://images.unsplash.com/photo-1566417713940-fe7c737a9ef2?w=800',
    description: 'Stijlvolle industriële loft in een gerenoveerd pakhuis.',
    amenities: ['Stadszicht', 'Rolstoeltoegankelijk', 'Catering', 'DJ'],
    featured: false
  },
  {
    id: 6,
    name: 'Boerderij De Eikenhoeve',
    location: 'Veluwe',
    type: 'Rustic',
    capacity: { min: 30, max: 120 },
    priceRange: { min: 3000, max: 7000 },
    rating: 4.7,
    reviews: 112,
    image: 'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=800',
    description: 'Authentieke boerderij met landelijke charme en warme sfeer.',
    amenities: ['Weiland', 'Dieren', 'Kampvuur', 'Overnachting'],
    featured: true
  },
  {
    id: 7,
    name: 'Luxe Hotel Palazzo',
    location: 'Den Haag',
    type: 'Luxury',
    capacity: { min: 50, max: 250 },
    priceRange: { min: 8000, max: 25000 },
    rating: 4.9,
    reviews: 178,
    image: 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800',
    description: 'Five-star hotel met exclusieve zalen en eersteklas service.',
    amenities: ['Wellness', 'Suite', 'Chauffeur', 'Fine Dining'],
    featured: true
  },
  {
    id: 8,
    name: 'Modern Art Space',
    location: 'Eindhoven',
    type: 'Modern',
    capacity: { min: 20, max: 100 },
    priceRange: { min: 2800, max: 5500 },
    rating: 4.4,
    reviews: 54,
    image: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800',
    description: 'Moderne kunstgalerie die omgetoverd wordt tot unieke trouwlocatie.',
    amenities: ['Kunstcollectie', 'Projector', 'Catering', 'Bar'],
    featured: false
  }
];

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { WEDDING_TYPES, VENUE_CAPACITY, MOCK_VENUES };
}

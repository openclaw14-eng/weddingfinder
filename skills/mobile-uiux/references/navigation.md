# Navigation Patterns

## Stack Navigator

Best for: Deep navigation, hierarchical flows (onboarding, settings)

```tsx
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

export function HomeStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: '#fff' },
        headerShadowVisible: false,
        headerTitleStyle: { fontWeight: '600' },
      }}
    >
      <Stack.Screen 
        name="Home" 
        component={HomeScreen}
        options={{ title: 'Discover' }}
      />
      <Stack.Screen 
        name="Details" 
        component={DetailsScreen}
        options={{ headerBackTitle: 'Back' }}
      />
      <Stack.Screen 
        name="Modal" 
        component={ModalScreen}
        options={{ presentation: 'modal' }}
      />
    </Stack.Navigator>
  );
}
```

## Tab Navigator

Best for: Top-level sections, equal importance

```tsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, Search, Heart, User } from 'lucide-react-native';

const Tab = createBottomTabNavigator();

export function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          const icons = {
            Home: Home,
            Search: Search,
            Favorites: Heart,
            Profile: User,
          };
          const Icon = icons[route.name];
          return <Icon size={size} color={color} fill={focused ? color : 'none'} />;
        },
        tabBarActiveTintColor: '#3b82f6',
        tabBarInactiveTintColor: '#9ca3af',
        tabBarStyle: {
          borderTopWidth: 0,
          elevation: 0,
          shadowOpacity: 0,
          height: 64,
          paddingBottom: 8,
        },
        headerShown: false,
      })}
    >
      <Tab.Screen name="Home" component={HomeStack} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Favorites" component={FavoritesScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
```

## Drawer Navigator

Best for: Many sections, settings-heavy apps

```tsx
import { createDrawerNavigator } from '@react-navigation/drawer';

const Drawer = createDrawerNavigator();

export function MainDrawer() {
  return (
    <Drawer.Navigator
      screenOptions={{
        drawerStyle: { width: 280 },
        drawerActiveTintColor: '#3b82f6',
        drawerInactiveTintColor: '#6b7280',
      }}
    >
      <Drawer.Screen name="Home" component={HomeScreen} />
      <Drawer.Screen name="Settings" component={SettingsScreen} />
    </Drawer.Navigator>
  );
}
```

## Nested Navigation

Common pattern: Tabs → Stacks

```tsx
// Root navigator
export function RootNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Main" component={MainTabs} />
        <Stack.Screen 
          name="Auth" 
          component={AuthStack}
          options={{ presentation: 'fullScreenModal' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Each tab can have its own stack
function HomeStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="HomeList" component={HomeScreen} />
      <Stack.Screen name="VenueDetails" component={VenueDetailsScreen} />
      <Stack.Screen name="Booking" component={BookingScreen} />
    </Stack.Navigator>
  );
}
```

## Navigation Types

```typescript
// types/navigation.ts
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';

export type RootStackParamList = {
  Main: undefined;
  Auth: undefined;
  VenueDetails: { venueId: string };
  Booking: { venueId: string; date?: string };
};

export type HomeTabParamList = {
  HomeList: undefined;
  Search: { query?: string };
  Favorites: undefined;
  Profile: undefined;
};

// Hook helpers
export type NavigationProp = NativeStackNavigationProp<RootStackParamList>;
export type VenueDetailsRoute = RouteProp<RootStackParamList, 'VenueDetails'>;

// Usage in component
import { useNavigation, useRoute } from '@react-navigation/native';

function VenueDetailsScreen() {
  const navigation = useNavigation<NavigationProp>();
  const route = useRoute<VenueDetailsRoute>();
  const { venueId } = route.params;
  
  const handleBook = () => {
    navigation.navigate('Booking', { venueId });
  };
}
```

## Header Customization

```tsx
// Large header (iOS style)
<Stack.Screen
  name="Home"
  component={HomeScreen}
  options={{
    headerLargeTitle: true,
    headerLargeTitleShadowVisible: false,
    headerSearchBarOptions: {
      placeholder: 'Search venues...',
      onChangeText: (e) => setSearchQuery(e.nativeEvent.text),
    },
  }}
/>

// Custom header component
<Stack.Screen
  name="Details"
  component={DetailsScreen}
  options={{
    header: ({ navigation }) => (
      <View style={styles.customHeader}>
        <BackButton onPress={() => navigation.goBack()} />
        <Text style={styles.headerTitle}>Venue Details</Text>
        <ShareButton />
      </View>
    ),
  }}
/>

// Transparent header
<Stack.Screen
  name="ImageGallery"
  component={ImageGalleryScreen}
  options={{
    headerTransparent: true,
    headerTintColor: '#fff',
    headerTitle: '',
  }}
/>
```

## Deep Linking

```tsx
// Configuration
const linking = {
  prefixes: ['weddingfinder://', 'https://weddingfinder.app'],
  config: {
    screens: {
      Main: {
        screens: {
          Home: 'home',
          Search: 'search',
        },
      },
      VenueDetails: 'venue/:venueId',
      Booking: 'booking/:venueId',
    },
  },
};

// App entry
export default function App() {
  return (
    <NavigationContainer linking={linking}>
      <RootNavigator />
    </NavigationContainer>
  );
}
```

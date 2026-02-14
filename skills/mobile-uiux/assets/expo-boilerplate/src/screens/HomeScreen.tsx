import { View, Text, StyleSheet, ScrollView, Pressable } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useTheme } from '../theme/ThemeProvider';

export function HomeScreen({ navigation }) {
  const insets = useSafeAreaInsets();
  const { colors, spacing } = useTheme();

  return (
    <ScrollView
      style={[styles.container, { backgroundColor: colors.background }]}
      contentContainerStyle={{ paddingTop: insets.top + spacing[4] }}
    >
      <View style={{ padding: spacing[4] }}>
        <Text style={[styles.title, { color: colors.text }]}>
          Discover Venues
        </Text>
        <Text style={{ color: colors.textSecondary, marginTop: spacing[2] }}>
          Find your perfect wedding location
        </Text>
      </View>

      <Pressable
        onPress={() => navigation.navigate('Details', { id: '1' })}
        style={[
          styles.card,
          {
            backgroundColor: colors.surface,
            margin: spacing[4],
            padding: spacing[4],
          },
        ]}
      >
        <Text style={{ color: colors.text, fontWeight: '600' }}>
          Featured Venue
        </Text>
        <Text style={{ color: colors.textSecondary, marginTop: spacing[2] }}>
          Tap to view details
        </Text>
      </Pressable>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  title: {
    fontSize: 32,
    fontWeight: '700',
  },
  card: {
    borderRadius: 12,
  },
});

import { View, Text, StyleSheet } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useTheme } from '../theme/ThemeProvider';

export function DetailsScreen({ route }) {
  const insets = useSafeAreaInsets();
  const { colors, spacing } = useTheme();
  const { id } = route.params;

  return (
    <View style={[styles.container, { backgroundColor: colors.background, paddingTop: insets.top }]}>
      <View style={{ padding: spacing[4] }}>
        <Text style={[styles.title, { color: colors.text }]}>Venue Details</Text>
        <Text style={{ color: colors.textSecondary, marginTop: spacing[2] }}>
          ID: {id}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
  },
});

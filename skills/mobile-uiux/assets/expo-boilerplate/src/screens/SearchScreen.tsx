import { View, Text } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useTheme } from '../theme/ThemeProvider';

export function SearchScreen() {
  const insets = useSafeAreaInsets();
  const { colors, spacing } = useTheme();

  return (
    <View style={{ flex: 1, backgroundColor: colors.background, paddingTop: insets.top, padding: spacing[4] }}>
      <Text style={{ fontSize: 24, fontWeight: '700', color: colors.text }}>Search</Text>
    </View>
  );
}

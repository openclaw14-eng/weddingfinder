# Component Patterns

## Button

### Variants
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  onPress: () => void;
  children: string;
}
```

### Base Implementation
```tsx
import { Pressable, Text, ActivityIndicator } from 'react-native';
import { useTheme } from './ThemeProvider';

export const Button = ({
  variant = 'primary',
  size = 'md',
  disabled,
  loading,
  icon,
  iconPosition = 'left',
  onPress,
  children,
}: ButtonProps) => {
  const { colors, spacing } = useTheme();
  
  const variants = {
    primary: {
      bg: colors.primary[500],
      text: colors.neutral[0],
      pressed: colors.primary[600],
    },
    secondary: {
      bg: colors.neutral[100],
      text: colors.neutral[900],
      pressed: colors.neutral[200],
    },
    outline: {
      bg: 'transparent',
      text: colors.primary[500],
      pressed: colors.primary[50],
      border: colors.primary[500],
    },
    ghost: {
      bg: 'transparent',
      text: colors.primary[500],
      pressed: colors.primary[50],
    },
    danger: {
      bg: colors.semantic.error,
      text: colors.neutral[0],
      pressed: '#dc2626',
    },
  };
  
  const sizes = {
    sm: { py: 8, px: 12, fontSize: 14 },
    md: { py: 12, px: 16, fontSize: 16 },
    lg: { py: 16, px: 24, fontSize: 18 },
  };
  
  const style = variants[variant];
  const s = sizes[size];
  
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled || loading}
      style={({ pressed }) => ({
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: s.py,
        paddingHorizontal: s.px,
        borderRadius: 8,
        backgroundColor: pressed ? style.pressed : style.bg,
        borderWidth: variant === 'outline' ? 1 : 0,
        borderColor: style.border,
        opacity: disabled ? 0.5 : 1,
        gap: 8,
      })}
    >
      {loading ? (
        <ActivityIndicator color={style.text} size="small" />
      ) : (
        <>
          {icon && iconPosition === 'left' && icon}
          <Text style={{ color: style.text, fontSize: s.fontSize, fontWeight: '600' }}>
            {children}
          </Text>
          {icon && iconPosition === 'right' && icon}
        </>
      )}
    </Pressable>
  );
};
```

## Card

```tsx
import { View, StyleSheet } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export const Card = ({ children, style, padding = 16, onPress }) => {
  const Wrapper = onPress ? Pressable : View;
  
  return (
    <Wrapper
      onPress={onPress}
      style={[
        styles.card,
        { padding },
        style,
      ]}
    >
      {children}
    </Wrapper>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 3,
      },
    }),
  },
});
```

## Input

```tsx
import { TextInput, View, Text } from 'react-native';

export const Input = ({
  label,
  error,
  helper,
  leftIcon,
  rightIcon,
  ...textInputProps
}) => {
  const [focused, setFocused] = useState(false);
  
  return (
    <View style={{ gap: 4 }}>
      {label && <Text style={styles.label}>{label}</Text>}
      <View
        style={[
          styles.inputContainer,
          focused && styles.inputFocused,
          error && styles.inputError,
        ]}
      >
        {leftIcon}
        <TextInput
          {...textInputProps}
          style={styles.input}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholderTextColor="#9ca3af"
        />
        {rightIcon}
      </View>
      {error ? (
        <Text style={styles.errorText}>{error}</Text>
      ) : helper ? (
        <Text style={styles.helperText}>{helper}</Text>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  label: {
    fontSize: 14,
    fontWeight: '500',
    color: '#374151',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 8,
    paddingHorizontal: 12,
    gap: 8,
    height: 48,
  },
  inputFocused: {
    borderColor: '#3b82f6',
  },
  inputError: {
    borderColor: '#ef4444',
  },
  input: {
    flex: 1,
    fontSize: 16,
    color: '#111827',
  },
  errorText: {
    fontSize: 12,
    color: '#ef4444',
  },
  helperText: {
    fontSize: 12,
    color: '#6b7280',
  },
});
```

## Avatar

```tsx
import { Image, View, Text } from 'react-native';

export const Avatar = ({ source, name, size = 48, style }) => {
  const initials = name
    ?.split(' ')
    .map((n) => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();
  
  const sizeStyles = {
    sm: 32,
    md: 48,
    lg: 64,
    xl: 96,
  };
  
  const s = typeof size === 'string' ? sizeStyles[size] : size;
  
  return (
    <View
      style={[
        {
          width: s,
          height: s,
          borderRadius: s / 2,
          backgroundColor: '#e5e7eb',
          alignItems: 'center',
          justifyContent: 'center',
          overflow: 'hidden',
        },
        style,
      ]}
    >
      {source ? (
        <Image source={source} style={{ width: s, height: s }} />
      ) : (
        <Text style={{ fontSize: s * 0.4, fontWeight: '600', color: '#6b7280' }}>
          {initials}
        </Text>
      )}
    </View>
  );
};
```

## Badge

```tsx
export const Badge = ({ children, variant = 'default', size = 'md' }) => {
  const variants = {
    default: { bg: '#f3f4f6', text: '#374151' },
    primary: { bg: '#dbeafe', text: '#1d4ed8' },
    success: { bg: '#dcfce7', text: '#15803d' },
    warning: { bg: '#fef3c7', text: '#b45309' },
    error: { bg: '#fee2e2', text: '#dc2626' },
  };
  
  const sizes = {
    sm: { px: 6, py: 2, fontSize: 10 },
    md: { px: 8, py: 3, fontSize: 12 },
    lg: { px: 10, py: 4, fontSize: 14 },
  };
  
  const v = variants[variant];
  const s = sizes[size];
  
  return (
    <View
      style={{
        backgroundColor: v.bg,
        paddingHorizontal: s.px,
        paddingVertical: s.py,
        borderRadius: 9999,
        alignSelf: 'flex-start',
      }}
    >
      <Text style={{ color: v.text, fontSize: s.fontSize, fontWeight: '500' }}>
        {children}
      </Text>
    </View>
  );
};
```

## List Item

```tsx
export const ListItem = ({
  title,
  subtitle,
  left,
  right,
  onPress,
  showChevron = false,
  divider = true,
}) => {
  return (
    <Pressable onPress={onPress} style={styles.container}>
      <View style={styles.content}>
        {left && <View style={styles.left}>{left}</View>}
        <View style={styles.textContainer}>
          <Text style={styles.title}>{title}</Text>
          {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
        </View>
        {right && <View style={styles.right}>{right}</View>}
        {showChevron && <ChevronRight size={20} color="#9ca3af" />}
      </View>
      {divider && <View style={styles.divider} />}
    </Pressable>
  );
};
```

## Skeleton Loading

```tsx
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withTiming,
} from 'react-native-reanimated';

export const Skeleton = ({ width, height, circle = false }) => {
  const opacity = useSharedValue(0.3);
  
  useEffect(() => {
    opacity.value = withRepeat(
      withTiming(0.7, { duration: 800 }),
      -1,
      true
    );
  }, []);
  
  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
  }));
  
  return (
    <Animated.View
      style={[
        {
          width,
          height,
          backgroundColor: '#e5e7eb',
          borderRadius: circle ? height / 2 : 4,
        },
        animatedStyle,
      ]}
    />
  );
};
```

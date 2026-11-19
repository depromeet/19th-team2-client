import { tokens } from "@team2/shared";
import { Pressable, StyleSheet, Text } from "react-native";
import type { ButtonProps } from "./types";

export function Button({ label, onPress, variant = "primary", disabled }: ButtonProps) {
  const isPrimary = variant === "primary";
  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.base,
        isPrimary ? styles.primary : styles.secondary,
        (disabled || pressed) && styles.dimmed,
      ]}
    >
      <Text style={[styles.label, isPrimary ? styles.primaryLabel : styles.secondaryLabel]}>
        {label}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    borderRadius: tokens.radius.card,
    paddingHorizontal: 16,
    paddingVertical: 12,
    alignItems: "center",
  },
  primary: { backgroundColor: tokens.color.primary },
  secondary: {
    backgroundColor: tokens.color.background,
    borderWidth: 1,
    borderColor: tokens.color.border,
  },
  dimmed: { opacity: 0.5 },
  label: { fontWeight: "600" },
  primaryLabel: { color: tokens.color["primary-foreground"] },
  secondaryLabel: { color: tokens.color.foreground },
});

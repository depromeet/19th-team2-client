"use client";

import { cn } from "../cn";
import type { ButtonProps } from "./types";

type WebButtonProps = ButtonProps & {
  className?: string;
};

const variantClass = {
  primary: "bg-primary text-primary-foreground",
  secondary: "border border-border bg-background text-foreground",
} as const;

export function Button({
  label,
  onPress,
  variant = "primary",
  disabled,
  className,
}: WebButtonProps) {
  return (
    <button
      type="button"
      onClick={onPress}
      disabled={disabled}
      className={cn(
        "rounded-card px-4 py-3 font-semibold disabled:opacity-50",
        variantClass[variant],
        className,
      )}
    >
      {label}
    </button>
  );
}

/**
 * 웹·앱 공통 디자인 토큰.
 * 웹은 apps/web/src/app/globals.css의 @theme에 같은 값을 둔다 (값이 어긋나면 web 테스트가 실패한다).
 * Figma 디자인 시스템 토큰이 확정되면 두 곳을 함께 교체한다.
 */
export const tokens = {
  color: {
    background: "#ffffff",
    foreground: "#171717",
    primary: "#2563eb",
    "primary-foreground": "#ffffff",
    muted: "#f4f4f5",
    "muted-foreground": "#71717a",
    border: "#e4e4e7",
    danger: "#dc2626",
  },
  radius: {
    /** 1rem */
    card: 16,
  },
} as const;

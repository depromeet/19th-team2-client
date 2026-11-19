export type ButtonVariant = "primary" | "secondary";

/** 웹·앱 공통 props. 플랫폼 전용 값은 각 구현 파일에서 확장한다. */
export type ButtonProps = {
  label: string;
  onPress?: () => void;
  variant?: ButtonVariant;
  disabled?: boolean;
};

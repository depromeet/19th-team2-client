import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/** 조건부 className을 합치고, 충돌하는 Tailwind 클래스는 뒤의 것을 남긴다. */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

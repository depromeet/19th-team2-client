---

name: new-component
description: Use when creating a new React component, page section, or feature module in this repo. Applies the team's file layout, naming, server/client and test conventions.
---

# New component

## 위치 결정

- 도메인 무관 재사용 UI → `src/components/ui/<Name>.tsx`
- 특정 도메인 전용 → `src/features/<domain>/components/<Name>.tsx`
- 라우트 파일(`src/app/**/page.tsx`)에는 조합만 두고 로직은 feature로.

## 작성 규칙

- 기본 Server Component. 상태/이벤트/브라우저 API가 필요할 때만 `"use client"`, 그리고 클라이언트 범위를 가능한 한 잎(leaf) 컴포넌트로 좁힌다.
- named export, `type <Name>Props = {...}`, `@/` 경로 별칭.
- 스타일은 Tailwind. 외부 클래스 주입은 `className?: string` prop으로 받는다.
- 접근성: 인터랙티브 요소는 시맨틱 태그(`button`, `a`) 사용, 아이콘 버튼엔 `aria-label`.

## 템플릿

```tsx
type ExampleProps = {
  title: string;
  className?: string;
};

export function Example({ title, className }: ExampleProps) {
  return <section className={className}>{title}</section>;
}
```

## 테스트

같은 폴더에 `<Name>.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react";
import { Example } from "./Example";

it("제목을 렌더링한다", () => {
  render(<Example title="hello" />);
  expect(screen.getByText("hello")).toBeInTheDocument();
});
```

(TanStack Query를 쓰는 컴포넌트는 테스트에서 `QueryClientProvider`로 감싼다. async Server Component는 Vitest로 렌더 불가 → 로직을 순수 함수로 분리해 테스트)

마지막에 `verify` 스킬을 실행한다.

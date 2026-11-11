<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->


# 19th-team2-client — Agent Guide

이 파일이 **AI 에이전트 공통 규칙의 단일 원본(single source of truth)** 입니다.
Codex는 이 파일을 직접 읽고, Claude Code는 `CLAUDE.md`에서 `@AGENTS.md`로 불러옵니다.
규칙을 바꿀 땐 이 파일만 수정하세요. 도구 전용 설정만 `CLAUDE.md` / `.codex/`에 둡니다.
폴더 구조·네이밍의 상세 설명은 `README.md`에 있습니다.

## 제품 맥락

- 사용자는 **X(트위터) 링크를 타고 로그인 없이** 공구 페이지로 처음 들어온다.
  → 공구 상세 같은 진입 페이지는 Server Component로 렌더링하고, `generateMetadata`로
  OG/Twitter 카드 메타데이터(title, description, image)를 반드시 채운다.
  → 진입 페이지의 클라이언트 JS·첫 로딩 비용을 늘리는 변경은 이유를 PR에 적는다.
- 배포는 Vercel. PR마다 Preview URL이 생기며 디자인 QA에 쓴다.

## Stack

- Next.js 16 (App Router, Turbopack, `cacheComponents` 활성) · React 19 · TypeScript (strict)
- 스타일: Tailwind CSS v4 (디자인 토큰은 `src/app/globals.css`의 `@theme`에 정의)
- 서버 상태: TanStack Query v5 (`src/lib/queryClient.ts`, `src/app/providers.tsx`)
- 클라이언트 상태: **전역 상태 라이브러리 없음.** `useState`/URL 상태로 해결한다.
  "로그인 전 담은 상품을 로그인 후에도 유지" 같은 요구가 생기면 그때 Zustand 도입을 제안한다 (임의 도입 금지).
- 린트·포맷: **Biome** (`biome.json`) — ESLint/Prettier 사용 안 함. Tailwind 클래스 정렬도 Biome 규칙(`useTailwindSortedClasses`)이 처리.
- 테스트: Vitest + Testing Library
- 패키지 매니저: **pnpm** (`packageManager` 필드로 고정). npm/yarn 사용 금지. · Node 22 (`.nvmrc`)

## Commands

| 목적           | 명령                                                             |
| -------------- | ---------------------------------------------------------------- |
| 개발 서버      | `pnpm dev`                                                       |
| 타입 체크      | `pnpm typecheck`                                                 |
| 린트+포맷 검사 | `pnpm lint` (자동 수정: `pnpm lint:fix`)                         |
| 포맷만         | `pnpm format`                                                    |
| 테스트         | `pnpm test` (단일 파일: `pnpm vitest run path/to/file.test.tsx`) |
| 전체 검증      | `pnpm check` — 작업 완료 전 반드시 통과 (CI와 동일)              |

## Directory structure

```
src/
  app/            # 라우트 전용 (page/layout/loading/error). 조합만, 로직은 feature로
  components/ui/  # 도메인 무관 공용 UI (Button, Input ...)
  features/<domain>/
    components/   # 해당 도메인 전용 컴포넌트
    api/          # fetch 함수, queryOptions, server actions
    hooks/
    types.ts
  lib/            # 공용 유틸, 상수, 클라이언트 설정
  test/           # 테스트 setup
```

- import는 `@/` 별칭 사용. 상위 상대경로(`../../`) 금지 (Biome가 에러 처리).
- feature 간 직접 import는 지양하고, 공용이 되면 `components/ui` 또는 `lib`으로 승격.

## Code conventions

- 기본은 **Server Component**. 상태·이벤트·브라우저 API가 필요할 때만 `"use client"`, 범위는 잎(leaf) 컴포넌트로 좁힌다.
- 컴포넌트: `PascalCase.tsx`, named export. Next 라우트 파일(`page.tsx`, `layout.tsx` 등)만 default export.
- 훅: `useXxx.ts` · 유틸: `camelCase.ts` · 테스트: 대상 옆 `*.test.ts(x)`.
- `any` 금지 → `unknown` + 타입 가드. props 타입은 `type XxxProps = {...}`.
- TanStack Query: 쿼리 키·fetch는 `features/<domain>/api/`에 `queryOptions()`로 정의해 재사용한다.
  컴포넌트에서 `useQuery({ queryKey: [...], queryFn })`를 직접 인라인으로 만들지 않는다.
- 스타일: Tailwind 유틸리티 클래스만 사용 (CSS Modules/styled 금지). 색·반경 등은 `globals.css`의 `@theme` 토큰을 쓰고
  임의값(`bg-[#123456]`)은 토큰이 없을 때만. 조건부/외부 className 병합은 `cn()` (`@/lib/cn`, clsx + tailwind-merge).
- 환경변수: 클라이언트 노출은 `NEXT_PUBLIC_` 접두사 필수. `.env*` 파일은 커밋/열람 금지.
- 주석은 "왜"만 적고 "무엇"은 코드로 표현.

## Git workflow (3인 협업)

- `main` 하나 + 기능 브랜치. `main`은 **PR로만 병합**, **squash merge**.
- 브랜치 이름: `feat/설명`, `fix/설명`, `chore/설명`, `docs/설명`, `refactor/설명` (예: `feat/group-buy-detail`).
  이슈 도구가 정해지면 이슈 번호를 붙인다.
- 커밋 메시지: `feat:` `fix:` `chore:` `docs:` `refactor:` 접두어 (예: `feat: 공구 상세 페이지 추가`).
  형식은 `.gitmessage` 템플릿 참고 (`<접두어>: <제목>` + 선택 본문 "왜" + 선택 꼬리말 `closes #N`).
  `pnpm install` 시 `git commit`에 템플릿이 자동 적용된다.
- PR: `.github/pull_request_template.md`(무엇을 / 왜 / 확인 방법 / 스크린샷) 작성. **승인 1명 이상**이면 병합.
- 리뷰: 요청받으면 **24시간 안에** 본다.
- pre-commit 훅이 staged 파일에 Biome를 실행한다. `--no-verify` 사용 금지.

## Rules for AI agents

1. 코드 작성 전 관련 Next 문서(`node_modules/next/dist/docs/`)와 기존 코드를 먼저 확인.
2. 요청 범위 밖의 리팩터링·파일 이동·의존성 추가 금지. 필요하면 먼저 제안.
3. 의존성 추가는 `pnpm add`로만, 이유를 PR/응답에 명시.
4. 완료 선언 전 `pnpm check` 실행 후 결과를 그대로 보고 (실패를 숨기지 말 것).
5. `main`에 직접 커밋/푸시 금지. 커밋·푸시·PR 생성은 사용자가 요청할 때만.
6. 공용 스킬은 `.agents/skills/`에 있음 (Claude는 `.claude/skills` 심볼릭 링크로 동일하게 사용).

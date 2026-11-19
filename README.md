# 19th-team2-client

디프만 19기 2팀 프론트엔드 — X 링크로 로그인 없이 들어오는 공구 페이지 서비스

## 기술 스택

| 항목            | 선택                                 | 이유                                                                   |
| --------------- | ------------------------------------ | ---------------------------------------------------------------------- |
| 프레임워크      | Next.js 16 (App Router) + TypeScript | 첫 화면이 X 링크 진입 공구 페이지 → 링크 미리보기(OG)와 첫 로딩이 중요 |
| 패키지 매니저   | pnpm                                 |                                                                        |
| 스타일          | Tailwind CSS v4                      | 디자인 시스템 토큰을 옮기기 쉬움                                       |
| 서버 상태       | TanStack Query v5                    |                                                                        |
| 클라이언트 상태 | 없음 (필요 시 Zustand)               | 로그인 전 담은 상품을 로그인 후에도 유지해야 하면 도입                 |
| 린트·포맷       | Biome                                | 도구·설정이 하나. Tailwind 클래스 정렬도 Biome 규칙으로 처리           |
| 테스트          | Vitest + Testing Library             |                                                                        |
| 배포            | Vercel                               | PR마다 Preview URL → 디자인 QA                                         |
| 앱              | Expo SDK 58 + Expo Router            | 웹과 로직·토큰·컴포넌트 props 공유, 렌더링만 네이티브로                |
| 레포            | pnpm workspace 모노레포              | `apps/web`, `apps/mobile`, `packages/shared`, `packages/ui`            |

## 시작하기

```bash
corepack enable          # pnpm 버전은 package.json의 packageManager로 고정
pnpm install             # pre-commit 훅(husky)도 함께 설치됨
cp .env.example .env.local
pnpm dev                 # 웹 (http://localhost:3000)
pnpm dev:mobile          # 앱 (Expo Go 앱으로 QR 스캔, 또는 i / a 키로 시뮬레이터)
```

VS Code는 추천 확장(Biome, Tailwind CSS IntelliSense)을 설치하면 저장 시 자동 포맷됩니다.

| 명령              | 설명                                                    |
| ----------------- | ------------------------------------------------------- |
| `pnpm dev`        | 웹 개발 서버                                            |
| `pnpm dev:mobile` | 앱 개발 서버 (Expo)                                     |
| `pnpm check`      | typecheck + Biome 검사 + 테스트 (PR 전 필수, CI와 동일) |
| `pnpm lint:fix`   | 포맷·import 정렬·Tailwind 클래스 정렬 자동 수정         |
| `pnpm build`      | 웹 프로덕션 빌드                                        |

## 폴더 구조

```
apps/
  web/                  # Next.js (Vercel 배포, Root Directory = apps/web)
  mobile/               # Expo 앱
packages/
  shared/               # @team2/shared — 타입, API·queryOptions, 유틸, 디자인 토큰 (UI 없음)
  ui/                   # @team2/ui — 공용 컴포넌트
    src/Button/
      types.ts          # 웹·앱 공통 props
      Button.tsx        # 웹 (button + Tailwind)  ← Next가 선택
      Button.native.tsx # 앱 (Pressable)          ← Metro가 선택
```

- 디자인 토큰 원본은 `packages/shared/src/tokens.ts`. 웹 `globals.css`의 `@theme`도 같은 값이어야 하고, 어긋나면 웹 테스트가 실패합니다.
- 웹에는 react-native-web을 쓰지 않습니다. 진입 페이지 첫 로딩과 Server Component를 지키기 위해서입니다.

### apps/web

```
src/
  app/                  # 라우트 전용 (page, layout, loading, error). 조합만 하고 로직은 features로
    providers.tsx       # QueryClientProvider 등 클라이언트 Provider
  components/ui/        # 도메인과 무관한 공용 UI (Button, Input, Modal ...)
  features/<domain>/    # 도메인별 모듈 (예: group-buy, auth, cart)
    components/         # 이 도메인에서만 쓰는 컴포넌트
    api/                # fetch 함수, queryOptions, server actions
    hooks/              # 이 도메인 전용 훅
    types.ts
  lib/                  # 공용 유틸, 상수, 설정 (queryClient.ts, cn.ts ...)
  test/                 # 테스트 setup
```

- import는 `@/` 별칭 사용 (`@/features/group-buy/api/...`). `../../` 같은 상위 상대경로는 Biome가 막습니다.
- 한 도메인에서만 쓰던 것이 다른 도메인에서도 필요해지면 `components/ui` 또는 `lib`으로 옮깁니다.

## 네이밍

| 대상          | 규칙                      | 예                                                  |
| ------------- | ------------------------- | --------------------------------------------------- |
| 컴포넌트 파일 | PascalCase, named export  | `GroupBuyCard.tsx` → `export function GroupBuyCard` |
| 라우트 파일   | Next 규칙, default export | `page.tsx`, `layout.tsx`                            |
| 훅            | `use` + camelCase         | `useCartItems.ts`                                   |
| 유틸          | camelCase                 | `formatPrice.ts`                                    |
| 도메인 폴더   | kebab-case                | `features/group-buy/`                               |
| 테스트        | 대상 옆 `*.test.ts(x)`    | `formatPrice.test.ts`                               |
| props 타입    | `컴포넌트명Props`         | `type GroupBuyCardProps = {...}`                    |

## 협업 규칙

- **브랜치**: `main` 하나 + 기능 브랜치. `feat/설명`, `fix/설명` (이슈 도구가 정해지면 이슈 번호 추가)
  - 소문자 kebab-case. 이슈 번호는 `feat/12-group-buy-detail`처럼 접두어 뒤에 붙입니다.
  - `pre-push` 훅과 CI(`branch-name` job)가 이름을 검사하고, 훅은 `main`으로의 직접 push를 막습니다.
- **병합**: PR로만, squash merge, 승인 1명 이상
- **커밋**: `feat:` `fix:` `chore:` `docs:` `refactor:` 접두어 — `git commit`(에디터)을 실행하면 `.gitmessage` 템플릿이 열립니다 (`pnpm install` 때 자동 설정)
- **PR**: 템플릿(무엇을 / 왜 / 확인 방법 / 스크린샷) 작성
- **리뷰**: 요청 후 24시간 안에

## AI 에이전트 (Claude Code / Codex)

두 도구가 **같은 규칙과 스킬**을 쓰도록 구성되어 있습니다.

| 파일                    | 대상        | 역할                                                     |
| ----------------------- | ----------- | -------------------------------------------------------- |
| `AGENTS.md`             | 공통 (원본) | 제품 맥락, 스택, 명령어, 구조, 컨벤션, 에이전트 규칙     |
| `CLAUDE.md`             | Claude Code | `@AGENTS.md` import + Claude 전용 메모                   |
| `.agents/skills/`       | 공통 (원본) | 팀 스킬: `verify`, `new-component`, `create-pr`          |
| `.claude/skills`        | Claude Code | → `.agents/skills` 심볼릭 링크                           |
| `.claude/settings.json` | Claude Code | 권한 allow/deny, 편집 후 Biome 포맷 hook                 |
| `.codex/config.toml`    | Codex       | 승인/샌드박스 정책 (Codex에서 이 repo를 trust 해야 적용) |

규칙 변경은 `AGENTS.md`, 스킬 추가는 `.agents/skills/<name>/SKILL.md`에만 하면 두 도구에 모두 반영됩니다.
개인 설정은 `.claude/settings.local.json`, `CLAUDE.local.md`, `~/.codex/config.toml`에 두세요 (커밋 안 됨).

> Windows 사용자는 심볼릭 링크를 위해 `git config core.symlinks true` 후 클론하세요.

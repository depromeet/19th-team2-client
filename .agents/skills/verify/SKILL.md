---

name: verify
description: Use before claiming any code change is done, or when asked to check/verify the project. Runs typecheck, lint, format check and tests, and reports results honestly.
---

# Verify

1. 프로젝트 루트에서 `pnpm check` 실행 (typecheck → biome check → test).
2. 포맷·import 정렬·Tailwind 클래스 정렬 같은 자동 수정 가능 항목은 `pnpm lint:fix` 후 재실행.
3. 타입/테스트 실패는 원인을 고친 뒤 다시 `pnpm check`. 관련 없는 기존 실패라면 고치지 말고 보고.
4. UI 변경이면 `pnpm build`도 실행해 서버/클라이언트 경계 오류가 없는지 확인.
5. 결과 보고: 실행한 명령, 통과/실패 여부, 실패 시 에러 핵심 줄을 그대로 인용. 통과하지 않았으면 "완료"라고 말하지 않는다.

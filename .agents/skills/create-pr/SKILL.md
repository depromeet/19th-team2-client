---

name: create-pr
description: Use when the user asks to commit, push, or open a pull request. Follows the team branch, commit prefix, and PR template rules.
---

# Create PR

사용자가 명시적으로 요청했을 때만 실행한다.

1. `git status` / `git diff`로 변경 범위 확인. 관련 없는 변경이 섞였으면 사용자에게 알린다.
2. 현재 브랜치가 `main`이면 `feat|fix|chore|docs|refactor/<설명>` 브랜치 (예: `feat/group-buy-detail`)를 새로 만든다.
3. `verify` 스킬로 `pnpm check` 통과 확인. 실패 시 PR 만들지 않는다.
4. `feat:` `fix:` `chore:` `docs:` `refactor:` 접두어로 커밋 (예: `feat: 공구 상세 페이지 추가`). 제목 50자 이내·마침표 없음, 필요하면 빈 줄 뒤 본문에 "왜"를 적는다 (`.gitmessage` 형식). `--no-verify` 금지.
5. `git push -u origin <branch>` 후 `gh pr create --base main`.
   본문은 `.github/pull_request_template.md` 항목을 채운다 (무엇을 / 왜 / 확인 방법 / 스크린샷).
6. PR URL을 사용자에게 전달.

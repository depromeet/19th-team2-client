@AGENTS.md

# Claude Code 전용 메모

- 공통 규칙은 위 `AGENTS.md`가 원본입니다. 여기에는 Claude 전용 내용만 적습니다.
- 팀 공용 설정: `.claude/settings.json` (커밋됨). 개인 설정은 `.claude/settings.local.json` (gitignore).
- 파일 편집 후 Biome 포맷터가 hook으로 자동 실행됩니다 (포맷만, import 정리·린트 수정은 하지 않음). 포맷 때문에 diff가 바뀌어도 되돌리지 마세요.
- 스킬: `/verify`, `/new-component`, `/create-pr` (`.claude/skills` → `.agents/skills`)

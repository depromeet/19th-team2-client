import { readFileSync } from "node:fs";
import { join } from "node:path";
import { tokens } from "@team2/shared";

// 앱은 @team2/shared 토큰을, 웹은 globals.css @theme을 쓰므로 두 값이 같은지 확인한다.
const css = readFileSync(join(__dirname, "globals.css"), "utf8");

describe("globals.css 디자인 토큰", () => {
  it.each(Object.entries(tokens.color))("--color-%s가 shared 토큰과 같다", (name, value) => {
    expect(css).toContain(`--color-${name}: ${value};`);
  });

  it("--radius-card가 shared 토큰과 같다", () => {
    expect(css).toContain(`--radius-card: ${tokens.radius.card / 16}rem;`);
  });
});

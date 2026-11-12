import { cn } from "@/lib/cn";

describe("cn", () => {
  it("falsy 값을 제외하고 합친다", () => {
    expect(cn("a", false, null, undefined, "b")).toBe("a b");
  });

  it("충돌하는 Tailwind 클래스는 뒤의 것을 남긴다", () => {
    expect(cn("p-2 text-sm", "p-4")).toBe("text-sm p-4");
  });
});

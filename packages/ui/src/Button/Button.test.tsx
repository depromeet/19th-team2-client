import { fireEvent, render, screen } from "@testing-library/react";
import { Button } from "./Button";

describe("Button (web)", () => {
  it("라벨을 렌더링하고 누르면 onPress를 호출한다", () => {
    const onPress = vi.fn();
    render(<Button label="참여하기" onPress={onPress} />);
    fireEvent.click(screen.getByRole("button", { name: "참여하기" }));
    expect(onPress).toHaveBeenCalledOnce();
  });

  it("disabled면 누를 수 없다", () => {
    render(<Button label="참여하기" disabled />);
    expect(screen.getByRole("button")).toBeDisabled();
  });
});

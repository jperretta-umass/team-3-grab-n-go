import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import App from "../App.vue";

describe("App", () => {
  it("renders the app heading", () => {
    const wrapper = mount(App);
    expect(wrapper.find("h1").text()).toBe("Grab-n-Go");
  });

  it("renders the HelloWorld component", () => {
    const wrapper = mount(App);
    expect(wrapper.text()).toContain("Welcome to Grab-n-Go");
  });
});

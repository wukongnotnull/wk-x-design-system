const test = require("node:test");
const assert = require("node:assert/strict");
const { applyTheme, applyAccent, persist, loadPersisted, boot } = require("../theme.js");

function fakeRoot() {
  const styles = {};
  return {
    dataset: {},
    style: {
      setProperty(name, value) {
        styles[name] = value;
      },
      getPropertyValue(name) {
        return styles[name] || "";
      }
    }
  };
}

function fakeStorage(initial) {
  const data = { ...initial };
  return {
    getItem(key) {
      return Object.prototype.hasOwnProperty.call(data, key) ? data[key] : null;
    },
    setItem(key, value) {
      data[key] = String(value);
    },
    _data: data
  };
}

test("applyTheme sets data-theme and rejects unknown values", () => {
  const root = fakeRoot();
  assert.equal(applyTheme(root, "dim"), "dim");
  assert.equal(root.dataset.theme, "dim");
  assert.equal(applyTheme(root, "nope"), "lights-out");
  assert.equal(root.dataset.theme, "lights-out");
});

test("applyAccent sets --main-accent CSS variable", () => {
  const root = fakeRoot();
  assert.equal(applyAccent(root, "pink"), "pink");
  assert.equal(root.style.getPropertyValue("--main-accent"), "var(--accent-pink)");
  assert.equal(applyAccent(root, "nope"), "blue");
  assert.equal(root.style.getPropertyValue("--main-accent"), "var(--accent-blue)");
});

test("persist and loadPersisted use xds-theme and xds-accent", () => {
  const storage = fakeStorage({});
  persist(storage, "default", "green");
  assert.deepEqual(loadPersisted(storage), { theme: "default", accent: "green" });
});

test("boot defaults to lights-out and blue when storage is empty", () => {
  const root = fakeRoot();
  const storage = fakeStorage({});
  const result = boot(root, storage);
  assert.deepEqual(result, { theme: "lights-out", accent: "blue" });
  assert.equal(root.dataset.theme, "lights-out");
  assert.equal(root.style.getPropertyValue("--main-accent"), "var(--accent-blue)");
  assert.equal(storage.getItem("xds-theme"), "lights-out");
  assert.equal(storage.getItem("xds-accent"), "blue");
});

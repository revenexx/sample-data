// The linter half of the TypeScript floor (cicd-standard.md, rule 1: tsc + a
// linter). The recommended rules and nothing else: a first linter is there to
// exist and stay green, not to settle style — prettier does that.
import js from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import globals from "globals";
import tseslint from "typescript-eslint";

export default defineConfig(
  // ESLint does not read .gitignore: build output has to be named here, or a
  // local --suppress-all records it in the baseline.
  globalIgnores(["dist/", "build/", "coverage/", ".nuxt/", ".next/", ".output/"]),
  js.configs.recommended,
  tseslint.configs.recommended,
  // Plain .js/.mjs files need to know where they run, or `no-undef` flags
  // `process` and `console`. A browser project uses globals.browser.
  { languageOptions: { globals: { ...globals.node } } },
);

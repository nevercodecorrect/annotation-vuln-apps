import { defineConfig } from "@playwright/test";

export default defineConfig({
	use: {
		screenshot: "only-on-failure",
		trace: "retain-on-failure",
		permissions: ["clipboard-read", "clipboard-write"],
		bypassCSP: true,
		launchOptions: {
			args: ["--disable-web-security"]
		}
	},
	expect: { timeout: 60000 },
	timeout: 90000,
	testMatch: /.*.spec.ts/,
	testDir: "..",
	globalSetup: "./playwright-setup.js",
	workers: process.env.CI ? 1 : undefined
});

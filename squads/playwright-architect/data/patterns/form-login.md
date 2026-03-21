# Pattern: form-login

**Category:** Authentication
**When to use:** Site requires email + password login
**Stagehand mode:** act (sequential actions)
**Tested:** Yes (2026-03-19)

## Code

```javascript
// Pattern: form-login
// Prerequisite: page already at login URL
async function formLogin(stagehand, page, { loginUrl, email, password }) {
  await page.goto(loginUrl, { waitUntil: 'domcontentloaded' });

  await stagehand.act({ action: `type "${email}" in the email or username field` });
  await stagehand.act({ action: `type "${password}" in the password field` });
  await stagehand.act({ action: 'click the login, sign in, or submit button' });

  // Wait for redirect after login
  await page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 });

  console.log('Login successful');
}
```

## Usage Example

```javascript
await formLogin(stagehand, page, {
  loginUrl: 'https://app.example.com/login',
  email: process.env.LOGIN_EMAIL,
  password: process.env.LOGIN_PASSWORD,
});
```

## Notes
- Use natural language for button text — Stagehand finds "Sign In", "Login", "Submit"
- If login fails silently, check for redirect URL or dashboard element
- For OAuth, use a different pattern (oauth-login)
- Credentials should ALWAYS come from .env, never hardcoded

# Stagehand v3 Knowledge Base

## Overview

Stagehand é um framework AI-powered de browser automation criado pela Browserbase.
Combina o poder do Playwright com LLMs para automação inteligente.

## API Reference

### Initialization

```javascript
import { Stagehand } from '@browserbasehq/stagehand';

const stagehand = new Stagehand({
  env: 'LOCAL',
  localBrowserLaunchOptions: {
    headless: false,
    viewport: { width: 1280, height: 720 },
  },
  apiKey: process.env.OPENAI_API_KEY,
  model: {
    modelName: 'openai/gpt-4o-mini',
    apiKey: process.env.OPENAI_API_KEY,
  },
});

await stagehand.init();
const page = stagehand.page; // Raw Playwright page
```

### Methods

#### `stagehand.act(options)`
Execute a single action using natural language.

```javascript
await stagehand.act({ action: 'click the sign in button' });
await stagehand.act({ action: 'type "hello@email.com" in the email field' });
await stagehand.act({ action: 'scroll down to the pricing section' });
```

**When to use:** Single deterministic actions (click, type, scroll)
**Cost:** ~50-100 tokens per action

#### `stagehand.extract(options)`
Extract structured data from the current page.

```javascript
import { z } from 'zod';

const result = await stagehand.extract({
  instruction: 'extract all product names and prices',
  schema: z.object({
    products: z.array(z.object({
      name: z.string().describe('Product name'),
      price: z.string().describe('Price with currency symbol'),
    }))
  }),
});
```

**When to use:** Structured data extraction from visible page
**Cost:** ~200-500 tokens per extraction
**Note:** v3.2 may return raw DOM — use agent mode for complex extraction

#### `stagehand.observe(options)`
List available actions/elements on the page.

```javascript
const actions = await stagehand.observe({
  instruction: 'find all clickable buttons',
});
// Returns array of possible actions
```

**When to use:** Reconnaissance, understanding page state
**Cost:** ~100-200 tokens

#### `stagehand.agent(options)`
Create an autonomous agent for multi-step tasks.

```javascript
const agent = stagehand.agent({
  modelName: 'openai/gpt-4o-mini',
});

const result = await agent.execute(
  'Go to the reports page, find the monthly report for March, and download it as PDF'
);
```

**When to use:** Complex multi-step tasks, navigation + actions
**Cost:** ~1000-3000 tokens per task
**Best for:** Login flows, multi-page workflows, complex interactions

#### `stagehand.page` (Playwright Page)
Direct access to the Playwright page object.

```javascript
const page = stagehand.page;
await page.goto('https://example.com');
await page.waitForSelector('.loaded');
await page.screenshot({ path: 'screenshot.png' });
const content = await page.content();
```

**When to use:** Deterministic operations (goto, wait, screenshot)
**Cost:** 0 tokens (no AI involved)

## Decision Matrix: Which Method to Use

| Scenario | Method | Why |
|----------|--------|-----|
| Navigate to URL | `page.goto()` | Deterministic, free |
| Click a button | `act()` | Natural language, reliable |
| Fill a form field | `act()` | Handles various input types |
| Extract table data | `extract()` | Returns structured Zod-typed data |
| Complex multi-step flow | `agent()` | Plans and executes autonomously |
| Take screenshot | `page.screenshot()` | Deterministic, free |
| Wait for element | `page.waitForSelector()` | Deterministic, free |
| Scroll the page | `page.evaluate(scroll)` | Deterministic, free |
| Discover page elements | `observe()` | AI-powered reconnaissance |
| Download a file | `page.waitForEvent('download')` | Playwright native |

## Cost Optimization

| Strategy | Savings |
|----------|---------|
| Use `page.*` for navigation instead of `act()` | 100% (0 tokens) |
| Use `extract()` instead of `agent()` for simple data | 60-80% |
| Use `gpt-4o-mini` instead of `gpt-4o` | 90% |
| Batch extractions (extract all at once vs one-by-one) | 50-70% |
| Cache results for repeated runs | 100% on reruns |

## Common Patterns

### Login + Action
```javascript
await page.goto(loginUrl);
await stagehand.act({ action: `type "${email}" in email field` });
await stagehand.act({ action: `type "${pass}" in password field` });
await stagehand.act({ action: 'click sign in button' });
await page.waitForNavigation();
// Now do the actual task...
```

### Paginated Extraction
```javascript
let allData = [];
let hasNext = true;
while (hasNext) {
  const batch = await stagehand.extract({ instruction, schema });
  allData.push(...batch.items);
  try {
    await stagehand.act({ action: 'click the next page button' });
    await page.waitForTimeout(1000);
  } catch {
    hasNext = false;
  }
}
```

### Infinite Scroll
```javascript
let prevHeight = 0;
for (let i = 0; i < maxScrolls; i++) {
  const height = await page.evaluate(() => document.body.scrollHeight);
  if (height === prevHeight) break;
  prevHeight = height;
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(1500);
}
// Now extract all loaded content
```

### File Download
```javascript
const [download] = await Promise.all([
  page.waitForEvent('download'),
  stagehand.act({ action: 'click the download PDF button' }),
]);
await download.saveAs('./downloads/' + download.suggestedFilename());
```

## Known Limitations (v3.2)

1. **CAPTCHA:** Stagehand cannot solve CAPTCHAs automatically
2. **2FA:** Requires manual intervention or pre-authenticated session
3. **Rate limiting:** No built-in rate limiting, add `waitForTimeout()` between actions
4. **Dynamic content:** May need explicit waits for JS-rendered content
5. **extract() in v3.2:** Can return raw DOM instead of clean data — use `agent()` for complex extraction
6. **iframes:** Stagehand methods work on the main frame only — use `page.frameLocator()` for iframes

## Model Selection

| Model | Speed | Quality | Cost | Use When |
|-------|-------|---------|------|----------|
| openai/gpt-4o-mini | Fast | Good | ~$0.001/task | Default, simple tasks |
| openai/gpt-4o | Medium | Excellent | ~$0.01/task | Complex pages, ambiguous UI |
| openai/gpt-4.1 | Medium | Excellent | ~$0.01/task | Latest, best quality |

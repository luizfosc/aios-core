# Pattern: file-download

**Category:** Actions
**When to use:** Need to download a file (PDF, CSV, Excel, etc.)
**Stagehand mode:** act + Playwright download event
**Tested:** Yes (2026-03-19)

## Code

```javascript
// Pattern: file-download
// Prerequisite: page already at the page with download link/button
async function downloadFile(stagehand, page, { clickDescription, outputDir }) {
  const { mkdirSync } = await import('node:fs');
  const { resolve } = await import('node:path');

  mkdirSync(outputDir, { recursive: true });

  const [download] = await Promise.all([
    page.waitForEvent('download', { timeout: 60000 }),
    stagehand.act({ action: clickDescription }),
  ]);

  const filename = download.suggestedFilename();
  const filePath = resolve(outputDir, filename);
  await download.saveAs(filePath);

  console.log(`Downloaded: ${filePath}`);
  return filePath;
}
```

## Usage Example

```javascript
const path = await downloadFile(stagehand, page, {
  clickDescription: 'click the download PDF button',
  outputDir: './downloads',
});
```

## Notes
- `Promise.all` is critical — register download event BEFORE clicking
- timeout of 60s accounts for slow downloads
- Some sites open download in new tab — may need `page.context().waitForEvent('page')`
- For authenticated downloads, ensure login pattern ran first

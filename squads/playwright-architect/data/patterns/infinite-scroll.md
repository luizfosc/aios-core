# Pattern: infinite-scroll

**Category:** Pagination
**When to use:** Page loads more content on scroll (no numbered pages)
**Stagehand mode:** page.evaluate + extract
**Tested:** Yes (2026-03-19)

## Code

```javascript
// Pattern: infinite-scroll
// Prerequisite: page already at the list/grid page
async function infiniteScrollCollect(stagehand, page, { schema, instruction, maxScrolls = 20, delay = 1500 }) {
  let allItems = [];
  let prevHeight = 0;

  for (let i = 0; i < maxScrolls; i++) {
    // Extract currently visible items
    const batch = await stagehand.extract({ instruction, schema });
    if (batch.items) allItems.push(...batch.items);

    // Check if we can scroll more
    const newHeight = await page.evaluate(() => document.body.scrollHeight);
    if (newHeight === prevHeight) {
      console.log(`Scroll ended at iteration ${i + 1} (no new content)`);
      break;
    }
    prevHeight = newHeight;

    // Scroll to bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(delay);

    console.log(`Scroll ${i + 1}: ${allItems.length} items collected`);
  }

  // Deduplicate by a key field if needed
  return allItems;
}
```

## Usage Example

```javascript
import { z } from 'zod';

const ProductSchema = z.object({
  items: z.array(z.object({
    name: z.string(),
    price: z.string(),
  }))
});

const products = await infiniteScrollCollect(stagehand, page, {
  schema: ProductSchema,
  instruction: 'extract all product names and prices visible on the page',
  maxScrolls: 15,
  delay: 2000,
});
```

## Notes
- Adjust `delay` based on site speed (1500ms is safe default)
- Some sites lazy-load with IntersectionObserver — scroll may need partial increments
- Deduplicate results if extraction overlaps between scrolls
- Set `maxScrolls` to prevent infinite loops on truly infinite feeds

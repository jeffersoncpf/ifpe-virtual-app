const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [dir, ...jobs] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage();
  for (const j of jobs) { const [src, out, w, h, transparent] = j.split(':');
    const svg = fs.readFileSync(path.join(dir, src), 'utf8');
    await p.setViewportSize({ width: +w, height: +h });
    await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace(/width="[\d.]+" height="[\d.]+"/, `width="${w}" height="${h}"`)}</body></html>`);
    await p.screenshot({ path: out, omitBackground: transparent === 't', clip: { x: 0, y: 0, width: +w, height: +h } });
  } await b.close(); })();

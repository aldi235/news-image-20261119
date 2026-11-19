// Entry program for the news-image-20261119 bounty (Node 22, stdlib only).
// The front page is drawn ahead of time by draw_news.py and stored as
// entry.png next to this file; this program copies it to the grader's
// output directory. Locally, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));

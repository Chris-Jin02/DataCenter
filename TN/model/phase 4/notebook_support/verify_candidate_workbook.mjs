import fs from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
const require = createRequire(`${process.env.CODEX_NODE_MODULES}/package.json`);
const { FileBlob, SpreadsheetFile } = require("@oai/artifact-tool");

const phase4 = fileURLToPath(new URL("../", import.meta.url));
const results = `${phase4}results`;
const file = await FileBlob.load(`${results}/TN-DC-1.0.0_candidate_ranking.xlsx`);
const workbook = await SpreadsheetFile.importXlsx(file);
const table = await workbook.inspect({ kind: "table", range: "Candidate ranking!A1:R18", include: "values,formulas", tableMaxRows: 18, tableMaxCols: 18 });
const errors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 50 }, summary: "formula error scan" });
console.log(table.ndjson);
console.log(errors.ndjson);

import fs from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
const require = createRequire(`${process.env.CODEX_NODE_MODULES}/package.json`);
const { SpreadsheetFile, Workbook } = require("@oai/artifact-tool");

const phase4 = fileURLToPath(new URL("../", import.meta.url));
const results = `${phase4}results`;
const source = await fs.readFile(`${results}/TN-DC-1.0.0_candidate_ranking.csv`, "utf8");
const workbook = await Workbook.fromCSV(source, { sheetName: "Candidate details" });
const details = workbook.worksheets.getItem("Candidate details");
const raw = details.getUsedRange();
const values = raw.values;
const headers = values[0];
const index = new Map(headers.map((header, i) => [header, i]));
const selected = [
  "candidate_rank", "site_id", "site_name", "candidate_type", "candidate_confidence", "latitude", "longitude",
  "final_score", "final_raw_score", "score_p05", "score_p95", "score_iqr", "grid_regime", "regime_distance",
  "novelty_flag", "review_band", "external_score_notice", "required_diligence_checks",
];
const labels = {
  candidate_rank: "Rank", site_id: "ID", site_name: "Candidate", candidate_type: "Type", candidate_confidence: "Confidence",
  latitude: "Latitude", longitude: "Longitude", final_score: "Final score", final_raw_score: "Raw score",
  score_p05: "P05", score_p95: "P95", score_iqr: "IQR", grid_regime: "Regime", regime_distance: "Regime distance",
  novelty_flag: "Novelty", review_band: "Review band", external_score_notice: "External-score note", required_diligence_checks: "Required diligence",
};
const numeric = new Set(["candidate_rank", "latitude", "longitude", "final_score", "final_raw_score", "score_p05", "score_p95", "score_iqr", "regime_distance"]);
const typed = (name, value) => numeric.has(name) && value !== "" ? Number(value) : value;
for (const name of numeric) {
  const col = index.get(name);
  if (col !== undefined) details.getRangeByIndexes(1, col, values.length - 1, 1).values = values.slice(1).map(row => [typed(name, row[col])]);
}
const ranking = workbook.worksheets.add("Candidate ranking");
ranking.getRange("A1").values = [["Candidate ranking — TN-DC-1.0.0"]];
ranking.getRange("A2").values = [["External score exercise only. Candidate records are not model accuracy evidence."]];
ranking.getRangeByIndexes(3, 0, 1, selected.length).values = [selected.map(name => labels[name])];
ranking.getRangeByIndexes(4, 0, values.length - 1, selected.length).values = values.slice(1).map(row => selected.map(name => typed(name, row[index.get(name)] ?? "")));

const font = { name: "Arial", size: 10 };
for (const sheet of [details, ranking]) {
  sheet.showGridLines = false;
  sheet.getUsedRange().format.font = font;
}
details.getRangeByIndexes(0, 0, 1, headers.length).format = { fill: "#1F4E78", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" } };
details.freezePanes.freezeRows(1);
details.getUsedRange().format.autofitColumns();
details.getUsedRange().format.autofitRows();
ranking.getRange("A1").format = { font: { name: "Arial", size: 14, bold: true, color: "#111827" } };
ranking.getRange("A2").format = { font: { name: "Arial", size: 10, italic: true, color: "#4B5563" } };
ranking.getRangeByIndexes(3, 0, 1, selected.length).format = { fill: "#1F4E78", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" } };
ranking.getRangeByIndexes(3, 0, 1, selected.length).format.wrapText = true;
ranking.getRangeByIndexes(3, 0, 1, selected.length).format.rowHeightPx = 32;
const rankingTableRange = ranking.getRangeByIndexes(3, 0, values.length, selected.length);
const rankingDataRange = ranking.getRangeByIndexes(4, 0, values.length - 1, selected.length);
ranking.freezePanes.freezeRows(4);
rankingTableRange.format.autofitColumns();
for (const [name, width] of [["site_name", 230], ["candidate_type", 220], ["external_score_notice", 300], ["required_diligence_checks", 300]]) {
  ranking.getRangeByIndexes(3, selected.indexOf(name), values.length, 1).format.columnWidthPx = width;
}
rankingDataRange.format.wrapText = true;
rankingTableRange.format.autofitRows();
for (const name of ["candidate_rank", "final_score", "final_raw_score", "score_p05", "score_p95", "score_iqr", "regime_distance"]) {
  const col = index.get(name);
  if (col !== undefined) details.getRangeByIndexes(1, col, values.length - 1, 1).format.numberFormat = "0.00";
  const rankCol = selected.indexOf(name);
  if (rankCol >= 0) ranking.getRangeByIndexes(4, rankCol, values.length - 1, 1).format.numberFormat = "0.00";
}
ranking.getRangeByIndexes(4, selected.indexOf("candidate_rank"), values.length - 1, 1).format.numberFormat = "0";
ranking.getRangeByIndexes(4, selected.indexOf("final_score"), values.length - 1, 1).conditionalFormats.add("colorScale", { colors: ["#EFF6FF", "#FDE68A", "#B91C1C"], thresholds: ["min", { type: "percentile", value: 50 }, "max"] });
rankingTableRange.format.borders = { preset: "outside", style: "thin", color: "#CBD5E1" };
ranking.tables.add(`A4:R${values.length + 3}`, true, "CandidateRankingTable");

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${results}/TN-DC-1.0.0_candidate_ranking.xlsx`);

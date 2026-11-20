// Parses the CSV report returned by the API: File,Cell,<smell columns...>
// File names may be quoted (they can contain commas).
export function parseReport(text) {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  if (lines.length === 0) return { smells: [], rows: [] };

  const [header, ...body] = lines.map(splitCsvLine);
  const smells = header.slice(2);
  const rows = body.map(([file, cell, ...flags]) => ({
    file,
    cell: Number(cell),
    smells: smells.filter((_, i) => flags[i] === '1'),
  }));
  return { smells, rows };
}

function splitCsvLine(line) {
  const values = [];
  let current = '';
  let quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (quoted) {
      if (ch === '"' && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        current += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      values.push(current);
      current = '';
    } else {
      current += ch;
    }
  }
  values.push(current);
  return values;
}

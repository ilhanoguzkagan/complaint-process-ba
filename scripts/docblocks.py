"""Write generated content between <!-- NAME:START --> / <!-- NAME:END --> markers so docs never drift from outputs."""


def replace_block(path, name, body):
    text = path.read_text()
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    i, j = text.index(start) + len(start), text.index(end)
    path.write_text(text[:i] + "\n" + body.strip() + "\n" + text[j:])


def md_table(df):
    rows = [list(df.columns)] + df.astype(str).values.tolist()
    lines = ["| " + " | ".join(r) + " |" for r in rows]
    lines.insert(1, "|" + "---|" * len(df.columns))
    return "\n".join(lines)

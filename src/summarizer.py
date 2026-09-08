import re


def build_prompt(ctx: dict) -> str:
    return f"""You are a data quality assistant.
Summarise this dataset profile in exactly 3 sentences,
then give 1 recommended action.

Use ONLY the numbers provided. Do NOT invent any column name,
count or percentage that is not in the input.
Write "not available" for anything missing. No speculation.

Dataset : {ctx['name']}
Rows : {ctx['rows']} Columns: {ctx['cols']}
Worst missing : {ctx['worst_missing']}
Outlier counts: {ctx['outliers']}
Changed since last run: {ctx['changed']}
"""


def verify(summary: str, ctx: dict) -> bool:
    """Check every number in `summary` exists in `ctx`.

    KNOWN LIMIT: this only verifies numbers, not column names.
    A summary could reference a column that doesn't exist and
    still pass, as long as it contains no invented numbers.
    Reliably detecting a fabricated column name via plain text
    matching is unreliable (English words overlap with column
    names), so this is intentionally out of scope for now.
    """
    allowed_numbers = set()
    for value in ctx.values():
        for n in re.findall(r"\d[\d,\.]*", str(value)):
            allowed_numbers.add(n)

    for n in re.findall(r"\d[\d,\.]*", summary):
        if n not in allowed_numbers:
            return False

    return True


def summarize(ctx: dict, llm_client) -> str:
    prompt = build_prompt(ctx)
    try:
        summary = llm_client.generate(prompt)
    except Exception:
        return str(ctx)

    if verify(summary, ctx):
        return summary
    return str(ctx)

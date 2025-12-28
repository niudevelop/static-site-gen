def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
        if line.startswith("##"):
            continue
    raise Exception("No h1 header found")

def strip_lines(string: str, symbols: str = None) -> str:
    return "\n".join([line.strip(symbols) for line in string.split("\n")])

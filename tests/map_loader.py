def load_movingai_map(path):
    grid = []
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip("\n")

            # Skip header lines
            if line.startswith("type") or \
               line.startswith("height") or \
               line.startswith("width") or \
               line.startswith("map"):
                continue

            if not line:
                continue

            # '.' = walkable (0)
            # anything else = blocked (1)
            grid.append([0 if c == '.' else 1 for c in line])

    return grid

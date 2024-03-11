from random import sample


def format_raw_file():
    names_list = [
        name.rstrip("\n") if "-" not in name else ""
        for name in open("resources/raw.txt", "r").readlines()
    ]

    names_list = list(filter(lambda x: x, names_list))  # remove empty strings

    with open("resources/raw.txt", "w") as f:
        f.write("\n".join(names_list))


def generate_names(n: int) -> None:
    # ─── Generating Lists ─────────────────────────────────────────────────────────────────────────────────────────

    names_list = [
        name.rstrip("\n") for name in open("resources/raw.txt", "r").readlines()
    ]
    reserved_names = sample(names_list, n)

    # Removing words that are reserved
    for name in reserved_names:
        names_list.remove(name)

    # ─── Saving Files ─────────────────────────────────────────────────────────────────────────────────────────────

    with open("resources/names.txt", "w") as f:
        f.write("\n".join(names_list))

    with open("resources/reserved_names.txt", "w") as f:
        f.write("\n".join(reserved_names))


if __name__ == "__main__":
    generate_names(1000)

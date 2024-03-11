import base64
import os
import random
import string


def generate_random_string(number: int = 1, length: int = 10):
    """
    Generates a random string or a list of random strings.

    Args:
        number (int): The number of random strings to generate. Defaults to 1.
        length (int): The length of each random string. Defaults to 10.

    Returns:
        list: A list of random strings if number > 1, otherwise a single random string.
    """
    output = []
    for _ in range(number):
        output.append(
            "".join(
                random.choices(
                    string.ascii_lowercase + string.ascii_uppercase, k=length
                )
            )
        )
    return output


def generate_random_number(number: int = 1, length: int = 10):
    """
    Generate random number strings.

    Args:
        number (int): The number of random number strings to generate. Defaults to 1.
        length (int): The length of each random number string. Defaults to 10.

    Returns:
        list: A list of random number strings if number > 1, otherwise a single random number string.
    """
    output = []
    for _ in range(number):
        output.append("".join(random.choices([str(i) for i in range(1, 10)], k=length)))
    return output


def multi_encode(text: str, n: int) -> str:
    if n > 0:
        try:
            text = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        except AttributeError:
            text = base64.b64encode(text).decode("utf-8")
        return multi_encode(text, n - 1)
    else:
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def multi_decode(text: str, n: int) -> str:
    if n > 0:
        try:
            text = base64.b64decode(text.encode("utf-8")).decode("utf-8")
        except AttributeError:
            text = base64.b64decode(text).decode("utf-8")
        return multi_decode(text, n - 1)
    else:
        return base64.b64decode(text.encode("utf-8")).decode("utf-8")


def obfuscate_code(code: str, raw: str, step: int) -> str:
    ENCODE_LAYERS = 4

    fillers_types = {
        "var_str": 4,
        "var_int": 2,
        "const_str": 4,
        "const_int": 2,
        "comment": 1,
        "empty_line": 1,
    }

    # ─── Fillers Parameters ───────────────────────────────────────────────────────────────────────────────────────

    filler_names = open("resources/names.txt", "r").read().splitlines()
    min_filler_size = len(raw) // 10
    max_filler_size = int(min_filler_size * 1.2)
    target_size = len(
        multi_encode(
            generate_random_string(
                number=1, length=random.randint(min_filler_size, max_filler_size)
            )[0],
            n=ENCODE_LAYERS,
        )
    )
    filler_count = max(
        (
            len(raw)
            // len(
                multi_encode(
                    generate_random_string(
                        number=1,
                        length=random.randint(min_filler_size, max_filler_size),
                    )[0],
                    n=ENCODE_LAYERS,
                )
            )
        )
        * ((step + 2) ** 2),
        15,
    )

    fillers = []

    # ─── Generating Fillers ───────────────────────────────────────────────────────────────────────────────────────

    for _ in range(filler_count):
        current_type = random.choices(
            list(fillers_types.keys()), weights=list(fillers_types.values())
        )[0]
        if current_type == "var_str":
            name = f"{random.choice(filler_names)}_{str(random.randint(2, 999))}"
            value = str.encode(
                generate_random_string(
                    number=1, length=random.randint(min_filler_size, max_filler_size)
                )[0]
            )
            fillers.append(name)

            if random.choices([True, False], weights=[0.2, 0.8])[0]:
                comment = str.encode(
                    generate_random_string(
                        number=1,
                        length=random.randint(min_filler_size, max_filler_size),
                    )[0]
                )
                code += f"\n{name} = base64.b64decode('{multi_encode(value, n=ENCODE_LAYERS)}').decode(\"utf-8\") #{comment}"
            else:
                code += f"\n{name} = base64.b64decode('{multi_encode(value, n=ENCODE_LAYERS)}').decode(\"utf-8\")"

        elif current_type == "var_int":
            name = f"{random.choice(filler_names)}_{str(random.randint(2, 999))}"
            value = generate_random_number(number=1, length=random.randint(3, 9))[0]
            # fillers.append(name)

            if random.choices([True, False], weights=[0.2, 0.8])[0]:
                comment = str.encode(
                    generate_random_string(
                        number=1,
                        length=random.randint(min_filler_size, max_filler_size),
                    )[0]
                )
                code += f"\n{name} = {value} #{comment}"
            else:
                code += f"\n{name} = {value}"

        elif current_type == "const_str":
            name = (
                f"{random.choice(filler_names).upper()}_{str(random.randint(2, 999))}"
            )
            value = str.encode(
                generate_random_string(
                    number=1, length=random.randint(min_filler_size, max_filler_size)
                )[0]
            )
            fillers.append(name)

            if random.choices([True, False], weights=[0.2, 0.8])[0]:
                comment = str.encode(
                    generate_random_string(
                        number=1,
                        length=random.randint(min_filler_size, max_filler_size),
                    )[0]
                )
                code += f"\n{name} = base64.b64decode('{multi_encode(value, n=ENCODE_LAYERS)}').decode(\"utf-8\") #{comment}"
            else:
                code += f"\n{name} = base64.b64decode('{multi_encode(value, n=ENCODE_LAYERS)}').decode(\"utf-8\")"

        elif current_type == "const_int":
            name = (
                f"{random.choice(filler_names).upper()}_{str(random.randint(2, 999))}"
            )
            value = generate_random_number(number=1, length=random.randint(3, 9))[0]
            # fillers.append(name)

            if random.choices([True, False], weights=[0.2, 0.8])[0]:
                comment = str.encode(
                    generate_random_string(
                        number=1,
                        length=random.randint(min_filler_size, max_filler_size),
                    )[0]
                )
                code += f"\n{name} = {value} #{comment}"
            else:
                code += f"\n{name} = {value}"

        elif current_type == "comment":
            for _ in range(random.randint(1, 5)):
                comment = generate_random_string(
                    number=1, length=random.randint(min_filler_size, max_filler_size)
                )[0] + ("=" * random.randint(0, 3))
                code += f"\n# {comment}"
        elif current_type == "empty_line":
            code += "\n" * random.randint(1, 3)

    # ─── Splitting Code ───────────────────────────────────────────────────────────────────────────────────────────

    reserved_names = open("resources/reserved_names.txt", "r").read().split("\n")
    code_list = code.split("\n")

    values = [raw[i : i + target_size] for i in range(0, len(raw), target_size)]
    names = [
        f"{var_name}_{str(random.randint(2, 999))}"
        for var_name in random.choices(reserved_names, k=len(values))
    ]
    vars = names.copy()

    for _ in range(len(names)):
        code_list.insert(
            random.randint(len(code_list) // 2, len(code_list)),
            f"{names.pop(0)} = base64.b64decode('{multi_encode(values.pop(0), n=2)}').decode(\"utf-8\")",
        )

    # ─── Joining Code ─────────────────────────────────────────────────────────────────────────────────────────────

    code = "\n".join(code_list)
    queue = ["filler"] * min(len(vars), 10)
    queue.insert(random.randint(1, len(queue)), "code")
    for step in queue:
        if step == "code":
            name = f"{random.choice(reserved_names)}_{str(random.randint(2, 999))}_{str(random.randint(2, 999))}"
            real_code = " + ".join(
                [
                    f'base64.b64decode(base64.b64decode({var})).decode("utf-8")'
                    for var in vars
                ]
            )

            code += f"""
{name} = {real_code}
try:
    exec(compile({name}, "<string>", "exec"))
except NameError:
    try:
        {name} = base64.b64decode({name}).decode("utf-8")
        {name} = base64.b64decode({name}).decode("utf-8")
    except UnicodeDecodeError:
        pass
    ...
except SyntaxError:
    ..."""
            code_list.append(f"{name} = {real_code}")
            code_list.append(f'exec(compile({name}, "<string>", "exec"))')
        else:
            name = f"{random.choice(filler_names)}_{str(random.randint(2, 999))}_{str(random.randint(2, 999))}"
            fillers_sample = random.sample(fillers, len(vars))
            filler_code = " + ".join(
                [
                    f'base64.b64decode(base64.b64decode({var})).decode("utf-8")'
                    for var in fillers_sample
                ]
            )
            code += f"""
{name} = {filler_code}
try:
    exec(compile({name}, "<string>", "exec"))
except NameError:
    try:
        {name} = base64.b64decode({name}).decode("utf-8")
        {name} = base64.b64decode({name}).decode("utf-8")
    except UnicodeDecodeError:
        pass
    ...
except SyntaxError:
    ..."""

    return code


def process_file(file: str = "", fill_code: bool = False, **kwargs):
    # ─── Imports ──────────────────────────────────────────────────────────────────────────────────────────────────

    imports = ["import base64"]

    if file == "":
        file = input("[HideMyCode]: Enter file name (without .py): ")
        output_file = file + "_HideMyCode.py"
        raw = open(file + ".py", "rb").readlines()
    else:
        output_file = file.rstrip(".py") + "_HideMyCode.py"
        raw = open(file, "rb").readlines()
    if os.path.exists(output_file):
        os.remove(output_file)

    for i, line in enumerate(raw.copy()):
        if "import" in line.decode("utf-8"):
            if "base64" in line.decode("utf-8"):
                continue
            imports.append(line.decode("utf-8").rstrip("\n"))
        else:
            raw = b"".join(raw[i:])
            break

    # ─── Code ─────────────────────────────────────────────────────────────────────────────────────────────────────

    if fill_code:
        FILLER_STEPS = kwargs.get("filler_steps", 2)
        ENCODE_STEPS = kwargs.get("encode_steps", 2)

        for step in range(FILLER_STEPS):
            code = ""
            code = obfuscate_code(code, raw, step)
            raw = code
        for step in range(ENCODE_STEPS):
            raw = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
            code = f'''
raw_code = """{raw}"""

eval(compile(base64.b64decode(raw_code),"<string>","exec"))'''
            raw = code

    else:
        raw = base64.b64encode(raw).decode("utf-8")
        code = f'''
raw_code = """{raw}"""

eval(compile(base64.b64decode(raw_code),"<string>","exec"))'''

    # ─── Saving File ──────────────────────────────────────────────────────────────────────────────────────────────

    imports_str = "\n".join(imports)
    code = imports_str + code

    with open(output_file, "w") as f:
        f.write(code)

    # ─── Formatting Output ────────────────────────────────────────────────────────────────────────────────────────

    try:
        import subprocess

        subprocess.run(["black", output_file])
    except Exception:
        pass

    print("[HideMyCode]: File generated successfully.")


if __name__ == "__main__":
    process_file("examples/example_0.py", fill_code=True, filler_steps=2, encode_steps=2)

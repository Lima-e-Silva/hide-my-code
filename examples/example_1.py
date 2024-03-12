from time import sleep

import numpy as np
from toolboxy import delay_print

if __name__ == "__main__":
    array_0 = np.random.randint(0, 5, (3, 3))
    array_1 = np.random.randint(0, 5, (3, 3))

    delay_print(
        "Obfuscation is the obscuring of the intended meaning of communication by making the message difficult to understand, usually with confusing and ambiguous language.",
        wpm=350,
    )
    delay_print(
        "This code is an example of obfuscation. The algorithm is calculating the inverse of the two arrays below:",
        wpm=350,
    )

    sleep(1)

    print(array_0)
    sleep(0.5)
    print(array_1)

    delay_print(
        "Of course you cannot see this happening in the code due to obfuscation.",
        wpm=350,
    )
    delay_print("The inverse matrix of the two arrays above are:", wpm=350)

    try:
        print(np.linalg.inv(array_0))
        print(np.linalg.inv(array_1))
    except np.linalg.LinAlgError:
        delay_print(
            "Wow ... i feel a little embarrassed right now... One of the arrays is a singular matrix. So i cannot calculate the inverse (Math's fault). Try again.",
            wpm=350,
        )

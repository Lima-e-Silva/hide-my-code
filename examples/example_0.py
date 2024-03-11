from random import randint
import toolboxy as tb

def main():
    random_number_0 = randint(1, 100)
    random_number_1 = randint(1, 100)

    text = f"""First number: {random_number_0}\nSecond number: {random_number_1}\nSum: {random_number_0 + random_number_1}"""
    tb.delay_print(text)

if __name__ == "__main__":
    main()
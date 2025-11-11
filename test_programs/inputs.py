def main():
    """
            Main menu:
            1) Add two values
            2) Multiply two values
            3) Divide two values
    """

    choice = int(input())
    value1 = int(input())
    value2 = int(input())

    if choice == 1:
        print(value1 + value2)
        return
    elif choice == 2:
        print(value1 * value2)
        return
    elif choice == 3:
        print(value1 / value2)
        return

    # loop indefinitely to ensure inputs work properly
    while True:
        continue


if __name__ == '__main__':
    main()

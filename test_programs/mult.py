from Class import RandomClass


def main():
    value = 10
    rc = RandomClass(10)
    rc.multiply(10)
    print(rc.value)
    rc.reset_val()
    print(rc.value)
    for i in range(1000):
        rc.add(1)
    print(rc.value)


if __name__ == '__main__':
    main()

def main():
    size = 8
    start = [1 for _ in range(0, size)]

    for _ in range(1, 255):
        for i in range(size):
            for j in range(20, 255):
                start[i] = j
                try:
                    print(bytes(start).decode("UTF-8"))
                except UnicodeDecodeError:
                    pass


main()
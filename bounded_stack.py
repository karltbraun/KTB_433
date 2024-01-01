from collections import deque

DEFAULT_MAX_STACK_SIZE = 10


class BoundedStack:
    def __init__(self, stacksize=DEFAULT_MAX_STACK_SIZE):
        self.container = deque(maxlen=stacksize)

    def __len__(self):
        return len(self.container)

    def push(self, item):
        self.container.append(item)

    def pop(self):
        value = None
        if self.size() > 0:
            value = self.container.pop()
        return value

    def get_all(self):
        return list(self.container)

    def clear(self):
        items = self.get_all()
        self.container.clear()
        return items


# ########################### MAIN #########################


def main() -> int:
    stk = BoundedStack()

    # test 1
    print("------ test 1 ------")

    for i in range(DEFAULT_MAX_STACK_SIZE - 1):
        stk.push(i)

    print(f"Pop from stack: {stk.pop()}")
    print(f"Pop from stack: {stk.pop()}")
    print(f"Pop from stack: {stk.pop()}")

    # test 2
    print("------ test 2 ------")

    for i in range(DEFAULT_MAX_STACK_SIZE):
        stk.push(i)

    print(f"Pop from stack: {stk.pop()}")
    print(f"Pop from stack: {stk.pop()}")
    print(f"Pop from stack: {stk.pop()}")

    # test 3
    print("------ test 3 ------")

    for i in range(DEFAULT_MAX_STACK_SIZE):
        stk.push(i)

    print(f"Size of stack: {stk.size()}")

    print(f"Last value: {stk.pop()}")
    print(f"Size of stack: {stk.size()}")
    print(f"Last value: {stk.pop()}")
    print(f"Size of stack: {stk.size()}")

    # test 4
    print("------ test 4 ------")

    for i in range(DEFAULT_MAX_STACK_SIZE):
        stk.push(i)

    print(f"Size of stack: {stk.size()}")

    lst_stk = stk.get_all()
    print(f"List of stack ({len(lst_stk)}):\n\t{lst_stk}")

    lst_stk = stk.clear()
    print(f"List from stack ({len(lst_stk)}):\n\t{lst_stk}")
    print(f"Size of stack: {stk.size()}")

    print(f"Popping from empty stack: {stk.pop()}")

    return 0


if __name__ == "__main__":
    exit(main())

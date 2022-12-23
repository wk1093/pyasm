from pyasm import *


def main(p):
    # for i in range(10):
    #     p.printf(str(i) + " ")
    # p.puts("")

    p.mov(ecx, 10)
    p.label("startofloop")
    p.printf("A")
    p.dec(ecx)
    p.jnz("startofloop")

    return 0


if __name__ == "__main__":
    pr = AsmProgram("testprog")         # Creates a program called testprog (a program always has an assembly main function)
    pr.run(main, True)                        # Generates assembly code and runs it

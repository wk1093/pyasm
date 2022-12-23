from pyasm import *


def main(p):
    # for i in range(10):
    #     p.printf(str(i) + " ")
    # p.puts("")
    p.mov(r8, 10)
    p.printreg(r8)
    p.printf(" ")
    p.printreg(r8)
    # p.label("startofloop")
    # p.puts("A")
    # p.dec(r8)
    # p.jnz("startofloop")

    return 0


if __name__ == "__main__":
    pr = AsmProgram("testprog")         # Creates a program called testprog (a program always has an assembly main function)
    pr.run(main, True)                        # Generates assembly code and runs it

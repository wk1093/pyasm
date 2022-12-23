from pyasm import *  # Used for generating assembly code


def main(p):
    # Generate a basic program based of of example/for10.asm
    fmt = p.variable(CONSTVAR, "%d ")
    p.push(rbp)
    p.lea(rbp, fmt)
    p.push(rbx)
    p.zero(ebx)
    p.sub(rsp, 8)
    loop = p.label()
    p.mov(edx, ebx)
    p.mov(rsi, rbp)
    p.mov(edi, 1)
    p.zero(eax)
    p.call("__printf_chk")
    p.add(ebx, 1)
    p.cmp(ebx, 10)
    p.jnz(loop)
    p.mov(edi, 10)
    p.call("putchar")
    p.add(rsp, 8)
    p.zero(eax)
    p.pop(rbx)
    p.pop(rbp)
    p.ret()


    return 0


if __name__ == "__main__":
    pr = AsmProgram("testprog")         # Creates a program called testprog (a program always has an assembly main function)
    pr.run(main, True)                        # Generates assembly code and runs it

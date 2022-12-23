INITVAR = 0
CONSTVAR = 1


class AsmProgram:
    def __init__(self, name: str):
        self.name = name
        self.data = []      # Initialized data
        self.rodata = []    # Read-only data
        self.text = []      # Code
        self.externs = []   # External functions
        self._print_num = 0
        self._rep_num = 0
        self.decvar = None
    def instruction(self, instruction: str, *args):
        """Adds an instruction to the .text section."""
        self.text.append("\t"+instruction + " " + ", ".join([str(a) for a in args]))
    def label(self, label: str):
        """Adds a label to the .text section."""
        self.text.append(label + ":")
    def val2asm(self, val: any):
        data: str  # the assembly that represents the value
        if type(val) == int:  # dword
            data = "dword " + str(val)
        elif type(val) == str:  # db
            if len(val) > 0:
                data = 'db ' + ", ".join([str(ord(c)) for c in val]) + ", 0"
            else:
                data = "db 0"
        elif type(val) == list:  # list of integers: db
            data = 'db' + ', '.join([int(v) for v in val])
        else:
            raise TypeError("Unsupported ASM type: " + str(type(val)))
        return data


    def variable(self, name: str, type: int, value: any):
        data: str = self.val2asm(value)
        if type == INITVAR:
            self.data.append(name + " " + data)
        elif type == CONSTVAR:
            self.rodata.append(name + " " + data)
        else:
            raise ValueError("Invalid variable type: " + str(type))
    
    def mov(self, dest: str, src: any):
        """Moves a value into a register."""
        self.instruction("mov", dest, src)
    
    def call(self, func: str):
        """Calls a function."""
        self.instruction("call", func)
    
    def loop(self, label: str):
        """Loops to a label."""
        self.instruction("loop", label)
    
    def push(self, reg: str):
        """Pushes a register onto the stack."""
        self.instruction("push", reg)
    
    def pop(self, reg: str):
        """Pops a register off the stack."""
        self.instruction("pop", reg)
    
    def dec(self, reg: str):
        """Decrements a register."""
        self.instruction("dec", reg)
    
    def inc(self, reg: str):
        """Increments a register."""
        self.instruction("inc", reg)
    
    def jnz(self, label: str):
        """Jumps to a label if the zero flag is not set."""
        self.instruction("jnz", label)
    
    def printf(self, string: str):
        """Calls printf with the passed string."""
        if "printf" not in self.externs:  # make sure printf is declared as an external function
            self.externs.append("printf")
        self.variable("_print_"+str(self._print_num), CONSTVAR, string)  # declares a constant string
        self.mov("rdi", "_print_"+str(self._print_num))  # puts the string in rdi
        self.call("printf")  # calls printf
        self._print_num += 1
    
    def printint(self, num: int):
        """Calls printf with the passed integer."""
        if "printf" not in self.externs:
            self.externs.append("printf")
        self.variable("_print_"+str(self._print_num), CONSTVAR, "%d")  # declares a constant string
        self.mov("rdi", "_print_"+str(self._print_num))  # puts the string in rdi
        self.mov("rsi", str(num))  # puts the integer in rsi
        self.call("printf")  # calls printf
        self._print_num += 1
    
    def printreg(self, reg: str):
        """Calls printf with the passed register."""
        if "printf" not in self.externs:
            self.externs.append("printf")
        self.variable("_print_"+str(self._print_num), CONSTVAR, "%d")
        self.mov("rdi", "_print_"+str(self._print_num))
        self.mov("rsi", reg)
        self.call("printf")
        self._print_num += 1
    
    def puts(self, string: str):
        """Calls puts with the passed string."""
        if "puts" not in self.externs:
            self.externs.append("puts")
        self.variable("_print_"+str(self._print_num), CONSTVAR, string)  # declares a constant string
        self.mov("rdi", "_print_"+str(self._print_num))  # puts the string in rdi
        self.call("puts")  # calls puts
        self._print_num += 1

    def _cmp(self):
        code = ""
        if len(self.externs) > 0:
            code += "\n".join(["extern "+f for f in self.externs]) + "\n"
        if len(self.data) > 0:
            code += "\n\t\tsection .data\t;Data\n\n"
            code += "\n".join(self.data) + "\n"
        if len(self.rodata) > 0:
            code += "\n\t\tsection .rodata\t;Read-Only Data\n\n"
            code += "\n".join(self.rodata) + "\n"
        if len(self.text) > 0:
            code += "\n\t\tsection .text\t;Code\n\n"
            code += "global main: function\t;Exposes main function\n"
            code += "main:\n"
            code += "\tenter 0, 0\n\n"
            code += "\n".join(self.text) + "\n"
            code += "\tleave\n"
            code += "\tret\n"
        with open(self.name + ".asm", "w") as f:
            f.write(code)    
    def build(self, func):  # takes a function with 1 argument: the AsmProgram, and returns an integer
        ret = func(self)
        if ret is None:
            ret = 0
        ret = int(ret)
        if ret == 0:
            self.instruction("\n\txor", "eax", "eax", "\t; return 0")
        else:
            self.instruction("\n\tmov", "eax", str(ret), "\t; return " + str(ret))
        
        self._cmp()
    def run(self, func, debug: bool = False):
        self.build(func)
        import os
        os.system("nasm -f elf64 " + self.name + ".asm -o " + "temp.o")
        if not debug:
            os.remove(self.name + ".asm")
        os.system("gcc -no-pie temp.o -o " + self.name)
        if not debug:
            os.remove("temp.o")
        os.system("./" + self.name)


rax = "rax"
rbx = "rbx"
rcx = "rcx"
rdx = "rdx"
rsi = "rsi"
rdi = "rdi"
rsp = "rsp"
rbp = "rbp"
r8 = "r8"
r9 = "r9"
r10 = "r10"
r11 = "r11"
r12 = "r12"
r13 = "r13"
r14 = "r14"
r15 = "r15"

eax = "eax"
ebx = "ebx"
ecx = "ecx"
edx = "edx"
esi = "esi"
edi = "edi"
esp = "esp"
ebp = "ebp"
r8d = "r8d"
r9d = "r9d"
r10d = "r10d"
r11d = "r11d"
r12d = "r12d"
r13d = "r13d"
r14d = "r14d"
r15d = "r15d"


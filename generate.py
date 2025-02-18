from opcodes import MEM, ALU, CMP, PC, OP, STACK, Program, alloc, free, createVar, decompile, startLib, endLib






p = Program()

a = createVar(1)
b = createVar(1)

#p += startLib()
#printNum = p.link(("printRam",), "./printNum.vmxlib")
#p += endLib()

p += MEM.SET8(a, 0)
p += MEM.SET8(b, 255)
target = p.target
p += MEM.CLA()
p += MEM.CLB()
p += MEM.LDBL(a)
p += MEM.LALD(1)
p += ALU.ADD()
p += OP.PRINT()
p += MEM.STAL(a)
p += MEM.LDBL(b)
p += CMP.GE()
t = p.target
p += PC.JMI(0, target)
p += PC.PUSH()
#p += PC.JMP(printNum["printRam"])
p += OP.EXIT(0)




compiled, ramSize = p.compile(0)
print(decompile(compiled))

with open("a", "wb") as f:
	f.write(chr(len(compiled)).encode())
	f.write(chr(ramSize).encode())
	f.write(compiled)
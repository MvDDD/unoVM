from opcodes import MEM, ALU, CMP, PC, OP, STACK, Program, alloc, free, createVar, decompile






p = Program()

counter = createVar(1)
end_value = createVar(1)
printRamStart = p.target
p += MEM.SET8(counter, 0)
p += MEM.SET8(end_value, 255)
loop_start = p.target

p += MEM.LDAL(counter)
p += MEM.LDBL(counter)
p += MEM.LALD(1)
p += ALU.ADD()
p += MEM.LBLA()
p += MEM.SWP()
p += OP.PRINT()
p += MEM.SWP()
p += MEM.STAL(counter)
p += MEM.LDBL(end_value)
p += CMP.GE()
p += PC.JMI(0, loop_start)
p += PC.POP()
free(*counter)
free(*end_value)


compiled = p.genLib(
	(printRamStart, "printRam")
)



print(compiled)
with open("printNum.vmxlib", "wb") as f:
	f.write(compiled)
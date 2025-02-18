from opcodes import MEM, ALU, CMP, PC, OP, Program, alloc, free, createVar
from sys import argv
argv.append("a.asm")

p = Program()

counter = createVar(2)
end_value = createVar(2)

# Initialize counter to 0
p += MEM.SET16(counter, 0)

# Set the loop limit (255)
p += MEM.SET16(end_value, 0xFFFF)

# Start of the loop
loop_start = p.target

# Perform some operation in the loop
p += OP.NOP()  # Replace with any meaningful operation

p += MEM.LDB(counter)
p += MEM.CLA()
p += MEM.LALD(1)
p += ALU.ADD()
p += MEM.STA(counter)
p += MEM.LDB(end_value)
p += CMP.GE()
p += PC.JMI(0, loop_start)

# Cleanup and exit
free(*counter)
free(*end_value)
p += OP.EXIT(0)


print(len(p.data))
compiled, ramSize = p.compile(0)
print(p.compile(0))
with open("a", "wb") as f:
	f.write(chr(len(compiled)).encode())
	f.write(chr(ramSize).encode())
	f.write(compiled)
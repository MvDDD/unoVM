from opcodes import MEM, ALU, CMP, PC, OP, STACK, Program, alloc, free, createVar, decompile
import sys


def split_by_chars(string, arr):
	out = []
	tmp = ""
	for char in string:
		if not char in arr:
			tmp += char
		else:
			if len(tmp) > 0:
				out.append(tmp)
				tmp = ""
	if len(tmp) > 0:
		out.append(tmp)
		tmp = ""
	return out

def compile(data, calcJumps = False, jumps = {}):

	p = Program()
	vars = {}

	def isVar(value):
		if value in vars:
			return 1

	def getSize(var):
		return vars[var].l[1]

	def getAddr(var):
		return vars[var].l[0]

	def isReg(value):
		if value == "A":
			return 1
		return 0

	def isValue(value):
		try:
			int(value)
			return 1
		except:
			return 0


	for line in data:
		print(p.data)
		if line.endswith(":"):
			jumps[line[:-1]] = p.target
			continue
		opcode = line.split(" ")[0].upper()
		args = split_by_chars(" ".join(line.split(" ")[1:]), " ,")
		print(opcode, args)
		match opcode:
			case "VAR":
				if args[0] == "_8":
					vars[args[1]] = createVar(1)
				elif args[0] == "_16":
					vars[args[1]] = createVar(2)
				else:
					vars[args[1]] = createVar(int(args[0]))
			case "FREE":
				free(*vars[args[0]])
			case "MOV":
				source = args[1]
				target = args[0]
				if isReg(target):
					if isVar(source):
						size = getSize(source)
						if target == "A":
							if size == 1:
								p += MEM.CLA()
								p += MEM.LDAL(getAddr(source))
							elif size == 2:
								p += MEM.LDA(getAddr(source))
						else:
							if size == 1:
								p += MEM.CLB()
								p += MEM.LDBL(getAddr(source))
							elif size == 2:
								p += MEM.LDB(getAddr(source))


					elif isValue(source):
						val = int(source)

						if target == "A":
							if val <= 255:
								p += MEM.CLA()
								p += MEM.LALD(int(source))
							elif val > 255:
								p += MEM.LALD(int(source)&0xFF)
								p += MEM.LAHD((int(source) >> 8 )&0xFF)
						else:
							p += STACK.PUSHA()
							if val <= 255:
								p += MEM.CLA()
								p += MEM.LALD(int(source))
							elif val > 255:
								p += MEM.LALD(int(source)&0xFF)
								p += MEM.LAHD((int(source) >> 8 )&0xFF)
							p += MEM.SWP()
							p += STACK.POPA()
				elif isVar(target):
					print("var")
					targetsize = getSize(target)
					if isVar(source):
						p += STACK.PUSHA()
						sourcesize = getSize(source)
						if sourcesize == 1:
							MEM.CLA()
							MEM.LDAL(getAddr(source))
						elif sourcesize == 2:
							MEM.LDA(getAddr(source))
						if targetsize == 1:
							MEM.STAL(getAddr(target))
						elif targetsize == 2:
							MEM.STAH(getAddr(target))
						p += STACK.POPA()
					elif isValue(source):
						val = int(source)
						if getSize(target) == 1:
							p += MEM.SET8(getAddr(target), val)
						elif getSize(target) == 2:
							p += MEM.SET16(getAddr(target), val)
					elif isReg(source):
						if source == "A":
							if targetsize == 1:
								MEM.STAL(getAddr(target))
							elif targetsize == 2:
								MEM.STA(getAddr(target))
						elif source == "B":
							if targetsize == 1:
								MEM.STBL(getAddr(target))
							elif targetsize == 2:
								MEM.STB(getAddr(target))



			case "CMP":
				pass
			case "ADD" | "SUB" | "MOD" | "SHL" | "SHR" | "AND" | "OR" | "NOT" | "XOR" | "NAND" | "NOR" | "XNOR" | "MSK" | "DIV" | "MULT":
				if isReg(args[0]) and isReg(args[1]):
					if args[0] == "A":
						if args[1] == "B":
							p += getattr(ALU, op)()
						elif args[1] == "A":
							p += STACK.PUSHB()
							p += STACK.PUSHA()
							p += STACK.POPB()
							p += getattr(ALU, op)()
							p += STACK.POPB()
					elif args[0] == "B":
						if args[1] == "A":
							p += STACK.PUSHA()
							p += getattr(ALU, op)()
							p += MEM.SWP()
							p += MEM.POPA()
						if args[1] == "B":
							p += STACK.PUSHA()
							p += STACK.PUSHB()
							p += STACK.POPA()
							p += getattr(ALU, op)()
							p += STACK.POPA()

				if isVar(target):
					pass
			case "JMP" | "JMI" | "CALL":
				if calcJumps:
					if opcode == "JMP":
						p += PC.JMP(0)
					if opcode == "JMI":
						p += PC.JMI(1, 0)
				else:
					if opcode == "JMP":
						p += PC.JMP(jumps[args[0]])
					if opcode == "JMI":
						p += PC.JMI(1, jumps[args[0]])
			case "PRINT":
				pass
			case "PUSH" | "POP":
				if opcode == "PUSH":
					if args[0] == "A":
						p += STACK.PUSHA()
					elif args[0] == "B":
						p += STACK.PUSHB()
					elif isVar(args[0]):
						size = getSize(args[0])
						addr = getSize(args[0])
						tmp = alloc(2)
						p += MEM.STA(tmp)
						if size == 1:
							p += MEM.LDAL(addr)
						elif size == 2:
							p += MEM.LDA(addr)
						p += STACK.PUSHA()
						p += MEM.LDA(tmp)
						free(tmp, 2)
				elif opcode == "POP":
					if args[0] == "A":
						p += STACK.POPA()
					elif args[0] == "B":
						p += STACK.POPB()
					elif isVar(args[0]):
						size = getSize(args[0])
						addr = getSize(args[0])
						tmp = alloc(2)
						p += MEM.STA(tmp)
						if size == 1:
							p += MEM.LDAL(addr)
						elif size == 2:
							p += MEM.LDA(addr)
						p += STACK.PUSHA()
						p += MEM.LDA(tmp)
						free(tmp, 2)
						
			case "CALL":
				p += PC.PUSH()
				if calcJumps:
					p += PC.JMP(0)
				else:
					jumps[args[0]]
			case "RET":
				p += PC.POP()

			case "CLEAR":
				p += OP.CLEAR()
			case "EXIT":
				p += OP.EXIT(int(args[0][2:], 16) if args[0].startswith("0x") else int(args[0]))
			case _:
				p += [l for l in line.encode()]
	p += OP.EXIT(0)
	if calcJumps:
		return jumps
	else:
		return p.compile(0)


sys.argv.append("./a.asm")
f = open(sys.argv[1], "r")
data = f.read()
f.close()

new = ""
cmt = 0
i = 0
while i < len(data):
	if data[i] == "/" and data[i+1]=="*":
		cmt = 1
		i += 2
	elif data[i] == "*" and data[i+1]=="/":
		cmt = 0
		i += 2
	else:
		if not cmt:
			new += data[i]
		i += 1

data = new
data = data.split("\n")
data = [line.split(";")[0].strip() for line in data if len(line.split(";")[0].strip())>0]
data = [line.split("//")[0].strip() for line in data if len(line.split("//")[0].strip())>0]
jumps = compile(data, True)

compiled, ramSize = compile(data, False, jumps)

print(decompile(compiled))

with open("a", "wb") as f:
	f.write(chr(len(compiled)).encode())
	f.write(chr(ramSize).encode())
	f.write(compiled)

class StaticOrPropertyMeta(type):
	def __new__(mcs, name, bases, dct):
		dct = {
			key: staticmethod(value) 
			if callable(value) else value 
			for key, value in dct.items()
		}

		return super().__new__(mcs, name, bases, dct)



# Base class for operations
class STATIC(metaclass=StaticOrPropertyMeta):
	pass

def generate_opcode():
	global opcode_counter
	op_code = opcode_counter
	opcode_counter += 1
	return op_code

opcode_counter = 0

def val8(val):
	if val>255:
		raise TypeError(f"addr {val} > 255")

def convert_to_val(val):
	if callable(val):
		return val()  # If the value is callable, call it
	elif isinstance(val, (list, tuple)):
		return val[0]  # If the value is a list or tuple, return the first element
	elif isinstance(val, (int, float)):
		return val  # If the value is an integer or float, return it as is
	else:
		raise TypeError(f"{type(val)} is not a valid value")  # Raise an error for unsupported types

def startLib():
	return "STARTLIB"
def endLib():
	return "ENDLIB"

class MEM(STATIC):
	(
		CLA_opcode, LDAL_opcode, LDAH_opcode, LDA_opcode, STAL_opcode, STAH_opcode, STA_opcode,
		CLB_opcode, LDBL_opcode, LDBH_opcode, LDB_opcode, STBL_opcode, STBH_opcode, STB_opcode,
		LALD_opcode, LAHD_opcode, LBLA_opcode, LBHA_opcode, LBA_opcode, SBLA_opcode, SBHA_opcode, SBA_opcode, SET8_opcode, SET16_opcode, SWP_opcode,
	) = [generate_opcode() for _ in range(25)]
	def CLA():
		"clear reg A"
		return [MEM.CLA_opcode]
	def LDAL(addr):
		"load Al from ram"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.LDAL_opcode, addr]
	def LDAH(addr):
		"load Ah from ram"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.LDAH_opcode, addr]
	def LDA(addr): 
		"load A as int16 from ram (BE)"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.LDA_opcode, addr]
	def STAL(addr):
		"store Al to ram"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.STAL_opcode, addr]
	def STAH(addr):
		"store Ah to ram"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.STAH_opcode, addr]
	def STA(addr):
		"store A as int16 to ram (BE)"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.STA_opcode, addr]
	def CLB():
		"clear reg B"
		return [MEM.CLB_opcode]
	def LDBL(addr): 
		"load Bl from ram"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.LDBL_opcode, addr]
	def LDBH(addr): 
		"load Bh from ram"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.LDBH_opcode, addr]
	def LDB(addr): 
		"load B as int16 from ram (BE)"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.LDB_opcode, addr]
	def STBL(addr):
		"store Bl to ram"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.STBL_opcode, addr]
	def STBH(addr):
		"store Bh to ram"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.STBH_opcode, addr]
	def STB(addr):
		"store B as int16 to ram (BE)"
		addr = convert_to_val(addr)
		val8(addr)
		return [MEM.STB_opcode, addr]
	def LALD(value):
		"load Al immediately"
		value = convert_to_val(value)
		val8(value)
		return [MEM.LALD_opcode, value]
	def LAHD(value):
		"load Ah immediately"
		value = convert_to_val(value)
		val8(value)
		return [MEM.LAHD_opcode, value]
	def LBLA(): 
		"load Bl from ram address A"
		return [MEM.LBA_opcode]
	def LBHA(): 
		"load Bh from ram address A"
		return [MEM.LBA_opcode]
	def LBA(): 
		"load B as int16 from ram address A"
		return [MEM.LBA_opcode]
	def SBLA():
		"store Bl at ram address A"
		return [MEM.SBA_opcode]
	def SBHA():
		"store Bh at ram address A"
		return [MEM.SBA_opcode]
	def SBA():
		"store B as int16 at ram address A"
		return [MEM.SBA_opcode]
	def SET8(addr, val):
		"set ram address"
		addr, val = [convert_to_val(addr), convert_to_val(val)]
		if isinstance(val, str):
			val = ord(val)
		val8(addr)
		return [MEM.SET8_opcode, addr, val & 0xFF]
	def SET16(addr, val):
		"set ram address as int16 (BE)"
		addr, val = [convert_to_val(addr), convert_to_val(val)]
		val8(addr)
		return [MEM.SET16_opcode, addr, (val >> 8) & 0xFF, val & 0xFF]
	def SWP():
		"swap A and B"
		return [MEM.SWP_opcode]
0x37
class ALU(STATIC):
	(
		ADD_opcode, SUB_opcode, MOD_opcode,
		SHL_opcode, SHR_opcode, AND_opcode,
		OR_opcode, NOT_opcode, XOR_opcode,
		NAND_opcode, NOR_opcode, XNOR_opcode,
		MSK_opcode, DIV_opcode, MULT_opcode
	) = [generate_opcode() for _ in range(15)]
	def ADD():	"A += B"; return [ALU.ADD_opcode]
	def SUB():	"A -= B"; return [ALU.SUB_opcode]
	def MOD():	"A %= B"; return [ALU.MOD_opcode]
	def SHL():	"A <<= B"; return [ALU.SHL_opcode]
	def SHR():	"A >>= B"; return [ALU.SHR_opcode]
	def AND():	"A &= B"; return [ALU.AND_opcode]
	def OR():	 "A |= B"; return [ALU.OR_opcode]
	def NOT():	"A = ~A"; return [ALU.NOT_opcode]
	def XOR():	"A ^= B"; return [ALU.XOR_opcode]
	def NAND(): "A = ~(A & B)"; return [ALU.NAND_opcode]
	def NOR():	"A = ~(A | B)"; return [ALU.NOR_opcode]
	def XNOR(): "A = ~(A ^ B)"; return [ALU.XNOR_opcode]
	def MSK():	"A &= ~B"; return [ALU.MSK_opcode]
	def DIV():	"A /= B"; return [ALU.DIV_opcode]
	def MULT(): "A *= B"; return [ALU.MULT_opcode]

class CMP(STATIC):
	(
		EQ_opcode, GT_opcode, LT_opcode,
		GE_opcode, LE_opcode, ZE_opcode,
		POS_opcode, NE_opcode, NEG_opcode,
	) = [generate_opcode() for _ in range(9)]
	def EQ():
		"set flag if A == B"
		return [CMP.EQ_opcode]
	def GT():
		"set flag if A > B"
		return [CMP.GT_opcode]
	def LT():
		"set flag if A < B"
		return [CMP.LT_opcode]
	def GE():
		"set flag if A >= B"
		return [CMP.GE_opcode]
	def LE():
		"set flag if A <= B"
		return [CMP.LE_opcode]
	def ZE():
		"set flag if A == 0"
		return [CMP.ZE_opcode]
	def POS():
		"set flag if A == B (converts uint16 to int16 just for this operation)"
		return [CMP.PO_opcode]
	def NE():
		"set flag if A != B"
		return [CMP.NE_opcode]
	def NEG():
		"set flag if A < 0"
		return [CMP.NG_opcode]

class STACK(STATIC):
	stackCounter = 0
	(
		PUSHA_opcode, POPA_opcode,
		PUSHB_opcode, POPB_opcode,
		PUSH_opcode,	POP_opcode,
	) = [generate_opcode() for _ in range(6)]
	def PUSHA():
		"pushes A to the stack"
		return [STACK.PUSHA_opcode]
	def POPA():
		"pops A from the stack"
		return [STACK.POPA_opcode]
	def PUSHB():
		"pushes B to the stack"
		return [STACK.PUSHB_opcode]
	def POPB():
		"pops B from the stack"
		return [STACK.POPB_opcode]
	def PUSH():
		"pushes A, B to the stack"
		return [STACK.PUSH_opcode]
	def POP():
		"pops A, B from the stack"
		return [STACK.POP_opcode]


class PC(STATIC):
	(
		JMP_opcode, JMI_opcode, PUSH_opcode, POP_opcode
	) = [generate_opcode() for i in range(4)]
	def JMP(addr):
		"unconditional jump to byte (warning: bytes are smaller than operations. make sure the target is the start of an operation)"
		addr = convert_to_val(addr)
		val8(addr)
		return [PC.JMP_opcode, addr]
	def JMI(JUMP_IF_RESULT_EQUAL_TO,addr):
		"conditional jump: if the last CMP operation returned JUMP_IF_RESULT_EQUAL_TO (warning: bytes are smaller than operations. make sure the target is the start of an operation)"
		JUMP_IF_RESULT_EQUAL_TO,addr = [convert_to_val(JUMP_IF_RESULT_EQUAL_TO), convert_to_val(addr)]
		val8(addr)
		return [PC.JMI_opcode,JUMP_IF_RESULT_EQUAL_TO, addr]
	def PUSH():
		return [PC.PUSH_opcode]
	def POP():
		return [PC.POP_opcode]

class OP(STATIC):
	(
	PRINT_opcode,
	CLEAR_opcode,
	NOP_opcode,
	) = [generate_opcode() for _ in range(3)]
	def PRINT():
		"print the value of A as char"
		return [OP.PRINT_opcode]
	def CLEAR():
		"clear the output"
		return [OP.CLEAR_opcode]
	def NOP():
		"nothing"
		return [OP.NOP_opcode]
	def EXIT(code):
		"exit, should be called at every possible end of the program"
		code = convert_to_val(code)
		return [255, code]





class Program:
	def __init__(self):
		self.data = []
		self.isLib = False
	
	def __iadd__(self, other):
		if isinstance(other, str):
			if other == "STARTLIB":
				self.isLib = len(self.data)
				self += PC.JMP(0)
			elif other == "ENDLIB":
				if self.isLib is False:
					print(self.isLib)
					raise TypeError("endLib called without startLib")
				self.data[self.isLib][1] = self.target
				self.isLib = False
		else:
			self.data.append(other)
		return self
	def link(self, path):
		with open(path, "rb") as f:
			ramuse = ord(f.read(1))
			addrTableLen = ord(f.read(1))
			addrTable = f.read(addrTableLen)
			addrtable = {}
			i = 0
			while i < addrTableLen:
				value = addrTable[i]
				i += 1
				name = b""
				while addrTable[i] != 0:
					name += bytes([addrTable[i]])
					i += 1
				addrtable[name.decode()] = value + self.target
				print(i)
				i += 1
			d = list(f.read())
			p = createVar(ramuse)
			self.data += self.decodeLib(d, memstart = len(usedRam))
			free(*p)
			print(addrtable)
		return addrtable
	@property
	def target(self):
		return sum([len(op) for op in self.data])
	
	def compile(self, numpasses=0):
		global usedRam
		for _ in range(numpasses):
			self.data = self.optimize()
		compiled = b""
		for op in self.data:
			compiled += bytes(op)
		return compiled, len(usedRam)
	def decodeLib(self, p, memstart = 0):
		addrstart = self.target
		a = []
		i = 0
		j = 0
		def nextj():
			nonlocal j
			j += 1
			return j - 1
		while i < len(p):
			print(i)
			j = 0
			op = p[i]
			if op == nextj(): # Check MEM CLA
				a.append(p[i:i+1])
				i += 1
			elif op in [nextj() for _ in range(6)]:
				func = p[i:i+2]
				func[1] += memstart
				a.append(func)
				i += 2
			elif op == nextj():  # Check MEM CLB
				a.append(p[i,i+1])
				i += 1
			elif op in [nextj() for _ in range(6)]:
				func = p[i:i+2]
				func[1] += memstart
				a.append(func)
				i += 2
			elif op in [nextj() for _ in range(2)]:
				a.append(p[i:i+2])
				i += 2
			elif op in [nextj() for _ in range(6)]:
				a.append(p[i:i+1])
				i += 1
			elif op == nextj():
				func = p[i:i+3]
				func[1] += memstart
				a.append(func)
				i += 3
			elif op == nextj():
				func = p[i:i+4]
				func[1] += memstart
				a.append(func)
				i += 4
			elif op in [nextj() for _ in range(26)]:
				a.append(p[i:i+1])
				i += 1
			elif op == nextj():  # Check PC JMP
				func = p[i:i+2]
				func[1] += addrstart
				i += 2
			elif op == nextj():  # Check PC JMI
				func = p[i:i+3]
				func[2] += addrstart
				i += 3
			elif op == nextj():  # Check PC PUSH
				a.append(p[i:i+1])
				i += 1
			elif op == nextj():  # Check PC POP
				a.append(p[i:i+1])
				i += 1
			elif op == nextj():  # Check OP PRINT
				a.append(p[i:i+1])
				i += 1
			elif op == nextj():  # Check OP CLEAR
				a.append(p[i:i+1])
				i += 1
			elif op == nextj():
				pass
				i += 1
			elif op == 255:  # Check OP EXIT
				a.append(p[i:i+2])
				i += 2
		return a
	def optimize(self):
		a = []
		i = 0
		spliced = 0
		p = [a[:] for a in self.data[:]]
		index = 0
		j = 0
		def nextj():
			nonlocal j
			j += 1
			return j - 1
		while i < len(self.data):
			j = 0
			op = p[i][0]
			index += len(p[i])
			if op == nextj(): # Check MEM CLA
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM LDAL
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM LDAH
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM LDA
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM STAL
				a.append(p[i])
			elif op == nextj():  # Check MEM STAH
				a.append(p[i])
			elif op == nextj():  # Check MEM STA
				a.append(p[i])
			elif op == nextj():  # Check MEM CLB
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM LDBL
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM LDBH
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM LDB
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM STBL
				a.append(p[i])
			elif op == nextj():  # Check MEM STBH
				a.append(p[i])
			elif op == nextj():  # Check MEM STB
				a.append(p[i])
			elif op == nextj():  # Check MEM LALD
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM LAHD
				if p[i+1][0] == STACK.POPA_opcode:
					spliced += 2
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM LBLA
				a.append(p[i])
			elif op == nextj():  # Check MEM LBHA
				a.append(p[i])
			elif op == nextj():  # Check MEM LBA
				a.append(p[i])
			elif op == nextj():  # Check MEM SBLA
				a.append(p[i])
			elif op == nextj():  # Check MEM SBHA
				a.append(p[i])
			elif op == nextj():  # Check MEM SBA
				a.append(p[i])
			elif op == nextj():  # Check MEM SET8
				currOP = p[i]
				nextOP = p[i+1]
				if currOP[0] == nextOP[0]:
					if currOP[1] == nextOP[1]:
						spliced += 3
						pass
					elif (currOP[1] + 1) == nextOP[1]:
						a.append([MEM.SET16_opcode, currOP[1], currOP[2], nextOP[2]])
						spliced += 2
						i += 1
					elif (currOP[1] - 1) == nextOP[1]: 
						a.append([MEM.SET16_opcode, currOP[1]-1, nextOP[2], currOP[2]])
						spliced += 2
						i += 1
					else:
						a.append(p[i])
				else:
					a.append(p[i])
			elif op == nextj():  # Check MEM SET16
				a.append(p[i])
			elif op == nextj():  # Check MEM SWP
				if p[i + 1][0] == op:
					spliced += 2
					i += 1
				else:
					a.append(p[i])
			elif op == nextj():  # Check ALU ADD
				a.append(p[i])
			elif op == nextj():  # Check ALU SUB
				a.append(p[i])
			elif op == nextj():  # Check ALU MOD
				a.append(p[i])
			elif op == nextj():  # Check ALU SHL
				a.append(p[i])
			elif op == nextj():  # Check ALU SHR
				a.append(p[i])
			elif op == nextj():  # Check ALU AND
				a.append(p[i])
			elif op == nextj():  # Check ALU OR
				a.append(p[i])
			elif op == nextj():  # Check ALU NOT
				a.append(p[i])
			elif op == nextj():  # Check ALU XOR
				a.append(p[i])
			elif op == nextj():  # Check ALU NAND
				a.append(p[i])
			elif op == nextj():  # Check ALU NOR
				a.append(p[i])
			elif op == nextj():  # Check ALU XNOR
				a.append(p[i])
			elif op == nextj():  # Check ALU MSK
				a.append(p[i])
			elif op == nextj():  # Check ALU DIV
				a.append(p[i])
			elif op == nextj():  # Check ALU MULT
				a.append(p[i])
			elif op == nextj():  # Check CMP EQ
				a.append(p[i])
			elif op == nextj():  # Check CMP GT
				a.append(p[i])
			elif op == nextj():  # Check CMP LT
				a.append(p[i])
			elif op == nextj():  # Check CMP GE
				a.append(p[i])
			elif op == nextj():  # Check CMP LE
				a.append(p[i])
			elif op == nextj():  # Check CMP ZE
				a.append(p[i])
			elif op == nextj():  # Check CMP PO
				a.append(p[i])
			elif op == nextj():  # Check CMP NE
				a.append(p[i])
			elif op == nextj():  # Check CMP NG
				a.append(p[i])
			elif op == nextj():  # Check STCKPUSHA
				if p[i+1][0] == STACK.POPA_opcode:
					i += 1
				else:
					a.append(p[i])
			elif op == nextj():  # Check STCKPOPA
				if p[i+1][0] == STACK.PUSHA_opcode:
					i += 1
				else:
					a.append(p[i])
			elif op == nextj():  # Check STCKPUSHB
				if p[i+1][0] == STACK.POPB_opcode:
					i += 1
				else:
					a.append(p[i])
			elif op == nextj():  # Check STCKPOPB
				if p[i+1][0] == STACK.PUSHB_opcode:
					i += 1
				else:
					a.append(p[i])
			elif op == nextj():  # Check STCKPUSH
				if p[i+1][0] == STACK.POP_opcode:
					i += 1
				else:
					a.append(p[i])
			elif op == nextj():  # Check STCKPOP
				if p[i+1][0] == STACK.PUSH_opcode:
					i += 1
				else:
					a.append(p[i])
			elif op == nextj():  # Check PC JMP
				target = p[i][1] - spliced
				if 0 <= target < len(p) and target > index:  # Valid target bounds
					a.append([PC.JMP_opcode, target])  # Forward-compatible jump
				else:
					a.append(p[i])  # Keep as-is for invalid jumps
			elif op == nextj():  # Check PC JMI
				print(spliced, "spliced")
				target = p[i][1] - spliced
				arg = p[i][1]
				if 0 <= target < len(p) and target > index:
					a.append([PC.JMI_opcode, arg, target])
				else:
					a.append(p[i])
			elif op == nextj():  # Check OP PRINT
				a.append(p[i])
			elif op == nextj():  # Check OP CLEAR
				a.append(p[i])
			elif op == nextj():  # Check OP NOP
				spliced += 1
			elif op == 255:  # Check OP EXIT
				if p[i - 1][0] == op and p[i - 1][1] == p[i][1]:
					spliced += 2
				else:
					a.append(p[i])
			else:
				a.append(p[i])
			i += 1
		print(a)
		return a
	def genLib(self, *targets):
		for pos, name in targets:
			self.data.append(PC.JMP(pos))  # Ensure jumps are preserved

		result, usedRam = self.compile(100)  # Optimize 100 times
		target_operations = result[-len(targets)*2:]  # Get updated targets (each JMP operation always (guaranteed) compiles to 2 bytes: b"opcode" + b"target")
		target_addresses = []
		for i in range(len(targets)):
			target_addresses.append(target_operations[i*2 + 1])
		headerTable = b""
		for t,n in zip(target_addresses, [t[1] for t in targets]): #get shifted target adresses and names
			headerTable += bytes([t]) + n.encode() + b"\x00"
		headerTableLength = len(headerTable)
		print(headerTable)
		resultFile =bytes([usedRam, headerTableLength]) + headerTable + result[:-len(targets)*2]
		return resultFile







def alloc(leng):
	global usedRam
	# Try to find a contiguous free block within the current usedRam
	for i in range(len(usedRam) - leng + 1):
		if all(usedRam[j] == 0 for j in range(i, i + leng)):
			# Mark the allocated block
			for j in range(i, i + leng):
				usedRam[j] = 1
			return i

	# Count the available contiguous space at the end of usedRam
	availableSpaceAtEnd = 0
	for i in range(len(usedRam) - 1, -1, -1):
		if usedRam[i] == 0:
			availableSpaceAtEnd += 1
		else:
			break

	# Check if extending usedRam would exceed the 255-byte limit
	if len(usedRam) + (leng - availableSpaceAtEnd) > 255:
		raise MemoryError("Cannot allocate memory: usedRam would exceed 255 bytes.")

	# Extend usedRam and mark the new block as allocated
	usedRam.extend([0] * (leng - availableSpaceAtEnd))
	for i in range(len(usedRam) - leng, len(usedRam)):
		usedRam[i] = 1
	return len(usedRam) - leng


def free(addr, leng = 0):
	global usedRam
	if isinstance(addr, createVar):
		free(addr.l[0], addr.l[1])
	elif leng > 0:
		for i in range(leng):
			usedRam[addr+i] = 0
	else:
		raise TypeError(f"invalid free: addr {addr}, or size {leng} invalid")


usedRam = []

class createVar():
	def __init__(self, size, len=0):
		if len == 0:
			self.l = [alloc(size), size]
		else: self.l = [size, len]
		print("createVar", self.l)
	def __call__(self):
		return self.l[0]
	def __add__(self, other):
		return createVar(self.l[0] + other, self.l[1])
	def __iter__(self):
		return iter(self.l)












def decompile(data):
	def printChrs(offset, size, maxsize):
		for i in range(maxsize):
			if (i >= size or i+offset >= len(data)):
				print("   ", end="");
			else:
				print("%.2X " % data[i + offset], end="");
		return size;

	linenumbers = "\033[0m\033[32m%.16X\033[0m: "
	formats = [
		"\033[0m%s.\033[34m%s\033[0m()              ",
		"\033[0m%s.\033[34m%s\033[0m(\033[33m%.2X\033[0m)            ",
		"\033[0m%s.\033[34m%s\033[0m(\033[33m%.2X\033[0m, \033[33m%.2X\033[0m)        ",
		"\033[0m%s.\033[34m%s\033[0m(\033[33m%.2X\033[0m, \033[33m%.2X\033[0m, \033[0m\033[33m%.2X\033[0m)    ",
		"\033[0m%s.\033[34m%s\033[0m(\033[33m%.2X\033[0m, \033[33m%.2X\033[0m, \033[0m\033[33m%.2X\033[0m, \033[33m%.2X\033[0m)"
	]
#	formats = [
#		"%s.%s()              ",
#		"%s.%s(%.2X)            ",
#		"%s.%s(%.2X, %.2X)        ",
#		"%s.%s(%.2X, %.2X, %.2X)    ",
#		"%s.%s(%.2X, %.2X, %.2X, %.2X)"
#	]
	i = 0;
	numlines = 0;
	j = 0
	while i < len(data):
		def next_opcode():
			nonlocal j
			j += 1
			return j - 1
		numlines+=1
		print(linenumbers % i, end="");
		j = 0
		if data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("MEM  ", "CLA  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "LDAL ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "LDAH ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "LDA  ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "STAL ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "STAH ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "STA  ", data[i+1]), end="")

		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[1] % ("MEM  ", "CLB  ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "LDBL ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "LDBH ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "LDB  ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "STBL ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "STBH ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "STB  ", data[i+1]), end="")

		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "LALD ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("MEM  ", "LAHD ", data[i+1]), end="")

		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("MEM  ", "LBLA "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("MEM  ", "LBHA "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("MEM  ", "LBA  "), end="")

		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("MEM  ", "SBLA "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("MEM  ", "SBHA "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("MEM  ", "SBA  "), end="")

		elif data[i] == next_opcode():
			k = printChrs(i, 3, 5)
			print(formats[2] % ("MEM  ", "SET8 ", data[i+1], data[i+2]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 4, 5)
			print(formats[3] % ("MEM  ", "SET16", data[i+1], data[i+2], data[i+3]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("MEM  ", "SWP  "), end="")

		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "ADD\x20 "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "SUB  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "MOD  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "SHL  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "SHR  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "AND  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "OR   "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "NOT  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "XOR  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "NAND "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "NOR  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "XNOR "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "MSK  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "DIV  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("ALU  ", "MULT "), end="")

		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("CMP  ", "EQ   "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("CMP  ", "GT   "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("CMP  ", "LT   "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("CMP  ", "GE   "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("CMP  ", "LE   "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("CMP  ", "ZE   "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("CMP  ", "PO   "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("CMP  ", "NE   "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("CMP  ", "NG   "), end="")

		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("STACK", "PUSHA"), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("STACK", "POPA "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("STACK", "PUSHB"), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("STACK", "POPB "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("STACK", "PUSH "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("STACK", "POP  "), end="")

		elif data[i] == next_opcode():
			k = printChrs(i, 2, 5)
			print(formats[1] % ("PC   ", "JMP  ", data[i+1]), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 3, 5)
			print(formats[2] % ("PC   ", "JMI  ", data[i+1], data[i+2]), end="")
		elif data[i] == next_opcode():
			print(formats[0] % ("PC   ", "PUSH "), end="")
		elif data[i] == next_opcode():
			print(formats[0] % ("PC   ", "POP  "), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("OP   ", "PRINT"), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("OP   ", "CLEAR"), end="")
		elif data[i] == next_opcode():
			k = printChrs(i, 1, 5)
			print(formats[0] % ("OP   ", "NOP  "), end="")
		elif data[i] == 255:
			k = printChrs(i, 2, 5)
			print(formats[1] % ("OP   ", "EXIT ", data[i+1]), end="")
		else:
			printChrs(i, 1, 5)
			print("  (unknown)              ", end="")
			k=1
		i += k
		print("\033[0m\033[31m    ||    ", end="");
		print(" ".join([hex(d)[2:].upper().rjust(2, "0") for d in data[i:]]), end="")
		print("\033[0m");
	print("\033[0m", end="");
	return numlines + 2;

############################## print all names and opcodes

if __name__ == '__main__':
	import re

	def lineReader(data):
		"""Yield lines from the given data."""
		for i in data.split("\n"):
			yield i
	
	def find_args(classname, funcname, file):
		"""Find the arguments of the function in the specified class."""
		f = lineReader(file)
		currClass = ""
		for line in f:
			line = line.strip()
			if line.startswith("class "):
				# Extract the class name (ignoring parameters in class definition)
				class_match = re.match(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
				if class_match:
					currClass = class_match.group(1)
			elif line.startswith("def "):
				# Extract function name and arguments
				func_match = re.match(r'def\s+(\w+)\((.*)\):', line)
				if func_match:
					func_name = func_match.group(1)
					if func_name == funcname and currClass == classname:
						return f"{currClass}.{func_name}({func_match.group(2)})"
		return ""  # Return an empty string if function not found in the class
	
	with open(__file__, "r") as f:
		file = f.read()
	
	items = []
	# Example classes for demonstration (replace with your actual class names)
	for cls in [MEM, ALU, CMP, STACK, PC, OP]:
		for a in dir(cls):
			if "_opcode" in a:
				print (a)
				func_name = a[:-7]  # Assuming '_opcode' suffix
				args_str = find_args(cls.__name__, func_name, file)
				doc_string = getattr(cls, func_name).__doc__ if getattr(cls, func_name).__doc__ else ""
				items.append([args_str, getattr(cls, a), doc_string])
	
	# Sort items by the second element (the value) and print
	for item in sorted(items, key=lambda a: a[1]):
		print(f"{item[0].ljust(36)} = 0x{hex(item[1])[2:].upper().rjust(2, '0')}\t{item[2]}")

	print("\n")
	
	print("Program: helper class for creating programs in binary")
	print("\t\t__iadd__ (+=) adds an operation to the program")
	print("\t\ttarget returns the length, therefore returning an in-between operations JMP target")
	print("\t\tcompile(passes) returns the compiled program as binary, passes=0 for no optimization, more for better optimizations (progmem only).")

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>



#define STACKOVERFLOW 101
#define STACKUNDERFLOW 102




#define printBinary(value) PRINTBINARY(&(value), sizeof(value))

#ifdef DEBUG
#include "printerpreter.h"

#else
void PRINTBINARY(void *value, size_t size) {
	unsigned char *byte = (unsigned char *)value;
	for (size_t i = 0; i < size; i++) {
		unsigned char currentByte = byte[i];
		for (int bit = 7; bit >= 0; bit--) {
			printf("%d", (currentByte >> bit) & 1);
		}
		if (i < size - 1) {
			printf(" ");
		}
	}
	printf("\n");
}
#endif




int handleExec(uint8_t *p, uint8_t ramsize, uint16_t length){
	uint8_t running = 1;
	uint8_t error = 0;
	uint8_t *ram = (uint8_t *)malloc(ramsize);
	uint16_t *stack = (uint16_t *)malloc(10*2);
	uint8_t *callStack = (uint8_t *)malloc(10);
	if (ram == NULL || stack == NULL || callStack == NULL){
		free(ram);
		free(stack);
		free(callStack);
		error = 99;
		return error;
	}
	for (uint8_t i = 0; i < ramsize; i++){
		ram[i] = 0;
	}
	uint8_t stackPTR = 0;
	uint8_t callStackPTR = 0;
	uint8_t stackSize = 10;
	uint8_t callStackSize = 10;
	uint16_t PC = 0;
	uint16_t A = 0;
	uint16_t B = 0;
	uint16_t C = 0;
	uint16_t D = 0;
	uint8_t f = 0;
	#ifdef DEBUG
	printerpret(p, length, PC, A, B, C, D, f);
	#endif
	printf("\n");
	while (running && !error){
		uint8_t opcode = 0;
		uint8_t op = p[PC++];
		#ifdef DEBUG
		printf("\033[s");
		printf("\033[H");
		printerpret(p, length, PC-1, A, B, C, D, f);
		print(ram, ramsize, 100);
		printBuffer(69, 139);
		printf("\033[u");
		fflush(stdout);
		usleep(sleepTime);
		#endif
		if (op == opcode++) {								// MEM_CLA
			A = 0;
		} else if (op == opcode++){  						// MEM_LDAL (Load Address Low byte)
			A = (A & 0xFF00) | (ram[p[PC++]] & 0xFF);
		} else if (op == opcode++) {  						// MEM_LDAH (Load Address High byte)
			A = (A & 0x00FF) | (ram[p[PC++]] << 8);
		} else if (op == opcode++) {  						// MEM_LDA (Load Address 16-bit)
			uint8_t addr = p[PC++];
			A = (ram[addr] << 8) | ram[addr + 1];
		} else if (op == opcode++) {  						// MEM_STAL (Store Address Low byte)
			ram[p[PC++]] = A & 0xFF;
		} else if (op == opcode++) {  						// MEM_STAH (Store Address High byte)
			ram[p[PC++]] = (A >> 8) & 0xFF;
		} else if (op == opcode++) {  						// MEM_STA (Store Address 16-bit)
			uint8_t addr = p[PC++];
			ram[addr] = (A >> 8) & 0xFF;
			ram[addr + 1] = A & 0xFF;
		} else if (op == opcode++){							// MEM_CLB
			B = 0;
		} else if (op == opcode++) {  						// MEM_LDBL (Load Byte Low byte)
			B = (B & 0xFF00) | ram[p[PC++]];
		} else if (op == opcode++) {  						// MEM_LDBH (Load Byte High byte)
			B = (B & 0x00FF) | (ram[p[PC++]] << 8);
		} else if (op == opcode++) {  						// MEM_LDB (Load Byte 16-bit)
			uint8_t addr = p[PC++];
			B = (ram[addr] << 8) | ram[addr + 1];
		} else if (op == opcode++) {  						// MEM_STBL (Store Byte Low byte)
			ram[p[PC++]] = B & 0xFF;
		} else if (op == opcode++) {  						// MEM_STBH (Store Byte High byte)
			ram[p[PC++]] = (B >> 8) & 0xFF;
		} else if (op == opcode++) {  						// MEM_STB (Store Byte 16-bit)
			uint8_t addr = p[PC++];
			ram[addr] = (B >> 8) & 0xFF;
			ram[addr + 1] = B & 0xFF;
		} else if (op == opcode++) {  						// MEM_LALD (Load Address Direct)
			A = (A & 0xFF00) | p[PC++];
		} else if (op == opcode++) {  						// MEM_LAHD (Load Address Direct)
			A = (A & 0x00FF) | (p[PC++] << 8);
		} else if (op == opcode++) {  						// MEM_LBLA (Load Byte from Address)
			B = (B & 0xFF00) | (ram[A] & 0xFF);
		} else if (op == opcode++) {  						// MEM_LBHA (Load Byte from Address)
			B = (B & 0x00FF) | (ram[A] << 8);
		} else if (op == opcode++) {  						// MEM_LBA (Load Byte from Address)
			uint8_t addr = p[PC++];
			B = (ram[A] << 8) | ram[A + 1];
		} else if (op == opcode++){ 						// MEM_SBA (store Byte B 16-bit at A)
			ram[A] = (B >> 8) & 0xFF;
			ram[A+1] = B & 0xFF;
		} else if (op == opcode++){ 						// MEM_SBLA (Store Byte Low byte)
			ram[A] = B & 0xFF;
		} else if (op == opcode++){ 						// MEM_SBHA (Store Byte High byte)
			ram[A] = (B >> 8) & 0xFF;
		} else if (op == opcode++) {  						// MEM_SET8 (Set 8-bit value)
			uint8_t addr = p[PC++];
			ram[addr] = p[PC++];
		} else if (op == opcode++) {  						// MEM_SET16 (Set 16-bit value)
			uint8_t addr = p[PC++];
			ram[addr] = p[PC++];
			ram[addr + 1] = p[PC++];
		} else if (op == opcode++) {  						// MEM_SWP (Swap A and B)
			uint16_t tmp = A;
			A = B;
			B = tmp;
		} else if (op == opcode++){							//ALU_ADD
			A=A+B;
		} else if (op == opcode++){							//ALU_SUB
			A=A-B;
		} else if (op == opcode++){							//ALU_MOD
			A=A%B;
		} else if (op == opcode++){							//ALU_SHL
			A=A<<B;
		} else if (op == opcode++){							//ALU_SHR
			A=A>>B;
		} else if (op == opcode++){							//ALU_AND
			A=A&B;
		} else if (op == opcode++){							//ALU_OR
			A=A|B;
		} else if (op == opcode++){							//ALU_NOT
			A=~A;
		} else if (op == opcode++){							//ALU_XOR
			A=A^B;
		} else if (op == opcode++){							//ALU_NAND
			A=~(A&B);
		} else if (op == opcode++){							//ALU_NOR
			A=~(A|B);
		} else if (op == opcode++){							//ALU_XNOR
			A=~(A^B);
		} else if (op == opcode++){							//ALU_MSK
			A=A&(~B);
		} else if (op == opcode++){							//ALU_DIV
			A=A/B;
		} else if (op == opcode++){							//ALU_MULT
			A=A*B;
		} else if (op == opcode++){							//CMP_EQ
			f=A==B;
		} else if (op == opcode++){							//CMP_GT
			f=A>B;
		} else if (op == opcode++){							//CMP_LT
			f=A<B;
		} else if (op == opcode++){							//CMP_GE
			f=A>=B;
		} else if (op == opcode++){							//CMP_LE
			f=A<=B;
		} else if (op == opcode++){							//CMP_ZE
			f=A==0;
		} else if (op == opcode++){							//CMP_PO
			f=((int16_t)A)>0;
		} else if (op == opcode++){							//CMP_NE
			f=A!=B;
		} else if (op == opcode++){							//CMP_NG
			f=((int16_t)A)<0;
		} else if (op == opcode++){							//STCK_PUSHA
			if (stackPTR < stackSize){
				stack[stackPTR++] = A;
			} else {
				error = STACKOVERFLOW;
			}
		} else if (op == opcode++){							//STCK_POPA
			if (stackPTR != 0){
				A = stack[--stackPTR];
			} else {
				error = STACKUNDERFLOW;
			}
		} else if (op == opcode++){							//STCK_PUSHB
			if (stackPTR < stackSize){
				stack[stackPTR++] = B;
			} else {
				error = STACKOVERFLOW;
			}
		} else if (op == opcode++){							//STCK_POPB
			if (stackPTR != 0){
				B = stack[--stackPTR];
			} else {
				error = STACKUNDERFLOW;
			}
		} else if (op == opcode++){							//STCK_PUSH
			if (stackPTR < stackSize - 1){
				stack[stackPTR++] = A;
				stack[stackPTR++] = B;
			} else {
				error = STACKOVERFLOW;
			}
		} else if (op == opcode++){							//STCK_POP
			if (stackPTR > 1){
				A = stack[--stackPTR];
				B = stack[--stackPTR];
			} else {
				error = STACKUNDERFLOW;
			}
		} else if (op == opcode++){							//PC__JMP
			PC = p[PC];
		} else if (op == opcode++){							//PC__JMI
			if (f == p[PC++]){
				PC = p[PC++];
			} else {
				PC++;
			}
		} else if (op == opcode++){							//PC__PUSH
			if (callStackPTR < callStackSize){
				callStack[callStackPTR] = PC;
				callStackPTR+=1;
			} else {
				error = STACKOVERFLOW;
			}
		} else if (op == opcode++){							//PC__POP
			if (callStackPTR > 0){
				callStackPTR-=1;
				PC = callStack[callStackPTR];
			} else {
				error = STACKUNDERFLOW;
			}
		} else if (op == opcode++){							//OP__PRINT
			#ifdef DEBUG
			addPrintBuffer(A);
			#else
			printf("%c", A);
			#endif
		} else if (op == opcode++){							//OP__CLEAR
			#ifdef DEBUG
			clearPrintBuffer();
			#else
			printf("\033[H");
			#endif
		} else if (op == opcode++){							//OP__NOP
		} else if (op == 0xFF)    {							//OP__EXIT
			running = 0;
			error = p[PC++];
		} else {
			error = op;
		}
	}
	free(ram);
	return error;
}
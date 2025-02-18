#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>


#define PRINTBUFFER_SIZE 2691
#define printBinary(value) PRINTBINARY(&(value), sizeof(value))


// Function to print `size` bytes from `buffer`
int print(uint8_t *buffer, uint16_t size, uint8_t maxsize) {
	if (!buffer) return -1;  // Handle null pointer
	for (int i = 0; i < maxsize; i++) {
		if (i >= size){
			printf("   ");
		} else{
			printf("%.2X ", buffer[i]);
		}
	}
	return size;
}


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
	printf("\n\n");
}


const char* linenumbers[] = {
	"\033[0m\033[7m\033[32m%.16X:\033[0m\033[7m ",
	"\033[0m\033[32m%.16X\033[0m: ",
};

const char *formats[] = {
	"\033[0m\033[7m%s.\033[34m%s\033[0m\033[7m()              ",
	"\033[0m\033[7m%s.\033[34m%s\033[0m\033[7m(\033[33m%.2X\033[0m\033[7m)            ",
	"\033[0m\033[7m%s.\033[34m%s\033[0m\033[7m(\033[33m%.2X\033[0m\033[7m, \033[33m%.2X\033[0m\033[7m)        ",
	"\033[0m\033[7m%s.\033[34m%s\033[0m\033[7m(\033[33m%.2X\033[0m\033[7m, \033[33m%.2X\033[0m\033[7m, \033[33m%.2X\033[0m\033[7m)    ",
	"\033[0m\033[7m%s.\033[34m%s\033[0m\033[7m(\033[33m%.2X\033[0m\033[7m, \033[33m%.2X\033[0m\033[7m, \033[33m%.2X\033[0m\033[7m, \033[33m%.2X\033[0m\033[7m)",
	"\033[0m%s.\033[34m%s\033[0m()              ",
	"\033[0m%s.\033[34m%s\033[0m(\033[33m%.2X\033[0m)            ",
	"\033[0m%s.\033[34m%s\033[0m(\033[33m%.2X\033[0m, \033[33m%.2X\033[0m)        ",
	"\033[0m%s.\033[34m%s\033[0m(\033[33m%.2X\033[0m, \033[33m%.2X, \033[0m\033[33m%.2X\033[0m)    ",
	"\033[0m%s.\033[34m%s\033[0m(\033[33m%.2X\033[0m, \033[33m%.2X, \033[0m\033[33m%.2X\033[0m, \033[33m%.2X\033[0m)"
};



char printbuffer[PRINTBUFFER_SIZE] = {0};  // Print buffer initialization
int printbufferIDX = 0;  // Keeps track of the current index in the buffer
int isOverFlow = 0;

// Adds a character to the buffer
int addPrintBuffer(char value) {
	if (printbufferIDX < PRINTBUFFER_SIZE) {  // Check for overflow
		printbuffer[printbufferIDX++] = value;
	} else {
		isOverFlow = 1;
		printbufferIDX = 0;
	}
	return 1;  // Successfully added the character
}

// Clears the print buffer
void clearPrintBuffer() {
	isOverFlow = 0;
	printbufferIDX = 0;
}

// Prints the buffer from 'start' to 'end' position
void printBuffer(int start, int end) {
	int idx = 0;
	int y = 0;  // Row position

	while (idx < (isOverFlow?PRINTBUFFER_SIZE:printbufferIDX)) {  // Process the buffer
		for (int x = start; x <= end && idx < (isOverFlow?PRINTBUFFER_SIZE:printbufferIDX); x++) {
			char c = printbuffer[idx++];
			if (c == 10) {
				y++;             // Move to the next row
				break;           // Exit the column loop on newline
			} else {
				if (c == 7) {
					continue;
				}
				printf("\033[%d;%dH%c", y + 1, x, c);
				if (x >= end){
					y++;
				}
			}
		}
	}
}



int printerpret(uint8_t *code, uint8_t length, uint16_t currPTR, uint16_t A, uint16_t B, uint16_t C, uint16_t D, uint8_t f) {  
	uint8_t i = 0;
	int numlines=0;
	const char *ARG0STR;
	const char *ARG1STR;
	const char *ARG2STR;
	const char *ARG3STR;
	const char *ARG4STR;
	while (i < length) {
		numlines++;
		if (i == currPTR){
			ARG0STR = formats[0];
			ARG1STR = formats[1];
			ARG2STR = formats[2];
			ARG3STR = formats[3];
			ARG4STR = formats[4];
			printf(linenumbers[0], i);
		} else {
			ARG0STR = formats[5];
			ARG1STR = formats[6];
			ARG2STR = formats[7];
			ARG3STR = formats[8];
			ARG4STR = formats[9];
			printf(linenumbers[1], i);
		}
		uint8_t *args = code+i+1;
		uint8_t opcode = 0;
		uint8_t len;
		if (code[i] == opcode++){        i += print(code+i, 1, 5);printf(ARG0STR, "MEM ", "CLA  ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "LDAL ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "LDAH ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "LDA  ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "STAL ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "STAH ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "STA  ", args[0]);

		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "MEM ", "CLB  ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "LDBL ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "LDBH ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "LDB  ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "STBL ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "STBH ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "STB  ", args[0]);

		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "LALD ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "MEM ", "LAHD ", args[0]);

		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "MEM ", "LBLA ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "MEM ", "LBHA ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "MEM ", "LBA  ");

		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "MEM ", "SBLA ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "MEM ", "SBHA ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "MEM ", "SBA  ");

		} else if (code[i] == opcode++){ i += print(code+i, 3, 5);printf(ARG2STR, "MEM ", "SET8 ", args[0], args[1]);
		} else if (code[i] == opcode++){ i += print(code+i, 4, 5);printf(ARG3STR, "MEM ", "SET16", args[0], args[1], args[2]);
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "MEM ", "SWP  ");


		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "ADD  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "SUB  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "MOD  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "SHL  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "SHR  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "AND  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "OR  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "NOT  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "XOR   ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "NAND  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "NOR  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "XNOR  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "MSK  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "DIV  ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "ALU ", "MULT ");


		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "CMP ", "EQ   ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "CMP ", "GT   ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "CMP ", "LT   ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "CMP ", "GE   ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "CMP ", "LE   ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "CMP ", "ZE   ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "CMP ", "PO   ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "CMP ", "NE   ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "CMP ", "NG   ");

		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "STCK", "PUSHA");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "STCK", "POPA ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "STCK", "PUSHB");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "STCK", "POPB ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "STCK", "PUSH ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "STCK", "POP  ");

		} else if (code[i] == opcode++){ i += print(code+i, 2, 5);printf(ARG1STR, "PC  ", "JMP  ", args[0]);
		} else if (code[i] == opcode++){ i += print(code+i, 3, 5);printf(ARG2STR, "PC  ", "JMI  ", args[0], args[1]);
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "PC  ", "PUSH ");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "PC  ", "POP  ");

		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "OP  ", "PRINT");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "OP  ", "CLEAR");
		} else if (code[i] == opcode++){ i += print(code+i, 1, 5);printf(ARG0STR, "OP  ", "NOP  ");
		} else if (code[i] == 255)     { i += print(code+i, 2, 5);printf(ARG1STR, "OP  ", "EXIT ", args[0]);
		} else {
			print(code, 1, 5);
			len = printf("  (unknown)             ");
			i++;
		}
		printf("\033[0m\033[31m    ||   ");
		printf("\033[0m\n");
	}
	printf("\033[0m");
	printf("A: 0x%.4X B: 0x%.4X C: 0x%.4X D: 0x%.4X F: 0b", A, B, C, D);PRINTBINARY(&f, 1);
	printf("\n");
	return numlines + 2;
}
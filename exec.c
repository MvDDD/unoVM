#define DEBUG
#define TEST
#define sleepTime 100
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "interpreter.h"

#include <stdio.h>

int streq(char *a, char *b) { 
    int i = 0;
    while (a[i] != '\0' && b[i] != '\0') {
        if (a[i] != b[i]) {
            return 0;
        }
        i++;
        printf("%d\n", i);
    }
    return a[i] == '\0' && b[i] == '\0';
}
 	
int main(int argc, char *argv[]){
	setvbuf(stdout, NULL, _IOFBF, 1024);
	FILE *file = fopen(
		#ifdef TEST
		"a"
		#else
		argv[1]
		#endif
		, "rb");
	if (file == NULL){
		printf("error: file is Null\n");
		return 0;
	}
	uint8_t length;
	fread(&length, 1, 1, file);
	uint8_t ramsize;
	fread(&ramsize, 1, 1, file);
	uint8_t *data = malloc(length);
	fread(data, length, 1, file);
	fclose(file);
	#ifdef DEBUG
	system("clear");
	printf("\033[H");
	#endif
	int error = handleExec(data, ramsize, length);
	free(data);
	printf("\n\n[Finished with code %X]\n\n", error);
	return error;
}
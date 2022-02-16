#include <stdio.h>
#include <unistd.h>

void empty(char * buffer){
    for (int i = 0; i<72/4; i+=4)
        *((int *)buffer + i) = 0xc3f48948;
}

int main(int argc, char * argv[]){
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    int i;
    char buffer[56];
    printf("What shall we use\nTo fill the empty spaces\nWhere we used to pwn?\n");
    read(0, buffer, 137);
    empty(buffer);

    return 0;

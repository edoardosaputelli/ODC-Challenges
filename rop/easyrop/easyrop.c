#define SIZE 10

int read(int fd, char *buf, int size){
    int res;
    asm ("mov $0, %%rax\n\t"
         "syscall\n\t"
        : "=a" (res)
         : "D" (fd), "S" (buf), "d" (size)
         );
    return res;
}

int write(int fd, char *buf, int size){
    int res;
    asm ("mov $1, %%rax\n\t"
         "syscall\n\t"
         : "=a" (res)
         : "D" (fd), "S" (buf), "d" (size)
         );
    return res;
}

void exit(int code){
    int res;
    asm ("mov $60, %%rax\n\t"
         "syscall"
         :
         : "D" (code)
         );
    return res;
}


#define MTDO "Try easyROP!\n"

long len = 0;
int index = 0;

// Do you know that there are some tools to find gadgets ? :P

int main() {
    int array[SIZE];
    int a, b;
    len = 0xc3585a5e5f;
    write(1, MTDO, 13);
    while(len > 2) {
        len = 0;
        len += read(0, &a, 4);
        len += read(0, &b, 4);
        array[index++] = a + b;
        write(1,&len, 4);
    }

}

int _start() {
    main();
    exit(0);
}

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

void * mmap(unsigned long addr, unsigned long len, unsigned long prot, unsigned long flags, unsigned long fd, unsigned long off){
    void * res;
    register long r10 __asm__("r10") = flags;
    register long r8 __asm__("r8") = fd;
    register long r9 __asm__("r9") = off;
    asm ("mov $9, %%rax\n\t"
         "syscall\n\t"
         : "=a" (res)
         : "D" (addr), "S" (len), "d" (prot), "r" (r10), "r" (r9), "r" (r8)
         );
    return res;
}

void exit(int code){
    asm ("mov $60, %%rax\n\t"
         "syscall"
         :
         : "D" (code)
         );
}

__attribute__((always_inline)) static inline void reset_register() {
    asm("xor %rbx, %rbx\n\t"
        "xor %rcx, %rcx\n\t"
        "xor %rdx, %rdx\n\t"
        "xor %rdi, %rdi\n\t"
        "xor %rsi, %rsi\n\t"
        "xor %r8, %r8\n\t"
        "xor %r9, %r9\n\t"
        "xor %r10, %r10\n\t"
        "xor %r11, %r11\n\t"
        "xor %r12, %r12\n\t"
        "xor %r13, %r13\n\t"
        "xor %r14, %r14\n\t"
        "xor %r15, %r15\n\t"
        "xor %rbp, %rbp\n\t"
        "xor %rsp, %rsp\n\t");
}


#define MTDO "Still want a shell!\n"


int main() {
    void *data;
    data = mmap(0, 0x1000, 7, 0x22, -1, 0);
    read(0, data, 0x200);
    register long rax __asm__("rax") = data;
    reset_register();
    asm("jmp %rax");
    return 0;
}

int _start() {
    main();
    exit(0);
}

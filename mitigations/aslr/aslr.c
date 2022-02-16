#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <stdio.h>

#define PS1SIZE 100

char ps1[PS1SIZE];

int main(){
  char echostring[100];
  int l;
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  puts("Welcome to Leakers!\n");
  if (mprotect((long)ps1 & 0xfffffffffffff000, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC) == -1){
    puts("Failed mprotect!");
    return -1;
  }
  l = read(0, ps1, PS1SIZE);
  if (l>1){
    ps1[l-1]='\x00';
   }
  while(2){
    l = read(0, echostring, 200);
    if(l == 1 && (echostring[0] == '\n' || echostring[0] == '\x00')){
      puts("Bye!");
      break;
    }
    printf("%s> %s", ps1, echostring);
  }

}

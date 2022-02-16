#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
typedef void sigrout_t(void);

#define MAXCHAR 20

char buffer[MAXCHAR];

void get_name(char *local_buf){
  int i = 0;
  printf("What is your name?\n");
  read(0, buffer, MAXCHAR);
  memcpy(local_buf, buffer, MAXCHAR);
}

void prog(){
  char local_buf[MAXCHAR];
  get_name(local_buf);
  printf("Hello Mr.%s\n", local_buf);
}

int main(){
  sigrout_t * ptr;
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  printf("   _____ __    _____ ____                __ _____ _    __ ___\n  / ___// /_  |__  // / /_________  ____/ /|__  /| |  / /|__ \\\n  \\__ \\/ __ \\  /_ </ / // ___/ __ \\/ __  /  /_ < | | / / __/ /\n ___/ / / / /___/ / / // /__/ /_/ / /_/ / ___/ / | |/ / / __/ \n/____/_/ /_//____/_/_/ \\___/\\____/\\__,_/ /____/  |___/ /____/ \n                                                             \n  ");
  prog();
  printf("Executing you shellcode.");
  ptr = buffer;
  ptr();
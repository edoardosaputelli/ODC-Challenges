#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char buffer[1000];

void get_name(char *local_buf){
  int i = 0;
  printf("What is your name?\n");
  read(0, buffer, 1000);
  for (i = 0; i < 1000; i++){
      if (buffer[i] == 0){
          printf("Nonono!\n");
          exit(-1);
      }
  }
  memcpy(local_buf, buffer, 1000);
}

void prog(){
  char local_buf[200];
  get_name(local_buf);
  printf("Hello Mr.%s\n", local_buf);
}

int main(){
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  printf("   _____ __    _____ ____                __ _____ _    __ ___\n  / ___// /_  |__  // / /_________  ____/ /|__  /| |  / /|__ \\\n  \\__ \\/ __ \\  /_ </ / // ___/ __ \\/ __  /  /_ < | | / / __/ /\n ___/ / / / /___/ / / // /__/ /_/ / /_/ / ___/ / | |/ / / __/ \n/____/_/ /_//____/_/_/ \\___/\\____/\\__,_/ /____/  |___/ /____/ \n                                                             \n  ");
  prog();

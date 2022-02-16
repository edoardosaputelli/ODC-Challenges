#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char buffer[0x1000];

void get_name(char *local_buf){
  printf("What is your name?\n");
  read(0, buffer, 0x1000);
  memcpy(local_buf, buffer, 0x1000);
}

void prog(){
  char local_buf[1000];
  get_name(local_buf);
  printf("Hello Mr.%s\n", local_buf);
}

int main(){
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  printf("  _________.__           .__  .__                   .___      \n /   _____/|  |__   ____ |  | |  |   ____  ____   __| _/____  \n \\_____  \\ |  |  \\_/ __ \\|  | |  | _/ ___\\/  _ \\ / __ |/ __ \\ \n /        \\|   Y  \\  ___/|  |_|  |_\\  \\__(  <_> ) /_/ \\  ___/ \n/_______  /|___|  /\\___  >____/____/\\___  >____/\\____ |\\___  >\n        \\/      \\/     \\/               \\/           \\/    \\/ \n\n\n\n");
  prog();
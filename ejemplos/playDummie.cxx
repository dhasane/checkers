#include <iostream>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <vector>
#include <iostream>
#include <fstream>
using namespace std;

int * makepos(int x, int y){
  int* pos=new int[2];
  pos[0]=x;
  pos[1]=y;
  return pos;
}


void send(char* pipe,char*  msg){
  int pipeM = open(pipe, O_WRONLY);
  write(pipeM,msg, strlen(msg)+1);
  close(pipeM);
}

char *get(char* pipe,char* msg){
  int pipeT = open(pipe, O_RDONLY);
  read(pipeT,msg,35);
  close(pipeT);
  return msg;
}

char getTablero(char* pipe,char **tablero){
  char msg[35];
  get(pipe,msg);
  int pos=0;
  for(int i=0;i<8;i++){
    for(int j=0;j<8;j++){
      if((i+j)%2==0){
        tablero[i][j]=msg[pos];
        pos++;
      }else{
        tablero[i][j]='-';
      }
    }
  }
  return msg[33];
}

void sendMove(char* pipe,vector<int*> M){
  char msg[M.size()*4];
  for(int i=0;i<M.size();i++){
    msg[i*4]=M[i][0]+97;
    msg[i*4+1]=',';
    msg[i*4+2]=M[i][1]+48;
    msg[i*4+3]=';';
  }
  msg[M.size()*4-1]=0;
  send(pipe,msg);
}



int main(int argc, char *argv[]){


  char *pipeT,*pipeM;
  strcpy(pipeT,"pipe");strcat(pipeT,argv[0]+2);strcat(pipeT,"T");
  strcpy(pipeM,"pipe");strcat(pipeM,argv[0]+2);strcat(pipeM,"M");
  cout<< pipeT<<endl;
  cout<< pipeM<<endl;
  //seguro
  char msg[35];
  char **tablero=new char*[8];
  for(int i=0;i<8;i++){tablero[i]=new char[8];}
  char j=' ';
  vector<int*> M1,M2,M;

  M1.push_back(makepos(2,0));M1.push_back(makepos(3,1));
  M2.push_back(makepos(5,1));M2.push_back(makepos(4,0));


  while(true){
    j=getTablero(pipeT,tablero);
    if(j=='X'){M=M1;}else{M=M2;}
    sendMove(pipeM,M);
  }

}

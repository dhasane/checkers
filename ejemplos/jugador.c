

// general ---
# include <stdio.h> 
# include <string.h>  
# include <stdlib.h>

// pipes -----
# include <fcntl.h>
# include <unistd.h>

//# include "comunicacion.cxx"

# include <time.h>
# include <stdio.h> 
# include <string.h> 
# include <sys/stat.h> 

# include <signal.h>


char * pipeReceive ;
char * pipeSend;




// al cerrar el programa con ctrl-c
void signalCierre(int sig)
{
    unlink(pipeReceive);
    unlink(pipeSend);
    free(pipeReceive);
    free(pipeSend);
    printf("\n");
    exit(1);
}

// abre el pipe "pipe", envia un mensaje "txt" a traves de este y cierra el pipe
// sin retorno
void send(char* pipe, char txt[])
{
    int fd;
    fd = open(pipe, O_WRONLY);
    write(fd, txt, strlen(txt)+1);
    close(fd);
}

// recive datos a traves de pipe "pipe"
// retorna un string con los datos, por referencia -> ret
void receive(char* pipe, char* ret, int tam)
{
    char txt[tam];
    int fd;
    strcpy(txt," ");
    fd = open(pipe, O_RDONLY);
    read(fd, txt, sizeof(txt));
    close(fd);
    strcpy(ret,txt);
}

char conseguirTablero(char* pipe,char tablero[][8]){
  char msg[35];
  receive(pipe,msg,35);
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

// por si acaso
void imprimirTablero(char tablero[][8])
{
    printf(" |0|1|2|3|4|5|6|7|\n");
    for( int a = 0 ; a < 8 ;a++ )
    {
        printf("%d",a);
        for ( int b = 0 ; b < 8 ; b++ )
        {
            printf("|%c",tablero[a][b]);
        }
        printf("|\n");
    }
}

// una jugada perfectamente aleatoria, muy probablemente invalida, sis valida, fue pura casualidad
void decidirJugadaRandom(char * jugada)
{
    int num = 0, num2 = 0;
    char mov;

    int sig = 1 ; 
    int porc = 5;
    strcpy(jugada,"");
    srand(time(NULL)); 
    while(sig)
    {
        num  = (rand() % 8) + '0'; 
        num2 = (rand() % 8) + '0'; 
        
        sprintf(jugada,"%s%c,%c",jugada,num,num2);

        
        sig = 0;

        if ((rand() % 8) > porc)
        {
            sig = 1;
            sprintf(jugada,"%s;",jugada);
            porc --;
        }
    }
}


int main(int argc, char **argv)
{ 
    signal(SIGINT, signalCierre);

    int fd; 
    pipeReceive = (char*)malloc(sizeof(char)*strlen(argv[0]+7) );
    pipeSend    = (char*)malloc(sizeof(char)*strlen(argv[0]+7) );

    sprintf(pipeReceive,"pipe%sT",argv[0]+2);
    sprintf(pipeSend,"pipe%sM",argv[0]+2);

    printf("%s\n%s\n%s\n",argv[0],pipeSend,pipeReceive);
    char tablero [8][8];
    char jugador[2];
    
    // jugadas -------------------------------------------------
    char jugada[50];
    while(1){
        conseguirTablero(pipeReceive,tablero);
        decidirJugadaRandom(jugada);
        //printf("%s\n",jugada);
        send(pipeSend, jugada );
    }
    // fin jugadas ---------------------------------------------

    free(pipeReceive);
    free(pipeSend);

    return 0; 
} 

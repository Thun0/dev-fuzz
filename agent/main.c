#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdlib.h>

#define PORT 42501
#define MAX_MSG_LEN 4096

#define MSG_DEV_PATH 1
#define MSG_IOCTL 2
#define MSG_WRITE 3
#define MSG_MMAP 4

char driver_path[4096];

int create_listen_socket()
{
    struct sockaddr_in serv_addr;
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(PORT); 
    bind(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    return sock;
}

void start_receiver(int sock)
{
    printf("Started receiver\n");
    while(1)
    {
        char msg[MAX_MSG_LEN+1];
        memset(msg, 0, MAX_MSG_LEN);
        int read_len = recv(sock, msg, MAX_MSG_LEN, 0);
        if(!read_len)
        {
            printf("Connection finished!\n");
            break;
        }
        printf("Recv %d\n", read_len);
        if(read_len < 4)
        {
            printf("ERROR: Message is too short!\n");
            continue;
        }
        printf("Received %d bytes of data: %s\n", read_len, msg);
        for(int i = 0; i < read_len; ++i)
            printf("0x%x ", msg[i]);
        int msg_type = msg[3]<<24 | msg[2]<<16 | msg[1]<<8 | msg[0];
        char* rest_msg = &msg[4];
        if(msg_type == MSG_DEV_PATH)
        {
            printf("Got path!\n");
            int path_len = rest_msg[3]<<24 | rest_msg[2]<<16 | rest_msg[1]<<8 | rest_msg[0];
            if(path_len >= 4096)
            {
                printf("ERROR: Driver path too long!\n");
                continue;
            }
            strncpy(driver_path, &rest_msg[4], path_len);
            driver_path[path_len] = '\0';
            printf("Received dev path[%d]: %s\n", (int)strlen(driver_path), driver_path);
        }
        else if(msg_type == MSG_IOCTL)
        {
        }
        else if(msg_type == MSG_WRITE)
        {
        }
        else if(msg_type == MSG_MMAP)
        {
        }
        else
        {
        }
    }
}

int main()
{
    int listen_socket = create_listen_socket();
    listen(listen_socket, 10);
    printf("Starting to listen...\n");
    while(1)
    {
        struct sockaddr_in rec_addr;
        int ssize = sizeof(struct sockaddr_in);
        int rec_sock = accept(listen_socket, (struct sockaddr*)&rec_addr, (socklen_t*)&ssize);
        char ip_str[INET_ADDRSTRLEN];
        if(inet_ntop(AF_INET, &(rec_addr.sin_addr), ip_str, INET_ADDRSTRLEN) == NULL)
        {
            printf("ERROR!!\n");
        }
        printf("Connection accepted from %s:%d.\n", ip_str, rec_addr.sin_port);
        start_receiver(rec_sock);
    }
    return 0;
}
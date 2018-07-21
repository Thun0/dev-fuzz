#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <fcntl.h>

#define PORT 42501
#define MAX_MSG_LEN 4096

#define MSG_DEV_PATH 1
#define MSG_IOCTL 2
#define MSG_WRITE 3
#define MSG_MMAP 4

char driver_path[4096];
int driver_fd = -1;

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
        char msg[4];
        memset(msg, 0, 4);
        int read_len = recv(sock, msg, 4, 0);
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
        int msg_type = msg[3]<<24 | msg[2]<<16 | msg[1]<<8 | msg[0];

        char rest_msg[4096];
        if(msg_type == MSG_DEV_PATH)
        {
            printf("Got path!\n");

            recv(sock, rest_msg, 4, 0);
            int path_len = rest_msg[3]<<24 | rest_msg[2]<<16 | rest_msg[1]<<8 | rest_msg[0];
            if(path_len >= 4096)
            {
                printf("ERROR: Driver path too long!\n");
                continue;
            }
            recv(sock, rest_msg, path_len, 0);
            strncpy(driver_path, rest_msg, path_len);
            driver_path[path_len] = '\0';
            printf("Received dev path[%d]: %s\n", (int)strlen(driver_path), driver_path);
            driver_fd =  open(driver_path, O_RDONLY);
            printf("%d\n", driver_fd);
            if(driver_fd > 0)
            {
                printf("Driver opened\n");
            }
            else
            {
                printf("ERR: Failed to open driver\n");
            }
        }
        else if(msg_type == MSG_IOCTL)
        {
            printf("Got IOCTL!\n");
            recv(sock, rest_msg, 8, 0);
            unsigned long request = rest_msg[7]<<56 | rest_msg[6]<<48 | rest_msg[5]<<40 | rest_msg[4]<<32 | rest_msg[3]<<24 | rest_msg[2]<<16 | rest_msg[1]<<8 | rest_msg[0];
            recv(sock, rest_msg, 4, 0);
            int args_len = rest_msg[3]<<24 | rest_msg[2]<<16 | rest_msg[1]<<8 | rest_msg[0];
            printf("Args len: %d\n", args_len);
            char* args = calloc(args_len+1, sizeof(char));
            recv(sock, args, args_len, 0);
            printf("Got args: %s\n", args);
            if(driver_fd < 0)
            {
                printf("%d\n", driver_fd);
                printf("ERR: Fuzzing can't continue. No driver chosen!\n");
                continue;
            }
            printf("Exectuing ioctl on %s..\n", driver_path);

            int ret = ioctl(driver_fd, request, args);
            printf("IOCTL ret code: %d", ret);
            free(args);
        }
        else if(msg_type == MSG_WRITE)
        {
            printf("Got WRITE\n");
        }
        else if(msg_type == MSG_MMAP)
        {
            printf("Got MMAP\n");
        }
        else
        {
            printf("ERR: Unknown message!\n");
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
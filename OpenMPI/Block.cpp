#include <bits/stdc++.h>
#include <iostream>
#include <time.h>
#include "mpi.h"
#define N 8000

using namespace std;

// Function to multiply two Matrices
void Mult(float *A, float *B, float *C, int n, int m, int p){
    // Size(A)=n*m, Size(B)=m*p, Size(C)=n*p
    for(int i = 0; i<n; i++){
        for(int j = 0; j<p; j++){
            C[i*p+j] = 0;
            for(int k = 0; k<m; k++){
                C[i*p+j] += A[i*m+k]*B[k*p+j];
            }
        }
    }
}

// Function to check if the matrices are equal
int IsEqual(float *A, float *B, int n, int m){
    for(int i = 0; i<n; i++){
        for(int j = 0; j<m; j++){
            if(A[i*m+j] != B[i*m+j])
                return 1;
        }
    }
    return 0;
}

void Initialise(float *a, float *b, float *c, int n){
    for(int i = 0; i<n; i++){
        for(int j = 0; j<32; j++){
            a[i*32+j] = 1 + rand()%5;
        }
    }
    for(int i = 0; i<32; i++){
        for(int j = 0; j<n; j++){
            b[i*n+j] = 1 + rand()%5;
        }
    }

    for(int i = 0; i<n; i++){
        for(int j = 0; j<n; j++){
            c[i*n+j] = 0;
        }
    }
}

void PrintMatrix(float *A, int n, int m){
    for(int i = 0; i<n; i++){
        for(int j = 0; j<m; j++){
            cout<<A[i*m+j]<<" ";
        }
        cout<<endl;
    }
    cout<<"------------------\n";
}

int main(int argc, char **argv){
    srand(time(0));
    int rank, total;
    int n = N;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &total);

    int basic = n/total;
    // The Root Process intializes the Matrices and gives to the other process
    if(rank == 0){
        float *a = (float *)malloc(sizeof(float)*N*32);
        float *b = (float *)malloc(sizeof(float)*N*32);
        float *c = (float *)malloc(sizeof(float)*N*N);
        Initialise(a, b, c, n);

        // Sending the Slice of A to different Process
        for(int i = 1; i<total; i++){
            MPI_Send(a + basic*i*32, basic*32, MPI_FLOAT, i, 1, MPI_COMM_WORLD);
            MPI_Send(b, 32*n, MPI_FLOAT, i, 0, MPI_COMM_WORLD);
        } 

        Mult(a, b, c, basic, 32, n);
        float *te = (float *)malloc(sizeof(float)*basic*n);

        // Reciving the Result from different Process
        for(int i = 1; i<total; i++){
            MPI_Recv(c + basic*i*n, basic*n, MPI_FLOAT, i, i, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }

        float *cc = (float *)malloc(sizeof(float)*N*N);
        Mult(a, b, cc, n, 32, n);
        cout<<IsEqual(c, cc, n, n)<<endl;
        free(a);
        free(b);
        free(c);
        free(te);

    }else{
        float *temp = (float *)malloc(sizeof(float)*basic*32);
        float *result = (float *)malloc(sizeof(float)*N*basic);
        float *b = (float *)malloc(sizeof(float)*N*32);
        MPI_Recv(temp,basic*32, MPI_FLOAT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(b,n*32, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        
        Mult(temp, b, result, basic, 32, n);

        MPI_Send(result, basic*n, MPI_FLOAT, 0, rank, MPI_COMM_WORLD);
        free(temp);
        free(result);
        free(b);
    }

    MPI_Finalize();

    return 0;
}

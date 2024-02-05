#include <bits/stdc++.h>
#include <iostream>
#include <time.h>
#include "mpi.h"

// #define N 7000
#define MaxProc 16

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
    int N = stoi(argv[1]);
    int n = N;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &total);

    int basic = n/total;

    MPI_Request recv_req;
    MPI_Request send_req;
    MPI_Status status;

    int ir;

    // The Root Process intializes the Matrices and gives to the other process
    if(rank == 0){
        float *a = (float *)malloc(sizeof(float)*N*32);
        float *b = (float *)malloc(sizeof(float)*N*32);
        float *c = (float *)malloc(sizeof(float)*N*N);
        Initialise(a, b, c, n);

        double start = MPI_Wtime();
        // Sending the Slice of A to different Process
        for(int i = 1; i<total; i++){
            MPI_Isend(a + basic*i*32, basic*32, MPI_FLOAT, i, 1, MPI_COMM_WORLD, &send_req);
            ir = MPI_Wait(&send_req, &status);
        }
    
        // Sending the  slice of B to different Process after transposing the matrix B.
        // float *bb = (float *)malloc(sizeof(float)*N*32);
        // ColumnOrder(bb, b, 32, N);
        // PrintMatrix(bb, N, 32);

        // variable that are defined for every process atemp not necessary as it is constant for a process
        float *rtemp = (float *)malloc(sizeof(float)*basic*basic);
        float *btemp = (float *)malloc(sizeof(float)*basic*32); 

        int offset = 0;
        // ir = MPI_Wait(&send_req, &status);
        // Outer Loops Broadcast values of B to every process and takes the result and store it in the address
        for(int i = 0; i<total; i++){
            // Loop to Broadcast a small set of values of B to every process 
            for(int j = 0; j<total; j++){
                if(j == 0){
                    // Copyping the value of small portion of B in the temp Matrix
                    for(int k = 0; k<32; k++){
                        for(int l = 0; l<basic; l++){
                            btemp[k*basic + l] = b[offset + k*N + l]; 
                        }
                    }
                }else{
                    MPI_Isend(btemp, basic*32, MPI_FLOAT, j, 0, MPI_COMM_WORLD, &send_req);
                    ir = MPI_Wait(&send_req, &status);
                }
            }

            // Calculating the result of the process 0
            Mult(a, btemp, rtemp, basic, 32, basic);

            // Collecting the result from every thread 
            int off = 0;
            for(int k = 0; k<total; k++){
                if(k != 0){
                    MPI_Irecv(rtemp, basic*basic, MPI_FLOAT, k, k, MPI_COMM_WORLD, &recv_req);  
                    int ir = MPI_Wait(&recv_req, &status);
                }
                for(int l = 0; l<basic; l++){
                    for(int m = 0; m<basic; m++){
                        c[offset + off +l*N + m] = rtemp[l*basic + m];
                    }
                }
                off += basic*N;
            }
            offset += basic;
        }

        double end = MPI_Wtime();
        cout<<"Time taken by the parallel programm "<<end - start<<endl;

        start = MPI_Wtime();
        // Verification done here 
        float *cc = (float *)malloc(sizeof(float)*N*N);
        Mult(a, b, cc, n, 32, n);
        end = MPI_Wtime();
        cout<<"Time taken by the Serial Program "<<end - start<<endl;
        cout<<IsEqual(c, cc, n, n)<<endl;

        // Releasing the memory
        free(a);    
        free(b);
        free(c);
        free(rtemp);
        free(btemp);
        free(cc);

    }else{
        float *atemp = (float *)malloc(sizeof(float)*basic*32);
        float *rtemp = (float *)malloc(sizeof(float)*basic*basic);
        float *btemp = (float *)malloc(sizeof(float)*basic*32);

        MPI_Irecv(atemp,basic*32, MPI_FLOAT, 0, 1, MPI_COMM_WORLD, &recv_req);
        int ir = MPI_Wait(&recv_req, &status);

        for(int i = 0; i<total; i++){
            MPI_Irecv(btemp, basic*32, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, &recv_req);
            ir = MPI_Wait(&recv_req, &status);
            Mult(atemp, btemp, rtemp, basic, 32, basic);
            MPI_Isend(rtemp, basic*basic, MPI_FLOAT, 0, rank, MPI_COMM_WORLD, &send_req);
            ir = MPI_Wait(&send_req, &status);
        }

        free(atemp);
        free(rtemp);
        free(btemp);
    }

    MPI_Finalize();

    return 0;
}
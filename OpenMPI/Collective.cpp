#include <bits/stdc++.h>
#include <iostream>
#include <time.h>
#include "mpi.h"

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

    float *a = (float *)malloc(sizeof(float)*N*32);
    float *b = (float *)malloc(sizeof(float)*N*32);
    float *c = (float *)malloc(sizeof(float)*N*N);
    float *cc = (float *)malloc(sizeof(float)*N*N);

    float *atemp = (float *)malloc(sizeof(float)*basic*32);
    float *rtemp = (float *)malloc(sizeof(float)*basic*basic);
    float *btemp = (float *)malloc(sizeof(float)*basic*32); 

    float *tempans = (float *)malloc(sizeof(float)*N*basic);

    if(rank == 0){
        Initialise(a, b, c, n);
    }
    // MPI_Barrier(MPI_COMM_WORLD);
    double start = MPI_Wtime();
    double end;
    MPI_Scatter(a, 32*basic, MPI_FLOAT, atemp, 32*basic, MPI_FLOAT, 0, MPI_COMM_WORLD);

    int offset = 0;
    // Outer Loops Broadcast values of B to every process and takes the result and store it in the address
    for(int i = 0; i<total; i++){
        if(rank == 0){
            // Copyping the value of small portion of B in the temp Matrix
            for(int k = 0; k<32; k++){
                for(int l = 0; l<basic; l++){
                    btemp[k*basic + l] = b[offset + k*N + l]; 
                }
            }
        }

        MPI_Bcast(btemp, basic*32, MPI_FLOAT, 0, MPI_COMM_WORLD);

        Mult(atemp, btemp, rtemp, basic, 32, basic);

        MPI_Gather(rtemp, basic*basic, MPI_FLOAT, tempans, basic*basic, MPI_FLOAT, 0, MPI_COMM_WORLD);

        if(rank == 0){
            for(int k = 0; k<N; k++){
                for(int l = 0; l<basic; l++){
                    c[offset+ k*N + l] = tempans[k*basic + l];
                }
            }
        }
        offset += basic;
    }
    end = MPI_Wtime();

    if(rank == 0){
        cout<<"Time taken by the parallel programm "<<end - start<<endl;
        start = MPI_Wtime();

        // Verification done here 
        Mult(a, b, cc, n, 32, n);
        end = MPI_Wtime();
        cout<<"Time taken by the Serial Program "<<end - start<<endl;
        cout<<IsEqual(c, cc, n, n)<<endl;
    }

    free(a);    
    free(b);
    free(c);
    free(cc);
    free(atemp);
    free(btemp);
    free(rtemp);

    MPI_Finalize();

    return 0;
}
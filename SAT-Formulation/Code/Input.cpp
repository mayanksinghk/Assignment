#include "commonlib.h"
#include "node.h"
#include<bits/stdc++.h>
#include<iostream>


//Function for reading the file 
int read(int &v1, int &v2, char *arg[]){
    string s=arg[1];
    ifstream input;
    ofstream outp("size.txt");
    input.open(s.append(".graphs"));

    int a, b;
    while (input >> a >> b)
    {
        if(a==0 && b==0){
            break;
        }
        if(a>=v1){
            v1=a;
        }
        if(b>=v1){
            v1=b;
        }
        
    }
    
    while (input >> a >> b){
        if(a>=v2){
            v2=a;
        }
        if(b>=v2){
            v2=b;
        }
        
    }
    outp<<v1<<" "<<v2;
    return 0;
}

// Function to convert graph to adjacency matrix or adjacency list
void convert(vector<vector<int>> &graph1, vector<vector<int>> &graph2, char *arg[]){
    ifstream input2;
    string s=arg[1];
    input2.open(s.append(".graphs"));
    int a, b;

    while (input2 >> a >> b)
    {   
        if(a==0 && b==0){
            break;
        }
        graph1[a-1][b-1]=1;
    }
    
    while (input2 >> a >> b){
        graph2[a-1][b-1]=1;
    }
}

//sample int main implementation
/*int main(int argc, char *argv[]) 
{
    int c=0;
    int c2=0;
    
    read(c, c2, argv);
    //G1 is the bigger graph and G2 is the smaller graph
    //This code is for the adjacency matrix
    vector<vector<int>> G1(c, vector<int> (c, 0));
    vector<vector<int>> G2(c2, vector<int> (c2, 0));
    convert(c, c2, G1, G2, argv);

    return 0;
}
*/
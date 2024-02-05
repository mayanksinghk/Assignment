#include "commonlib.h"
#include<bits/stdc++.h>
//Main will join our code and can be used for testing purposes. Define global variable in commonlib.h if any.
int si1, si2;
int main(int argc, char *argv[]) 
{
    
    int c=0;
    int c2=0;
    string s;
    s = argv[1];
    read(c, c2, argv);
    si1=c;
    si2=c2;
    //G1 is the bigger graph and G2 is the smaller graph
    //This code is for the adjacency matrix
    vector<vector<int> > G1(c, vector<int> (c, 0));
    vector<vector<int> > G2(c2, vector<int> (c2, 0));
    convert(G1, G2, argv);

    // ofstream fout("ans.txt", ios::in | ios::app);
    // fout<<"p cnf "<<c*c2;
    int count1 = Unique(G2, G1);
    int count2 = Clauses(G2, G1);
    // cout<<endl<<endl;
    // cout<<count1<<endl;
    // cout<<count2<<endl;
    // cout<<count1 + count2<<endl;
    ofstream fout(s.append(".satinput"), ios::in | ios::app);
    fout<<"p cnf "<<c*c2<<" "<<count1+count2<<endl;

    ifstream fin;
    fin.open("ans.txt");
    int flag = 0; 
    for( std::string line; getline( fin, line ); ){
        if(flag == 0){
            flag = 1;
            fout<<line;
        }else{
            fout<<endl<<line;
        }
    }

    return 0;
}
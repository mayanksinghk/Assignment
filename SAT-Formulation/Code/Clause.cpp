#include "commonlib.h"
#include<bits/stdc++.h>
int Clauses(vector<vector<int> >GraphE, vector<vector<int> >GraphP){
    int m1 = GraphE.size();
    int m2 = GraphP.size();
    int n1 = GraphE[0].size();
    int n2 = GraphP[0].size();

    int count = 0;
    ofstream fout("ans.txt", ios::in | ios::app);
    // cout<<"print";
    //Taking one edge at a time
    for(int i1 = 0; i1<m1; i1++){
        for(int i2 = 0; i2<n1; i2++){

            //If i1 emails i2 then i1 must have called i2 at some point
            if(GraphE[i1][i2] == 1){
                for(int j1 = 0; j1<m2; j1++){
                    int flag = 0;
                    for(int j2 = 0; j2<n2; j2++){
                        if(GraphP[j1][j2] == 1 && j1 != j2){
                            flag = 1;
                            // cout<<i1*m2 + j1 + 1<<" ";
                            //If there is an edge between i1 and j1 then there must be an edge between i2 and j2
                            fout<<-1*(i1*m2 + j1 + 1)<<" "<<(i2*m2 + j2 + 1)<<" ";
                        }
                    }
                    if(flag == 1){
                        fout<<0<<endl;
                        count++;
<<<<<<< HEAD

                    }
                    
                }
=======
                    }
                    
                }
                // cout<<0<<endl;
                // fout<<0<<endl;
                
>>>>>>> 1af176e553c3e29f5da482ceffa73ad90f530cea
            }

            //If i1 does not email i2 then i1 did not i2 
            if(GraphE[i1][i2] != 1){
                for(int j1 = 0; j1<m2; j1++){
                    int flag = 0;
                    for(int j2 = 0; j2<n2; j2++){
                        if(GraphP[j1][j2] != 1 && j1 != j2){
                            flag = 1;
                            // cout<<i1*m2 + j1 + 1<<" ";
                            //If there is no edge between i1 and j1 then there must not be an edge between i2 and j2 (-Ei1Pj1 -> -Ei2Pj2)
                            fout<<i1*m2 + j1 + 1<<" "<<-1*(i2*m2 + j2 + 1)<<" ";
                        }
                    }
                    if(flag == 1){
                        fout<<0<<endl;
                        count++;
                    }
                }
<<<<<<< HEAD
=======
                // cout<<0<<endl;
                // fout<<0<<endl;
                
>>>>>>> 1af176e553c3e29f5da482ceffa73ad90f530cea
            }

        }
    }

    return count;
}

int Unique(vector<vector<int> > GraphE, vector<vector<int> > GraphP){
    int m1 = GraphE.size();
    int m2 = GraphP.size();
    int n1 = GraphE[0].size();
    int n2 = GraphP[0].size();
    
    int count = 0;

    ofstream fout("ans.txt", ios::in | ios::app);

    //Each var has at least 1 value      X WA-r v X WA-g v X WA-b
    for(int i = 0; i<m1; i++){
        for(int j = 0; j<m2; j++){
            // cout<<i*m2+j+1<<" ";
            fout<<i*m2+j+1<<" ";
        }
        // cout<<0<<endl;
        fout<<0<<endl;
        count++;
    }

    // cout<<"------------------------------\n";
    //No var has two values
    for(int i = 0; i<m1; i++){
        for(int j1 = 0; j1<m2-1; j1++){
            // cout<<i*m2 + j1 + 1<<" ";
            for(int j2 = j1 + 1; j2<m2; j2++){
                // cout<<-1*(i*m2 + j1 + 1)<<" "<<-1*(i*m2 + j2 + 1)<<" 0"<<endl;
                fout<<-1*(i*m2 + j1 + 1)<<" "<<-1*(i*m2 + j2 + 1)<<" 0"<<endl;
                count++;
            }
        }
    }

    // cout<<"------------------------------\n";
    //Constraints no email has same value
    for(int j = 0; j<m2; j++){
        for(int i1 = 0; i1<m1; i1++){
            for(int i2 = 0; i2<m1; i2++){
                if(i1 != i2){
                    // cout<<-1*(i1*m2 + j + 1)<<" "<<-1*(i2*m2 + j + 1)<<" 0"<<endl;
                    fout<<-1*(i1*m2 + j + 1)<<" "<<-1*(i2*m2 + j + 1)<<" 0"<<endl;
                    count++;
                }
            }
        }
    }

    //cout<<"------------------------------\n";
    return count;
}


//Numbering pattern EiPj = i*(no. of total j) + j + 1
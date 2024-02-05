#include<iostream>
#include<bits/stdc++.h>
using namespace std;

void outwrite(string s, string s2){
    string x("../");
    ifstream input(s.append(".satoutput"));
    ofstream out,temp;
    int si1,si2;
    
    out.open(s2.append(".mapping"));
    ifstream fin("./size.txt");
    fin>>si1>>si2;
    
    std::string ran;
    string sat("SAT");
    getline(input, ran);
    if (ran!=sat){
        out<<0;
    }
    else{
    getline(input, ran);
    
    int i=0,num,max=0;
    
    istringstream is( ran );
    
    while( is >> num ) { 
        if(num>max){
            max=num;
        }
        i++;
    }
    
    i=0;
    istringstream is1( ran );
    while( is1 >> num ) { 
        if(num==(i+1)){
            if(num<max){
            // cout<<(i/si1)+1<<" "<<(i%si1)+1<<endl;
            //cout<<si1<<endl;
            out<< (i/si1)+1<<" "<<(i%si1)+1<<endl;
            }
            else{
                out<< (i/si1)+1<<" "<<(i%si1)+1;
            }
        }
        i++;
    }


    //ifstream tinp("temp.txt");
    //for( std::string line; getline( tinp, line ); ){
    //    if(line!=""){
    //        cout<<line<<endl;
    //        out<<line<<endl;
    //    }
    //}
    
    }
    out.close();
    input.close();
    fin.close();
}

int main(int argc, char *argv[]){
    outwrite(argv[1], argv[1]);
    return 0;
}
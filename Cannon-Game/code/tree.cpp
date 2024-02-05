#include "tree.h"

//expands the children. for d = 0 children of root are leaves.
//DONT SET CHILDREN BEFORE CREATE TREE FUNCTION!!
//d = 2 reasonable
void create_tree(Node* root,int d){
  (*root).SetChildren();

  if (d != 0 ){
    d--;
    vector<Node*> succ = (*root).GetChildren();
    // if (succ.size()==0){
    //   cerr<<"No Successors"<<endl;
    // }
    // cout<<"Current depth: "<<d+1<<" Number of children = "<<succ.size()<<endl;
    for (int k = 0; k<succ.size(); k++){
      Node* curr_child = succ[k];
      create_tree(curr_child,d);
    }
  }
}

void print_board_new(vector<vector<int> > v){
  for (int i = 0; i< v.size() ; i++){
    vector<int> ll = v[i];
    for (int j = 0; j < ll.size();j++){
      cout<<ll[j]<<"  ";
    }
    cout<<endl;
  }
}

#include "node.h"



void Node::SetBoard(vector<vector<int> > temp){
    board_config = temp;
}
void Node::SetBlack(bool t){
  black = t;
}

void Node::SetMove(MOVE m){
  move = m;
}


void Node::SetEval(float t){
  eval = t;
}


Node* Node::newNode(vector<vector<int> > new_board, MOVE move, bool black ){
  Node* temp = new Node;
  (*temp).SetBlack(!black);
  (*temp).SetBoard(new_board);
  (*temp).SetMove(move);
  // print_move((*temp).GetMove());
  return temp;
}


//Use this function only once!
void Node::SetChildren(){
  int n = board_config.size();
  int m = board_config[0].size();
  // cout <<n<<" "<<m<<" ";
  int b_size;
  if (n==8){
    b_size=1;
  }else if(m == 8){
    b_size =2;
  }else{
    b_size=3;
  }
  vector<coord> black_soldiers = Soldiers_list(1,board_config);
  vector<coord> white_soldiers = Soldiers_list(-1,board_config);
  //first is black and second is white
  tuple<vector<CANNON>,vector<CANNON> > cannon_lists = Update(board_config);
  // print_cannon(get<0>(cannon_lists));
  //if current chance is black
  vector<MOVE> next_possibilities;
  children.clear();
  if (GetBlack() == true){
    next_possibilities = next_moves(get<0>(cannon_lists),black_soldiers,white_soldiers,true,b_size);
  }  else{
    next_possibilities = next_moves(get<1>(cannon_lists),white_soldiers,black_soldiers,false,b_size);
  }
  for (int j =0; j<next_possibilities.size();j++){
    MOVE curr_move = next_possibilities[j];
    // cout << get<0>(curr_move)<< get<1>(curr_move)<< get<2>(curr_move)<< get<3>(curr_move)<< get<4>(curr_move)<< get<5>(curr_move)<<endl;
    vector<vector <int> > new_board =Update_board(curr_move,board_config);
    Node* next_state = newNode(new_board,curr_move,GetBlack());
    // print_board_new(new_board);
    (children).push_back(next_state);
  }
}

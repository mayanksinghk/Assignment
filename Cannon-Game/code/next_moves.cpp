#include "next_moves.h"



vector<MOVE> next_moves(vector<CANNON> cannon_list, vector<coord> soldier_list, vector<coord> opp_soldier_list, bool black,int b_size) {
  int l;
  int b;
  if (b_size ==1){
    l=8;
    b=8;
  }else if (b_size==2){
    l=8;
    b=10;
  }else{
    l =10;
    b =10;
  }
  // cout<<"l: "<<l<<" b: "<<b;
  vector<MOVE> possibilities;
  MOVE curr_move;
  tuple<vector<coord>,vector<coord> > tup = create_th_list(b_size);
  vector<coord> white_town_halls = get<0>(tup);
  vector<coord> black_town_halls = get<1>(tup);
  vector<coord>own_town_halls,opposition_town_halls;
  if (black){
    own_town_halls = black_town_halls;
    opposition_town_halls = white_town_halls;
  } else{
    own_town_halls = white_town_halls;
    opposition_town_halls = black_town_halls;
  }

  //individual soldier's moves
  for (int i = 0; i < soldier_list.size(); i++){
    coord curr_sold = soldier_list[i];
    vector<coord> all_mov = soldier_moves(curr_sold, opp_soldier_list, black);
    vector<coord> fil_mov = moves_filter(all_mov,soldier_list,l,b); //Not on your own soldiers.
    fil_mov = moves_filter(fil_mov,own_town_halls,l,b);  //Not on your own town halls.
    vector<MOVE> curr_sol_moves = coord_to_move(curr_sold,fil_mov);
    possibilities.reserve(possibilities.size() + distance(curr_sol_moves.begin(),curr_sol_moves.end()));
    possibilities.insert(possibilities.end(),curr_sol_moves.begin(), curr_sol_moves.end());
  }
  vector<MOVE> curr_cannon_moves = cannon_action(cannon_list,soldier_list, opp_soldier_list,own_town_halls,opposition_town_halls);
  possibilities.reserve(possibilities.size() + distance(curr_cannon_moves.begin(),curr_cannon_moves.end()));
  possibilities.insert(possibilities.end(),curr_cannon_moves.begin(), curr_cannon_moves.end());

  return possibilities;
}

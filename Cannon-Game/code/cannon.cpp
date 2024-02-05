#include "cannon.h"

// 0: horizontal
// 1: vertical
// 2: away from origin
// 3: towards origin

int orientation(CANNON c){
  coord f = get<0>(c);
  coord s = get<1>(c);
  coord t = get<2>(c);
  int den = f.x - t.x;
  int num = f.y - t.y;
  if (num == 0){
    return 0;
  } else if (den == 0){
    return 1;
  } else{
    return (int)((((float)(num/den))/2)+2.5);
  }
}


vector<MOVE> cannon_coord_to_shot(coord soldier, vector<coord> shots){
  vector<MOVE> shts ;
  for (int k = 0; k < shots.size(); k++){
    coord curr_coord = shots[k];
    MOVE tmp;
    tmp = make_tuple('S',soldier.x,soldier.y,'B',curr_coord.x,curr_coord.y);
    shts.push_back(tmp);
  }
  return shts;
}

MOVE cannon_coord_to_move(coord soldier, coord move, int n, int m){
  MOVE tmp;
  if (move.x >= 0 && move.x < n && move.y >= 0 && move.y < m){
    tmp = make_tuple('S',soldier.x,soldier.y,'M',move.x,move.y);
  }else{
    tmp = make_tuple('A',0,0,'A',0,0);
  }
  return tmp;
}

vector<MOVE> cannon_action(vector<CANNON> cannon_list,vector<coord> soldier_list, vector<coord> opp_soldier_list, vector<coord> own_ths, vector<coord> opp_ths){
  vector<MOVE> possibilities;
  vector<coord> all_soldiers, all_ths;
  all_soldiers.insert(all_soldiers.end(),soldier_list.begin(),soldier_list.end());
  all_soldiers.insert(all_soldiers.end(),opp_soldier_list.begin(),opp_soldier_list.end());
  all_ths.insert(all_ths.end(),opp_ths.begin(),opp_ths.end());
  all_ths.insert(all_ths.end(),own_ths.begin(),own_ths.end());

  for (int i = 0;i < cannon_list.size(); i++){
    CANNON curr_cannon = cannon_list[i];
    vector<coord> shots;
    vector<MOVE> cannon_moves;
    coord f = get<0>(curr_cannon);
    coord s = get<1>(curr_cannon);
    coord t = get<2>(curr_cannon);
    int orie = orientation(curr_cannon);
    coord lb,rb,shot1,shot2,c_dest,s_move;
    MOVE cannon_shift;
    if (orie == 0){
      lb.x = s.x - 2;
      rb.x = s.x + 2;
      lb.y = rb.y = s.y;
      if (contains(lb,all_soldiers) == false && contains(lb,all_ths) == false){
        c_dest = lb;
        if (f.x > t.x){
          s_move = f;
        }else{
          s_move = t;
        }
        cannon_shift = cannon_coord_to_move(s_move,c_dest);
        char t = get<0>(cannon_shift);
        if (t != 'A'){
          cannon_moves.push_back(cannon_shift);
        }
        shot1.x = s.x - 3;
        shot2.x = s.x - 4;
        shot1.y = shot2.y = s.y;
        shots.push_back(shot1);
        shots.push_back(shot2);
      }
      if (contains(rb,all_soldiers) == false && contains(rb,all_ths) == false){
        c_dest = rb;
        if (f.x < t.x){
          s_move = f;
        }else{
          s_move = t;
        }
        cannon_shift = cannon_coord_to_move(s_move,c_dest);
        char t = get<0>(cannon_shift);
        if (t != 'A'){
          cannon_moves.push_back(cannon_shift);
        }
        shot1.x = s.x + 3;
        shot2.x = s.x + 4;
        shot1.y = shot2.y = s.y;
        shots.push_back(shot1);
        shots.push_back(shot2);
      }
    }else if (orie == 1){
      lb.y = s.y - 2;
      rb.y = s.y + 2;
      lb.x = rb.x = s.x;
      if (contains(lb,all_soldiers) == false && contains(lb,all_ths) == false){
        c_dest = lb;
        if (f.y > t.y){
          s_move = f;
        }else{
          s_move = t;
        }
        cannon_shift = cannon_coord_to_move(s_move,c_dest);
        char t = get<0>(cannon_shift);
        if (t != 'A'){
          cannon_moves.push_back(cannon_shift);
        }
        shot1.y = s.y - 3;
        shot2.y = s.y - 4;
        shot1.x = shot2.x = s.x;
        shots.push_back(shot1);
        shots.push_back(shot2);
      }
      if (contains(rb,all_soldiers) == false && contains(rb,all_ths) == false){
        c_dest = rb;
        if (f.y < t.y){
          s_move = f;
        }else{
          s_move = t;
        }
        cannon_shift = cannon_coord_to_move(s_move,c_dest);
        char t = get<0>(cannon_shift);
        if (t != 'A'){
          cannon_moves.push_back(cannon_shift);
        }
        shot1.y = s.y + 3;
        shot2.y = s.y + 4;
        shot1.x = shot2.x = s.x;
        shots.push_back(shot1);
        shots.push_back(shot2);
      }

    }else if (orie == 2){
      lb.x = s.x - 2;
      rb.x = s.x + 2;
      lb.y = s.y + 2;
      rb.y = s.y - 2;
      if (contains(lb,all_soldiers) == false && contains(lb,all_ths) == false){
        c_dest = lb;
        if (f.x > t.x){
          s_move = f;
        }else{
          s_move = t;
        }
        cannon_shift = cannon_coord_to_move(s_move,c_dest);
        char t = get<0>(cannon_shift);
        if (t != 'A'){
          cannon_moves.push_back(cannon_shift);
        }
        shot1.x = s.x - 3;
        shot2.x = s.x - 4;
        shot1.y = s.y + 3;
        shot2.y = s.y + 4;
        shots.push_back(shot1);
        shots.push_back(shot2);
      }
      if (contains(rb,all_soldiers) == false && contains(rb,all_ths) == false){
        c_dest = rb;
        if (f.x < t.x){
          s_move = f;
        }else{
          s_move = t;
        }
        cannon_shift = cannon_coord_to_move(s_move,c_dest);
        char t = get<0>(cannon_shift);
        if (t != 'A'){
          cannon_moves.push_back(cannon_shift);
        }
        shot1.x = s.x + 3;
        shot2.x = s.x + 4;
        shot1.y = s.y - 3;
        shot2.y = s.y - 4;
        shots.push_back(shot1);
        shots.push_back(shot2);
      }

    }else{
      lb.x = s.x - 2;
      rb.x = s.x + 2;
      lb.y = s.y - 2;
      rb.y = s.y + 2;
      if (contains(lb,all_soldiers) == false && contains(lb,all_ths) == false){
        c_dest = lb;
        if (f.x > t.x){
          s_move = f;
        }else{
          s_move = t;
        }
        cannon_shift = cannon_coord_to_move(s_move,c_dest);
        char t = get<0>(cannon_shift);
        if (t != 'A'){
          cannon_moves.push_back(cannon_shift);
        }
        shot1.x = s.x - 3;
        shot2.x = s.x - 4;
        shot1.y = s.y - 3;
        shot2.y = s.y - 4;
        shots.push_back(shot1);
        shots.push_back(shot2);
      }
      if (contains(rb,all_soldiers) == false && contains(rb,all_ths) == false){
        c_dest = rb;
        if (f.x < t.x){
          s_move = f;
        }else{
          s_move = t;
        }
        cannon_shift = cannon_coord_to_move(s_move,c_dest);
        char t = get<0>(cannon_shift);
        if (t != 'A'){
          cannon_moves.push_back(cannon_shift);
        }
        shot1.x = s.x + 3;
        shot2.x = s.x + 4;
        shot1.y = s.y + 3;
        shot2.y = s.y + 4;
        shots.push_back(shot1);
        shots.push_back(shot2);
      }
    }
    vector<coord> filter_shots = moves_filter(shots,soldier_list);
    filter_shots = moves_filter(filter_shots,own_ths);
    vector<MOVE> cannon_shots = cannon_coord_to_shot(s,filter_shots);
    possibilities.insert(possibilities.end(),cannon_shots.begin(),cannon_shots.end());
    possibilities.insert(possibilities.end(),cannon_moves.begin(),cannon_moves.end());
  }
return possibilities;
}

#include "soldier.h"


vector<MOVE> coord_to_move(coord soldier, vector<coord> moves){
  vector<MOVE> mvs ;
  for (int k = 0; k < moves.size(); k++){
    coord curr_coord = moves[k];
    MOVE tmp = make_tuple('S',soldier.x,soldier.y,'M',curr_coord.x,curr_coord.y);
    mvs.push_back(tmp);
  }
  return mvs;
}

vector<coord> soldier_moves(coord soldier, vector<coord> op_soldier_list, bool black){ //black = 1 if black else white
	vector<coord> capture_and_retreat;

	bool adj = false;

	// forward to the soldier
	for (int i =-1; i<2; i++){
		coord always;
		always.x = soldier.x + i;
    if (black == true){
      always.y = soldier.y - 1;
    } else{
      always.y = soldier.y + 1;
    }
		if (contains(always,op_soldier_list) == true){
			adj = true;
		}
		capture_and_retreat.push_back(always);
	}

	//Same line and behind the soldier.
	for (int i = -1 ; i<2 ;i++){
		coord new_coord;
		coord only_retreat;
		new_coord.y = soldier.y; // same irrespective of black or white
    if (black == true){
      only_retreat.y = soldier.y + 1; //behind
    } else {
      only_retreat.y = soldier.y - 1; //behind
    }
		only_retreat.x = soldier.x + i;
		// if (contains(only_retreat,op_soldier_list) == true){
		// 	adj = true;
		// }
		if (i == 0){
			continue;
		} else{
			new_coord.x = soldier.x + i;
			if (contains(new_coord,op_soldier_list)){
				adj = true;
				capture_and_retreat.push_back(new_coord);
			}
		}
	}

	if (adj == true){
		coord retreat1,retreat2,retreat3;
    if (black == true){
      retreat1.y = retreat2.y = retreat3.y = soldier.y + 2;
    } else {
      retreat1.y = retreat2.y = retreat3.y = soldier.y - 2;
    }
		retreat1.x = soldier.x;
		retreat2.x = soldier.x - 2;
		retreat3.x = soldier.x + 2;
		capture_and_retreat.push_back(retreat1);
		capture_and_retreat.push_back(retreat2);
		capture_and_retreat.push_back(retreat3);
	}
	return capture_and_retreat;
}

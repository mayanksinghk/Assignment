#ifndef CANNON_H
#define CANNON_H
#include "commonlib.h"

vector<MOVE> cannon_action(vector<CANNON> cannon_list,vector<coord> soldier_list, vector<coord> opp_soldier_list, vector<coord>own_ths, vector<coord>opp_ths);
int orientation(CANNON c);
vector<MOVE> cannon_coord_to_shot(coord soldier, vector<coord> moves);
MOVE cannon_coord_to_move(coord soldier, coord move, int n=8, int m=8);

#endif

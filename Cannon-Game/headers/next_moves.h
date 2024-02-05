#ifndef NEXT_MOVES_H
#define NEXT_MOVES_H

#include "commonlib.h"
#include "soldier.h"
#include "cannon.h"

vector<MOVE> next_moves(vector<CANNON> cannon_list, vector<coord> soldier_list, vector<coord> opp_soldier_list, bool black,int b_size);

#endif

#ifndef SOLDIER_H
#define SOLDIER_H

#include "commonlib.h"

vector<MOVE> coord_to_move(coord soldier, vector<coord> moves);
vector<coord> soldier_moves(coord soldier, vector<coord> op_soldier_list, bool black); //black = 1 if black else white

#endif

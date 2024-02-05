#ifndef EVALUATION_H
#define EVALUATION_H

#include "commonlib.h"
#include "cannon_list.h"
#include "cannon.h"

tuple<int, int> townhall_dist(vector<coord> Soldiers_list, vector<vector<int> > board);

float Eval(vector<vector<int> > board, int type);
int blocked_cannon(vector<coord>opp_soldier_list,vector<CANNON>cannon_list);



#endif

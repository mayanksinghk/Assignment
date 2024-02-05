#ifndef CANNON_LIST_H
#define CANNON_LIST_H

#include "commonlib.h"

vector<vector<int> > initialise(int b_size);
tuple<vector<CANNON>, vector<CANNON> > Update(vector<vector<int> >);
vector<CANNON> Get_list(int, vector<vector<int> >);
vector<vector<int> > Update_board(MOVE, vector<vector<int> >);
vector<coord> Soldiers_list(int, vector<vector<int> >);
bool Search(vector<CANNON>, CANNON);

#endif

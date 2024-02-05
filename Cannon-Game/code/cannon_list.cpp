#include "cannon_list.h"
//Initialising the board
vector<vector<int> > initialise(int b_size){
    int n,m;
    if (b_size == 1){
        n=8;
        m=8;
    }else if (b_size==2){
        n=10;
        m=8;
    }else{
        n=10;
        m=10;
    }
    vector<vector<int> > board;
    for(int i = 0; i<n; i++){
        vector<int> temp;
        for(int j = 0; j<m; j++){
            temp.push_back(0);
        }
        board.push_back(temp);
    }
    for (int j = 0; j<m;j+=2){
        // Townhalls
        board[0][j] = -2;
        board[n-1][j+1] = 2;
        //Soldiers
        for (int i = 0; i<3;i++){
            board[i][j+1]= -1;
            board[n-1-i][j] = 1;
        }
    }
    //Position of townhall
    // board[0][0] = -2; board[0][2] = -2; board[0][4] = -2; board[0][6] = -2;
    // board[n-1][1] = 2; board[n-1][3] = 2; board[n-1][5] = 2; board[n-1][7] = 2;

    //Position of soldiers
    //White
    // board[0][1] = -1; board[1][1] = -1; board[2][1] = -1;
    // board[0][3] = -1; board[1][3] = -1; board[2][3] = -1;
    // board[0][5] = -1; board[1][5] = -1; board[2][5] = -1;
    // board[0][7] = -1; board[1][7] = -1; board[2][7] = -1;
    //Black
    // board[7][0] = 1; board[6][0] = 1; board[5][0] = 1;
    // board[7][2] = 1; board[6][2] = 1; board[5][2] = 1;
    // board[7][4] = 1; board[6][4] = 1; board[5][4] = 1;
    // board[7][6] = 1; board[6][6] = 1; board[5][6] = 1;

    return board;

}

//Changes the board after a MOVE
vector<vector<int> > Update_board(MOVE move, vector<vector<int> > temp){//S76M46
    vector<vector<int> > board = temp;
    int src_x = get<1>(move), src_y = get<2>(move);
    int dest_x = get<4>(move), dest_y = get<5>(move);

    int type = board[src_y][src_x];

    //updating the board from the move we get
    if(get<3>(move) == 'B'){
        board[dest_y][dest_x] = 0;
    }else{
        board[src_y][src_x] = 0;
        board[dest_y][dest_x] = type;
    }
    return board;
}

//Returns a tuple with black_cannon, white_cannon
tuple<vector<CANNON>, vector<CANNON> > Update(vector<vector<int> > board){
    vector<CANNON> Clist1 = Get_list(1, board);
    vector<CANNON> Clist2 = Get_list(-1, board);
    tuple<vector<CANNON>, vector<CANNON> > ans;
    ans = make_tuple(Clist1, Clist2);

    // cout<<"Of type black:- "<<endl;
    //print_cannon(Clist1);

    // cout<<"Of type white:- "<<endl;
    //print_cannon(Clist2);

    return ans;
}

bool Search(vector<CANNON> list, CANNON temp){
        coord middle_temp_cannon = get<1>(temp);
        coord first_temp_cannon = get<0>(temp);
        coord last_temp_cannon = get<2>(temp);

    for(int i = 0; i<list.size(); i++){
        CANNON t = list[i];
        coord middle_list_cannon = get<1>(t);
        coord first_list_cannon = get<0>(t);
        coord last_list_cannon = get<2>(t);

        if(middle_list_cannon.x == middle_temp_cannon.x && middle_temp_cannon.y == middle_list_cannon.y){
            if(first_list_cannon.x == first_temp_cannon.x && first_temp_cannon.y == first_list_cannon.y){
                if(last_list_cannon.x == last_temp_cannon.x && last_temp_cannon.y == last_list_cannon.y){
                    return true;
                }
            }else{
                if(first_temp_cannon.x == last_list_cannon.x && last_list_cannon.y == first_temp_cannon.y){
                    if(last_temp_cannon.x == first_list_cannon.x && first_list_cannon.y == last_temp_cannon.y){
                        return true;
                    }
                }
            }
        }
    }

    return false;
}

//returns cannon list
vector<CANNON> Get_list(int type, vector<vector<int> > board){
    vector<CANNON> list;
    // int n = 8;
    // int m = 8;
    int n = board.size();
    int m = board[0].size();
    for(int i = 0; i<n; i++){
        for (int j = 0; j<m; j++){
            if(board[i][j] == type){
                if(i<n-1 && i>0 && j<m-1 && j>0){
                    CANNON temp;
                    coord F, M, L;

                    M.y = i; M.x = j;

                    //Horizontal Cannon
                    F.y = i+1; F.x = j;
                    L.y = i-1; L.x = j;
                    if(board[F.y][F.x] == type && board[L.y][L.x] == type){
                        //cout<<i<<" "<<j<<" "<<type<<endl;
                        CANNON t = make_tuple(F, M, L);
                        bool res = Search(list, t);
                        //cout<<F.x<<" "<<F.y<<" -> "<<M.x<<" "<<M.y<<" -> "<<L.x<<" "<<L.y<<endl;
                        if(res == false){
                            list.push_back(t);
                            //CANNON temp = list[0];
                            //coord F = get<0>(temp), M = get<1>(temp), L = get<2>(temp);
                            //cout<<list.size()<<endl;
                            //cout<<F.x<<" "<<F.y<<" -> "<<M.x<<" "<<M.y<<" -> "<<L.x<<" "<<L.y<<endl;
                        }
                    }

                    //Vertical Cannon
                    F.y = i; F.x = j+1;
                    L.y = i; L.x = j-1;
                    if(board[F.y][F.x] == type && board[L.y][L.x] == type){
                        //cout<<i<<" "<<j<<" "<<type<<endl;
                        CANNON t = make_tuple(F, M, L);
                        bool res = Search(list, t);
                        if(res == false){
                            list.push_back(t);
                        }
                    }

                    //Main Diagonal Cannon
                    F.y = i-1; F.x = j-1;
                    L.y = i+1; L.x = j+1;
                    if(board[F.y][F.x] == type && board[L.y][L.x] == type){
                        //cout<<i<<" "<<j<<" "<<type<<endl;
                        CANNON t = make_tuple(F, M, L);
                        bool res = Search(list, t);
                        if(res == false){
                            list.push_back(t);
                        }
                    }

                    //Secondary Diagonal Cannon
                    F.y = i-1; F.x = j+1;
                    L.y = i+1; L.x = j-1;
                    if(board[F.y][F.x] == type && board[L.y][L.x] == type){
                        //cout<<i<<" "<<j<<" "<<type<<endl;
                        CANNON t = make_tuple(F, M, L);
                        bool res = Search(list, t);
                        if(res == false){
                            list.push_back(t);
                        }
                    }
                }
                if(i == 0 || i == n-1){ //taking only first or last row. Hence only horizontal cannon possible.
                    if(j == 0 || j == m-1){
                        continue;
                    }else{
                        coord M, F, L;
                        M.y = i; M.x = j;
                        F.y = i; F.x = j+1;
                        L.y = i; L.x = j-1;

                        if(board[F.y][F.x] == type && board[L.y][L.x] == type){
                            //cout<<i<<" "<<j<<" "<<type<<endl;
                            CANNON t = make_tuple(F, M, L);
                            bool res = Search(list, t);
                            if(res == false){
                                list.push_back(t);
                            }
                        }
                    }
                }
                if(j == 0 || j == m-1){//taking only last or first colum. Hence only vertical cannon possible.
                    if(i == 0 || i == n-1){
                        continue;
                    }else{
                        coord M, F, L;
                        M.y = i; M.x = j;
                        F.y = i+1; F.x = j;
                        L.y = i-1; L.x = j;

                        if(board[F.y][F.x] == type && board[L.y][L.x] == type){
                            //cout<<i<<" "<<j<<" "<<type<<endl;
                            CANNON t = make_tuple(F, M, L);
                            bool res = Search(list, t);
                            //cout<<res;
                            if(res == false){
                                list.push_back(t);
                            }
                        }
                    }
                }
            }
        }
    }

    return list;
}

//Generates a list of soldiers on the boards given type 1 or -1
vector<coord> Soldiers_list(int type, vector<vector<int> > board){
    vector<coord> list;
    for(int i = 0; i<board.size(); i++){
        for(int j = 0; j<board[0].size(); j++){
            if(type == board[i][j]){
                coord t;
                t.x = j;
                t.y = i;
                list.push_back(t);
            }
        }
    }
    return list;
}

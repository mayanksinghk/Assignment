#include "Evaluation.h"


float Eval(vector<vector<int> > board,  int type){
    int m, n;   //Configuration of board, n is no. of rows and m is no. of columns
    n = board.size();
    m = board[0].size();

    float ans = 0;
    tuple<vector<CANNON>, vector<CANNON> > cannon_list = Update(board);
    float w1, w2, w3, w4, w5, w6, w7, w8;
    w1 = 1;    //Number of soldier  
    w2 = 5;    //Number of enemy soldier
    
    w3 = 3;     //No. of cannon
    w4 = 5;    //No. of enemy cannon
    
    w5 = 2.5;    //oppn blocked cannon
    w6 = 2;   // blocked cannon

    w7 = 3;    //Our Attack line
    w8 = 3.5;    //Opposition Attack line

    float u = 20;    //No. of town 
    float v = 20;   //No. of enemy town

    // ans = (float)(w1*no_of_soldier) + (float)(w2*no_of_enemy_soldier);
    // ans = (float)(ans) + (float)(w3*no_of_cannon) + (float)(w4*oppn_no_of_cannon);
    // ans = (float)(ans) + (float)(w5*oppn_blocked_cannon) + (float)(w6*blocked_cannon1);
    // ans = (float)(ans) + (float)(a_line)*w7 + (float)(a_opp_line)*w8;
    // ans = (float)(ans) + (float)(u*town) + (float)(v*oppn_town);
    

    vector<coord> Black_S_list = Soldiers_list(1, board);
    vector<coord> White_S_list = Soldiers_list(-1, board);
    vector<CANNON> White_C_list = get<0>(cannon_list);
    vector<CANNON> Black_C_list = get<1>(cannon_list);
    float no_of_soldier = 0 , no_of_enemy_soldier = 0;  //done
    float no_of_cannon = 0, oppn_no_of_cannon = 0; //done
    float oppn_town = 0, town = 0;  //done
    float oppn_soldier_from_town = 0, soldier_from_town = 0; //done
    float soldier_from_oppn_town = 0, oppn_soldier_from_oppn_town = 0;//done
    float oppn_blocked_cannon = 0, blocked_cannon1 = 0; //done
    float a_line = 0, a_opp_line = 0;

    float a = Black_C_list.size();
    float b = White_C_list.size();

    float c = White_S_list.size();
    float d = Black_S_list.size();

    float e = blocked_cannon(Black_S_list, White_C_list);
    float f = blocked_cannon(White_S_list, Black_C_list);

    float g = 10 - AttackLine(board, 1);
    float h = (-1)*AttackLine(board, -1);

    if(type == 1){//Black 
        no_of_soldier = d;
        no_of_enemy_soldier = (-1)*c;
        
        no_of_cannon = a;
        oppn_no_of_cannon = (-1)*b;

        for(int j = 1; j<m; j+=2){
            town = town + abs(float(board[n-1][j]/2));
            oppn_town = oppn_town - abs(float(board[0][j-1]/2));
        }
        a_line = g;
        a_opp_line = (-1)*h;
        
        blocked_cannon1 = (-1)*f;
        oppn_blocked_cannon = e; 
    }else{//White
        no_of_enemy_soldier = (-1)*d;
        no_of_soldier = c;
        
        oppn_no_of_cannon = (-1)*a;
        no_of_cannon = b;

        for(int j = 1; j<m; j+=2){
            town = town + abs(float(board[0][j-1]/2));
            oppn_town = oppn_town - abs(float(board[n-1][j]/2));
        }

        blocked_cannon1 = (-1)*e;
        oppn_blocked_cannon = f;

        a_line = h;
        a_opp_line = (-1)*g;
        }   
    
    ans = (float)(w1*no_of_soldier) + (float)(w2*no_of_enemy_soldier);
    ans = (float)(ans) + (float)(w3*no_of_cannon) + (float)(w4*oppn_no_of_cannon);
    ans = (float)(ans) + (float)(w5*oppn_blocked_cannon) + (float)(w6*blocked_cannon1);
    ans = (float)(ans) + (float)(a_line)*w7 + (float)(a_opp_line)*w8;
    // ans = (float)(ans) + (float)(u*town) + (float)(v*oppn_town);

    return ans;

}


int blocked_cannon(vector<coord>opp_soldier_list,vector<CANNON>cannon_list){
  int number=0;
  vector<coord> blocked_positions;
  for (int j = 0; j< cannon_list.size(); j++){
    CANNON curr_cannon = cannon_list[j];
    coord mid_ele = get<1>(curr_cannon);
    int orie = orientation(curr_cannon);
    if (orie == 0){
      coord bp1= {mid_ele.x-2,mid_ele.y};
      coord bp2= {mid_ele.x+2,mid_ele.y};
      blocked_positions.push_back(bp1);
      blocked_positions.push_back(bp2);
    }else if (orie == 1){
      coord bp1= {mid_ele.x,mid_ele.y-2};
      coord bp2= {mid_ele.x,mid_ele.y+2};
      blocked_positions.push_back(bp1);
      blocked_positions.push_back(bp2);
    }else if (orie == 2){
      coord bp1= {mid_ele.x-2,mid_ele.y+2};
      coord bp2= {mid_ele.x+2,mid_ele.y-2};
      blocked_positions.push_back(bp1);
      blocked_positions.push_back(bp2);
    }else{
      coord bp1= {mid_ele.x-2,mid_ele.y-2};
      coord bp2= {mid_ele.x+2,mid_ele.y+2};
      blocked_positions.push_back(bp1);
      blocked_positions.push_back(bp2);
    }
  }


  for (int k = 0; k < opp_soldier_list.size(); k++){
    coord soldier = opp_soldier_list[k];
    for (int i = 0; i < blocked_positions.size(); i++){
      coord curr_pos = blocked_positions[i];
      if (soldier.x == curr_pos.x && soldier.y == curr_pos.y){
          number++;
      }
    }
  }
  return number;
}

//This function returns the attack line wrt to the type black or white for black it gives an positive number and for white it gives an negative number
//for black less the number favours appreciates his condition and similarly for white.
int AttackLine(vector<vector<int> > board, int type){
    int n = board.size();
    int m = board[0].size();
    int ans = n/2;

    if(type == 1){  //1 is for Black attack line 
        for(int i = n-1; i>-1; i--){
            int flag = 1;
            for(int j = 0; j<m; j++){
                if(board[i][j] < 0){
                    flag = -1;
                    ans = i;
                    break;
                }
            }
            if(flag == -1){
                break;
            }
        }
    }else{
        for(int i = 0; i<n; i++){
            int flag = -1;
            for(int j = 0; j<m; j++){
                if(board[i][j] > 0){
                    flag = 1;
                    ans = i*-1;
                    break;
                }
            }
            if(flag == 1){
                break;
            }
        }
    }
    return ans;
}
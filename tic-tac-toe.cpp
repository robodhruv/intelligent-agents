#include <iostream>
#include <vector>
#include <map>
#include <stdlib.h>
#include <ctime>
using namespace std;

float alpha = 0.3; // Coefficient for updating score in temporal difference method
int episodes = 10000; // Number of games played by the agent with itself
int epsilon = 0.5; // Coefficient for Exploitation vs Exploration. epsilon fraction of time exploitation would be preffered

map<vector<char>,float> qTable;

vector<vector<char> > observation_space(vector<vector<char> > & a){
	int len = a.size();
	vector<vector<char> > b = a;
	b.insert(b.end(),a.begin(),a.end());
	b.insert(b.end(),a.begin(),a.end());
	for(int i = 0 ; i < len ; i++){
		b[i].push_back('*');
		b[i+len].push_back('1');
		b[i+2*len].push_back('0');
	}
	return b;
}

void print2DVec(vector<vector<char> > &x){
	for(vector<vector<char> >::iterator i1 = x.begin() ; i1 != x.end() ; i1 ++){
		for(vector<char>::iterator i2 = i1->begin() ; i2 != i1->end() ; i2++){
			cout << *i2 << " ";
		}
		cout << endl;
	}
	return;
	
} 
void printChar(vector<char> a){
	for(vector<char>::iterator i1 = a.begin() ; i1 != a.end() ; i1++){
		cout << *i1 << " ";
	}
	return;
}

void printInt(vector<int> a){
	for(vector<int>::iterator i1 = a.begin() ; i1 != a.end() ; i1++){
		cout << *i1 << " ";
	}
	return;
}

void printMap(map<vector<char>, float> &a){
	for(map<vector<char>,float>::iterator i1 = a.begin() ; i1 != a.end() ; i1++){
		cout << "Board : ";
		printChar(i1->first);
		cout << "\t" << "Reward : " << i1->second;
		cout << endl;
	}
	return;
}

float AllocateScore(vector<char> &a)
{
	if (a[0] == a[1] && a[1] == a[2]) {if (a[0] == '1') return 1.0; else return 0.0;}
	else if (a[3] == a[4] && a[4] == a[5]) {if (a[3] == '1') return 1.0; else return 0.0;}
	else if (a[6] == a[7] && a[7] == a[8]) {if (a[6] == '1') return 1.0; else return 0.0;}
	else if (a[0] == a[3] && a[3] == a[6]) {if (a[0] == '1') return 1.0; else return 0.0;}
	else if (a[1] == a[4] && a[4] == a[7]) {if (a[1] == '1') return 1.0; else return 0.0;}
	else if (a[2] == a[5] && a[5] == a[8]) {if (a[2] == '1') return 1.0; else return 0.0;}
	else if (a[0] == a[4] && a[4] == a[8]) {if (a[0] == '1') return 1.0; else return 0.0;}
	else if (a[2] == a[4] && a[4] == a[6]) {if (a[2] == '1') return 1.0; else return 0.0;}
	else if (a[0] != '*' && a[1] != '*' && a[2] != '*' && a[3] != '*' && a[4] != '*' && a[5] != '*' 
                  && a[6] != '*' && a[7] != '*' && a[8] != '*') return 0.5;
	else return 0.0;

}
bool gameover(vector<char> &a)
{
	if (a[0] == a[1] && a[1] == a[2] && (a[0] == '1' || a[0] == '0')) return true;
	else if (a[3] == a[4] && a[4] == a[5] && (a[3] == '1' || a[3] == '0')) return true;
	else if (a[6] == a[7] && a[7] == a[8] && (a[6] == '1' || a[6] == '0')) return true;
	else if (a[0] == a[3] && a[3] == a[6] && (a[0] == '1' || a[0] == '0')) return true;
	else if (a[1] == a[4] && a[4] == a[7] && (a[1] == '1' || a[1] == '0')) return true;
	else if (a[2] == a[5] && a[5] == a[8] && (a[2] == '1' || a[2] == '0')) return true;
	else if (a[0] == a[4] && a[4] == a[8] && (a[0] == '1' || a[0] == '0')) return true;
	else if (a[2] == a[4] && a[4] == a[6] && (a[2] == '1' || a[2] == '0')) return true;
	else if (a[0] != '*' && a[1] != '*' && a[2] != '*' && a[3] != '*' && a[4] != '*' && a[5] != '*' 
                  && a[6] != '*' && a[7] != '*' && a[8] != '*') return true;
	else return false;

}
// This Function populates the initial value of q-Table with
// | Fate | Reward |
// | Win  |  1.0   |
// | Draw |  0.5   |
// | Loss |  0.0   |


void init(){
	vector<vector<char> > temp(3,vector<char> (1));
	temp[0][0] = '*';
	temp[1][0] = '1';
	temp[2][0] = '0';
	vector<vector<char> > c = observation_space(temp);
	for(int i = 2 ; i < 9; i++){
		c = observation_space(c);
	}
	for(int i = 0 ; i < c.size(); i++){
		float reward = AllocateScore(c[i]);
		qTable[c[i]] = reward;
	}
	return;
}

int randomMove(vector<char> &board){
	vector<int> available_posn(0);
	for(int i = 0 ; i < 9 ; i++){
		if(board[i] == '*') available_posn.push_back(i);
	}
	int randIndex = rand() % available_posn.size();
	return available_posn[randIndex];
}

void updateBoard(vector<char> &board, bool player , int pos){
	if (player) {
		board[pos] = '1';
	}
	else {
		board[pos] = '0';
	}
	return;
}

int maxMove(vector<char> &board){
	vector<int> possible_moves(0);
	for(int i = 0 ; i < 9 ; i++){
		if(board[i] == '*') possible_moves.push_back(i);
	}
	if(possible_moves.size() == 1){
		return possible_moves[0];
	}
	vector<float> reward(0);
	for(int j = 0 ; j < possible_moves.size() ; j++){
		vector<char> temp = board;
		updateBoard(temp, 1, possible_moves[j]);
		updateBoard(temp , 0 , randomMove(temp));
		reward.push_back(qTable[temp]);
	}
	float max_reward = 0.0;
	int index_of_move = 0;
	for(int j = 0 ; j < reward.size();j++){
		if (reward[j] > max_reward){
			max_reward = reward[j];
			index_of_move = j;
		}
	}
	return possible_moves[index_of_move];
}

void PlayGame(vector<char> &board){
	int fate = rand() % 100;
	if (fate < 50){
		int bestMove = maxMove(board);
		vector<char> temp = board;
		updateBoard(temp, 1, bestMove);
		if (gameover(temp)) {
			map<vector<char>, float>::iterator i1 = qTable.find(board);
			map<vector<char>, float>::iterator i2 = qTable.find(temp);
			float qBoard = i1->second, qTemp = i2->second;
			i1->second = qBoard + alpha*(qTemp - qBoard);
			return;
		}
		int randMove = randomMove(temp);
		updateBoard(temp, 0 , randMove);

		if(gameover(temp)){
			map<vector<char>, float>::iterator i1 = qTable.find(board);
			map<vector<char>, float>::iterator i2 = qTable.find(temp);
			float qBoard = i1->second, qTemp = i2->second;
			i1->second = qBoard + alpha*(qTemp - qBoard);
		}
		 	map<vector<char>, float>::iterator i1 = qTable.find(board);
			map<vector<char>, float>::iterator i2 = qTable.find(temp);
			float qBoard = i1->second, qTemp = i2->second;
			i1->second = qBoard + alpha*(qTemp - qBoard);
		PlayGame(temp);
	}
	else {
		int randMove = randomMove(board);
		vector<char> temp = board;
		updateBoard(temp, 1, randMove);
		if (gameover(temp)) {
			return;
		}
		randMove = randomMove(temp);
		updateBoard(temp, 0 , randMove);
		if(gameover(temp)){
			return;
			
		}
		PlayGame(temp);
	}
}
	
int main(){
	init();
	srand ( time(NULL) );
	vector<char> initialBoard(9,'*');
	for(int i = 0 ; i< 100*episodes ; i++){
		cout << i << endl;
		PlayGame(initialBoard);
	}
	printMap(qTable);
}
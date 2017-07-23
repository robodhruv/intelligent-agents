#include <iostream>
#include <vector>
#include <map>
#include <stdlib.h>
#include <ctime>
#include <fstream>

using namespace std;

float alpha = 0.3; // Coefficient for updating score in temporal difference method
int episodes = 10000; // Number of games played by the agent with itself
float epsilon = 0.5; // Coefficient for Exploitation vs Exploration. epsilon fraction of time exploitation would be preffered

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
void printBoard(vector<char> &c){
	cout << "\n\n\tTic Tac Toe\n\n";

	cout << "Player 1 (X)  -  Player 2 (O)" << endl << endl;
	cout << endl;
	cout << "     |     |     " << endl;
	cout << "  " << c[0] << "  |  " << c[1] << "  |  " << c[2] << endl;
	cout << "_____|_____|_____" << endl;
	cout << "     |     |     " << endl;
	cout << "  " << c[3] << "  |  " << c[4] << "  |  " << c[5] << endl;
	cout << "_____|_____|_____" << endl;
	cout << "     |     |     " << endl;
	cout << "  " << c[6] << "  |  " << c[7] << "  |  " << c[8] << endl;
	cout << "     |     |     " << endl << endl;
}

void printMap(map<vector<char>, float> &a){
	for(map<vector<char>,float>::iterator i1 = a.begin() ; i1 != a.end() ; i1++){
		cout << "Board : ";
		printBoard(i1->first);
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
	else return 0.2;

}
bool gameover(vector<char> &a, char c)
{
	if (a[0] == a[1] && a[1] == a[2] && a[0] == c) return true;
	else if (a[3] == a[4] && a[4] == a[5] && a[3] == c) return true;
	else if (a[6] == a[7] && a[7] == a[8] && a[6] == c) return true;
	else if (a[0] == a[3] && a[3] == a[6] && a[0] == c) return true;
	else if (a[1] == a[4] && a[4] == a[7] && a[1] == c) return true;
	else if (a[2] == a[5] && a[5] == a[8] && a[2] == c) return true;
	else if (a[0] == a[4] && a[4] == a[8] && a[0] == c) return true;
	else if (a[2] == a[4] && a[4] == a[6] && a[2] == c) return true;
	else if (a[0] != '*' && a[1] != '*' && a[2] != '*' && a[3] != '*' && a[4] != '*' && a[5] != '*' 
                  && a[6] != '*' && a[7] != '*' && a[8] != '*') return true;
	else return false;

}
// This Function populates the initial value of q-Table with
// | Fate | Reward |
// | Win  |  1.0   |
// | Draw |  0.5   |
// | Loss |  0.0   |


bool goodPosition(vector<char> &c){
	int count1 = 0, count0 = 0;
	for(int i = 0 ; i<9; i++){
		if(c[i] == '1') count1++;
		else if (c[i] == '0') count0++;
	}
	return ((count1 == count0) || (count1 == count0 + 1));
}

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
		if(goodPosition(c[i])){
			if (!(gameover(c[i] ,'1') && gameover(c[i] ,'0'))){
				float reward = AllocateScore(c[i]);
				qTable[c[i]] = reward;
			}
		}
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

int maxMove(vector<char> &board,char c){
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
	float min_reward = 1.0;
	int max_move = 0;
	int min_move = 0;
	for(int j = 0 ; j < reward.size();j++){
		if (reward[j] > max_reward){
			max_reward = reward[j];
			max_move = j;
		}
		if (reward[j] < min_reward){
			min_reward = reward[j];
			min_move = j;
		}
	}
	if(c == '1') return possible_moves[max_move];
	else return possible_moves[min_move];
}

void PlayGame(vector<char> &board){
	int fate = rand() % 100;
	if (fate < 100.0*epsilon){
		int move = maxMove(board,'1');
		vector<char> temp = board;
		updateBoard(temp, 1, move);
		if (gameover(temp,'1')) {
			map<vector<char>, float>::iterator i1 = qTable.find(board);
			map<vector<char>, float>::iterator i2 = qTable.find(temp);
			float qBoard = i1->second, qTemp = i2->second;
			i1->second = qBoard + alpha*(qTemp - qBoard);
			return;
		}
		move = maxMove(temp,'0');
		updateBoard(temp, 0 , move);

		if(gameover(temp,'0')){
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
		int move = randomMove(board);
		vector<char> temp = board;
		updateBoard(temp, 1, move);
		if (gameover(temp,'1')) {
			return;
		}
		move = maxMove(temp,'0');
		updateBoard(temp, 0 , move);
		if(gameover(temp,'0')){
			return;
			
		}
		PlayGame(temp);
	}
}


int main(){
	ofstream outfile("Q-Table Tic-Tac-Toe.txt");
	init();
	srand ( time(NULL) );
	vector<char> initialBoard(9,'*');
	int cwin = 0 , closs = 0 , cdraw=0;
	for(map <vector<char>, float>::iterator i1 = qTable.begin() ; i1 != qTable.end() ; i1++){
		if (i1->second == 1.0) cwin++;
		else if (i1->second == 0.5) cdraw++;
		else if (i1->second == 0.0) closs++;
	}

	cout << endl << "The number of wins : " << cwin << endl;
	cout << "The number of draws : " << cdraw << endl;
	cout << "The number of loss : " << closs << endl;

	for(int i = 0 ; i< episodes ; i++){
		if(i%1000 == 0) cout << i/100 << "%" << endl;
		PlayGame(initialBoard);
	}
	printMap(qTable);
	cwin = 0 ; closs = 0 ; cdraw=0;
	for(map <vector<char>, float>::iterator i2 = qTable.begin() ; i2 != qTable.end() ; i2++){
		if (i2->second >= 0.8) cwin++;
		else if ((i2->second >= 0.4) && (i2->second <= 0.6)) cdraw++;
		else if (i2->second < 0.2) closs++;
		vector<char> tt = i2->first;
		for(int i = 0; i < tt.size() ; i++){
			outfile << tt[i];
		}
		outfile << " " << i2->second << endl;

	}
	cout << endl << "The number of wins : " << cwin << endl;
	cout << "The number of draws : " << cdraw << endl;
	cout << "The number of loss : " << closs << endl;
	cout << "End of Learning Phase" << endl;
	epsilon = 1.0;
	alpha = 0.1;
	cout << "Lets play a game : " << endl;
	for(int i = 0; i<10;i++){
		vector<char> newBoard(9,'*');
		while(!(gameover(newBoard,'1') || gameover(newBoard,'0'))){
			updateBoard(newBoard,'1',maxMove(newBoard,'1'));
			printBoard(newBoard);
			if(gameover(newBoard,'1')) break;
			int my_move;
			cin >> my_move;
			updateBoard(newBoard,0,my_move);
			printBoard(newBoard);
		}
	}
}
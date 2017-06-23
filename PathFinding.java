/*
 * Implementing http://mnemstudio.org/path-finding-q-learning-tutorial.htm
 * Q-learning formula http://www.computing.dcu.ie/~humphrys/Notes/RL/Code/code.q.html
 */

import java.util.ArrayList;
import java.util.Random;

public class PathFinding {
	
	double Gamma = 0.7; 
	double Alpha = 0.3;
	
	/* The instant reward structure of the environment
	 * -1 indicates null values (where there isn't a link between nodes)
	 */
	
	final double[][] R = new double[][] {
		{ -1, -1, -1, -1,  0, -1  },
		{ -1, -1, -1,  0, -1, 100 },
		{ -1, -1, -1,  0, -1,  -1 },
		{ -1,  0,  0, -1,  0,  -1 },
		{  0, -1, -1,  0, -1, 100 },
		{ -1,  0, -1, -1,  0, 100 }     
	};

	/*Q matrix is the brain of the bot.
	 *It will get updated as the bot learns more about the environment.
	 */
	
	public double[][] Q = new double[6][6];
	
	public void printmat (double[][] mat) {
	    for (double[] row : mat) {
	    	System.out.format("%20s%20s%20s%20s%20s%20s\n", 
	    			row[0], row[1], row[2], row[3], row[4], row[5]);
	    }
	    
		System.out.println();
	}
	
	public double[][] normalize (double[][] mat) {
		double maxsofar = 0;
		double[][] matcopy = new double[6][6];
		
		for (int i = 0; i < mat.length; i++) {
			for (int j = 0; j < mat.length; j++) {
				if (mat[i][j] > maxsofar) maxsofar = mat[i][j];
			}
		}
		for (int i = 0; i < mat.length; i++) {
			for (int j = 0; j < mat.length; j++) {
				matcopy[i][j] = mat[i][j] / maxsofar * 100;
			}
		}
		
		return matcopy;
	}
	
	//This gives the action from the current state with the maximum immediate reward
	
	public int maxAction (int Qstate)
	{
		int maxsofar = 0;
		for (int i = 1; i < Q.length; i++) {
			if (Q[Qstate][i] > Q[Qstate][maxsofar]) maxsofar = i;
		}
		return maxsofar;
	}
	
	public void updateQ (int state, int action) {
		if (state > 5 || state < 0 || action > 5 || action < 0 ) {
			throw new java.lang.IndexOutOfBoundsException(); 
		}
		
		double qtemp = R[state][action] + Gamma * Q[action][maxAction(action)];
		Q[state][action] = (1 - Alpha) * Q[state][action] + Alpha * qtemp;
	}
	
	public int[] possibleAct (int state) {
		ArrayList<Integer> temp = new ArrayList<Integer>();
		
		for (int i = 0; i < R.length; i++) {
			if (R[state][i] != -1) temp.add(i);
		}
		
		int i = 0;
		int[] pa = new int[temp.size()];
        for (int n : temp) {
        	pa[i++] = n;
        }
        return pa;
	}
	
	public int randomAct (int[] pa) {
		Random r = new Random();
		int index = r.nextInt(pa.length);
		return pa[index];
	}
	
	public void episode() {
		Random r = new Random();
		int state = r.nextInt(R.length);
		
		// 5 is the goal state
		while (state != 5) {
			int action = randomAct(possibleAct(state));
			updateQ(state, action); 
			
			System.out.print(state + " -> "); //This will give a visual representation of what path the bot takes in each episode
			
			state = action;
		}
		System.out.print(5);
		System.out.println();
	}
	
	// This function will test how well the bot knows it's path
	public void test(int state_input) {
		if (state_input > 5 || state_input < 0) throw new java.lang.IndexOutOfBoundsException();
		
		int state = state_input;
		
		while (state != 5) {
			int action = maxAction(state);
			System.out.print(state + " -> ");
			state = action;
		}
		System.out.print(5);
		System.out.println();
	}
	
	public static void main(String[] args) {
		
		PathFinding m = new PathFinding();
		
		for (int i=0; i<1000; i++) {
			m.episode();
		}
		m.printmat(m.Q);
		m.printmat(m.normalize(m.Q));
		
		m.test(3); //test any initial state here, it will take the best path
	}
}

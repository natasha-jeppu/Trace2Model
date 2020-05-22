// ******************************************** Iteration:33

#include<stdio.h>
#include<stdbool.h>
#include<stdint.h>
void main()
{
	uint8_t event_seq_length = 11;
	uint8_t num_input = 1;
	uint8_t event_seq[1][11] = {{1,2,11,12,22,27,26,12,15,15,3}};
	uint8_t num_states = 18;
	uint8_t t[118][3];
	uint8_t count=0;
	uint8_t t_gen[107][3] = {{1,1,2},{2,2,3},{2,2,6},{2,2,7},{2,2,8},{2,2,9},{2,2,10},{2,2,11},{2,2,12},{2,2,13},{2,2,17},{2,2,18},{3,3,4},{3,4,3},{3,5,3},{3,7,5},{3,8,16},{3,9,5},{3,10,6},{3,19,7},{4,6,4},{5,3,4},{5,8,5},{5,9,5},{5,9,16},{5,14,5},{5,14,6},{5,14,8},{5,15,5},{5,15,8},{5,15,13},{5,22,11},{5,23,11},{6,3,4},{6,5,5},{6,5,9},{6,18,9},{6,20,10},{6,20,12},{7,8,5},{7,10,6},{7,11,8},{7,14,6},{7,14,15},{7,16,7},{8,7,9},{8,12,5},{8,12,16},{8,13,5},{8,13,17},{8,15,14},{8,18,9},{9,12,5},{9,16,5},{9,17,6},{9,17,17},{9,23,8},{9,23,13},{9,25,14},{10,7,10},{10,16,14},{10,16,18},{10,17,6},{10,19,7},{10,21,6},{10,24,12},{11,4,3},{11,5,8},{11,9,5},{11,12,5},{11,13,5},{11,23,11},{12,5,6},{12,7,10},{12,7,12},{12,15,14},{12,20,10},{12,23,6},{12,23,16},{12,25,15},{13,11,8},{13,11,15},{13,19,7},{13,24,12},{14,3,4},{14,9,14},{14,14,12},{14,22,11},{14,23,8},{14,23,11},{15,16,14},{15,20,12},{15,25,14},{16,3,4},{16,8,16},{16,9,16},{16,13,14},{16,26,14},{16,27,16},{16,28,5},{17,8,16},{17,12,5},{17,16,14},{17,17,17},{18,10,18},{18,23,13},{18,24,12}};

	for(uint8_t i=0;i<107;i++)				
		{																		
			t[count][0] = t_gen[i][0];											
			t[count][1] = t_gen[i][1];											
			t[count][2] = t_gen[i][2];											
			count = count + 1;													
		}
 																		
	for (uint8_t i=0;i<num_input;i++) 													
	{																				
		uint8_t start_state_var;														
		__CPROVER_assume(start_state_var <= num_states && start_state_var > 1);		
		assert(start_state_var <= num_states);										

		t[count][0] = start_state_var;												
		for (uint8_t j=0;j<event_seq_length;j++)										
		{																			
			uint8_t next_state_var;														
			t[count][1] = event_seq[i][j];											
			if(event_seq[i][j] == 1)												
				t[count][0] = 1;													
			__CPROVER_assume(next_state_var <= num_states && next_state_var > 1);	
			assert(next_state_var <= num_states);									
			t[count][2] = next_state_var;											
			count = count+1;															
			t[count][0] = t[count-1][2];											
		}																			
	}

	bool in[num_states][28];												
	bool o[num_states][28];														
																					
	for (uint8_t i=0;i<num_states;i++)												
		for (uint8_t j=0;j<28;j++)													
		{																			
			in[i][j] = false;														
			o[i][j] = false;														
		}																			
																					
	for (uint8_t i=0;i<count;i++)													
	{																				
		o[t[i][0]-1][t[i][1]-1] = true;											
		in[t[i][2]-1][t[i][1]-1] = true;											
	}
																		
	bool wrong_transition = false;														
	for (uint8_t i=0; i<num_states;i++)														
	{																				
			if (in[i][ 0] && (o[i][0] || o[i][2] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12] || o[i][13] || o[i][14] || o[i][15] || o[i][16] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][21] || o[i][22] || o[i][23] || o[i][24] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 1] && (o[i][0] || o[i][1] || o[i][5] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 2] && (o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12] || o[i][13] || o[i][14] || o[i][15] || o[i][16] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][21] || o[i][22] || o[i][23] || o[i][24] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 3] && (o[i][0] || o[i][1] || o[i][5] || o[i][10] || o[i][11] || o[i][14] || o[i][16] || o[i][20] || o[i][21] || o[i][24] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 4] && (o[i][0] || o[i][1] || o[i][5] || o[i][10] || o[i][20] || o[i][23] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 5] && (o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12] || o[i][13] || o[i][14] || o[i][15] || o[i][16] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][21] || o[i][22] || o[i][23] || o[i][24] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 6] && (o[i][0] || o[i][1] || o[i][5] || o[i][12] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 7] && (o[i][0] || o[i][1] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][9] || o[i][10] || o[i][15] || o[i][16] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][23] || o[i][24] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 8] && (o[i][0] || o[i][1] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][9] || o[i][10] || o[i][15] || o[i][16] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][23] || o[i][24]))
				wrong_transition = true;
			else if (in[i][ 9] && (o[i][0] || o[i][1] || o[i][3] || o[i][5] || o[i][6] || o[i][8] || o[i][10] || o[i][11] || o[i][12] || o[i][14] || o[i][15] || o[i][20] || o[i][21] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 10] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][5] || o[i][9] || o[i][10] || o[i][13] || o[i][16] || o[i][20] || o[i][22] || o[i][23] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 11] && (o[i][0] || o[i][1] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][9] || o[i][10] || o[i][11] || o[i][15] || o[i][16] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][23] || o[i][24]))
				wrong_transition = true;
			else if (in[i][ 12] && (o[i][0] || o[i][1] || o[i][4] || o[i][5] || o[i][6] || o[i][9] || o[i][10] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][23]))
				wrong_transition = true;
			else if (in[i][ 13] && (o[i][0] || o[i][1] || o[i][5] || o[i][9] || o[i][10] || o[i][16] || o[i][18] || o[i][20] || o[i][23]))
				wrong_transition = true;
			else if (in[i][ 14] && (o[i][0] || o[i][1] || o[i][4] || o[i][5] || o[i][9] || o[i][19]))
				wrong_transition = true;
			else if (in[i][ 15] && (o[i][0] || o[i][1] || o[i][3] || o[i][5] || o[i][11] || o[i][16] || o[i][18] || o[i][19] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 16] && (o[i][0] || o[i][1] || o[i][3] || o[i][5] || o[i][6] || o[i][9] || o[i][10] || o[i][12] || o[i][13] || o[i][18] || o[i][21] || o[i][23] || o[i][24] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 17] && (o[i][0] || o[i][1] || o[i][2] || o[i][5] || o[i][8] || o[i][9] || o[i][13] || o[i][18] || o[i][20] || o[i][21] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 18] && (o[i][0] || o[i][1] || o[i][2] || o[i][5] || o[i][8] || o[i][12] || o[i][16] || o[i][18] || o[i][21] || o[i][22] || o[i][23] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 19] && (o[i][0] || o[i][1] || o[i][2] || o[i][5] || o[i][7] || o[i][9] || o[i][10] || o[i][21] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 20] && (o[i][0] || o[i][1] || o[i][5] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12] || o[i][13] || o[i][15] || o[i][21] || o[i][22] || o[i][23] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 21] && (o[i][0] || o[i][1] || o[i][5] || o[i][6] || o[i][9] || o[i][10] || o[i][16] || o[i][19] || o[i][20] || o[i][21] || o[i][23] || o[i][24] || o[i][27]))
				wrong_transition = true;
			else if (in[i][ 22] && (o[i][0] || o[i][1] || o[i][5] || o[i][15] || o[i][20] || o[i][24]))
				wrong_transition = true;
			else if (in[i][ 23] && (o[i][0] || o[i][1] || o[i][2] || o[i][5] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12] || o[i][13] || o[i][15] || o[i][17] || o[i][21] || o[i][23] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 24] && (o[i][0] || o[i][1] || o[i][4] || o[i][5] || o[i][7] || o[i][10] || o[i][16] || o[i][20] || o[i][23] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 25] && (o[i][0] || o[i][1] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][9] || o[i][10] || o[i][15] || o[i][16] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][23] || o[i][24] || o[i][25] || o[i][26] || o[i][27] || o[i][28]))
				wrong_transition = true;
			else if (in[i][ 26] && (o[i][0] || o[i][1] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][9] || o[i][10] || o[i][11] || o[i][15] || o[i][16] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][23] || o[i][24]))
				wrong_transition = true;
			else if (in[i][ 27] && (o[i][0] || o[i][1] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][9] || o[i][10] || o[i][11] || o[i][15] || o[i][16] || o[i][17] || o[i][18] || o[i][19] || o[i][20] || o[i][23] || o[i][24] || o[i][25]))
				wrong_transition = true;
	}
	assert(wrong_transition != false);
}
// ******************************************** Iteration:7

#include<stdio.h>
#include<stdbool.h>
#include<stdint.h>
void main()
{
	uint8_t event_seq_length = 9;
	uint8_t num_input = 1;
	uint8_t event_seq[1][9] = {{1,2,3,4,8,13,8,6,7}};
	uint8_t num_states = 12;
	uint8_t t[28][3];
	uint8_t count=0;
	uint8_t t_gen[19][3] = {{1,1,8},{2,3,4},{4,4,7},{4,4,9},{5,6,6},{6,7,3},{7,5,5},{7,8,5},{7,8,11},{7,9,5},{7,10,10},{8,2,2},{9,5,5},{9,5,9},{10,11,5},{10,11,12},{11,6,6},{11,12,11},{12,9,5}};
for(uint16_t i=0;i<19;i++)				
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

	bool in[num_states][13];												
	bool o[num_states][13];														
																					
	for (uint8_t i=0;i<num_states;i++)												
		for (uint8_t j=0;j<13;j++)													
		{																			
			in[i][j] = false;														
			o[i][j] = false;														
		}																			
																					
	for (uint16_t i=0;i<count;i++)													
	{																				
		o[t[i][0]-1][t[i][1]-1] = true;											
		in[t[i][2]-1][t[i][1]-1] = true;											
	}
																		
	bool wrong_transition = false;														
	for (uint8_t i=0; i<num_states;i++)														
	{																				
			if (in[i][ 0] && (o[i][0] || o[i][2] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12]))
				wrong_transition = true;
			else if (in[i][ 1] && (o[i][0] || o[i][1] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12]))
				wrong_transition = true;
			else if (in[i][ 2] && (o[i][0] || o[i][1] || o[i][2] || o[i][4] || o[i][5] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12]))
				wrong_transition = true;
			else if (in[i][ 3] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][5] || o[i][6] || o[i][10] || o[i][11]))
				wrong_transition = true;
			else if (in[i][ 4] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12]))
				wrong_transition = true;
			else if (in[i][ 5] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][5] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12]))
				wrong_transition = true;
			else if (in[i][ 6] && (o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12]))
				wrong_transition = true;
			else if (in[i][ 7] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 8] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][6] || o[i][7] || o[i][8] || o[i][10] || o[i][11] || o[i][12]))
				wrong_transition = true;
			else if (in[i][ 9] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][7] || o[i][9] || o[i][11] || o[i][12]))
				wrong_transition = true;
			else if (in[i][ 10] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][6] || o[i][7] || o[i][9] || o[i][10] || o[i][11] || o[i][12]))
				wrong_transition = true;
			else if (in[i][ 11] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 12] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][8] || o[i][9] || o[i][10] || o[i][11] || o[i][12]))
				wrong_transition = true;
	}
	assert(wrong_transition != false);
}
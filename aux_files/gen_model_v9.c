// ******************************************** Iteration:31

#include<stdio.h>
#include<stdbool.h>
#include<stdint.h>
void main()
{
	uint8_t event_seq_length = 14;
	uint8_t num_input = 1;
	uint8_t event_seq[1][14] = {{1,2,4,3,7,5,8,7,9,10,6,5,8,7}};
	uint8_t num_states = 9;
	uint8_t t[48][3];
	uint8_t count=0;
	uint8_t t_gen[34][3] = {{1,1,4},{2,5,6},{2,5,7},{2,6,2},{2,6,7},{2,7,2},{2,7,7},{3,4,2},{3,4,5},{3,4,6},{4,2,3},{4,2,5},{5,3,2},{5,3,3},{5,3,6},{6,6,2},{6,6,6},{6,6,7},{6,7,2},{6,7,6},{6,7,7},{7,6,2},{7,6,7},{7,7,2},{7,7,7},{7,8,6},{7,8,8},{7,8,9},{8,10,6},{8,10,9},{9,6,7},{9,7,8},{9,9,6},{9,9,8}};

	for(uint8_t i=0;i<34;i++)				
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

	bool in[num_states][10];												
	bool o[num_states][10];														
																					
	for (uint8_t i=0;i<num_states;i++)												
		for (uint8_t j=0;j<10;j++)													
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
			if (in[i][ 0] && (o[i][0] || o[i][2] || o[i][3] || o[i][4] || o[i][5] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 1] && (o[i][0] || o[i][1] || o[i][4] || o[i][5] || o[i][6] || o[i][7] || o[i][8] || o[i][9] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 2] && (o[i][0] || o[i][1] || o[i][2] || o[i][7] || o[i][8] || o[i][9] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 3] && (o[i][0] || o[i][1] || o[i][3] || o[i][7] || o[i][8] || o[i][9] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 4] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][8] || o[i][9] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 5] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][8] || o[i][9] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 6] && (o[i][1] || o[i][2] || o[i][3] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 7] && (o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][7] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 8] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][7] || o[i][8] || o[i][10]))
				wrong_transition = true;
			else if (in[i][ 9] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][4] || o[i][7] || o[i][9] || o[i][10]))
				wrong_transition = true;
	}
	assert(wrong_transition != false);
}
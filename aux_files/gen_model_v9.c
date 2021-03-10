// ******************************************** Iteration:0

#include<stdio.h>
#include<stdbool.h>
#include<stdint.h>
void main()
{
	uint8_t event_seq_length = 3;
	uint8_t num_input = 10;
	uint8_t event_seq[10][3] = {{1,2,3},{2,3,4},{3,4,5},{4,5,2},{5,2,5},{2,5,2},{5,2,3},{5,2,6},{2,6,3},{6,3,4}};
	uint8_t num_states = 6;
	uint8_t t[30][3];
	uint8_t count=0;
 																		
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

	bool in[num_states][6];												
	bool o[num_states][6];														
																					
	for (uint8_t i=0;i<num_states;i++)												
		for (uint8_t j=0;j<6;j++)													
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
			if (in[i][ 0] && (o[i][0] || o[i][2] || o[i][3] || o[i][4] || o[i][5]))
				wrong_transition = true;
			else if (in[i][ 1] && (o[i][0] || o[i][1] || o[i][3]))
				wrong_transition = true;
			else if (in[i][ 2] && (o[i][0] || o[i][1] || o[i][2] || o[i][4] || o[i][5]))
				wrong_transition = true;
			else if (in[i][ 3] && (o[i][0] || o[i][1] || o[i][2] || o[i][3] || o[i][5]))
				wrong_transition = true;
			else if (in[i][ 4] && (o[i][0] || o[i][2] || o[i][3] || o[i][4] || o[i][5]))
				wrong_transition = true;
			else if (in[i][ 5] && (o[i][0] || o[i][1] || o[i][3] || o[i][4] || o[i][5]))
				wrong_transition = true;
	}
	assert(wrong_transition != false);
}
#include<stdio.h>
#include<stdbool.h>
#include<stdint.h>
void main()
{
	uint8_t event_seq_length = 129;
	uint8_t num_input = 1;
	uint8_t event_seq[1][129] = {{1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,4,3,4,3,4,3,4,3,4,3,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,4,3,4,4,4,4,4,3,4,3,4,3,4,2,2,2,2,2,2,2,2,2,2,3,4,3,4,3,4,4,3}};
	uint8_t length = sizeof(event_seq)/sizeof(event_seq[0][0]);
	uint8_t num_states = 5;
	uint8_t t[num_states][5];
	for (uint8_t i=0;i<num_states;i++)								
		for (uint8_t j=0;j<5;j++)												
			t[i][j] = 0;

	uint8_t t_gen[10][3] = {{1,1,5},{2,2,4},{2,3,3},{2,4,3},{2,5,3},{3,4,2},{4,2,4},{4,3,3},{4,5,3},{5,2,4}};
	for(uint8_t i=0;i<10;i++)											
		t[t_gen[i][0]-1][t_gen[i][1]-1] = t_gen[i][2];

	bool wrong_transition = false;
	uint8_t temp;															
	uint8_t c = 0;																		
	uint8_t count = 1;																	
																						
	for (uint8_t i=0;i<num_input;i++)												
	{																				
																					
		uint8_t state1; 															
		__CPROVER_assume(state1 <= num_states && state1 > 1);						
		temp = state1;																
																					
		for (uint8_t j=0;j<event_seq_length;j++)									
		{																			
			bool p;																	
																					
			if(i==0 && j==0)														
				printf("%d\n",1);												
																					
			uint8_t state2;															
			__CPROVER_assume(state2 <= num_states && state2 > 1);					
																					
			if(event_seq[i][j]==1)													
			{																		
				if(t[0][event_seq[i][j]-1]!=0)										
					if(p && c<count)												
					{																
						t[0][event_seq[i][j]-1] = state2;							
						c = c+1;													
					}																
					else 															
						t[0][event_seq[i][j]-1] = t[0][event_seq[i][j]-1];			
				else 																
					t[0][event_seq[i][j]-1] = state2;								
				temp = t[0][event_seq[i][j]-1];										
			}																		
			else																	
			{																		
				if(t[temp-1][event_seq[i][j]-1]!=0)									
					if(p && c<count)												
					{																
						t[temp-1][event_seq[i][j]-1] = state2;						
						c = c+1;													
					}																
					else 															
						t[temp-1][event_seq[i][j]-1] = t[temp-1][event_seq[i][j]-1];
				else 																
					t[temp-1][event_seq[i][j]-1] = state2;							
				temp = t[temp-1][event_seq[i][j]-1];								
			}																		
																					
		}																			
																					
	}

	bool t1[num_states];														
	for (uint8_t i=0;i<num_states;i++)												
		t1[i] = false;																
																				
	for (uint8_t i=0;i<num_states;i++)								
		for (uint8_t j=0;j<5;j++)									
		{															
			if(t[i][j] > 0 && t[i][j] != i+1)											
				t1[t[i][j] - 1] = true;								
	}
																		
	for (uint8_t i=1;i<num_states;i++)								
		wrong_transition = wrong_transition | !t1[i];

	for (uint8_t i=0;i<num_states;i++)								
		for (uint8_t j=0;j<5;j++)												
			printf("%d",t[i][j]);

	for (uint8_t i=0; i<num_states;i++)							
	{
		if(t[i][0]!=0 && t[t[i][0]-1][0]!=0)
				wrong_transition = true;
		if(t[i][0]!=0 && t[t[i][0]-1][2]!=0)
				wrong_transition = true;
		if(t[i][0]!=0 && t[t[i][0]-1][3]!=0)
				wrong_transition = true;
		if(t[i][0]!=0 && t[t[i][0]-1][4]!=0)
				wrong_transition = true;
		if(t[i][1]!=0 && t[t[i][1]-1][3]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][0]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][1]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][2]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][4]!=0)
				wrong_transition = true;
		if(t[i][3]!=0 && t[t[i][3]-1][0]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][0]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][1]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][2]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][4]!=0)
				wrong_transition = true;
	}
	assert(wrong_transition != false);
}
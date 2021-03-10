#include<stdio.h>
#include<stdbool.h>
#include<stdint.h>
void main()
{
	uint8_t event_seq_length = 3;
	uint8_t num_input = 37;
	uint8_t event_seq[37][3] = {{1,2,2},{2,2,2},{2,2,3},{2,3,4},{3,4,2},{4,2,2},{3,4,5},{4,5,6},{5,6,3},{6,3,4},{3,4,7},{4,7,6},{7,6,3},{3,4,3},{4,3,4},{2,2,5},{2,5,6},{5,6,5},{6,5,6},{5,6,2},{6,2,2},{2,2,7},{2,7,6},{7,6,7},{6,7,6},{7,6,2},{6,2,5},{6,2,7},{2,2,1},{2,1,5},{1,5,6},{6,2,1},{2,1,7},{1,7,6},{2,1,3},{1,3,4},{2,1,2}};
	uint8_t length = sizeof(event_seq)/sizeof(event_seq[0][0]);
	uint8_t num_states = 4;
	uint8_t t[num_states][7];
	for (uint8_t i=0;i<num_states;i++)								
		for (uint8_t j=0;j<7;j++)												
			t[i][j] = 0;

	bool wrong_transition = false;
 																		
	uint8_t temp;																	
																					
	for (uint8_t i=0;i<num_input;i++)												
	{																				
																					
		uint8_t state1; 															
		__CPROVER_assume(state1 <= num_states && state1 > 1);						
		temp = state1;																
																					
		for (uint8_t j=0;j<event_seq_length;j++)									
		{																			
			if(i==0 && j==0)														
				printf("%d\n",1);												
																						
			uint8_t state2;														
			__CPROVER_assume(state2 <= num_states && state2 > 1);					
																					
			if(event_seq[i][j]==1)					
			{
				t[0][event_seq[i][j]-1] = t[0][event_seq[i][j]-1] ? t[0][event_seq[i][j]-1] : state2;						
				temp = t[0][event_seq[i][j]-1];							
			}
			else																	
			{
				t[temp-1][event_seq[i][j]-1] = t[temp-1][event_seq[i][j]-1] ? t[temp-1][event_seq[i][j]-1] : state2;		
				temp = t[temp-1][event_seq[i][j]-1];									
			}
																					
		}																			
																					
	}
	for (uint8_t i=0;i<num_states;i++)								
		for (uint8_t j=0;j<7;j++)												
			printf("%d",t[i][j]);

	for (uint8_t i=0; i<num_states;i++)							
	{
		if(t[i][0]!=0 && t[t[i][0]-1][0]!=0)
				wrong_transition = true;
		if(t[i][0]!=0 && t[t[i][0]-1][3]!=0)
				wrong_transition = true;
		if(t[i][0]!=0 && t[t[i][0]-1][5]!=0)
				wrong_transition = true;
		if(t[i][1]!=0 && t[t[i][1]-1][3]!=0)
				wrong_transition = true;
		if(t[i][1]!=0 && t[t[i][1]-1][5]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][0]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][1]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][2]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][4]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][5]!=0)
				wrong_transition = true;
		if(t[i][2]!=0 && t[t[i][2]-1][6]!=0)
				wrong_transition = true;
		if(t[i][3]!=0 && t[t[i][3]-1][0]!=0)
				wrong_transition = true;
		if(t[i][3]!=0 && t[t[i][3]-1][3]!=0)
				wrong_transition = true;
		if(t[i][3]!=0 && t[t[i][3]-1][5]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][0]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][1]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][2]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][3]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][4]!=0)
				wrong_transition = true;
		if(t[i][4]!=0 && t[t[i][4]-1][6]!=0)
				wrong_transition = true;
		if(t[i][5]!=0 && t[t[i][5]-1][0]!=0)
				wrong_transition = true;
		if(t[i][5]!=0 && t[t[i][5]-1][3]!=0)
				wrong_transition = true;
		if(t[i][5]!=0 && t[t[i][5]-1][5]!=0)
				wrong_transition = true;
		if(t[i][6]!=0 && t[t[i][6]-1][0]!=0)
				wrong_transition = true;
		if(t[i][6]!=0 && t[t[i][6]-1][1]!=0)
				wrong_transition = true;
		if(t[i][6]!=0 && t[t[i][6]-1][2]!=0)
				wrong_transition = true;
		if(t[i][6]!=0 && t[t[i][6]-1][3]!=0)
				wrong_transition = true;
		if(t[i][6]!=0 && t[t[i][6]-1][4]!=0)
				wrong_transition = true;
		if(t[i][6]!=0 && t[t[i][6]-1][6]!=0)
				wrong_transition = true;
	}
	assert(wrong_transition != false);
}
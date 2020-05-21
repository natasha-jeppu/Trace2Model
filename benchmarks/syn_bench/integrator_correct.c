#include<stdio.h>
#include <time.h>
#include <stdlib.h>


int main()
{	
	//Test Cases
	// int ip[11] = {0,1,1,1,1,1,1,1,1,1,1};
	// int ip[11] = {0,-1,-1,-1,-1,-1,-1,-1,-1,-1};
	// int ip[20] = {1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1};
	int ip[22] = {1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1};
	
	//int ip;
	int op,prev_op;

	int i=0;

	prev_op=0;
	op=0;
	srand(time(NULL));
	

	/*code for testing

	while(1)
	{

	*/

	//code for tracing
	while(i < (sizeof(ip)/sizeof(ip[0])))
	//while(i<2000)
	{

	//

		// code for tracing
		printf("nil %d %d\n",ip[i],op);
		op = prev_op + ip[i];
		//

		/* code for tracing
		ip = rand()%3 - 1;
		printf("%d %d\n",op,ip);
		op = prev_op + ip;
		*/

		/* code for testing
		int ip;
		__CPROVER_assume(ip>=-1 && ip<=1);
		op = prev_op + ip;
		*/

		
		if (op>=5)
			op=5;
		else if (op<=-5)
			op=-5;

		/*code for testing
		if(!((prev_op==5 && ip==1) || (prev_op==-5 && ip==-1)))
			assert(op == prev_op + ip);

		if ((prev_op==5 && ip==1) || (prev_op==-5 && ip==-1))
			assert(prev_op == op);
		*/


		i=i+1;
		prev_op = op;
	}
}




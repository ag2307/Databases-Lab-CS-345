#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

// input struct
struct student{
	long long int roll;
	char *date;
	char *status;
};

// converting string to integer
long long toll(char * temp){
	int i=0;
	long long sum=0;
	for(i=0;i<9;i++){
		sum=sum*10+(temp[i]-'0');
	}
	return sum;
}

//checks null pointer
void nullcheck(FILE *f){
	if(f==NULL){
		printf("Could not open the file !!\n");
		exit(0);
	}
	return ;
}

void main(){
	long long int j,k,i;

    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    char *temp; char *status;
    struct student *a;
    a=(struct student *)malloc(sizeof(struct student));
    long long int initial=-1; long long int previous=-1;
	char *ABSENT="Absent";

	FILE *input=fopen("database_12jan2017.csv","r");
	FILE *lower=fopen("L75.csv","w");
	FILE *upper=fopen("G75.csv","w");
	nullcheck(input); nullcheck(lower); nullcheck(upper);

	long long int cnt_present=0; long long int cnt_absent=0;
	long long int net_present=0; long long int net_absent=0;
	while((read = getline(&line, &len, input)) != -1){
		temp=strtok(line,", ");
		a->roll=toll(temp);
		a->date=strtok(NULL,", ");
		a->status=strtok(NULL,", ");

		if(initial==-1 && previous!=-1 && a->roll!=previous){
			double percentage=(double)(cnt_present)/(cnt_present+cnt_absent);
			if(percentage<.75){
				fprintf(lower,"%lld, %lld, %lf\n",previous,cnt_present,percentage*100);
			}
			else{
				fprintf(upper,"%lld, %lld, %lf\n",previous,cnt_present,percentage*100);
			}
			cnt_present=cnt_absent=0;
			initial=previous;
			previous=a->roll;
		}
		if(initial!=-1 && a->roll!=previous){
			double percentage=((double)(cnt_present))/(cnt_present+cnt_absent);
			if(percentage<.75){
				fprintf(lower,"%lld, %lld, %lf\n",previous,cnt_present,percentage*100);
			}
			else{
				fprintf(upper,"%lld, %lld, %lf\n",previous,cnt_present,percentage*100);
			}
			cnt_present=cnt_absent=0;
			initial=previous;
			previous=a->roll;
		}
		previous=a->roll;
		if(a->status[0]=='A'){
			cnt_absent++;
		}
		else{
			cnt_present++;
		}
	}
	double percentage=(double)(cnt_present)/(cnt_present+cnt_absent);
	if(percentage<.75){
		fprintf(lower,"%lld, %lld, %lf\n",previous,cnt_present,percentage*100);
	}
	else{
		fprintf(upper,"%lld, %lld, %lf\n",previous,cnt_present,percentage*100);
	}
	fclose(input);
	fclose(lower);
	fclose(upper);
	return ;	
}
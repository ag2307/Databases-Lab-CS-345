/*
	PUT THE 'C' CODE OUTSIDE THE 'database-19-jan-2018' FOLDER AS THE PATH IS SET ACCORDING TO THAT !!

*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>
//////////////////////////////////////////////////////////////////////////////////
int number_of_candidates=0;
int exam_file_count=0;
int credits_list_count=0;
//////////////////////////////////////////////////////////////////////////////////
struct student{
	char roll[20];
	char name[100];
	int count;
	char registered_courses[100][100];
};
//////////////////////////////////////////////////////////////////////////////////
struct student candidates[30000];
int mark_time_clash[30000];
int mark_credits[30000];
//////////////////////////////////////////////////////////////////////////////////
struct course_credits{
	char course[15];
	int credits;
};
//////////////////////////////////////////////////////////////////////////////////
struct course_credits credits_list[300];
//////////////////////////////////////////////////////////////////////////////////
struct exam_time{
	char course[15];
	char date[20];
	int start_time;
	int end_time;
};
//////////////////////////////////////////////////////////////////////////////////
struct exam_time schedule[1500];
int mark_duplicate[1500]={0};
//////////////////////////////////////////////////////////////////////////////////
// converting string to integer
int toll(char * temp){
	int i=0;
	int sum=0;
	for(i=0;i<2;i++){
		sum=sum*10+(temp[i]-'0');
	}
	return sum;
}
//////////////////////////////////////////////////////////////////////////////////
int map_time_to_number(char * time){
	char *first  = strtok(time,":");
	// printf("%s\n",first );
	char *second = strtok(NULL,":");
	// printf("%s\n",second );
	return toll(first)*60+toll(second);
}
//////////////////////////////////////////////////////////////////////////////////
int check_for_roll(char *roll){	
	int i;
	// printf("**%s**\n",candidates[0].roll);
	// printf("%d\n",number_of_candidates );
	for(i=0;i<number_of_candidates;i++){
		// printf("%s\n",roll );
		// if(i==0){
		// 	printf("%s\n",candidates[i].roll);
		// }
		if(strcmp(roll,candidates[i].roll)==0){
			return i;
		}
	}
	return i;
}
//////////////////////////////////////////////////////////////////////////////////
int course_duplicacy_check(char *id,int count,int index){
	int i;
	for(i=0;i<count;i++){
		if(strcmp(id,candidates[index].registered_courses[i])==0){
			return i;
		}
	}
	return i;
}

//////////////////////////////////////////////////////////////////////////////////
//checks null pointer
void nullcheck(FILE *f){
	if(f==NULL){
		printf("Could not open the file !!\n");
		exit(0);
	}
	return ;
}
//////////////////////////////////////////////////////////////////////////////////
void listdir(const char *name)
{
    DIR *dir;
    int j,k,i,roll;
    struct dirent *entry;

    if (!(dir = opendir(name)))
        return;

    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_DIR) {
            char path[1024];
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
                continue;
            snprintf(path, sizeof(path), "%s/%s", name, entry->d_name);
            //printf("%s\n", entry->d_name);
            listdir(path);
        } 
        else {
            char temp[300];
			// printf("***%s***\n",entry->d_name);
            strncpy(temp,name,299);
            strcat(temp,"/");
            strcat(temp,entry->d_name);
            // printf("%s\n",temp);
            FILE *fp = fopen(temp,"r");
            nullcheck(fp);
            int red; size_t len = 0;ssize_t read;
            char * data=NULL;
            char *id=strtok(entry->d_name,".");
            // printf("%s\n",id);
            while((read = getline(&data, &len, fp)) != -1){
            	// printf("%s\n",data);
            	strtok(data,",");
            	char *roll = strtok(NULL,",");
            	// printf("%s\n", roll);
            	int index = check_for_roll(roll);
            	// printf("%d\n",index );
            	if(index==number_of_candidates)
            		number_of_candidates++;
     			// printf("%d\n",number_of_candidates );
            	strcpy(candidates[index].roll,roll);
            	char *name = strtok(NULL,",");
            	strcpy(candidates[index].name,name);
            	int index1= course_duplicacy_check(id,candidates[index].count,index);
            	if(index1==candidates[index].count)
            		candidates[index].count++;
            	strcpy(candidates[index].registered_courses[index1],id);
            }
            // printf("\n\n");
            fclose(fp);
        }
    }
    closedir(dir);
}
////////////////////////////////////////////////////////////////////////////////////

check_time_clash(){
	FILE *timetable=fopen("./database-19-jan-2018/exam-time-table.csv","r");
	FILE *output=fopen("time_clash_check.csv","w");
	nullcheck(timetable);
	char * data=NULL; size_t len = 0; ssize_t read;
	while((read = getline(&data, &len, timetable)) != -1){
		char *code=strtok(data,",");
		char *date=strtok(NULL,",");
		char *first=strtok(NULL,","); char *second=strtok(NULL,",");
		// printf("%s\n",second );
		int start=map_time_to_number(first);
		int end=map_time_to_number(second);
		// printf("%d %d\n",start,end );
		strcpy(schedule[exam_file_count].course,code);
		strcpy(schedule[exam_file_count].date,date);
		schedule[exam_file_count].start_time=start;
		schedule[exam_file_count++].end_time=end;
	}
	fclose(timetable);
	int i;
	int n;
	for(i=0;i<exam_file_count-1;i++){
		for(n=i+1;n<exam_file_count;n++){
			if(strcmp(schedule[i].course,schedule[n].course)==0&&strcmp(schedule[i].date,schedule[n].date)==0&&schedule[i].start_time==schedule[n].start_time&&schedule[i].end_time==schedule[n].end_time){
				mark_duplicate[n]=1;
			}
		}
	}
	for(i=0;i<number_of_candidates;i++){
		int j;
		for(j=0;j<candidates[i].count-1;j++){
			int k;
			for(k=j+1;k<candidates[i].count;k++){
				int l;
				int flag=0;
				for(l=0;l<exam_file_count;l++){
					if(mark_duplicate[l])
						continue;
					if(strcmp(schedule[l].course,candidates[i].registered_courses[j])==0){
						int m;
						for(m=0;m<exam_file_count;m++){
							if(mark_duplicate[m])
								continue;
							if(strcmp(schedule[m].course,candidates[i].registered_courses[k])==0){
								if(strcmp(schedule[l].date,schedule[m].date)==0){
									if((schedule[l].start_time<=schedule[m].end_time && schedule[l].start_time>=schedule[m].start_time)||(schedule[l].end_time<=schedule[m].end_time && schedule[l].end_time>=schedule[m].start_time)){
										fprintf(output,"%s,%s,%s,%s\n",candidates[i].roll,candidates[i].name,schedule[l].course,schedule[m].course);
										flag=1;
										if(flag)
											break;
									}
								}
							}
						}
						if(flag)
							break;
					}
				}
			}
		}
	}
	fclose(output);
}

/////////////////////////////////////////////////////////////////////////////////////////

check_credit_excess(){
	FILE *cc=fopen("./database-19-jan-2018/course-credits.csv","r");
	FILE *output=fopen("credits_overflow_check.csv","w");
	nullcheck(cc);
	char * data=NULL; size_t len = 0; ssize_t read;
	while((read = getline(&data, &len, cc)) != -1){
		char *id=strtok(data,",");
		char *credits=strtok(NULL,",");
		// printf("%s\n",second );
		int temp=(int)(credits[0]-'0');
		// printf("%d\n",temp);
		strcpy(credits_list[credits_list_count].course,id);
		credits_list[credits_list_count++].credits=temp;
	}
	fclose(cc);
	int i,j,k;
	for(i=0;i<number_of_candidates;i++){
		int sum=0;
		for(j=0;j<candidates[i].count;j++){
			for(k=0;k<credits_list_count;k++){
				if(strcmp(candidates[i].registered_courses[j],credits_list[k].course)==0){
					sum+=credits_list[k].credits;
					break;
				}
			}
		}
		if(sum>40){
			fprintf(output,"%s,%s,%d\n",candidates[i].roll,candidates[i].name,sum);
		}
	}
	fclose(output);
}



//////////////////////////////////////////////////////////////////////////////////////////

void main(){

	char *directory="./database-19-jan-2018/course-wise-students-list";

	int i;
	for(i=0;i<30000;i++){
		candidates[i].count=0;
	}

	listdir(directory);
	check_time_clash();
	check_credit_excess();

	return ;	
}



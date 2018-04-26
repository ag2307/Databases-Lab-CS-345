#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>

//checks null pointer
void nullcheck(FILE *f){
	if(f==NULL){
		printf("Could not open the file !!\n");
		exit(0);
	}
	return ;
}

void add_ett_entries(){
	FILE *input=fopen("./database-19-jan-2018/exam-time-table.csv","r");
	FILE *output=fopen("150123001_ett.sql","w");
	nullcheck(input); nullcheck(output);
	char * data=NULL; size_t len = 0; ssize_t read;
	while((read = getline(&data, &len, input)) != -1){
		char *code=strtok(data,",");
		char *date=strtok(NULL,",");
		char *first=strtok(NULL,","); 
		char *second=strtok(NULL,",");
		fprintf(output,"INSERT INTO ett VALUES (\"%s\",\"%s\",\"%s\",\"%s\");\n",code,date,first,second);
		fprintf(output,"INSERT INTO ett_temp VALUES (\"%s\",\"%s\",\"%s\",\"%s\");\n",code,date,first,second);
		fprintf(output,"INSERT INTO ett_clone VALUES (\"%s\",\"%s\",\"%s\",\"%s\");\n",code,date,first,second);
	}
	fclose(input); fclose(output);
	return;
}

void add_cc_entries(){
	FILE *input=fopen("./database-19-jan-2018/course-credits.csv","r");
	FILE *output=fopen("150123001_cc.sql","w");
	nullcheck(input); nullcheck(output);
	char * data=NULL; size_t len = 0; ssize_t read;
	while((read = getline(&data, &len, input)) != -1){
		char *code=strtok(data,",");
		char *credits=strtok(NULL,",");
		fprintf(output,"INSERT INTO cc VALUES (\"%s\",%s);\n",code,credits);
		fprintf(output,"INSERT INTO cc_temp VALUES (\"%s\",%s);\n",code,credits);
		fprintf(output,"INSERT INTO cc_clone VALUES (\"%s\",%s);\n",code,credits);
	}
	fclose(input); fclose(output);
	return;
}

void add_cwsl_entries(char * name,FILE * output){

	DIR *dir;
	int j,k,i,roll;
	struct dirent *entry;

	if (!(dir = opendir(name)))
		return;
	nullcheck(output);

	while ((entry = readdir(dir)) != NULL) {
		if (entry->d_type == DT_DIR) {
			char path[1024];
			if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
				continue;
			snprintf(path, sizeof(path), "%s/%s", name, entry->d_name);
			add_cwsl_entries(path,output);
		} 
		else {
			char temp[300];
			strncpy(temp,name,299);
			strcat(temp,"/");
			strcat(temp,entry->d_name);
			FILE *fp = fopen(temp,"r");
			nullcheck(fp);
			int red; size_t len = 0;ssize_t read;
			char * data=NULL;
			char *id=strtok(entry->d_name,".");
			while((read = getline(&data, &len, fp)) != -1){
				char *sno=strtok(data,",");
				char *roll = strtok(NULL,",");
				char *name = strtok(NULL,",");
				char *email = strtok(NULL,",");
				fprintf(output,"INSERT INTO cwsl VALUES (\"%s\",%s,\"%s\",\"%s\",\"%s\");\n",id,sno,roll,name,email);
				fprintf(output,"INSERT INTO cwsl_temp VALUES (\"%s\",%s,\"%s\",\"%s\",\"%s\");\n",id,sno,roll,name,email);
				fprintf(output,"INSERT INTO cwsl_clone VALUES (\"%s\",%s,\"%s\",\"%s\",\"%s\");\n",id,sno,roll,name,email);
			}
			fclose(fp);
		}
	}
	closedir(dir);
	return;
}

void main(){
	add_ett_entries();
	add_cc_entries();
	char * name="./database-19-jan-2018/course-wise-students-list";
	FILE *output=fopen("150123001_cwsl.sql","w");
	nullcheck(output);
	add_cwsl_entries(name,output);
	return;
}
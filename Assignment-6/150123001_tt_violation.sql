delimiter $$
CREATE PROCEDURE tt_violation()
BEGIN
	declare done1 int DEFAULT FALSE;
	declare var_name varchar(50);
	declare var_roll_number varchar(20);
	declare var_exam_date date;
	declare var_start_time time;
	declare var_end_time time;
	declare var_ed date;
	declare var_st time;
	declare var_et time;
	declare var_cid varchar(10);
	declare cid_ varchar(10);
	declare var_course_id_1 varchar(10);
	declare var_course_id_2 varchar(10);
	declare cursor1 cursor for select a.name,a.roll_number,a.course_id,b.exam_date,
	b.start_time,b.end_time from cwsl as a join ett as b where a.course_id=b.course_id;
	declare continue handler for NOT FOUND set done1=TRUE;
	drop table if exists temp;
	create table temp (roll_number varchar(20),name varchar(50),course_id_1 varchar(10),course_id_2 varchar(10));
	open cursor1;
	outer_loop: LOOP
		fetch cursor1 into var_name,var_roll_number,cid_,var_exam_date,var_start_time,var_end_time;
		if done1 then
			LEAVE outer_loop;
		end if;
		inner_block:BEGIN
			declare done2 int DEFAULT FALSE;
			declare cursor2 cursor for select a.course_id,b.exam_date,b.start_time,
			b.end_time from cwsl as a join ett as b where a.course_id=b.course_id and a.roll_number=var_roll_number;
			declare continue handler for NOT FOUND set done2=TRUE;
			open cursor2;
			inner_loop: LOOP	
				fetch next from cursor2 into var_cid,var_ed,var_st,var_et;
				if done2 then
					LEAVE inner_loop;
				end if;
				if var_cid>cid_ and var_ed=var_exam_date then
					if var_st=var_start_time then
						insert into temp values(var_roll_number,var_name,cid_,var_cid);
					end if;
				end if;
			end LOOP inner_loop;
			close cursor2;
		END inner_block;
	end LOOP outer_loop; 
	close cursor1;
	select distinct * from temp;	
END;
$$
delimiter ;

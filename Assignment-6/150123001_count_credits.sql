delimiter $$
CREATE PROCEDURE count_credits()
BEGIN
	declare done1 int DEFAULT FALSE;
	declare var_name varchar(50);
	declare var_roll_number varchar(20);
	declare var_number_of_credits int;

	declare cursor1 cursor for select a.name,a.roll_number,sum(b.number_of_credits) from cwsl as a natural join cc as b group by a.roll_number,a.name;
	declare continue handler for NOT FOUND set done1=TRUE;
	drop table if exists temp_cc;
	create table temp_cc (roll_number varchar(20),name varchar(50),total_credits int);
	open cursor1;
	outer_loop: LOOP
		fetch cursor1 into var_name,var_roll_number,var_number_of_credits;
		if done1 then
			LEAVE outer_loop;
		end if;
		if var_number_of_credits>40 then
			insert into temp_cc values(var_roll_number,var_name,var_number_of_credits);
		end if;
	end LOOP outer_loop; 
	close cursor1;
	select * from temp_cc;
END;
$$
delimiter ;

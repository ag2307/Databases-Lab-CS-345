-- First
select ScheduledIn.course_id 
from ScheduledIn 
where ScheduledIn.room_number=2001;

-- Second
select ScheduledIn.course_id 
from ScheduledIn 
where ScheduledIn.letter='C';

-- Third
select distinct ScheduledIn.division 
from ScheduledIn 
where ScheduledIn.room_number='L3' or ScheduledIn.room_number='L2';

-- Fourth
select distinct ScheduledIn.course_id
from ScheduledIn
where ScheduledIn.course_id in (
	select ScheduledIn.course_id
	from ScheduledIn
	group by ScheduledIn.course_id
	having count(distinct ScheduledIn.room_number)>1
);

-- Fifth
select Department.name
from Department
where Department.department_id in (
	select distinct ScheduledIn.department_id
	from ScheduledIn
	where ScheduledIn.room_number='L1' or ScheduledIn.room_number='L2' 
	or ScheduledIn.room_number='L3' or ScheduledIn.room_number='L4'
);

-- Sixth
select Department.name
from Department
where Department.department_id not in (
	select distinct ScheduledIn.department_id
	from ScheduledIn
	where ScheduledIn.room_number='L1' or ScheduledIn.room_number='L2'
);

-- Seventh
select Department.name
from Department
where Department.department_id in (
	select ScheduledIn.department_id
	from ScheduledIn
	group by ScheduledIn.department_id
	having count(distinct ScheduledIn.letter)=17
);

-- Eighth
select letter,count(distinct course_id)
from ScheduledIn
group by letter
order by 2;

-- Ninth
select room_number,count(distinct course_id)
from ScheduledIn
group by room_number
order by 2 desc;

-- Tenth
select letter,number_of_courses
from(
	select letter,count(distinct course_id) as number_of_courses
	from ScheduledIn
	group by letter
) as x
where x.number_of_courses=(
	select min(number_of_courses)
	from (
		select letter,count(distinct course_id) as number_of_courses
		from ScheduledIn
		group by letter
	) as y
);

-- Eleventh
select distinct letter
from ScheduledIn
where course_id like '%M';

-- Twelfth
select a.department_id,a.letter
from (
	select x.department_id,y.letter
	from Department as x
	join(
		select distinct letter
		from Slot
	) as y
) as a
left join(
	select distinct ScheduledIn.department_id,ScheduledIn.letter
	from ScheduledIn
	group by department_id,letter
) as b
on a.department_id=b.department_id and a.letter=b.letter
where b.department_id is null
order by 1;
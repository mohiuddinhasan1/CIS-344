create database restaurant_reservations;
use restaurant_reservations;

create table customers (
    customerId int not null auto_increment,
    customerName varchar(45) not null,
    contactInfo varchar(200),
    primary key (customerId)
);

insert into customers (customerName, contactInfo) values
('Joe Biden', 'joeB@yahoo.com'),
('Jane Smith', 'DonaldTrump1@gmail.com'),
('Sheikh Hasina', 'Sheikh.Hasina@gmail.com'),
('Johny Helman', 'John.jay@gmail.com'),
('Michael Jackson', 'michael.jackson@gmail.com');

create table reservations (
    reservationId int not null auto_increment,
    customerId int not null,
    reservationTime datetime not null,
    numberOfGuests int not null,
    specialRequests varchar(200),
    primary key (reservationId),
    foreign key (customerId) references customers(customerId)
);

insert into reservations (customerId, reservationTime, numberOfGuests, specialRequests) values
(1, '2024-05-11 18:00:00', 4, 'No Onion'),
(2, '2024-06-12 19:30:00', 2, 'Vegetarian meal for one guest'),
(3, '2024-07-10 15:30:00', 10, 'Please serve halal food'),
(4, '2024-06-11 18:30:00', 5, 'Mild spice'),
(5, '2024-06-10 16:00:00', 6, 'Please sing Happy Birthday for my daughter');

create table diningPreferences (
    preferenceId int not null auto_increment,
    customerId int not null,
    favoriteTable varchar(45),
    dietaryRestrictions varchar(200),
    primary key (preferenceId),
    foreign key (customerId) references customers(customerId)
);

insert into diningPreferences (customerId, favoriteTable, dietaryRestrictions) values
(1, 'Table 5', 'No nuts'),
(2, 'Table 2', 'No pork'),
(3, 'Table 3', 'Gluten-free'),
(4, 'Table 3', 'No nuts'),
(5, 'Table 10', NULL);

-- Create procedure to find reservations for a customer
delimiter //
create procedure findReservations(in customer_id int)
begin
    select * from reservations where customerId = customer_id;
end //
delimiter ;

-- Call procedure to find reservations for customer with ID 1
call findReservations(1);

-- Create procedure to update special requests for a reservation
delimiter //
create procedure addSpecialRequest(in reservation_id int, in requests varchar(200))
begin
    update reservations set specialRequests = requests where reservationId = reservation_id;
end //
delimiter ;

-- Create procedure to add a new reservation
delimiter //
create procedure addReservation(
    in customerName varchar(45), 
    in contactInfo varchar(200), 
    in reservationTime datetime, 
    in numberOfGuests int, 
    in specialRequests varchar(200), 
    in favoriteTable varchar(45), 
    in dietaryRestrictions varchar(200))
begin
    declare custId int;
    -- Check if customer exists
    select customerId into custId from customers where customerName = customerName and contactInfo = contactInfo limit 1;
    
    -- If customer does not exist, insert new customer
    if custId is null then
        insert into customers (customerName, contactInfo) values (customerName, contactInfo);
        set custId = last_insert_id();
    end if;

    -- Insert reservation
    insert into reservations (customerId, reservationTime, numberOfGuests, specialRequests) 
    values (custId, reservationTime, numberOfGuests, specialRequests);

    -- Insert dining preferences if provided
    if favoriteTable is not null or dietaryRestrictions is not null then
        insert into diningPreferences (customerId, favoriteTable, dietaryRestrictions) 
        values (custId, favoriteTable, dietaryRestrictions);
    end if;
end //
delimiter ;

-- Call procedure to add a reservation for Emma Watson
call addReservation('Emma Watson', 'emmaWatson@outlook.com', '2024-05-28 19:30:00', 3, 'None', 'Table 8', 'No dairy');
call addReservation('Emma Watson', 'emmaWatson@outlook.com', '2024-05-28 19:30:00', 6, 'Reserve side table', 'Table 8', 'No dairy');
call addReservation('John Carrera', 'johnWCarrera@outlook.com', '2024-06-02 14:45:00', 6, 'Window seats', 'Table 4', 'No peanuts');

-- Call procedure for adding a special request to a reservation
call addSpecialRequest(1, 'No Onion and No Garlic');
import mysql.connector
from mysql.connector import Error

class RestaurantDatabase():
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="restaurant_reservations",
                 user='root',
                 password='Password'):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)
            
            if self.connection.is_connected():
                print("Successfully connected to the database")
                return
        except Error as e:
            print("Error while connecting to MySQL", e)

    def addCustomer(self, customer_name, contact_info):
        ''' Method to add a new customer to the customers table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "INSERT INTO customers (customerName, contactInfo) VALUES (%s, %s)"
            self.cursor.execute(query, (customer_name, contact_info))
            self.connection.commit()
            print("Customer added successfully")
            return self.cursor.lastrowid

    def findCustomer(self, customer_name, contact_info):
        ''' Method to find a customer in the customers table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "SELECT customerId FROM customers WHERE customerName = %s AND contactInfo = %s"
            self.cursor.execute(query, (customer_name, contact_info))
            result = self.cursor.fetchone()
            return result[0] if result else None

    def addReservation(self, customer_name, contact_info, reservation_time, number_of_guests, special_requests):
        ''' Method to insert a new reservation into the reservations table '''
        if self.connection.is_connected():
            # Check if the customer exists, otherwise add the customer
            customer_id = self.findCustomer(customer_name, contact_info)
            if not customer_id:
                customer_id = self.addCustomer(customer_name, contact_info)
            
            # Insert the reservation
            self.cursor = self.connection.cursor()
            query = "INSERT INTO reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (customer_id, reservation_time, number_of_guests, special_requests))
            self.connection.commit()
            print("Reservation added successfully")

    def getAllReservations(self):
        ''' Method to get all reservations from the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "SELECT * FROM reservations"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def getCustomerPreferences(self, customer_id):
        ''' Method to retrieve dining preferences for a specific customer '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "SELECT * FROM diningPreferences WHERE customerId = %s"
            self.cursor.execute(query, (customer_id,))
            preferences = self.cursor.fetchall()
            return preferences

    def addDiningPreference(self, customer_id, favorite_table, dietary_restrictions):
        ''' Method to add dining preferences for a customer '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "INSERT INTO diningPreferences (customerId, favoriteTable, dietaryRestrictions) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (customer_id, favorite_table, dietary_restrictions))
            self.connection.commit()
            print("Dining preferences added successfully")

    def updateSpecialRequest(self, reservation_id, special_requests):
        ''' Method to update special requests for a reservation '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "UPDATE reservations SET specialRequests = %s WHERE reservationId = %s"
            self.cursor.execute(query, (special_requests, reservation_id))
            self.connection.commit()
            print("Special requests updated successfully")



from http.server import HTTPServer, BaseHTTPRequestHandler
from restaurantDatabase import RestaurantDatabase
import cgi

class RestaurantPortalHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.database = RestaurantDatabase()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == '/addReservation':
            self.handle_add_reservation()
        elif self.path == '/addCustomer':
            self.handle_add_customer()
        elif self.path == '/addSpecialRequests':
            self.handle_add_special_requests()
        else:
            self.send_error(404, 'Path Not Found: %s' % self.path)

    def handle_add_reservation(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        
        customer_id = int(form.getvalue("customer_id"))
        reservation_time = form.getvalue("reservation_time")
        number_of_guests = int(form.getvalue("number_of_guests"))
        special_requests = form.getvalue("special_requests")
        
        # Call the Database Method to add a new reservation
        self.database.addReservation(customer_id, reservation_time, number_of_guests, special_requests)
        print("Reservation added for customer ID:", customer_id)
        
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div> <a href='/'>Home</a>| \
                          <a href='/addReservation'>Add Reservation</a>|\
                          <a href='/viewReservations'>View Reservations</a>|\
                          <a href='/addCustomer'>Add Customer</a></div>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<h3>Reservation has been added</h3>")
        self.wfile.write(b"<div><a href='/addReservation'>Add Another Reservation</a></div>")
        self.wfile.write(b"</center></body></html>")

    def handle_add_customer(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        
        customer_name = form.getvalue("customer_name")
        contact_info = form.getvalue("contact_info")
        
        self.database.addCustomer(customer_name, contact_info)
        print("Customer added:", customer_name)
        
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div> <a href='/'>Home</a>| \
                          <a href='/addReservation'>Add Reservation</a>|\
                          <a href='/viewReservations'>View Reservations</a>|\
                          <a href='/addCustomer'>Add Customer</a></div>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<h3>Customer has been added</h3>")
        self.wfile.write(b"<div><a href='/addCustomer'>Add Another Customer</a></div>")
        self.wfile.write(b"</center></body></html>")

    def handle_add_special_requests(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        
        reservation_id = int(form.getvalue("reservation_id"))
        special_requests = form.getvalue("special_requests")
        
        self.database.updateSpecialRequest(reservation_id, special_requests)
        print("Special requests updated for reservation ID:", reservation_id)
        
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div> <a href='/'>Home</a>| \
                          <a href='/addReservation'>Add Reservation</a>|\
                          <a href='/viewReservations'>View Reservations</a>|\
                          <a href='/addCustomer'>Add Customer</a></div>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<h3>Special requests have been updated</h3>")
        self.wfile.write(b"<div><a href='/addSpecialRequests'>Update Another Request</a></div>")
        self.wfile.write(b"</center></body></html>")

    def do_GET(self):
        if self.path == '/':
            self.handle_home()
        elif self.path == '/addReservation':
            self.render_add_reservation_form()
        elif self.path == '/addCustomer':
            self.render_add_customer_form()
        elif self.path == '/addSpecialRequests':
            self.render_add_special_requests_form()
        else:
            self.send_error(404, 'Path Not Found: %s' % self.path)

    def handle_home(self):
        data = self.database.getAllReservations()
        print(data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div> <a href='/'>Home</a>| \
                          <a href='/addReservation'>Add Reservation</a>|\
                          <a href='/viewReservations'>View Reservations</a>|\
                          <a href='/addCustomer'>Add Customer</a></div>")
        self.wfile.write(b"<hr><h2>All Reservations</h2>")
        self.wfile.write(b"<table border=2> \
                           <tr><th> Reservation ID </th>\
                               <th> Customer ID </th>\
                               <th> Reservation Time </th>\
                               <th> Number of Guests </th>\
                               <th> Special Requests </th></tr>")
        for row in data:
            self.wfile.write(b'<tr><td>')
            self.wfile.write(str(row[0]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[1]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[2]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[3]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[4]).encode())
            self.wfile.write(b'</td></tr>')
        
        self.wfile.write(b"</table></center>")
        self.wfile.write(b"</body></html>")

    def render_add_reservation_form(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        self.wfile.write(b"<html><head><title>Add Reservation</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Add Reservation</h1>")
        self.wfile.write(b"<form method='POST' action='/addReservation'>")
        self.wfile.write(b"Customer ID: <input type='text' name='customer_id'><br>")
        self.wfile.write(b"Reservation Time: <input type='text' name='reservation_time'><br>")
        self.wfile.write(b"Number of Guests: <input type='text' name='number_of_guests'><br>")
        self.wfile.write(b"Special Requests: <input type='text' name='special_requests'><br>")
        self.wfile.write(b"<input type='submit' value='Add Reservation'>")
        self.wfile.write(b"</form></center></body></html>")

    def render_add_customer_form(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        self.wfile.write(b"<html><head><title>Add Customer</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Add Customer</h1>")
        self.wfile.write(b"<form method='POST' action='/addCustomer'>")
        self.wfile.write(b"Customer Name: <input type='text' name='customer_name'><br>")
        self.wfile.write(b"Contact Info: <input type='text' name='contact_info'><br>")
        self.wfile.write(b"<input type='submit' value='Add Customer'>")
        self.wfile.write(b"</form></center></body></html>")

    def render_add_special_requests_form(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        self.wfile.write(b"<html><head><title>Update Special Requests</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Update Special Requests</h1>")
        self.wfile.write(b"<form method='POST' action='/addSpecialRequests'>")
        self.wfile.write(b"Reservation ID: <input type='text' name='reservation_id'><br>")
        self.wfile.write(b"Special Requests: <input type='text' name='special_requests'><br>")
        self.wfile.write(b"<input type='submit' value='Update Requests'>")
        self.wfile.write(b"</form></center></body></html>")

def run(server_class=HTTPServer, handler_class=RestaurantPortalHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

run()

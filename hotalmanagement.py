import mysql.connector
from datetime import datetime

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sumit@11",  
    database="hotel_management"
)
cursor = conn.cursor()

# ----------- GUEST FUNCTIONS -----------
def add_guest():
    name = input("Enter guest name: ")
    email = input("Enter guest email: ")
    phone = input("Enter guest phone: ")
    cursor.execute("INSERT INTO Guests (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    conn.commit()
    print("Guest added successfully!\n")

def view_guests():
    cursor.execute("SELECT * FROM Guests")
    guests = cursor.fetchall()
    print("\nGuests List:")
    for guest in guests:
        print(guest)
    print()

def update_guest():
    guest_id = input("Enter guest ID to update: ")
    name = input("Enter new name: ")
    email = input("Enter new email: ")
    phone = input("Enter new phone: ")
    cursor.execute("UPDATE Guests SET name=%s, email=%s, phone=%s WHERE guest_id=%s", (name, email, phone, guest_id))
    conn.commit()
    print("Guest updated successfully!\n")

def delete_guest():
    guest_id = input("Enter guest ID to delete: ")
    cursor.execute("DELETE FROM Guests WHERE guest_id=%s", (guest_id,))
    conn.commit()
    print("Guest deleted successfully!\n")

# ----------- ROOM FUNCTIONS -----------
def add_room():
    room_type = input("Enter room type: ")
    price = float(input("Enter room price: "))
    cursor.execute("INSERT INTO Rooms (room_type, price) VALUES (%s, %s)", (room_type, price))
    conn.commit()
    print("Room added successfully!\n")

def view_rooms():
    cursor.execute("SELECT * FROM Rooms")
    rooms = cursor.fetchall()
    print("\nRooms List:")
    for room in rooms:
        print(room)
    print()

def update_room():
    room_id = input("Enter room ID to update: ")
    room_type = input("Enter new room type: ")
    price = float(input("Enter new price: "))
    status = input("Enter status (Available/Occupied): ")
    cursor.execute("UPDATE Rooms SET room_type=%s, price=%s, status=%s WHERE room_id=%s", (room_type, price, status, room_id))
    conn.commit()
    print("Room updated successfully!\n")

def delete_room():
    room_id = input("Enter room ID to delete: ")
    cursor.execute("DELETE FROM Rooms WHERE room_id=%s", (room_id,))
    conn.commit()
    print("Room deleted successfully!\n")

# ----------- BOOKING FUNCTIONS -----------
def add_booking():
    guest_id = input("Enter guest ID: ")
    room_id = input("Enter room ID: ")
    check_in = input("Enter check-in date (YYYY-MM-DD): ")
    check_out = input("Enter check-out date (YYYY-MM-DD): ")

    # Check if room is available
    cursor.execute("SELECT status FROM Rooms WHERE room_id=%s", (room_id,))
    status = cursor.fetchone()
    if status[0] == "Occupied":
        print("Room is already occupied!\n")
        return

    cursor.execute("INSERT INTO Bookings (guest_id, room_id, check_in, check_out) VALUES (%s, %s, %s, %s)", 
                   (guest_id, room_id, check_in, check_out))
    cursor.execute("UPDATE Rooms SET status='Occupied' WHERE room_id=%s", (room_id,))
    conn.commit()
    print("Booking added successfully!\n")

def view_bookings():
    cursor.execute("""
    SELECT b.booking_id, g.name, r.room_type, b.check_in, b.check_out 
    FROM Bookings b
    JOIN Guests g ON b.guest_id = g.guest_id
    JOIN Rooms r ON b.room_id = r.room_id
    """)
    bookings = cursor.fetchall()
    print("\nBookings List:")
    for booking in bookings:
        print(booking)
    print()

def delete_booking():
    booking_id = input("Enter booking ID to delete: ")
    # Free the room
    cursor.execute("SELECT room_id FROM Bookings WHERE booking_id=%s", (booking_id,))
    room_id = cursor.fetchone()[0]
    cursor.execute("UPDATE Rooms SET status='Available' WHERE room_id=%s", (room_id,))
    
    cursor.execute("DELETE FROM Bookings WHERE booking_id=%s", (booking_id,))
    conn.commit()
    print("Booking deleted successfully!\n")

# ----------- MAIN MENU -----------
def main_menu():
    while True:
        print("----- HOTEL MANAGEMENT SYSTEM -----")
        print("1. Add Guest")
        print("2. View Guests")
        print("3. Update Guest")
        print("4. Delete Guest")
        print("5. Add Room")
        print("6. View Rooms")
        print("7. Update Room")
        print("8. Delete Room")
        print("9. Add Booking")
        print("10. View Bookings")
        print("11. Delete Booking")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_guest()
        elif choice == '2':
            view_guests()
        elif choice == '3':
            update_guest()
        elif choice == '4':
            delete_guest()
        elif choice == '5':
            add_room()
        elif choice == '6':
            view_rooms()
        elif choice == '7':
            update_room()
        elif choice == '8':
            delete_room()
        elif choice == '9':
            add_booking()
        elif choice == '10':
            view_bookings()
        elif choice == '11':
            delete_booking()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.\n")

# Run the program
main_menu()

# Close the connection
cursor.close()
conn.close()


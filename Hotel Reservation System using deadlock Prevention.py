import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
from datetime import datetime
from threading import Lock

class HotelReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Room Reservation System")
        self.root.geometry("800x500")

        # Background Image
        self.background_image = PhotoImage(file="background2.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.available_rooms = set(range(101, 111))
        self.available_rooms.update(range(201, 211))
        self.available_rooms.update(range(301, 311))
        self.available_rooms.update(range(401, 411))
        self.available_rooms.update(range(501, 511))

        self.customer_rooms = {}
        self.reservation_history = []
        self.sno = 1

        # Create a Lock for synchronization
        self.reservation_lock = Lock()

        # Title
        self.title_label = tk.Label(root, text="Hotel Room Reservation System", font=("Helvetica", 20), bg="blue", fg="white")
        self.title_label.pack(pady=10)

        # Customer Name
        self.label_name = tk.Label(root, text="Enter Your Name:", bg="black", fg="white", font=("Helvetica", 12))
        self.label_name.pack()
        self.customer_name_entry = tk.Entry(root, font=("Helvetica", 12))
        self.customer_name_entry.pack()

        # Room Number
        self.label_room = tk.Label(root, text="Choose a Room (101-110, 201-210, 301-310, 401-410, 501-510):", bg="black", fg="white", font=("Helvetica", 12))
        self.label_room.pack()
        self.room_number_entry = tk.Entry(root, font=("Helvetica", 12))
        self.room_number_entry.pack()

        # Reservation Button
        self.reserve_button = tk.Button(root, text="Reserve Room", command=self.reserve_room, bg="green", fg="white", font=("Helvetica", 12))
        self.reserve_button.pack(pady=10)

        # Display Database Button
        self.display_db_button = tk.Button(root, text="Display Database", command=self.display_database, bg="blue", fg="white", font=("Helvetica", 12))
        self.display_db_button.pack(pady=10)

        # Reservation Status
        self.status_label = tk.Label(root, text="", font=("Helvetica", 16), bg="black", fg="white")
        self.status_label.pack()

    def reserve_room(self):
        customer_name = self.customer_name_entry.get()
        room_choice = self.room_number_entry.get()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            room_number = int(room_choice)
        except ValueError:
            self.display_reservation_status("Invalid room number. Please enter a valid room number.")
            return

        with self.reservation_lock:  # Use the lock to prevent concurrent room reservations
            if room_number not in self.available_rooms:
                self.display_reservation_status("Invalid room number. Please enter a valid room number.")
            elif customer_name in self.customer_rooms:
                self.display_reservation_status(f"{customer_name}, you have already booked a room.")
            elif room_number in self.customer_rooms.values():
                self.display_reservation_status(f"Room {room_number} is already booked.")
            else:
                self.customer_rooms[customer_name] = room_number
                self.available_rooms.remove(room_number)
                self.reservation_history.append((self.sno, customer_name, room_number, current_time))
                self.sno += 1
                self.display_reservation_status(f"Reserved room {room_number} for {customer_name}", "green")

    def display_reservation_status(self, message, color="red"):
        self.status_label.config(text=message, fg=color)

    def display_database(self):
        db_window = tk.Toplevel()
        db_window.title("Reservation Database")
        db_window.geometry("800x400")

        # Create Treeview
        tree = ttk.Treeview(db_window, columns=("S.no.", "Name", "Room no.", "Date and Time"), show="headings")
        tree.heading("#1", text="S.no.")
        tree.heading("#2", text="Name")
        tree.heading("#3", text="Room no.")
        tree.heading("#4", text="Date and Time")

        # Insert Data into Treeview
        for record in self.reservation_history:
            tree.insert("", "end", values=record)

        tree.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelReservationSystem(root)
    root.mainloop()

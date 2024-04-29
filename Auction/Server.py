# Server GUI Window

# Imports: Libraries & Modules
import os
import tkinter as tk
import threading
import time as t
from PIL import Image, ImageTk
from tkinter import messagebox
from python_banyan.banyan_base import BanyanBase

# Window Width and Height
WINDOW_WIDTH = 383
WINDOW_HEIGHT = 450

# Define: EchoServer Class that inherits from BanyanBase
class EchoServer(BanyanBase):
    def __init__(self):
        # Initialize: BanyanBase
        super(EchoServer, self).__init__(process_name='Server')

        # Set: Subscriber Topic (Receiving messages)
        self.set_subscriber_topic('echo')

        # Initialize: Time & Bids Attributes
        self.time = 0
        self.bids = {}

        # Callback Function: Starting (Countdown)
        def start():
            # Get: Time Entered by the user
            self.time = int(self.main_entry.get())
            if self.time > 0:
                # Disable: Entry & Start buttons, enable the close button
                self.main_entry.configure(state=tk.DISABLED)
                self.main_button_start.configure(state=tk.DISABLED)
                self.main_button_close.configure(state=tk.NORMAL)
                # Start: Separate Thread (Countdown)
                threading.Thread(target=self.countdown).start()
            else:
                # Show: Error Message (Incorrect Time)
                messagebox.showerror('Error','Incorrect Time!')


        # Callback Function: Closing the countdown
        def close():
            # Set: Time to 1 and disable the close button
            self.time = 1
            self.main_button_close.configure(state=tk.DISABLED)


        # Create: Main Server Window
        self.main = tk.Tk()
        self.main.title("Auction Server")
        self.main.resizable(False, False)
        self.main.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.main.configure(bg="#1e1f22")


        # Bind the protocol method to handle window closing
        self.main.protocol("WM_DELETE_WINDOW", self.on_closing)


        # Load: Logo Image
        UI_logo = tk.PhotoImage(file="Gold.png")

        # Load: Background Image
        background_image = Image.open("Gold.png")
        background_image = background_image.convert("RGBA")
        
        # Convert: PIL Image to Tkinter PhotoImage
        background_photo = ImageTk.PhotoImage(background_image)


        # Label: Displaying Image in the Middle
        self.image_label = tk.Label(self.main, image=background_photo, bg="#1e1f22")
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")


        # Set: Logo Image for the Main Window
        self.main.iconphoto(True, UI_logo)



        # Label: Displaying "Distributed Auction"
        font_style = ('Arial', 12, 'bold italic')
        self.label_bottom = tk.Label(self.main, text="Distributed Auction", font=font_style, fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.label_bottom.grid(row=7, columnspan=4, pady=10)


        # Text Widget: Displaying Server Messages
        self.main_textbox = tk.Text(self.main, width=50, height=20, state=tk.DISABLED, font=('Arial', 10), fg='white' ,bg="#000000", bd=3, relief=tk.GROOVE)
        self.main_textbox.grid(row=0, column=0, padx=10, pady=10, columnspan=4)


        # Label: Entry for entering the countdown time
        self.main_label = tk.Label(self.main, text="Countdown (Seconds):", fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.main_label.grid(row=1, column=0, padx=0, pady=10)
        self.main_entry = tk.Entry(self.main, width=10, bd=3, relief=tk.GROOVE, justify='center')
        self.main_entry.grid(row=1, column=1, padx=10, pady=10)

        # Button: Starting the countdown
        self.main_button_start = tk.Button(self.main, text="Start", command=start, width=5, fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.main_button_start.grid(row=1, column=2, pady=10)

        # Button: Closing the countdown
        self.main_button_close = tk.Button(self.main, text="End", command=close, width=5, state=tk.DISABLED, fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.main_button_close.grid(row=1, column=3, padx=10, pady=10)

        # Start: Separate thread for receiving messages from clients
        threading.Thread(target=self.receive_loop).start()

        # Start: Tkinter main loop for the server window
        self.main.mainloop()



    # Method: Countdown Functionality
    def countdown(self):
        while True:
            # Publish: Current time to clients
            self.publish_payload({'time': self.time}, 'reply')
            if self.time == 0:
                # Enable: Entry & Start buttons, disable close button
                self.main_entry.configure(state=tk.NORMAL)
                self.main_button_start.configure(state=tk.NORMAL)
                self.main_button_close.configure(state=tk.DISABLED)

                # Enable: Text Box for displaying winners
                self.main_textbox.configure(state=tk.NORMAL)
                self.main_textbox.insert(tk.END, f"\n-----------------------------LIST OF WINNERS-----------------------------\n")
                self.main_textbox.configure(state=tk.DISABLED)

                # Iterate: Through Bids & Determine Winners
                for item_name, bid_data in self.bids.items():
                    self.bid_list = bid_data['bids']
                    self.bidder_list = bid_data['bidders']

                    self.highest_bid_index = self.bid_list.index(max(self.bid_list))
                    self.highest_bid = self.bid_list[self.highest_bid_index]
                    self.highest_bidder_name = self.bidder_list[self.highest_bid_index]

                    self.item_name = item_name

                    # Publish: Winner Information to clients
                    self.publish_payload({'item_name': self.item_name, 'highest_bid': self.highest_bid,
                                          'highest_bidder': self.highest_bidder_name}, 'reply')
                    
                    # Display: Winner Information in the text box
                    self.main_textbox.configure(state=tk.NORMAL)
                    self.main_textbox.insert(tk.END, f"WINNER is: {self.highest_bidder_name}, Item: {self.item_name}, with the highest bid of {self.highest_bid}!\n")
                    self.main_textbox.configure(state=tk.DISABLED)

                break

            # Sleep: One second (Decrement the time)
            t.sleep(1)
            self.time -= 1




    # Method: Processing Incoming Messages from clients
    def incoming_message_processing(self, topic, payload):

        if 'client_name' in payload:

            # Display: Message when a client is ready
            self.main_textbox.configure(state=tk.NORMAL)
            self.main_textbox.insert(tk.END, f"{payload['client_name']} is ready...\n")
            self.main_textbox.configure(state=tk.DISABLED)



        if 'sell_item_name' in payload and 'sell_item_price' in payload and 'seller_name' in payload:

            # Display: Message when an item is put up for sale
            self.main_textbox.configure(state=tk.NORMAL)
            self.main_textbox.insert(tk.END, f"Selling: {payload['sell_item_name']}, Php{payload['sell_item_price']}, seller: {payload['seller_name']}\n")
            self.main_textbox.configure(state=tk.DISABLED)

            # Publish: Sell Request to clients
            self.publish_payload({'sell_item_name': payload['sell_item_name'], 'sell_item_price': payload['sell_item_price'],
                                  'seller_name': payload['seller_name']}, 'reply')



        if 'bid_item_name' in payload and 'bid_price' in payload and 'bidder_name' in payload:

            # Display: Message when a bid is made
            self.main_textbox.configure(state=tk.NORMAL)
            self.main_textbox.insert(tk.END, f"Bidding: {payload['bid_item_name']}, Php{payload['bid_price']}, bidder: {payload['bidder_name']}\n")
            self.main_textbox.configure(state=tk.DISABLED)


            # Publish: Bid Request to clients
            self.publish_payload({'bid_item_name': payload['bid_item_name'], 'bid_price': payload['bid_price'],
                                  'bidder_name': payload['bidder_name']}, 'reply')

            # Update: Bids Dictionary with the bid information
            if payload['bid_item_name'] not in self.bids:
                self.bids[payload['bid_item_name']] = {'bids': [payload['bid_price']], 'bidders': [payload['bidder_name']]}
            else:
                self.bids[payload['bid_item_name']]['bids'].append(payload['bid_price'])
                self.bids[payload['bid_item_name']]['bidders'].append(payload['bidder_name'])


    def on_closing(self):
        # Handle window closing
        self.main.destroy()
        os._exit(0)

# Function: Running (Server)
def echo_server():
    EchoServer()

# Run: Server (if the script is executed directly)
if __name__ == '__main__':
    echo_server()

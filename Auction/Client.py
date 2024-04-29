# Client GUI Window

# Imports: Libraries & Modules
import os
import argparse
import signal
import tkinter as tk
from PIL import Image, ImageTk
import threading
from tkinter import messagebox
from python_banyan.banyan_base import BanyanBase

# Constants: Window Width and Height
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 660

# Define: EchoCmdClient Class that inherits from BanyanBase
class EchoCmdClient(BanyanBase):
   
    def __init__(self, **kwargs):

        # Initialize: BanyanBase (Specified Parameters)
        super(EchoCmdClient, self).__init__(
            back_plane_ip_address=kwargs['back_plane_ip_address'],
            subscriber_port=kwargs['subscriber_port'],
            publisher_port=kwargs['publisher_port'],
            process_name=kwargs['process_name'],
            loop_time=kwargs['loop_time']
        )

        # Set: Subscriber Topic (Receiving Messages)
        self.set_subscriber_topic('reply')

        # Initialize: client_name
        self.client_name = ''

        # Callback Function: Accepting User's Name
        def accept_name():
            # Get: Client's Name from the entry field
            self.client_name = self.main_entry.get()
            if self.client_name != '':
                # Publish: Client's Name to the server & close the name entry window
                self.publish_payload({'client_name': self.client_name}, 'echo')
                self.main.destroy()
                # Open: Main Client Window
                self.client_window()
            else:
                # Show an error message for an invalid name
                messagebox.showerror("Error", "Invalid Name!")


        # Create: Main Window (Entry: Client's Name)
        self.main = tk.Tk()
        self.main.title("ENTER YOUR NAME")
        self.main.geometry("300x150")
        self.main.resizable(False, False)
        self.main.configure(bg="#1e1f22")


        # Bind the protocol method to handle window closing
        self.main.protocol("WM_DELETE_WINDOW", self.on_closingmain)

        # Load: Logo Image
        UI_logo = tk.PhotoImage(file="Gold.png")

        # Load: Background Image
        background_image = Image.open("Gold.png")
        background_image = background_image.convert("RGBA")
        
        # Create: Transparent Image with 80% Opacity
        transparent_image = Image.new("RGBA", background_image.size, (0, 0, 0, 0))
        background_image = Image.blend(transparent_image, background_image, 0.8)

        # Convert: PIL Image to Tkinter PhotoImage
        background_photo = ImageTk.PhotoImage(background_image)

        # Label: Displaying Image in the Middle
        self.image_label = tk.Label(self.main, image=background_photo, bg="#1e1f22")
        self.image_label.place(relx=0, rely=2, anchor="center")

        # Set: Logo Image for the Main Window
        self.main.iconphoto(True, UI_logo)

        # Label: Displaying "Distributed Auction" at the bottom (bold and italic)
        font_style = ('Arial', 12, ' bold italic')
        self.label_bottom = tk.Label(self.main, text="DISTRIBUTED AUCTION APP", font=font_style, fg='white' ,bg="#1e1f22")
        self.label_bottom.grid(row=0, column=0, pady=10)

        # Entry Field: Client's Name
        self.main_entry = tk.Entry(self.main, width=46, justify='center')
        self.main_entry.grid(row=7, column=0, padx=10, pady=10)

        # Button: Login Client
        self.main_button = tk.Button(self.main, text="Login", command=accept_name, width=5, fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.main_button.grid(pady=10)
        
        # Start: Separate Thread (Receive Messages: Server)
        threading.Thread(target=self.receive_loop).start()

        # Start: Tkinter Main Loop
        self.main.mainloop()


    # Method: Creating the Main Client Window
    def client_window(self):
        # Create: Main Client Window
        self.client = tk.Tk()
        self.client.title(f"{self.client_name} - Client")
        self.client.resizable(False, False)
        self.client.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.client.configure(bg="#2b2d31")

        # Bind the protocol method to handle window closing
        self.client.protocol("WM_DELETE_WINDOW", self.on_closingclient)
        
        # Initialize: client_bid_items (attribute)
        self.client_bid_items = []

        # Text Widget: Time left
        self.client_text_time = tk.Text(self.client, width=0, height=0, state=tk.DISABLED, fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)

        # Label: Displaying the time left
        self.client_label_time = tk.Label(self.client, text="TIME LEFT", fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.client_label_time.grid(row=0, columnspan=4, padx=5, pady=10)

        # Label: Displaying items available for bidding
        self.client_label_bidding = tk.Label(self.client, text="Item/s Available for Bidding:", fg='white' ,bg="#1e1f22")
        self.client_label_bidding.grid(row=1, columnspan=1)

        # Button: Initiating the bidding process
        self.client_button_bid = tk.Button(self.client, text="Bid", command=self.bid_window, width=7, state=tk.DISABLED, fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.client_button_bid.grid(row=1, column=1)

        # Listbox: Displaying items available for bidding
        self.client_listbox_bidding = tk.Listbox(self.client, width=45, height=10, fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.client_listbox_bidding.grid(row=2, columnspan=4, padx=10, pady=10)

        # Label: Displaying items the client is selling
        self.client_label_selling = tk.Label(self.client, text="Item/s you are Selling:", fg='white' ,bg="#1e1f22")
        self.client_label_selling.grid(row=3, columnspan=1)

        # Button: Initiating the selling process
        self.client_button_sell = tk.Button(self.client, text="Sell", command=self.sell_window, width=7, state=tk.DISABLED, fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.client_button_sell.grid(row=3, column=1)

        # Listbox: Displaying items the client is selling
        self.client_listbox_selling = tk.Listbox(self.client, width=45, height=10, fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.client_listbox_selling.grid(row=4, columnspan=4, padx=10, pady=10)

        # Label: Displaying highest bidders
        self.client_label_highest = tk.Label(self.client, text="List of Bidders:", fg='white' ,bg="#1e1f22")
        self.client_label_highest.grid(row=5, columnspan=4)

        # Text Widget: Displaying highest bidders
        self.client_textbox_bidders = tk.Text(self.client, width=39, height=9, state=tk.DISABLED, font=('Arial', 10), fg='white' ,bg="#1e1f22", bd=3, relief=tk.GROOVE)
        self.client_textbox_bidders.grid(row=6, columnspan=4, padx=10, pady=5)

        # Start: Tkinter Main Loop (Client Window)
        self.client.mainloop()



    # Method: Creating the bidding window
    def bid_window(self):
        # Create: bidding window
        self.bid = tk.Tk()
        self.bid.title("BIDDING...")
        self.bid.resizable(False, False)
        self.bid.configure(bg="#1e1f22")

        # Initialize: bidding-related (attributes)
        self.bidder_name = self.client_name
        self.bid_item_index = self.client_listbox_bidding.curselection()[0]
        self.bid_item_name = self.client_bid_items[self.bid_item_index][0]
        self.bid_item_price = self.client_bid_items[self.bid_item_index][1]
        self.bid_price = 0


        # Callback Function: Accepting the bid
        def accept_bid():

            # Get: Bid Price Entered by the client
            self.bid_price = float(self.bid_entry_price.get())
            if self.bid_item_price < self.bid_price:

                # Publish: Bid to the server & close the bidding window
                self.publish_payload({'bid_item_name': self.bid_item_name, 'bid_price': self.bid_price,
                                      'bidder_name': self.bidder_name}, 'echo')
                self.bid.destroy()
            else:

                # Show: Error Message for an invalid bid price
                messagebox.showerror('Error', 'BID price should be higher than the item price!')

        # Label: Displaying the item available for bidding
        self.bid_label_item = tk.Label(self.bid, text=f"{self.bid_item_name}:", fg='white' ,bg="#1e1f22")
        self.bid_label_item.grid(row=0, column=0, padx=10, pady=10)

        # Entry Field: Entering the bid price
        self.bid_entry_price = tk.Entry(self.bid, width=20, fg='white' ,bg="#000000")
        self.bid_entry_price.grid(row=0, column=1, pady=10)

        # Button: Accepting the bid
        self.bid_button_accept = tk.Button(self.bid, text='Accept', command=accept_bid, width=5, fg='white' ,bg="#1e1f22")
        self.bid_button_accept.grid(row=0, column=2, padx=10, pady=10)

        # Start: Tkinter Main Loop for the bidding window
        self.bid.mainloop()



    # Method: Creating the selling window
    def sell_window(self):
        # Create: Selling Window
        self.sell = tk.Tk()
        self.sell.title("SELLING...")
        self.sell.resizable(False, False)
        self.sell.configure(bg="#1e1f22")

        # Initialize: Selling-related (attributes)
        self.seller_name = self.client_name
        self.sell_item_name = ''
        self.sell_item_price = 0

        # Callback Function: Accepting the sell request
        def accept_sell():
            # Get: Item name & price entered by the client
            self.sell_item_name = self.sell_entry_item.get()
            self.sell_item_price = float(self.sell_entry_price.get())

            # Insert: Item into the listbox of items the client is selling
            self.client_listbox_selling.insert(tk.END, f"{self.sell_item_name} Php{self.sell_item_price}")

            # Publish: Sell request to the server
            self.publish_payload({'sell_item_name': self.sell_item_name, 'sell_item_price': self.sell_item_price,
                                  'seller_name': self.seller_name}, 'echo')

            # Close: Selling Window
            self.sell.destroy()



        # Label: Entering the item name
        self.sell_label_item = tk.Label(self.sell, text='Item:', fg='white' ,bg="#1e1f22")
        self.sell_label_item.grid(row=0, column=0, padx=10, pady=10)

        # Entry Field: Entering the item name
        self.sell_entry_item = tk.Entry(self.sell, width=10, fg='white' ,bg="#000000")
        self.sell_entry_item.grid(row=0, column=1)

        # Label: Entering the item price
        self.sell_label_price = tk.Label(self.sell, text='Price:', fg='white' ,bg="#1e1f22")
        self.sell_label_price.grid(row=0, column=2, padx=10, pady=10)

        # Entry Field: Entering the item price
        self.sell_entry_price = tk.Entry(self.sell, width=10, fg='white' ,bg="#000000")
        self.sell_entry_price.grid(row=0, column=3)

        # Button: Accepting the sell request
        self.sell_button_accept = tk.Button(self.sell, text='Sell', command=accept_sell, width=6, fg='white' ,bg="#1e1f22")
        self.sell_button_accept.grid(row=0, column=4, padx=10, pady=10)

        # Start: Tkinter Main loop for the selling window
        self.sell.mainloop()


    def on_closingmain(self):
        # Handle: Main Closing
        self.main.destroy()
        os._exit(0)

    def on_closingclient(self):
        # Handle: Client Closing
        self.client.destroy()
        os._exit(0)



    # Method: Processing incoming messages from the server
    def incoming_message_processing(self, topic, payload):
        if 'time' in payload:

            # Update: Time left in the main client window
            minutes, seconds = divmod(payload['time'], 60)
            time_format = f"Time Remaining: {minutes:02d}:{seconds:02d}"
            self.client_label_time.config(text=time_format)
            self.client_text_time.configure(state=tk.DISABLED)

            # Enable: Bidding and selling buttons based on the remaining time
            self.client_button_bid.configure(state=tk.NORMAL)
            self.client_button_sell.configure(state=tk.NORMAL)

            
            if payload['time'] == 0:
                # Disable: Bidding and selling buttons when time is up
                self.client_button_bid.configure(state=tk.DISABLED)
                self.client_button_sell.configure(state=tk.DISABLED)

                # Enable: The text box for displaying winners
                self.client_textbox_bidders.configure(state=tk.NORMAL)
                self.client_textbox_bidders.insert(tk.END, f"\n---------------------------WINNERS--------------------------\n")
                self.client_textbox_bidders.configure(state=tk.DISABLED)



        if 'sell_item_name' in payload and 'sell_item_price' in payload and 'seller_name' in payload:
            if payload['seller_name'] != self.client_name:
                
                # Insert: Items into the listbox of items AVAILABLE FOR BIDDING
                self.client_listbox_bidding.insert(tk.END, f"Item: {payload['sell_item_name']}, Php{payload['sell_item_price']}, by: {payload['seller_name']}")
                # Add: Items to the list of bid items
                self.client_bid_items.append([payload['sell_item_name'], payload['sell_item_price']])



        # Display: Bidding Information in the text box for highest bidders
        if 'bid_item_name' in payload and 'bid_price' in payload and 'bidder_name' in payload:

            self.client_textbox_bidders.configure(state=tk.NORMAL)
            self.client_textbox_bidders.insert(tk.END, f"Item: {payload['bid_item_name']} , Php{payload['bid_price']}, bidder: {payload['bidder_name']}\n")
            self.client_textbox_bidders.configure(state=tk.DISABLED)


        # Display: Winner Information in the text box for highest bidders
        if 'item_name' in payload and 'highest_bid' in payload and 'highest_bidder' in payload:

            self.client_textbox_bidders.configure(state=tk.NORMAL)
            self.client_textbox_bidders.insert(tk.END, f"WINNER is: {payload['highest_bidder']}, Item: {payload['item_name']}, with the highest bid of {payload['highest_bid']}!\n")
            self.client_textbox_bidders.configure(state=tk.DISABLED)



# Function: Running the Command-line client
def echo_cmdline_client():

    # Parse: Command-line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-m", dest="number_of_messages", default="10",
                        help="Number of messages to publish")
    parser.add_argument("-n", dest="process_name", default="EchoCmdClient",
                        help="Set process name in banner")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-s", dest="subscriber_port", default='43125',
                        help="Subscriber IP port")
    parser.add_argument("-t", dest="loop_time", default=".1",
                        help="Event Loop Timer in seconds")
    args = parser.parse_args()


    # Handle: Case where back_plane_ip_address is 'None'
    if args.back_plane_ip_address == 'None':
        args.back_plane_ip_address = None


    # Create: Dictionary of keyword options
    kw_options = {
        'back_plane_ip_address': args.back_plane_ip_address,
        'number_of_messages': int(args.number_of_messages),
        'publisher_port': args.publisher_port,
        'subscriber_port': args.subscriber_port,
        'process_name': args.process_name,
        'loop_time': float(args.loop_time)
    }

    # Create: Instance of EchoCmdClient with the specified options
    EchoCmdClient(**kw_options)

# Signal Handlers: Interrupt & Termination Signals
def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt

# Set Up: Signal Handlers for Interrupt & Termination Signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Run: Command-line Client (if the script is executed directly)
if __name__ == '__main__':
    echo_cmdline_client()
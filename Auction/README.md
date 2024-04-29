# Server.py

## Code Explanation:

### Imports:
- `os`: Provides interaction with the operating system.
- `tkinter`: Used for creating the GUI.
- `threading`: Enables concurrent execution of the server and countdown.
- `time`: Used for time-related operations.
- `PIL` (Python Imaging Library): Used for working with images.
- `python_banyan.banyan_base`: A custom module for messaging functionality.

### Constants:
- `WINDOW_WIDTH` and `WINDOW_HEIGHT`: Define the dimensions of the main window.
- `blue`: A color code used in the GUI.

### Class: `EchoServer(BanyanBase)`:
- **Initialization:**
  - Sets up BanyanBase with a process name and subscriber topic.
  - Initializes attributes for time and bids.
- **Callback Functions:**
  - `start`: Initiates a countdown when the "Start" button is pressed.
  - `close`: Closes the countdown when the "Close" button is pressed.
- **GUI Setup:**
  - Creates the main Tkinter window with various widgets for the auction server.
- **Countdown Functionality:**
  - Implements a countdown mechanism in a separate thread.
  - Publishes the current time to clients and determines winners when the countdown reaches zero.
- **Incoming Message Processing:**
  - Handles messages from clients related to readiness, selling items, and making bids.
  - Updates a dictionary (`self.bids`) with bid information.
- **Window Closing Handling:**
  - Implements the `on_closing` method to handle window closing.

### Function: `echo_server`:
- Calls the `EchoServer` class to run the server.

### Script Execution:
- If the script is executed directly (`__name__ == '__main__'`), it runs the `echo_server` function.

### Time Complexity:
- The time complexity of the server is dominated by the countdown mechanism, which runs in a separate thread. The countdown runs for a specified time, resulting in a time complexity of O(n), where n is the countdown time.

# Client.py

## Code Explanation:

### Imports:
- `os`: Provides interaction with the operating system.
- `argparse`: Parses command-line arguments.
- `signal`: Handles signals, particularly interrupt and termination signals.
- `tkinter`: Used for creating the GUI.
- `PIL` (Python Imaging Library): Used for working with images.
- `threading`: Enables concurrent execution of the client and the receive loop.
- `random`: Used for choosing a random color for the client GUI.
- `python_banyan.banyan_base`: A custom module for messaging functionality.

### Constants:
- `WINDOW_WIDTH` and `WINDOW_HEIGHT`: Define the dimensions of the client window.
- `blue`: A color code used in the GUI.
- `allowed_colors`: A list of allowed colors for the GUI.
- `random_color`: A randomly chosen color from the allowed colors.

### Class: `EchoCmdClient(BanyanBase)`:
- **Initialization:**
  - Sets up BanyanBase with specified parameters.
  - Sets the subscriber topic.
  - Initializes the client's name and other attributes.
- **Callback Function: `accept_name`:**
  - Accepts the client's name entered through the GUI entry field.
  - Publishes the client's name to the server and opens the main client window.
- **Methods:**
  - `client_window`: Creates the main client window with various widgets for bidding and selling.
  - `bid_window`: Creates the bidding window for placing bids on items.
  - `sell_window`: Creates the selling window for offering items for sale.
  - `on_closingmain` and `on_closingclient`: Handle window closing for the main and client windows.
  - `incoming_message_processing`: Processes incoming messages from the server, updating the GUI accordingly.

### Function: `echo_cmdline_client`:
- Parses command-line arguments using `argparse`.
- Sets up signal handlers for interrupt and termination signals.
- Creates an instance of `EchoCmdClient` with the specified options.

### Signal Handlers:
- `signal_handler`: Handles interrupt and termination signals, raising a `KeyboardInterrupt` exception.

### Script Execution:
- If the script is executed directly (`__name__ == '__main__'`), it runs the `echo_cmdline_client` function.

### Time Complexity:
- The time complexity of the client code is mainly determined by the GUI interactions and the receive loop. The GUI operations typically have a time complexity of O(1), and the receive loop's time complexity depends on the server's message processing, resulting in O(n), where n is the number of received messages.

# Client-Server Communication in a Local Wi-Fi Network

## Overview

This explanation outlines the process when a client, running on a different PC, connects to a server through the Banyan backplane and IP address within the same Wi-Fi network. The communication is facilitated by the Banyan backplane, acting as an intermediary for message exchange.

## Steps

### 1. Banyan Backplane Setup

- The Banyan backplane serves as the communication infrastructure for distributed systems.
- Both the client and server scripts use the Banyan backplane for messaging.

### 2. Server Initialization

- The `Server.py` script is executed on a machine within the Wi-Fi network.
- The server initializes the BanyanBase with a specified IP address, subscriber port, and publisher port.

### 3. Client Initialization

- The `Client.py` script is executed on another machine within the same Wi-Fi network.
- The client initializes the BanyanBase with the same Banyan backplane IP address, subscriber port, and publisher port used by the server.

### 4. Connection Establishment

- The client and server scripts use the Banyan backplane to establish a connection.
- The Banyan backplane facilitates message passing between different processes or machines connected to it.

### 5. Client Name Entry

- The client GUI prompts the user to enter their name.
- The client sends the entered name to the server through the Banyan backplane using a specific topic.

### 6. Server and Client Communication

- Once the client's name is received by the server, the server and client can exchange messages through the Banyan backplane.
- The server can broadcast information about items for sale, current bidding status, and the countdown time to all connected clients.

### 7. Bidding and Selling

- Clients can place bids on items or offer items for sale through the GUI.
- The server processes these actions and updates the auction status.

### 8. Countdown Timer

- The server manages a countdown timer for the auction.
- The remaining time is communicated to all clients through the Banyan backplane.

### 9. Winners Announcement

- When the countdown reaches zero, the server determines the winners and communicates the results to all connected clients.

### 10. Client GUI Updates

- The client GUI updates in real-time based on the messages received from the server.

### 11. Closing Connection

- Clients can close their GUI windows, and the server script can be terminated, closing the communication connection.

## Important Considerations

- Ensure that the firewall settings on both the server and client machines allow communication through the specified ports.
- Use the correct local IP addresses of the machines within the Wi-Fi network.
- The Banyan backplane acts as a mediator for communication, and the specified IP address should be reachable by all machines involved.

This setup assumes that both the server and client are within the same local network and can communicate with each other using their local IP addresses. If the machines are on different networks, additional configurations, such as port forwarding or VPNs, may be required for successful communication.

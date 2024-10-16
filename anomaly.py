import os
import keyboard
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# Create a folder for saving images if it doesn't exist
if not os.path.exists('detected-image'):
    os.makedirs('detected-image')

# Simulating anomaly detection function
def anomaly_dect():
    anomaly_count = 0
    anomalies = []
    x_data = []
    y_data = []

    # Initialize the live plot
    plt.ion()  # Interactive mode on for live updates
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Data Stream")
    anomaly_points, = ax.plot([], [], 'ro', label="Anomalies")  # Red circles for anomalies
    ax.set_xlim(0, 100)  # Start with an arbitrary x-axis range
    ax.set_ylim(-6, 6)   # Set y-axis limits for better visibility

    try:
        while True:
            # Simulate incoming data stream and anomaly detection
            incoming_data = {'id': random.randint(1, 100), 'data': [[random.uniform(-5, 5)]], 'current_time': time.strftime("%Y-%m-%d %H:%M:%S")}
            current_value = incoming_data['data'][0][0]
            x_data.append(len(x_data))  # Use the length of x_data as the x-axis (time simulation)
            y_data.append(current_value)

            # Update graph limits dynamically
            ax.set_xlim(0, max(len(x_data), 100))

            # Simple check to simulate anomaly detection
            if abs(current_value) > 2:
                anomaly_count += 1
                anomalies.append((len(x_data)-1, current_value))  # Store anomaly position (x, y)
                print(f"Anomaly Detected: {incoming_data}")

            else:
                print(f"Incoming: {incoming_data}")

            # Update plot data for the live graph
            line.set_data(x_data, y_data)

            # Update anomalies on the graph
            if anomalies:
                anomaly_x, anomaly_y = zip(*anomalies)  # Extract x and y values for anomalies
                anomaly_points.set_data(anomaly_x, anomaly_y)

            # Redraw the plot to show updated data
            ax.legend()
            plt.draw()
            plt.pause(0.05)  # Pause for a short time to allow the graph to update

            # Check if 'q' is pressed to exit the loop
            if keyboard.is_pressed('q'):
                print("Stopping the program...")
                break

            time.sleep(0.5)  # To slow down the loop for demo purposes

    except KeyboardInterrupt:
        print("Program interrupted")

    finally:
        # Output anomalies after stopping
        print(f"\nTotal number of anomalies detected: {anomaly_count}")
        print("Anomalies:", anomalies)

        # Plot and save the graph when the loop ends
        save_anomaly_graph(x_data, y_data, anomalies, anomaly_count)

        # Turn off interactive mode
        plt.ioff()

def save_anomaly_graph(x_data, y_data, anomalies, anomaly_count):
    plt.figure(figsize=(10, 6))

    # Plot the normal data
    plt.plot(x_data, y_data, label="Data Stream")

    # Highlight anomalies
    if anomalies:
        anomaly_x, anomaly_y = zip(*anomalies)  # Extract x and y values for anomalies
        plt.scatter(anomaly_x, anomaly_y, color='red', label="Anomalies", zorder=5)  # Mark anomalies

    # Add title, labels, and legend
    plt.title(f"Anomaly Detection ({anomaly_count} anomalies detected)")
    plt.xlabel("Time (arbitrary units)")
    plt.ylabel("Value")
    plt.legend()

    # Add current time to the graph title
    current_time_str = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    # Save the plot to the 'detected-image' folder with the current date and time
    image_filename = f"detected-image/anomaly_graph_{current_time_str}.png"
    plt.savefig(image_filename)
    plt.close()

    print(f"Graph saved as {image_filename}")

# Run the anomaly detection
anomaly_dect()

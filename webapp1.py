import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for role, dumper ID, and tyre data
if "role" not in st.session_state:
    st.session_state.role = None
if "dumper_id" not in st.session_state:
    st.session_state.dumper_id = None
if "dumper_data" not in st.session_state:
    st.session_state.dumper_data = {
        "Dumper-001": {
            "tyre_pressures": [0, 0, 0, 0],
            "tyre_temperatures": [0, 0, 0, 0],
            "speeds": [],
            "pressure_history": {
                "time": [],
                "Front Left": [],
                "Front Right": [],
                "Rear Left": [],
                "Rear Right": [],
            },
            "temperature_history": {
                "time": [],
                "Front Left": [],
                "Front Right": [],
                "Rear Left": [],
                "Rear Right": [],
            },
        },
        "Dumper-002": {
            "tyre_pressures": [0, 0, 0, 0],
            "tyre_temperatures": [0, 0, 0, 0],
            "speeds": [],
            "pressure_history": {
                "time": [],
                "Front Left": [],
                "Front Right": [],
                "Rear Left": [],
                "Rear Right": [],
            },
            "temperature_history": {
                "time": [],
                "Front Left": [],
                "Front Right": [],
                "Rear Left": [],
                "Rear Right": [],
            },
        },
        "Dumper-003": {
            "tyre_pressures": [0, 0, 0, 0],
            "tyre_temperatures": [0, 0, 0, 0],
            "speeds": [],
            "pressure_history": {
                "time": [],
                "Front Left": [],
                "Front Right": [],
                "Rear Left": [],
                "Rear Right": [],
            },
            "temperature_history": {
                "time": [],
                "Front Left": [],
                "Front Right": [],
                "Rear Left": [],
                "Rear Right": [],
            },
        },
    }

# Define roles
ROLES = [None, "Operator (Driver)", "Manager", "Admin"]

# Sample dumper IDs
DUMPER_IDS = ["Dumper-001", "Dumper-002", "Dumper-003"]

# Login function
def login():
    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.experimental_rerun()  # Refresh the app to show the dashboard

# Logout function
def logout():
    st.session_state.role = None
    st.session_state.dumper_id = None  # Clear dumper ID on logout
    st.experimental_rerun()  # Refresh the app to show the login page

# Function to update tyre pressures, temperatures, and speed for the selected dumper
def update_tyre_data(dumper_id):
    pressures = [random.uniform(30.0, 40.0) for _ in range(4)]  # Random pressures between 30 and 40 PSI
    temperatures = [random.uniform(70.0, 90.0) for _ in range(4)]  # Random temperatures between 70 and 90°F
    speed = random.uniform(10.0, 100.0)  # Random speed between 10 and 100 km/h
    st.session_state.dumper_data[dumper_id]["tyre_pressures"] = pressures
    st.session_state.dumper_data[dumper_id]["tyre_temperatures"] = temperatures
    st.session_state.dumper_data[dumper_id]["speeds"].append(speed)
    return pressures, temperatures, speed

# Limit the number of values to 20 in history
def limit_history(dumper_id):
    max_entries = 20
    pressure_history = st.session_state.dumper_data[dumper_id]["pressure_history"]
    temperature_history = st.session_state.dumper_data[dumper_id]["temperature_history"]
    speeds = st.session_state.dumper_data[dumper_id]["speeds"]
    
    for key in pressure_history.keys():
        if len(pressure_history[key]) > max_entries:
            pressure_history[key] = pressure_history[key][-max_entries:]
    for key in temperature_history.keys():
        if len(temperature_history[key]) > max_entries:
            temperature_history[key] = temperature_history[key][-max_entries:]
    if len(speeds) > max_entries:
        speeds[:] = speeds[-max_entries:]  # Limit speed history

# Display pressure and temperature value side by side
def display_data(pressure, temperature, tyre_position):
    # Pressure color coding
    pressure_color = "green" if pressure >= 30.0 else "red"
    pressure_status = "Optimum" if pressure >= 30.0 else "Low"
    
    # Temperature color coding
    temperature_color = "green" if temperature <= 80.0 else "red"
    temperature_status = "Normal" if temperature <= 80.0 else "High"
    
    # Display pressure and temperature side by side
    st.markdown(f"""
    <div style='display:flex; justify-content:space-between;'>
        <div style='color:{pressure_color};'>
            <strong>{tyre_position} Pressure:</strong> {pressure:.2f} PSI ({pressure_status})
        </div>
        <div style='color:{temperature_color};'>
            <strong>Temperature:</strong> {temperature:.2f} °F ({temperature_status})
        </div>
    </div>
    """, unsafe_allow_html=True)
    
def plot_graphs(dumper_id):
    pressure_history = st.session_state.dumper_data[dumper_id]["pressure_history"]
    temperature_history = st.session_state.dumper_data[dumper_id]["temperature_history"]
    speeds = st.session_state.dumper_data[dumper_id]["speeds"][-20:]  # Get the last 20 speeds

    # Limit history to last 20 entries for pressure and temperature
    time_data = pressure_history["time"][-20:]
    front_left_pressure = pressure_history["Front Left"][-20:]
    front_right_pressure = pressure_history["Front Right"][-20:]
    rear_left_pressure = pressure_history["Rear Left"][-20:]
    rear_right_pressure = pressure_history["Rear Right"][-20:]

    front_left_temperature = temperature_history["Front Left"][-20:]
    front_right_temperature = temperature_history["Front Right"][-20:]
    rear_left_temperature = temperature_history["Rear Left"][-20:]
    rear_right_temperature = temperature_history["Rear Right"][-20:]

    # Create a new figure for the graphs, arranged vertically
    fig, axs = plt.subplots(3, 1, figsize=(10, 18))  # 3 rows and 1 column

    # Pressure plot
    axs[0].plot(time_data, front_left_pressure, label='Front Left', marker='o')
    axs[0].plot(time_data, front_right_pressure, label='Front Right', marker='o')
    axs[0].plot(time_data, rear_left_pressure, label='Rear Left', marker='o')
    axs[0].plot(time_data, rear_right_pressure, label='Rear Right', marker='o')
    axs[0].set_title('Tyre Pressure Over Time', pad=20)  # Add padding to the title
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Pressure (PSI)')
    axs[0].legend()
    axs[0].grid()
    axs[0].tick_params(axis='x', rotation=45)  # Tilt x-axis labels by 45 degrees

    # Temperature plot
    axs[1].plot(time_data, front_left_temperature, label='Front Left', marker='o')
    axs[1].plot(time_data, front_right_temperature, label='Front Right', marker='o')
    axs[1].plot(time_data, rear_left_temperature, label='Rear Left', marker='o')
    axs[1].plot(time_data, rear_right_temperature, label='Rear Right', marker='o')
    axs[1].set_title('Tyre Temperature Over Time', pad=20)  # Add padding to the title
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Temperature (°F)')
    axs[1].legend()
    axs[1].grid()
    axs[1].tick_params(axis='x', rotation=45)  # Tilt x-axis labels by 45 degrees

    # Speed plot
    speed_time = pressure_history["time"][-len(speeds):]  # Get matching time data for speeds
    axs[2].plot(speed_time, speeds, label='Speed', marker='o', color='orange')
    axs[2].set_title('Speed Over Time', pad=20)  # Add padding to the title
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Speed (km/h)')
    axs[2].legend()
    axs[2].grid()
    axs[2].tick_params(axis='x', rotation=45)  # Tilt x-axis labels by 45 degrees

    # Adjust layout to leave space between plots and avoid collision
    plt.subplots_adjust(hspace=0.5)  # Increase space between plots

    # Optionally, use tight layout
    # fig.tight_layout()

    # Display the plots
    st.pyplot(fig)
# Initialize session state for tyre wear and maximum life in kilometers
if "tyre_wear" not in st.session_state:
    st.session_state.tyre_wear = {
        "Dumper-001": {"Front Left": 100.0, "Front Right": 100.0, "Rear Left": 100.0, "Rear Right": 100.0},  # 100% life remaining
        "Dumper-002": {"Front Left": 100.0, "Front Right": 100.0, "Rear Left": 100.0, "Rear Right": 100.0},
        "Dumper-003": {"Front Left": 100.0, "Front Right": 100.0, "Rear Left": 100.0, "Rear Right": 100.0},
    }

# Set maximum tyre life in kilometers (assumption: 50,000 km for each tyre)
MAX_TYRE_LIFE_KM = {
    "Front Left": 500,  # Example value
    "Front Right": 550, # Example value
    "Rear Left": 480,   # Example value
    "Rear Right": 510,  # Example value
}

OPTIMAL_TEMPERATURE_MIN = 20  # Minimum optimal temperature (in °C)
OPTIMAL_TEMPERATURE_MAX = 40  # Maximum optimal temperature (in °C)
OPTIMAL_PRESSURE_MIN = 30     # Minimum optimal pressure (in PSI)
OPTIMAL_PRESSURE_MAX = 35     # Maximum optimal pressure (in PSI)

def calculate_wear_multiplier(temperature, pressure):
    temperature_multiplier = 1.0
    pressure_multiplier = 1.0

    # Increase multiplier if temperature is outside the optimal range
    if temperature < OPTIMAL_TEMPERATURE_MIN:
        temperature_multiplier += (OPTIMAL_TEMPERATURE_MIN - temperature) * 0.05  # e.g., 5% extra wear for each °C below optimal
    elif temperature > OPTIMAL_TEMPERATURE_MAX:
        temperature_multiplier += (temperature - OPTIMAL_TEMPERATURE_MAX) * 0.05  # 5% extra wear for each °C above optimal

    # Increase multiplier if pressure is outside the optimal range
    if pressure < OPTIMAL_PRESSURE_MIN:
        pressure_multiplier += (OPTIMAL_PRESSURE_MIN - pressure) * 0.1  # e.g., 10% extra wear for each PSI below optimal
    elif pressure > OPTIMAL_PRESSURE_MAX:
        pressure_multiplier += (pressure - OPTIMAL_PRESSURE_MAX) * 0.1  # 10% extra wear for each PSI above optimal

    return temperature_multiplier * pressure_multiplier  # Combined multiplier
# Function to simulate wear and calculate remaining kilometers for each tyre
def update_wear_kilometers(dumper_id, pressures, temperatures, speed):
    wear_decrease_rate = 0.001  # Decrease wear score by 0.1% per km traveled
    distances_covered = {}  # Store remaining kilometers for each tyre

    for i, tyre_position in enumerate(["Front Left", "Front Right", "Rear Left", "Rear Right"]):
        current_wear = st.session_state.tyre_wear[dumper_id][tyre_position]

        # Calculate wear multiplier based on temperature and pressure
        wear_multiplier = calculate_wear_multiplier(temperatures[i], pressures[i])

        # Decrease wear based on speed (distance covered since the last update)
        distance_covered = speed * (5 / 3600)  # Convert speed (km/h) to distance covered in 5 seconds
        wear_decrease = distance_covered * wear_decrease_rate * wear_multiplier

        # Update wear score, ensuring it doesn't drop below 0%
        st.session_state.tyre_wear[dumper_id][tyre_position] = max(0, current_wear - wear_decrease)

        # Calculate remaining kilometers based on the wear and max life for that tyre
        remaining_life_percentage = st.session_state.tyre_wear[dumper_id][tyre_position]
        remaining_km = (remaining_life_percentage / 100) * MAX_TYRE_LIFE_KM[tyre_position]

        distances_covered[tyre_position] = remaining_km

    return distances_covered





# Initialize session state for extended life if it doesn't exist
if 'extended_life' not in st.session_state:
    st.session_state.extended_life = {
        "Front Left": 0,
        "Front Right": 0,
        "Rear Left": 0,
        "Rear Right": 0
    }

# Current user role
role = st.session_state.role

# Header
st.title("Tyre Maintenance Monitoring System")

# Role-based logic
if role is None:
    login()  # Show the login page if not logged in
else:
    if st.button("Log out"):
        logout()  # Logout button

    st.write(f"Logged in as: {role}")

    # Operator Dashboard
# Operator Dashboard


# Operator Dashboard
    # Driver Dashboard
    # Driver Dashboard
    if role == "Operator (Driver)":
     st.subheader("Driver Dashboard")

     selected_dumper = st.selectbox("Select Dumper ID", DUMPER_IDS)
     st.session_state.dumper_id = selected_dumper

     st.write(f"Selected Dumper ID: {st.session_state.dumper_id}")

     while True:
        pressures, temperatures, speed = update_tyre_data(st.session_state.dumper_id)

        current_time = time.strftime("%H:%M:%S")
        remaining_km_data = update_wear_kilometers(st.session_state.dumper_id, pressures, temperatures, speed)

        st.write("Real-time Tyre Data:")
        for i, position in enumerate(["Front Left", "Front Right", "Rear Left", "Rear Right"]):
            display_data(pressures[i], temperatures[i], position)
            st.write(f"Predicted Remaining Life for {position}: {remaining_km_data[position]:.2f} km")

        # Get the extended life inputs for suggestions
        extended_life = {
            "Front Left": st.session_state.extended_life.get("Front Left", 0),
            "Front Right": st.session_state.extended_life.get("Front Right", 0),
            "Rear Left": st.session_state.extended_life.get("Rear Left", 0),
            "Rear Right": st.session_state.extended_life.get("Rear Right", 0)
        }

        # Overall suggestions based on aggregated data
        def provide_overall_suggestions(pressures, temperatures, speed):
            pressure_issues = any(p < 30 for p in pressures)
            temperature_issues = any(t > 80 for t in temperatures)

            suggestions = []

            if pressure_issues:
                suggestions.append("Increase pressure in tires to at least 30 PSI.")
            else:
                suggestions.append("Tire pressures are optimal.")

            if temperature_issues:
                suggestions.append("Reduce speed to help maintain optimal tire temperature.")
            else:
                suggestions.append("Tire temperatures are within optimal range.")

            if speed > 50:
                suggestions.append("Reduce speed to 50 km/h for optimal tire life.")
            else:
                suggestions.append("Speed is optimal.")

            return suggestions

        overall_suggestions = provide_overall_suggestions(pressures, temperatures, speed)

        st.write("Overall Suggestions for the Driver:")
        for suggestion in overall_suggestions:
            st.write(f"- {suggestion}")

        st.write(f"Current Speed: {speed:.2f} km/h")

       

        # Refresh every 5 seconds
        time.sleep(5)  # Change this value for different update intervals
        st.experimental_rerun()



# Manager Dashboard
    elif role == "Manager":
     st.subheader("Manager Dashboard")

     selected_dumper = st.selectbox("Select Dumper ID", DUMPER_IDS)
     st.session_state.dumper_id = selected_dumper

     st.write(f"Selected Dumper ID: {st.session_state.dumper_id}")

    # Manual Input to Extend Predicted Life of Each Tyre
     st.write("Enter desired kilometers for each tyre to last (0 to not extend):")

    # Create input boxes for each tyre
     extended_life_front_left = st.number_input(
        "Front Left:",
        min_value=0,
        value=0,
        step=10
     )

     extended_life_front_right = st.number_input(
        "Front Right:",
        min_value=0,
        value=0,
        step=10
     )

     extended_life_rear_left = st.number_input(
        "Rear Left:",
        min_value=0,
        value=0,
        step=10
     )

     extended_life_rear_right = st.number_input(
        "Rear Right:",
        min_value=0,
        value=0,
        step=10
     )

    # Update Tyre Data in an infinite loop with automatic refreshing
     while True:
        pressures, temperatures, speed = update_tyre_data(st.session_state.dumper_id)

        current_time = time.strftime("%H:%M:%S")
        pressure_history = st.session_state.dumper_data[st.session_state.dumper_id]["pressure_history"]
        temperature_history = st.session_state.dumper_data[st.session_state.dumper_id]["temperature_history"]

        # Append the new data
        pressure_history["time"].append(current_time)
        pressure_history["Front Left"].append(pressures[0])
        pressure_history["Front Right"].append(pressures[1])
        pressure_history["Rear Left"].append(pressures[2])
        pressure_history["Rear Right"].append(pressures[3])

        temperature_history["time"].append(current_time)
        temperature_history["Front Left"].append(temperatures[0])
        temperature_history["Front Right"].append(temperatures[1])
        temperature_history["Rear Left"].append(temperatures[2])
        temperature_history["Rear Right"].append(temperatures[3])

        limit_history(st.session_state.dumper_id)

        remaining_km_data = update_wear_kilometers(st.session_state.dumper_id, pressures, temperatures, speed)

        st.write("Real-time Tyre Data:")
        for i, position in enumerate(["Front Left", "Front Right", "Rear Left", "Rear Right"]):
            display_data(pressures[i], temperatures[i], position)
            st.write(f"Predicted Remaining Life for {position}: {remaining_km_data[position]:.2f} km")

        # Display extended life for each tyre if greater than zero
        if extended_life_front_left > 0:
            st.write(f"Extended predicted life for Front Left tyre: {extended_life_front_left} km")
        if extended_life_front_right > 0:
            st.write(f"Extended predicted life for Front Right tyre: {extended_life_front_right} km")
        if extended_life_rear_left > 0:
            st.write(f"Extended predicted life for Rear Left tyre: {extended_life_rear_left} km")
        if extended_life_rear_right > 0:
            st.write(f"Extended predicted life for Rear Right tyre: {extended_life_rear_right} km")

        st.write(f"Current Speed: {speed:.2f} km/h")

        # Plot graphs for pressure and temperature
        plot_graphs(st.session_state.dumper_id)

        # Refresh every 5 seconds
        time.sleep(5)  # Change this value for different update intervals
        st.experimental_rerun()





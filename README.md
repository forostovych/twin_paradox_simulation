🚀 Installation and Setup Guide
This guide will walk you through setting up the environment and running the Twin Paradox Interactive Visualization.

1. Prerequisites
Before you begin, ensure you have Python 3.12 or higher installed on your system. You can download it from python.org.

2. Setting Up the Project
Open your terminal (or Command Prompt / PowerShell) and follow these steps:

A. Clone the Repository
First, download the source code to your local machine:

Bash

git clone https://github.com/forostovych/twin_paradox_simulation.git
cd twin_paradox_simulation
B. Create a Virtual Environment (Recommended)
It is best practice to use a virtual environment to keep dependencies isolated:

Bash

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
C. Install Dependencies
The simulation requires the pygame library. Install it using pip:

Bash

pip install pygame
3. Running the Simulation
Once the installation is complete, launch the application:

Bash

python main.py
🎮 Interface Features
🧪 Smart Speed Slider
The Speed (c) field is not just a text box—it's an interactive logarithmic slider.

Linear Scale (Left): Easily select common speeds (0.1c, 0.5c).

Logarithmic Scale (Right): Precision control for extreme relativistic speeds (e.g., 0.99999999c).

How to use: Simply click and drag your mouse inside the Speed box.

📏 Automatic Scaling
The simulation automatically adjusts the visual scale of the tracks based on the maximum distance entered. This ensures that whether you travel 4 light-years or 1,000, the journey always fits perfectly on your screen.

⏱️ High-Precision Timers
The app tracks time down to the minute, converting the theoretical math into a human-readable format: Years, Days, Hours, and Minutes.

📐 The Physics Behind It
This simulation is based on Einstein's Special Relativity. The primary calculation is the Lorentz Factor
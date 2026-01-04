# Twin Paradox Simulation (Pygame) 🚀

An interactive visualization of relativistic time dilation (the "Twin Paradox") built with Python using the Pygame library.

The program allows you to compare two spaceflight scenarios with different speeds and distances simultaneously, visually demonstrating the difference in time flow on Earth versus on the spaceship.

## 📋 Features
- **Dual Independent Simulations:** Run two scenarios side-by-side to compare relativistic effects.
- **Interactive Input:**
  - Speed ($c$): From 0.1 to 0.9999... (supports a **logarithmic slider** inside the input box for precise high-speed adjustment).
  - Distance (light-years).
- **Real-time Unit Conversion:** Automatically converts inputs to km/s, km/h, and millions of km.
- **Full Flight Cycle:** Visualization includes the outbound trip, the stay at the destination, and the return trip.
- **Auto-Scaling:** The view automatically adjusts the scale to fit the largest distance on the screen.
- **Detailed Timers:** Displays time in Years, Days, and Hours:Minutes.

## 🛠 Tech Stack
- Python 3.x
- Pygame

## 🚀 How to Run

1. **Clone the repository** (or download the source code):
   ```bash
   git clone https://github.com/forostovych/twin_paradox_simulation.git

Install dependencies:Make sure you have Python installed, then run:Bashpip install pygame
Run the simulation:Bashpython main.py
🎮 ControlsInput Fields: Click to type values manually, or click and drag the mouse inside the "Speed" box to use the slider.START: Begin the simulation.PAUSE: Pause the simulation.RESET: Reset parameters and return ships to the starting position.Duration (s): Global setting for the animation duration in real-world seconds (controls how fast the ships move across the screen).📚 PhysicsThe simulation uses the Lorentz factor ($\gamma$) to calculate time dilation:$$ \gamma = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}} $$Time on the spaceship ($t'$) is related to time on Earth ($t$) by the formula:$$ t' = \frac{t}{\gamma} $$
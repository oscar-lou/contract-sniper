# Contract Sniper 🎯

A 2D tactical sniper simulation built in Python using the Processing framework. This project emphasizes precision gameplay by requiring the player to calculate dynamic wind and distance trajectories to successfully eliminate moving V.I.P. targets while avoiding civilian casualties.

![Gameplay Demo](![contract-sniper-demo](https://github.com/user-attachments/assets/cfd22ef5-aaad-4f49-8005-e5cea45175eb)
) 

## ⚙️ Key Technical Features
* **Dynamic Physics Calculations:** Implemented real-time bullet trajectory offsets using randomized wind speed and distance variables.
* **Custom Hitbox Detection:** Engineered precise coordinate-based hitboxes for the V.I.P. target (headshots only) and civilian NPCs.
* **State Machine Architecture:** Managed complex game flow (Menus, Active Gameplay, Intermission, Game Over) using dynamic state variables.
* **Algorithmic Pathing:** Programmed multi-directional, boundary-restricted patrol routes for the moving targets.
* **Resource Management:** Built a functioning ammo tracking system with magazine capacity, reserves, and reload mechanics.

## 🛠️ Tech Stack
* **Language:** Python
* **Framework:** Processing (Python Mode)

## 🚀 How to Run Locally
1. Download and install the [Processing IDE](https://processing.org/download).
2. Install **Python Mode** via the PDE tool (Tools > Add Tool > Modes > Python).
3. Clone this repository to your local machine:
   `git clone https://github.com/oscar-lou/contract-sniper.git`
4. Open the `contract_sniper.pyde` file in Processing.
5. Click the **Run** (Play) button in the top left corner.

## 🎮 Controls
* **Left Mouse Button:** Fire weapon
* **Mouse Movement:** Aim Scope
* **R:** Reload

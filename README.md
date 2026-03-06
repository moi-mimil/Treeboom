<div align="center">
  <img src="https://raw.githubusercontent.com/moi-mimil/Treeboom/main/miku1-no-w.png" width="80" height="120" />
  <h1>TREEBOOM</h1>
  <p><i>A Pygame survival challenge against Anti-Milo and environmental decay.</i></p>
</div>

<hr />

<h2>📖 Project Overview</h2>
<p>
  <b>Treeboom</b> is an arcade-style survival game developed in Python using the <b>Pygame</b> library. 
  Players must navigate the screen, defend themselves from enemies, and monitor the environment's CO2 levels.
</p>

<h2>🎮 How to Play</h2>
<p>
  The goal is to survive as long as possible while keeping the world green. 
  If your CO2 levels rise too high, the background turns grey, signaling environmental collapse!
</p>

<ul>
  <li><b>Move:</b> Use <code>Z/Q/S/D</code> (AZERTY) or <code>W/A/S/D</code> (QWERTY) to move Miku.</li>
  <li><b>Aim & Shoot:</b> Move the mouse to aim your "Damazon" box and <b>Left Click</b> to throw.</li>
  <li><b>Reload:</b> You have a limit of <b>3 boxes</b> on screen at once.</li>
  <li><b>Objective:</b> Hit the <i>Anti-Milo</i> enemy to increase your score and avoid the water!</li>
</ul>

<h2>✨ Core Features</h2>
<table border="0">
  <tr>
    <td><b>Dynamic Environment</b></td>
    <td>The background changes colors (4 stages) based on your <code>co2_level</code>.</td>
  </tr>
  <tr>
    <td><b>Smart Enemy AI</b></td>
    <td>Enemies calculate the shortest vector to the player and get faster as your score increases.</td>
  </tr>
  <tr>
    <td><b>Persistent Settings</b></td>
    <td>Reads controls, audio (mute), and high scores directly from <code>controls.txt</code>.</td>
  </tr>
  <tr>
    <td><b>Visual Feedback</b></td>
    <td>Includes a custom 8-bit font (<i>04b_25__.ttf</i>) and directional sprites for projectiles.</td>
  </tr>
</table>

<h2>🛠️ Installation & Setup</h2>
<p>Ensure you have <b>Python 3</b> and <b>Pygame</b> installed on your system.</p>

<pre>
# Clone the repository
git clone https://github.com/moi-mimil/Treeboom.git

# Enter the directory
cd Treeboom

# Install dependencies
pip install pygame

# Run the game
python treeboom.py
</pre>

<p align="center">
  <i>Note: Make sure <b>controls.txt</b> and all <b>.png/.mp3</b> assets are in the same folder.</i>
</p>

<hr />

<h2>🗂️ File Structure</h2>
<ul>
  <li><code>treeboom.py</code>: The main game engine and logic.</li>
  <li><code>treeboom-menu.py</code>: The game entry point and settings menu.</li>
  <li><code>controls.txt</code>: Configuration file for volume, keys, and high scores.</li>
  <li><code>assets/</code>: Contains Miku, Trees, Anti-Milo, and Damazon sprites.</li>
</ul>

<hr />

<div align="center">
  <p>Developed by <a href="https://github.com/moi-mimil"><b>@moi-mimil</b></a></p>
  <p><small>Built for fun and environmental awareness.</small></p>
</div>
<div align="center">
  <img src="https://raw.githubusercontent.com/moi-mimil/Treeboom/main/miku1-no-w.png" width="80" height="120" />
  <h1>TREEBOOM</h1>
  <p><i>The world is too green. It's time to fix that.</i></p>
</div>

<hr />

<h2>📉 Mission Objective</h2>
<p>
  In <b>Treeboom</b>, your goal is simple: <b>Total Environmental Collapse</b>. 
  The world starts clean and vibrant, and it is your job to drive the CO2 levels up by systematically destroying every tree in sight.
</p>

<h2>🎮 Gameplay Mechanics</h2>
<p>
  You control Miku, armed with endless <b>Damazon</b> delivery boxes. Use them to strike down the nature that surrounds you.
</p>

<ul>
  <li><b>The Goal:</b> Aim and throw boxes at trees. Every tree hit increases the <code>co2_level</code>.</li>
  <li><b>The Evolution:</b> As CO2 rises (Stages 12, 22, and 32), the world transforms from a lush forest into a grey, industrial wasteland.</li>
  <li><b>The Obstacle:</b> <u>Anti-Milo</u>. He is the guardian of the grove. He will hunt you down to protect the trees. If he touches you, it's game over.</li>
  <li><b>The Hazard:</b> Don't fall into the water! Stay on the land to continue your mission.</li>
</ul>

<h2>🕹️ Controls</h2>
<table border="1" cellpadding="10">
  <tr>
    <td><b>Movement</b></td>
    <td><code>Z/Q/S/D</code> (AZERTY) or <code>W/A/S/D</code> (QWERTY)</td>
  </tr>
  <tr>
    <td><b>Attack</b></td>
    <td><b>Left Click</b> to launch a Damazon box at trees or Anti-Milo.</td>
  </tr>
  <tr>
    <td><b>Ammo</b></td>
    <td>You can have a maximum of <b>3 boxes</b> in flight at any time.</td>
  </tr>
</table>

<h2>🛠️ Technical Stack</h2>
<p>
  Built with <b>Python</b> and <b>Pygame</b>. The game features:
</p>
<ul>
  <li><b>Vector-based AI:</b> Anti-Milo uses normalized direction vectors to track your position.</li>
  <li><b>Dynamic Difficulty:</b> The higher your score (trees destroyed/enemies hit), the faster Anti-Milo becomes.</li>
  <li><b>Data Persistence:</b> High scores and mute settings are saved in <code>controls.txt</code>.</li>
</ul>

<hr />

<h2>🚀 Quick Start</h2>
<pre>
# Install Pygame
pip install pygame

# Launch the destruction
python treeboom.py
</pre>

<hr />

<hr />
<div align="center">
  <p><b>Join the industrial revolution.</b></p>
  <p>
    Developed by 
    <a href="https://github.com/moi-mimil">mimil</a>, 
    <a href="https://github.com/nyarch-us3r">nyarch-us3r</a>, and 
    <a href="https://github.com/oyachii">oyachii</a>
  </p>
</div>
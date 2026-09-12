# Synthetic engineering forecasting task

This small original fixture is not an official GMCM problem or a real contest rehearsal.
At the end of hour t, forecast cooling load at t+1 using only measurements available by t.
Give held-out MAE, compare against a baseline on the same held-out hours, and explain what
can and cannot be inferred about the effect of temperature on load. No intervention was performed.
Data units: hour (integer), temperature (°C), load (kW). Chronological train hours: 0–5;
test forecast origins: 6–10. The measured load at hour 11 is only an evaluation label at origin 10.
Run from the fixture root: `python3 src/forecast.py`. Outputs go to results/.

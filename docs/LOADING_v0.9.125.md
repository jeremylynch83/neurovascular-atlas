# Initial loading and visibility v0.9.125

Restores the original Loading component and percentage bar until the initial bone and arterial geometry is prepared and the initial scene framed. Progress reflects the proportion of required initial meshes installed and is capped at 99% until primary readiness. Veins and brain are excluded from this initial percentage. Their subsequent loading retains existing inline Layers indicators and pending-selection feedback.

Both the application visibility map and renderer fallback now initialise veins as off. Background arrivals retain this visibility. Users can enable them through Layers, selection or presets as before. Brain visibility remains off; bone remains translucent and arteries visible.

Production build and controlled browser checks pass. Tests hold the arterial file to observe partial progress, then hold veins/brain separately to verify the initial bar disappears before background completion. All vein and brain meshes remain hidden after background loading; enabling veins through Layers still works. All five anatomical models and DSA data are byte-identical to v0.9.124.

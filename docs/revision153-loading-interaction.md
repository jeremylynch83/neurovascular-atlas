# v0.9.153: loading during interaction

Skull-first progressive loading is retained. Background installation no longer waits for a drag to end or for the 180 ms camera-motion/damping quiet period.

Each existing bounded worker packet still waits until after a paint. While actively dragging, installation is paced with a 24 ms minimum gap between packets. Slow rendering can increase that gap to at most 64 ms; this does not require the user to stop interacting. Without an active drag and with normal rendering, there is no additional timing delay beyond the paint yield.

Camera movement tracking remains for its existing rendering purpose, but no longer blocks anatomy installation. Worker decoding, geometry, pack order, defaults and DSA gates are unchanged. A single large source mesh remains an indivisible packet, so smooth GPU uploads on every device are not guaranteed.

The actual scheduling method is checked with controlled animation frames during a sustained drag, continual camera movement, slow frames, normal idle frames and disposal. The production build and existing CPU loading/scene, catalogue/DSA and startup checks are rerun. Successful GPU rendering and real-device interaction performance remain unverified in this environment.

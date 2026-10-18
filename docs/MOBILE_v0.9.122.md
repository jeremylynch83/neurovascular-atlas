# Mobile layout v0.9.122

The mobile title uses two lines and aligns with a compact Layers control. Search, theme and information controls sit below. Below 260 px the search uses its own row. Expanded panels and search results follow the measured header height and stay within the viewport. The bottom toolbar wraps when necessary. Tree indentation is capped on mobile to preserve space for names and visibility controls. Desktop layout is retained; its panel is also labelled Layers.

Checked the actual React app at widths 200, 220, 240, 259, 260, 280, 320, 360, 380, 393, 480, 680, 681, 768, 980, 1024 and 1440 px, plus deep tree expansion and search results at 240 x 520. Production build passed. All five anatomy models, descriptions, graph and DSA data are unchanged from v0.9.121.

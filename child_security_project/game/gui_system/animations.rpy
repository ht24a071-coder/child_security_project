# Common ATL transforms for the Semantic UI

transform pulse_on_hover:
    on hover:
        linear 0.1 zoom 1.05
    on idle:
        linear 0.1 zoom 1.0

transform click_shake:
    on hover:
        linear 0.05 xoffset 2
        linear 0.05 xoffset -2
        linear 0.05 xoffset 0
    on idle:
        xoffset 0

transform fade_in_up:
    alpha 0.0 yoffset 20
    linear 0.5 alpha 1.0 yoffset 0

transform fade_in_scale:
    alpha 0.0 zoom 0.5
    linear 0.3 alpha 1.0 zoom 1.0

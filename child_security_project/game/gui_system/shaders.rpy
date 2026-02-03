init python:
    # 1. Register Shader
    # This shader acts as a mask. It takes the existing texture (e.g. a Solid) 
    # and makes the corners transparent.
    renpy.register_shader("semantic.rounded_rect", variables="""
        uniform float u_radius;
        uniform vec2 u_size;
        varying vec2 v_tex_coord;
        uniform sampler2D tex0;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_200="""
        vec2 pos = v_tex_coord * u_size;
        
        // Calculate signed distance to the box edge
        vec2 d = abs(pos - u_size * 0.5) - (u_size * 0.5 - u_radius);
        float dist = length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
        
        // Alpha calculation (antialiased)
        float alpha_mask = 1.0 - smoothstep(0.0, 1.5, dist - u_radius);
        
        // Apply mask to the original texture color
        vec4 color = texture2D(tex0, v_tex_coord);
        gl_FragColor = color * alpha_mask;
    """)

    # 2. Helper Function (replacing the CDD)
    # Returns a Transform that applies the shader to a Solid color.
    def RoundedRect(width, height, color="#FFF", radius=10):
        return Transform(
            Solid(color, xysize=(width, height)),
            mesh=True,
            shader="semantic.rounded_rect",
            u_radius=float(radius),
            u_size=(float(width), float(height))
        )

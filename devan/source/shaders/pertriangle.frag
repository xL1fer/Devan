/*
Visual Computing 2022/2023
--------------------------
Samuel Silva, Oct. 2022

Fragment shader for flat-shading. The "flat" qualifier tells the shader not to interpolate per-vertex data and use
just the provoking vertex data.

*/

#version 330

uniform sampler2D p3d_Texture0;

// Passed by vertex shader
flat in vec4 vColor;

in vec2 texcoord;

// Output to the screen
out vec4 p3d_Color;

void main()
{
    vec4 textureColor = texture(p3d_Texture0, texcoord);
    p3d_Color = (vColor * textureColor);

    return;
}
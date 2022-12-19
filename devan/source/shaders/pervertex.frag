/*
Visual Computing 2022/2023
--------------------------
João Leite, Luís Batista, Oct. 2022

Fragment shader implementing Gouraud shading.
Illumination is computed for each vertex.

*/

#version 330

uniform sampler2D p3d_Texture0;

// Passed by vertex shader
in vec4 vColor;

in vec2 texcoord;

// Output to the screen
out vec4 p3d_FragColor;

void main()
{
    vec4 textureColor = texture(p3d_Texture0, texcoord);
    p3d_FragColor = (vColor * textureColor);

    return;
}
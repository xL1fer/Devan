/*
Visual Computing 2022/2023
--------------------------
João Leite, Luís Batista, Oct. 2022

Vertex shader implementing Gouraud shading.
Illumination is computed for each vertex.

*/

#version 330

// The texture coordinates associated with the Nth texture.
in vec2 p3d_MultiTexCoord0;
in vec2 p3d_MultiTexCoord1;
in vec2 p3d_MultiTexCoord2;


// The position, normal vector and color of the currently processed vertex.
in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec3 p3d_Color;

// Camera Position passed by main.py
uniform vec3 cameraPosition;

// This is probably the most important uniform, transforming a model-space
// coordinate into a clip-space (ie. relative to the window) coordinate.  This
// is usually used in the vertex shader to transform p3d_Vertex and store the
// result in gl_Position.
uniform mat4 p3d_ModelViewProjectionMatrix;

// These are parts of the above matrix.
uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ViewProjectionMatrix;

// Ouputs to the fragment shader
out vec4 vColor;
out vec3 vNormal;
out vec3 fragPos;

out vec2 texcoord;

void main()
{
    fragPos = vec3(p3d_ModelMatrix *  p3d_Vertex);
    vNormal = mat3(transpose(inverse(p3d_ModelMatrix))) * p3d_Normal;

    gl_Position = p3d_ProjectionMatrix * p3d_ViewMatrix * vec4(fragPos, 1.0);

    texcoord = p3d_MultiTexCoord0;
}
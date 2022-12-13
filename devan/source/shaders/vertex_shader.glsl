#version 150

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;

uniform mat4 p3d_ModelMatrix;


out vec3 vNormal;
out vec3 fragPos;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

out vec3 p3d_Normal;
out vec4 p3d_Color;


// Output to fragment shader
out vec2 texcoord;

void main() {
  fragPos = vec3(p3d_ModelMatrix *  p3d_Vertex);
  vNormal = mat3(transpose(inverse(p3d_ModelMatrix))) * p3d_Normal;

  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  texcoord = p3d_MultiTexCoord0;
}
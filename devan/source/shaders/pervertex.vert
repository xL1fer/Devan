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

// New in 1.10.  Contains information for each non-ambient light.
// May also be used to access a light passed as a shader input.
uniform struct p3d_LightSourceParameters {
  // Primary light color.
  vec4 color;

  // Light color broken up into components, for compatibility with legacy
  // shaders.  These are now deprecated.
  vec4 ambient;
  vec4 diffuse;
  vec4 specular;

  // View-space position.  If w=0, this is a directional light, with the xyz
  // being -direction.
  vec4 position;

  // Spotlight-only settings
  vec3 spotDirection;
  float spotExponent;
  float spotCutoff;
  float spotCosCutoff;

  // Individual attenuation constants
  float constantAttenuation;
  float linearAttenuation;
  float quadraticAttenuation;

  // constant, linear, quadratic attenuation in one vector
  vec3 attenuation;

  // Shadow map for this light source
  sampler2DShadow shadowMap;

  // Transforms view-space coordinates to shadow map coordinates
  mat4 shadowViewMatrix;
} p3d_LightSource[1];

// Access the material attributes assigned via a Material object.
// Unused struct parameters may be omitted without consequence.
uniform struct {
  vec4 ambient;
  vec4 diffuse;
  vec4 emission;
  vec3 specular;
  float shininess;

  // These properties are new in 1.10.
  vec4 baseColor;
  float roughness;
  float metallic;
  float refractiveIndex;
} p3d_Material;

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

out vec2 texcoord;

void main()
{
    //gl_Position = p3d_ModelViewProjectionMatrix * vec4(p3d_Vertex, 1.0);
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;

    //vec3 pos = vec3(p3d_ModelMatrix * vec4(p3d_Vertex, 1.0));
    vec3 pos = vec3(p3d_ModelMatrix * p3d_Vertex);

    vNormal = normalize(mat3(transpose(inverse(p3d_ModelMatrix))) * p3d_Normal);  


    // ambient component
    float ambientStrength = 0.3;
    vec4 ambient = ambientStrength * p3d_Material.ambient * p3d_LightSource[0].color;


    vec3 lightDir;
    if (p3d_LightSource[0].position[3] == 0.0)    // directional light
        lightDir = normalize(p3d_LightSource[0].position.xyz);
    else
        lightDir = normalize(p3d_LightSource[0].position.xyz - pos);
    //vec3 lightDir = p3d_LightSource[0].position.xyz;

    // diffuse component

    float diff = max(dot(vNormal, lightDir), 0.0);

    vec4 diffuse = diff * p3d_Material.diffuse * p3d_LightSource[0].color;

    // specular
    float specularStrength = 0.5;
    vec3 viewDir = normalize(cameraPosition - pos);
    vec3 reflectDir = reflect(-lightDir, vNormal);
    float spec = pow(max(dot(-viewDir, reflectDir), 0.0), p3d_Material.shininess);
    vec4 specular = specularStrength * spec * vec4(p3d_Material.specular, 1.0) * p3d_LightSource[0].color;

	  vColor = max(diffuse + specular, ambient);

    texcoord = p3d_MultiTexCoord0;
}
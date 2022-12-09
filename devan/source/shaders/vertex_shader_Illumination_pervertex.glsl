/*
Visual Computing 2022/2023
--------------------------
Samuel Silva, Oct. 2022

Vertex shader implementing Gouraud shading. Illumination is computed for each vertex. Note how a different normal and position will be used, at each time, resulting in distinct illumination for each of the vertices.

*/

#version 330

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
layout (location = 2) in vec3 normal;

out vec4 vColor;
out vec3 vNormal;


uniform vec4 lightPosition;
uniform vec3 viewerPosition;

// Model view and projection matrices

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;


uniform vec4 lightColor;

// these are properties of the OBJECT
struct Material {
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
    float shininess;
};

uniform Material material;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);

    vec3 pos = vec3(model * vec4(position, 1.0));

    vNormal = normalize(mat3(transpose(inverse(model))) * normal);  


    // ambient component
    float ambientStrength = 0.2;
    vec4 ambient = ambientStrength * material.ambient * lightColor;



    vec3 lightDir;

    if (lightPosition[3] == 0.0)    // directional light
        lightDir = normalize(lightPosition.xyz);
    else
        lightDir = normalize(lightPosition.xyz - pos);

    // diffuse component

    float diff = max(dot(vNormal, lightDir), 0.0);

    vec4 diffuse = diff * material.diffuse * lightColor;

    // specular
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewerPosition - pos);
    vec3 reflectDir = reflect(-lightDir, vNormal);
    float spec = pow(max(dot(-viewDir, reflectDir), 0.0), material.shininess);
    vec4 specular = specularStrength * spec * material.specular * lightColor;

    // something needs to be done, here
    //vColor = vec4(0.0, 0.0, 1.0, 1.0);
	
	//vColor = material.ambient;
	//vColor += diffuse;
	//vColor += specular;
	vColor = max(diffuse + specular, ambient);
}
# Sharing Information Between Entities
This sample app takes the generic concept of the universe as a basis to describe the concept of sharing information between entities. 

The universe contains multiple star systems, which in turn contain multiple planets. In this sample app, each of these (hierarchy) layers is defined as an Entity Type.
To analyse and plot a planetary orbit within a star system, we will need to retrieve some information from a Planet entity.

## App structure

```
Universe: has a controller but no parametrization so has no editor
  └─ System: has a controller and a parametrization 
     ├── Analaysis: 
     │     ├── controller with a WebAndDataView: uses data from System and Planet
     │     ├── parametrisation with a SiblingOptionField:  retrieves info from Planet
     └── Planet:   
           ├── controller with no view
           └── Planet: has a controller and a parametrization            
```
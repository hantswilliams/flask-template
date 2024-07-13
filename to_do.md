# TO DO 

1. Instruciton for CHAT: Should think about updating the datatable so instead of always looking for the 'id' column, we might look for something else. currently the datatable is looking for the 'id' column, which we then also assume is the primary key for the lookup, but but we might want to change that to look for another column that is a primary key that is not 'id'.So would need to build out some logic where we automatically look for the primary key column, and then use that for the lookup, so it may be 'id' sometimes but it may be something else.

## DONE 

1. Update models so the base models being with Base_ and the models that are used in the app start with the app. this way can add in logic to places like the base template where we display the models and do not want to display the base models, but can still display the app models for the other things. this is because we do not want to display base models like users and permissions there, that should be in the admin section only.
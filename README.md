# Security Software
#Security API

ollowing the guide to implement a secure API architecture and the Flask prototype implemented during the class, do the following: 

  

1) Implement each one of the layers: Rate-Limiting, Authentication, Audit Log, and Access Control. Explore and investigate more advanced techniques or configurations for each layer to set new security levels.  

Check other methods like Slide Window, Token Bucket or Leaky Bucket for Rate-Limiting. 

For Authentication, implement a database user table with password encryption using algorithms or database encryption options.  

For Audit Logs, implement a database log table saving the necessary audit log attributes (user, method, time, etc.) Your API's operational and business logic must collect log audit records. Configure the different levels such as INFO, ERROR, WARNING, etc. 

Finally, implement the rule-based access control (RBAC) method for access control using a database structure (user, role, permission, etc.) or a library or plugin for Flask. Define roles that can do specific operations with your API and assign these roles to the users. 

2) Check your implemented code using a Static Application Security Testing (SAST) tool like Bandit. Capture and save the vulnerabilities list and implement the recommendations given by the report. You must show evidence that you follow the guidance.    

3) Configure and run your API under HTTPS protocol.  

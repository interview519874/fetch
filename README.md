# Fetch SRE Assignment
Here's my submission for the Fetch SRE Python take home assignment. 

# Installation
1. Ensure you have the latest version of [python](https://www.python.org/downloads/) installed
2. Download sample.py, main.py and place into a project folder

# Running Python Script
Navigate to the project folder and execute the python script via `python3 main.py sample.yaml`

![image](https://github.com/user-attachments/assets/d5548dfd-509d-47ad-bb12-1425f3207d93)

# Modifications to code
1. The method declaraion was modified to ensure that GET was the default method of one was not specified:
![image](https://github.com/user-attachments/assets/b934c0ff-acc2-46b1-a7fe-e931c38643a9)

2. check_health was modified to also check for latency and deny if it's greater than 500ms
![image](https://github.com/user-attachments/assets/0d01a833-c11a-4936-b529-e0a0d63917e0)

3. check_endpoint was modified to remove the port number before running a health check:
![image](https://github.com/user-attachments/assets/137d04c9-ef28-49fd-8ad7-58c60dfd0100)

4. Many modifications were done to allow multithreading of the health check process. This was necessary to meet the 15 second time requirement even if there's a large amount of end points.

5. Log result function was added to clean up the code:
   ![image](https://github.com/user-attachments/assets/10a896f0-9b64-4169-9e23-aab77585af31)

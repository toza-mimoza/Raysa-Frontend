## Node 1: Ubuntu Server 20.04 with Rasa 3.0.0 installed

Tested on an Ubuntu 20.04 Azure VM. 

Note: Architecture for Rasa must be either **amd64** or **i386** since the **Tensorflow** packages that Rasa has as dependencies are only guaranteed to work on these platforms. 

Functionality: 
- Required:
    - [ ] train in a distributed setting
        - [ ] Rasa Open Source code needs to be rewritten using Ray
    - [ ] receive and handle requests from the Flask web app
- Optional: 
    - [ ] report logs to the Flask front-end    
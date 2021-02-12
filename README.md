# kubquizz
This is a training small Quizz application aimed add avaluating students around their knowledge on docker, kubernetes.

The idea is to test student ability so create a small kubernetes client Quizz application,
then to load the kubernetes Quizz from the client application
... and to execute the Quizz.

The application is separated in two part:
- A **frontent Quizz** application (Flask+Python)
  - Ths student has to build the application container and to deploy the application
  - When the application run, the student launch the Quizz.
  - The Quizz questions are located on a server side deployed in the Cloud.
  
**IMPORTANT**: the student must configure the `user` entry in the `config.yml` file before starting the Quizz
  
- A **backend Quizz** application (Flask+Python) delivering Quizz and storing :
  - Each student Quizz answer
  - The student frontend Quizz environment deployment as we evaluate also the frontend deployment quality ... :-)
  
  Have fun and happy Quizzing !

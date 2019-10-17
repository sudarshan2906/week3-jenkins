pipeline {
    agent any
    stages {
         stage('Build') {
            steps {
                bat 'python helper.py'

            }
         }
          stage('Deploy') {
            steps {
                bat 'python api_gateway.py'

            }
         }
    }
    }

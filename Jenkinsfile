pipeline {
  environment {
    registry = "jodennis/jenkins-docker"
    registryCredential = 'dockerhub'
    dockerImage = ''
  }
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt'
        sh 'python ./jenkinsFlask.py &'
      }
    }

    stage('Test App') {
      steps {
        sh 'python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt && python ./jenkinsUnittest.py && deactivate'
      }
      post {
        always {
          junit 'test-reports/*.xml'
        }
      } 
    }
    
    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build(registry + ":$BUILD_NUMBER")
        }
      }
    }

    stage('Upload Image to Registry') {
      steps{
        script {
          docker.withRegistry('', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
    stage('run image locally'){
      steps{
        sh "docker kill jenkins-docker"
        sh "docker run -itd -p 5005:5005 --name jenkins-docker $registry:$BUILD_NUMBER"
      }
    }

    //stage('Remove Unused docker image') {
    //  steps{
    //    sh "docker rmi $registry:$BUILD_NUMBER"
    //  }
    //}
  }
}

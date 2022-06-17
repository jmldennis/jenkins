pipeline {
  environment {
    registry = "jodennis/jenkins-docker"
    registryCredential = 'dockerhub'
    dockerImage = ''
  }
  agent { 
    docker { 
      image 'python:3.10'
      args '-p 5005:5005'
        } 
  }
  stages {
    stage('Build') {
      steps {
        sh 'pip install -r requirements.txt'
        //sh 'apk add libstdc++'
        sh 'python3 ./jenkinsFlask.py'
      }
    }
    stage('Test App') {
      steps {
        echo "${env.NODE_NAME}"
        sh 'pwd'
        sh 'uname -a'
        sh 'python jenkinsUnittest.py'
      }
      post {
        always {
          junit 'test-reports/*.xml'
        }
      } 
    }
    // Uncomment for SAST lab step 
    // Commented section starts
    /*
    stage('SAS Test') {
      steps {
        snykSecurity(
          snykInstallation: 'SnykV2Plugin',
          snykTokenId: 'snyktoken',
          severity: 'medium',
          failOnIssues: true)
      }
    }
    */
    // Commented section ends 
    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
        }
      }
    }
    stage('Upload Image to Registry') {
      steps{
        script {
          docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
    stage('Remove Unused docker image') {
      steps{
        sh "docker rmi $registry:$BUILD_NUMBER"
      }
    }
    // Uncomment for K8s app diployment step
    // Commented section starts
    
    stage('Deploy Application') {
      agent {
        kubernetes {
            cloud 'kubernetes'
          }
        }
        steps {
          container('kubectl') {
            sh """cat <<EOF | kubectl apply --validate=false -f -
apiVersion: v1
kind: Namespace
metadata:
  name: jenkinsFlask
---
apiVersion: v1
kind: Service
metadata:
  name: jenkinsFlask-Service
  namespace: jenkinsFlask
spec:
  selector:
    app: jenkinsFlask
  ports:
    - protocol: TCP
      port: 5005
      targetPort: 5005
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkinsFlask-deployment
  namespace: jenkinsFlask
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jenkinsFlask
  template:
    metadata:
      labels:
        app: jenkinsFlask
    spec:
      containers:
      - name: jenkinsFlask
        image: $registry:$BUILD_NUMBER
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
EOF"""
        }
      }
    }
  
  // Commented section ends
  }
}

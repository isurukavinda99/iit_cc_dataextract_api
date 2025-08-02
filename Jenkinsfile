pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS_ID = 'dockerhub'
        DOCKER_HUB_REPO = 'isurukavinda99/dataextract_api'
        K8S_DEPLOY_FILE = 'dataextract-api-deployment.yaml'
        K8S_SERVICE_FILE = 'dataextract-service.yaml'
        K8S_SECRET_FILE = 'dataextract-api-secret.yaml'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo '=== Building Docker Image ==='
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Install kubectl') {
            steps {
                sh '''
                    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    mkdir -p $HOME/bin
                    mv kubectl $HOME/bin/kubectl
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        export PATH=$HOME/bin:$PATH
                        kubectl apply -f ${K8S_SECRET_FILE} --validate=false
                        kubectl apply -f ${K8S_DEPLOY_FILE} --validate=false
                        kubectl apply -f ${K8S_SERVICE_FILE} --validate=false
                        kubectl apply -f dataextract-api-hpa.yaml --validate=false
                        kubectl rollout restart deployment/dataextract-api-deployment
                        kubectl rollout status deployment/dataextract-api-deployment
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Dataextract API deployed successfully!'
        }
        failure {
            echo '❌ Deployment failed. Please check logs.'
        }
    }
}

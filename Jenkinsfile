pipeline {
    agent any  // ← Change this from docker agent

    environment {
        DOCKER_HUB_REPO = 'chhak322025git/flask-devops-app'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo '🐳 Building Docker image...'
                    sh """
                        docker build -t ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG} .
                        docker tag ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG} ${DOCKER_HUB_REPO}:latest
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo '📤 Pushing to Docker Hub...'
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG}
                            docker push ${DOCKER_HUB_REPO}:latest
                            docker logout
                        '''
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    echo '🧹 Cleaning up...'
                    sh """
                        docker rmi ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG} || true
                        docker rmi ${DOCKER_HUB_REPO}:latest || true
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}

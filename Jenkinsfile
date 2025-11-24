pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'
        }
    }

    environment {
        DOCKER_HUB_REPO = 'chhak322025git/flask-devops-app'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo '📦 Installing Python dependencies...'
                    sh '''
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo '🧪 Running tests...'
                    sh '''
                        pip install pytest pytest-flask
                        pytest tests/ -v --tb=short
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            agent any  // Switch back to host for Docker commands
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
            agent any
            steps {
                script {
                    echo '📤 Pushing to Docker Hub...'
                    withCredentials([usernamePassword(
                        credentialsId: DOCKER_CREDENTIALS_ID,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker push ${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG}
                            docker push ${DOCKER_HUB_REPO}:latest
                            docker logout
                        '''
                    }
                }
            }
        }

        stage('Clean Up') {
            agent any
            steps {
                script {
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

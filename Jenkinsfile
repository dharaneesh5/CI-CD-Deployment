pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "dharaneesh5"
        FRONTEND_IMAGE = "${DOCKERHUB_USER}/organ-frontend"
        BACKEND_IMAGE  = "${DOCKERHUB_USER}/organ-backend"
        TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh """
                    docker build -t ${FRONTEND_IMAGE}:${TAG} ./frontend
                    docker build -t ${BACKEND_IMAGE}:${TAG} ./backend
                """
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh 'echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin'
                }
            }
        }

        stage('Push Images') {
            steps {
                sh """
                    docker push ${FRONTEND_IMAGE}:${TAG}
                    docker push ${BACKEND_IMAGE}:${TAG}

                    docker tag ${FRONTEND_IMAGE}:${TAG} ${FRONTEND_IMAGE}:latest
                    docker tag ${BACKEND_IMAGE}:${TAG} ${BACKEND_IMAGE}:latest

                    docker push ${FRONTEND_IMAGE}:latest
                    docker push ${BACKEND_IMAGE}:latest
                """
            }
        }
        stage('Pull Latest Images') {
    steps {
        sh """
            docker pull ${FRONTEND_IMAGE}:latest
            docker pull ${BACKEND_IMAGE}:latest
        """
    }
}

        stage('Stop Old Containers') {
            steps {
                sh """
                    docker rm -f organ_frontend || true
                    docker rm -f organ_backend || true
                    docker rm -f organ-prometheus || true
                    docker rm -f organ-grafana || true
                    docker rm -f organ_db || true
                """
            }
        }

        stage('Run Application and Monitoring') {
            steps {
                sh """
                    docker compose up -d
                """
            }
        }

        stage('Verify Running Containers') {
            steps {
                sh """
                    docker ps
                """
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
    }
}

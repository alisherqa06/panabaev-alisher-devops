pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
    }

    environment {
        STUDENT_NAME = 'Alisher'
        STUDENT_SURNAME = 'Panabaev'
        STUDENT_GROUP = 'It2-2308'
        STUDENT_ID = '37332'
        DOCKER_IMAGE = 'panabaev-alisher-devops'
        DOCKER_CONTAINER = 'panabaev-alisher-container'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Student: $STUDENT_NAME $STUDENT_SURNAME | Group: $STUDENT_GROUP | ID: $STUDENT_ID"'
                sh 'echo "Source commit: $(git rev-parse HEAD)"'
            }
        }

        stage('Build') {
            steps {
                sh 'python3 -m py_compile app/server.py scripts/check_http.py'
                sh 'echo "Application source compiled successfully."'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m unittest discover -s tests -v'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t "$DOCKER_IMAGE" .'
            }
        }

        stage('Docker Run') {
            steps {
                sh '''
                    docker rm -f "$DOCKER_CONTAINER" >/dev/null 2>&1 || true
                    docker run -d --name "$DOCKER_CONTAINER" \
                        --publish 8080:8080 \
                        --env STUDENT_NAME="$STUDENT_NAME" \
                        --env STUDENT_SURNAME="$STUDENT_SURNAME" \
                        --env STUDENT_GROUP="$STUDENT_GROUP" \
                        --env STUDENT_ID="$STUDENT_ID" \
                        "$DOCKER_IMAGE"
                    python3 scripts/check_http.py http://127.0.0.1:8080
                    docker ps --filter "name=^/${DOCKER_CONTAINER}$"
                    docker logs "$DOCKER_CONTAINER"
                '''
            }
        }
    }
}

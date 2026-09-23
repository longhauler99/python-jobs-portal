pipeline {
    agent { label 'local-docker' }

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    stages {
        stage('Verify tools') {
            steps {
                sh '''
                    git --version
                    docker version
                    docker compose version
                '''
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t jobs-portal:ci-${BUILD_NUMBER} .'
            }
        }
    }
}

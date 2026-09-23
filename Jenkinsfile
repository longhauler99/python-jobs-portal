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

            // Confirms Git and Compose are installed and Docker is reachable.
            // A failed command stops the pipeline before building the image.
        }

        stage('Build image') {
            steps {
                sh 'docker build -t jobs-portal:ci-${BUILD_NUMBER} .'
            }

            // Builds the checked-out application using its Dockerfile.
            // Tags the image with this Jenkins build number, e.g. jobs-portal:ci-12.
            // The image stays on the agent's Docker host; it is not deployed yet.
        }

        stage('Test') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }

            steps {
                sh '''
                    export TEST_IMAGE="jobs-portal:ci-${BUILD_NUMBER}"

                    docker compose \
                      -p "jobs-portal-tests-${BUILD_NUMBER}" \
                      -f compose.test.yaml \
                      up --abort-on-container-exit --exit-code-from tests
                '''
            }

            post {
                always {
                    sh '''
                        export TEST_IMAGE="jobs-portal:ci-${BUILD_NUMBER}"

                        docker compose \
                          -p "jobs-portal-tests-${BUILD_NUMBER}" \
                          -f compose.test.yaml \
                          down --volumes --remove-orphans
                    '''
                }
            }

            // Runs tests against the exact image built in the previous stage.
            // Uses a separate Compose project and temporary PostgreSQL database.
            // The tests container's exit code determines whether this stage passes.
            // Limits execution to 10 minutes to prevent indefinitely stuck tests.
            // Always attempts cleanup, including after test failure or timeout.
            // Cleanup targets this test project, not your development containers.
        }
    }
}
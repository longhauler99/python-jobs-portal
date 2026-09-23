pipeline {
    agent { label 'local-docker' }

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    triggers {
        pollSCM('H/5 * * * *')
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

        stage('Deploy locally') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }

            steps {
                sh '''
                    set -eu

                    export APP_IMAGE="jobs-portal:ci-${BUILD_NUMBER}"

                    # Use the same deployment configuration for every command.
                    compose_deploy() {
                        docker compose \
                          --env-file "$HOME/.config/jobs-portal/deploy.env" \
                          -p jobs-portal-local \
                          -f compose.deploy.yaml \
                          "$@"
                    }

                    # Find the currently running application container.
                    CURRENT_CONTAINER=$(docker ps -q \
                      --filter label=com.docker.compose.project=jobs-portal-local \
                      --filter label=com.docker.compose.service=web)

                    PREVIOUS_IMAGE=""

                    if [ -n "$CURRENT_CONTAINER" ]; then
                        # Record the exact image ID, even if its tag later changes.
                        PREVIOUS_IMAGE=$(docker inspect \
                          --format '{{.Image}}' "$CURRENT_CONTAINER")

                        CURRENT_TAG=$(docker inspect \
                          --format '{{.Config.Image}}' "$CURRENT_CONTAINER")

                        echo "Current application: $CURRENT_TAG"
                    fi

                    echo "Deploying: $APP_IMAGE"

                    if compose_deploy up --no-build --wait --wait-timeout 180; then
                        echo "Deployment passed its health checks."
                    else
                        echo "Deployment failed. Collecting logs..."
                        compose_deploy logs --tail=80 web db || true

                        if [ -n "$PREVIOUS_IMAGE" ]; then
                            echo "Restoring previous image: $CURRENT_TAG"
                            export APP_IMAGE="$PREVIOUS_IMAGE"

                            if compose_deploy up --no-build --wait --wait-timeout 180; then
                                echo "Rollback succeeded. Previous version is healthy."
                            else
                                echo "ROLLBACK FAILED. Manual attention is required."
                                compose_deploy logs --tail=80 web db || true
                            fi
                        else
                            echo "No previous running application was found."
                            echo "Automatic rollback is unavailable."
                        fi

                        # Keep Jenkins red: the attempted deployment failed,
                        # even if the previous application was restored.
                        exit 1
                    fi
                '''
            }

            // Records the running image before attempting the new deployment.
            // Restores it if deployment fails or health checks time out.
            // Checks that the restored application becomes healthy.
            // Preserves database and media volumes; does not reverse migrations.
            // Recovery requires the Jenkins agent and Docker to remain available.
        }
    }
}
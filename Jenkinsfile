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

        stage('Backup') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }

            steps {
                sh '''
                    set -eu
                    umask 077

                    DB_CONTAINER=$(docker ps -q \
                      --filter label=com.docker.compose.project=jobs-portal-local \
                      --filter label=com.docker.compose.service=db)

                    WEB_CONTAINER=$(docker ps -q \
                      --filter label=com.docker.compose.project=jobs-portal-local \
                      --filter label=com.docker.compose.service=web)

                    if [ -z "$DB_CONTAINER" ] || [ -z "$WEB_CONTAINER" ]; then
                        echo "Backup requires the existing database and web containers to be running."
                        exit 1
                    fi

                    BACKUP_ROOT="$HOME/backups/jobs-portal"
                    mkdir -p "$BACKUP_ROOT"
                    chmod 700 "$BACKUP_ROOT"

                    BACKUP_NAME="before-build-${BUILD_NUMBER}-$(date +%Y%m%d-%H%M%S)"
                    PARTIAL_DIR="$BACKUP_ROOT/$BACKUP_NAME.partial"
                    FINAL_DIR="$BACKUP_ROOT/$BACKUP_NAME"

                    mkdir "$PARTIAL_DIR"

                    # Restart the web container on normal exit or script failure.
                    resume_app() {
                        result=$?
                        trap - EXIT
                        if ! docker start "$WEB_CONTAINER" >/dev/null; then
                            echo "Could not restart the application. Manual attention required."
                            result=1
                        fi
                        exit "$result"
                    }

                    trap resume_app EXIT
                    trap 'exit 130' INT
                    trap 'exit 143' TERM

                    echo "Stopping web container for a consistent backup..."
                    docker stop --time 60 "$WEB_CONTAINER" >/dev/null

                    echo "Backing up PostgreSQL..."
                    docker exec "$DB_CONTAINER" sh -c \
                      'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' \
                      > "$PARTIAL_DIR/database.dump"

                    echo "Backing up uploaded files..."
                    docker cp "$WEB_CONTAINER":/app/media/. - \
                      > "$PARTIAL_DIR/media.tar"

                    echo "Checking that the backup archives can be read..."
                    docker exec -i "$DB_CONTAINER" pg_restore --list \
                      < "$PARTIAL_DIR/database.dump" > /dev/null

                    tar -tf "$PARTIAL_DIR/media.tar" > /dev/null

                    # Record the application image associated with this backup.
                    docker inspect --format '{{.Config.Image}} {{.Image}}' \
                      "$WEB_CONTAINER" > "$PARTIAL_DIR/application-image.txt"

                    # Only completed backups lose the .partial suffix.
                    mv "$PARTIAL_DIR" "$FINAL_DIR"

                    echo "Backup completed: $FINAL_DIR"
                    ls -lh "$FINAL_DIR"
                '''
            }

            // Backs up existing data before the new deployment changes it.
            // Briefly stops the web app so records and uploads stay consistent.
            // Attempts to restart the app even if a backup command fails.
            // A backup failure prevents the deployment stage from running.
            // Keeps backups outside Git and the Jenkins workspace.
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
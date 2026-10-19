# Panabaev Alisher - DevOps Lab

| Student field | Value |
| --- | --- |
| Name | Alisher |
| Surname | Panabaev |
| Group | It2-2308 |
| Student ID | 37332 |
| Course | DevOps |

Repository: <https://github.com/alisherqa06/panabaev-alisher-devops>

## Project contents

- `Panabaev_Alisher_info.txt` - student details used by the Linux lab.
- `scripts/Panabaev_Alisher_system.sh` - system and student-file report.
- `app/server.py` - standard-library Python HTTP application on port 8080.
- `tests/test_server.py` - unit and HTTP endpoint tests.
- `Dockerfile` and `docker-compose.yml` - application image and container.
- `Jenkinsfile` - five-stage declarative Pipeline.
- `jenkins/Dockerfile` and `docker-compose.jenkins.yml` - local Jenkins controller with Python and Docker CLI.
- `config/`, `logs/`, `private.txt`, and `public.txt` - Linux configuration, log-search, and permission exercises.
- `docs/video-demo-script-ru.md` and `docs/submission-checklist.md` - presentation guide and hand-in checklist.

## Linux lab

The Bash script resolves the project directory relative to its own location, so the student file check still works if the repository is moved:

```bash
cd /home/acer/devops/panabaev_alisher
chmod 755 scripts/Panabaev_Alisher_system.sh
./scripts/Panabaev_Alisher_system.sh
```

It prints the student record, user, hostname, date, OS release, disk use, and memory use. The log exercise uses `find`, `grep`, `grep -c`, `head`, and `tail` against `logs/application.log`; `*.log` is ignored by Git. The permissions exercise uses `chmod 600 private.txt` and `chmod 644 public.txt`. `ps`, `ps aux`, and `top` show process information.

## Application and Docker

The app reads `STUDENT_NAME`, `STUDENT_SURNAME`, `STUDENT_GROUP`, and `STUDENT_ID`. Missing or empty values fall back to Alisher, Panabaev, It2-2308, and 37332. It serves the student page at `/` and a readiness response at `/healthz`.

Run the local tests and Docker image:

```bash
python3 -m py_compile app/server.py scripts/check_http.py
python3 -m unittest discover -s tests -v
docker build -t panabaev-alisher-devops .
docker run -d --name panabaev-alisher-container \
  -p 8080:8080 \
  -e STUDENT_NAME=Alisher \
  -e STUDENT_SURNAME=Panabaev \
  -e STUDENT_GROUP=It2-2308 \
  -e STUDENT_ID=37332 \
  panabaev-alisher-devops
python3 scripts/check_http.py http://127.0.0.1:8080
```

Open <http://localhost:8080> in a Windows browser. The image is the built, reusable package; a container is a running instance of that image with its own process, environment, and network mapping.

To inspect the lifecycle:

```bash
docker ps
docker ps -a
docker logs panabaev-alisher-container
docker exec panabaev-alisher-container python -c 'print("container exec works")'
docker stop panabaev-alisher-container
docker start panabaev-alisher-container
docker rm -f panabaev-alisher-container
```

Compose provides the same app and publishes port 8080:

```bash
docker compose up --build -d
docker compose ps
docker compose logs
docker compose down
```

Do not run the Compose app and another container with the same required name at once. Stop or remove the existing instance before changing how it is started.

## Jenkins on Windows 11 and WSL 2

Docker Desktop's WSL integration supplies the Docker CLI and daemon to Ubuntu. The Jenkins controller runs in a Linux container on that same Docker Desktop engine. Its custom image contains Python, Git, and Docker CLI; the Compose file mounts the Docker socket so the Pipeline can build and run the app image. Port 8081 keeps the Jenkins dashboard separate from the app on port 8080. Jenkins therefore builds and runs containers in the same image list visible from Ubuntu and Docker Desktop.

From Ubuntu, start Jenkins and pass the Docker socket's group ID:

```bash
cd /home/acer/devops/panabaev_alisher
DOCKER_SOCKET_GID=$(stat -c '%g' /var/run/docker.sock) \
  docker compose -f docker-compose.jenkins.yml up --build -d
```

Open <http://localhost:8081>. On first start, read the one-time unlock password locally with `docker logs panabaev-alisher-jenkins`, enter it in the page, install the suggested plugins, and create an administrator account. Keep that password private.

Create a Jenkins item named `Panabaev_Alisher_DevOps` with type **Pipeline**. In its Pipeline section select **Pipeline script from SCM**, choose **Git**, set the repository URL to `https://github.com/alisherqa06/panabaev-alisher-devops`, branch to `*/main`, and script path to `Jenkinsfile`. If the repository is private, add GitHub credentials in Jenkins and select them there; never put a token in this repository. Save and choose **Build Now**.

The Jenkinsfile defines the environment values and the stages `Checkout`, `Build`, `Test`, `Docker Build`, and `Docker Run`. Checkout records the source commit. Build compiles the Python files, Test runs `unittest`, Docker Build creates the named image, and Docker Run replaces any old container with the required name before checking the HTTP page and printing its logs. A failed command fails the Pipeline; the final stage only succeeds when the health check sees the expected student values.

To see a recorded result, open the job's latest build and confirm `Finished: SUCCESS`, all five green stages, its Console Output, source commit, image, and running container. The Jenkins container needs Docker Engine access for this lab; keep the local dashboard and Docker socket confined to the local development machine.

## Integrated workflow

`Linux -> Git -> GitHub -> Jenkins -> Build -> Test -> Docker Build -> Docker Run -> SUCCESS`

Linux provides the shell and process, file, permission, and log tools used for development. Git records local changes and commits so a known revision can be reviewed or restored. GitHub hosts the shared remote repository. Jenkins checks out the selected GitHub revision so its build uses committed source instead of files from a developer's machine. Docker builds an image to package the app and its runtime consistently; a container runs that image. When a Pipeline starts, Jenkins checks out the configured branch and runs each stage in order. If a required stage fails, Jenkins stops the remaining stages, marks the build failed, and records the command output for diagnosis.

## Actual status and evidence

Checks confirmed on 2026-10-19:

- Ubuntu 26.04.1 is running as a WSL 2 distribution; Docker Desktop's `docker-desktop` distribution is also running.
- `docker --version` reports 29.8.2, `docker compose version` reports 5.6.0, `docker info` reaches the Docker Desktop engine, and `docker run --rm hello-world` completed.
- Four Python unit tests passed. The app image built as `panabaev-alisher-devops`; the named container returned the expected student page and health response. Its `logs`, `exec`, `stop`, `start`, and `rm` lifecycle was checked.
- `docker compose up --build -d`, `docker compose ps`, `docker compose logs`, and `docker compose down` completed; the app health check passed while Compose was running.
- The custom Jenkins controller image was built with Python, Git, and Docker CLI. From inside the image, Docker reported the same 29.8.2 Desktop Engine. The controller is running at <http://localhost:8081> and its `/login` page returned HTTP 200.

The Jenkins first-run setup and job creation still require a local administrator action. No Jenkins Pipeline result is claimed until the `Panabaev_Alisher_DevOps` job is configured and its build actually finishes.

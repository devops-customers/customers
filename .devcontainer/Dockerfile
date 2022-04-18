# Image for a Python 3 development environment
FROM rofrano/pipeline-selenium:latest

# # For Feiyang to speed up
# Run sed -i 's/deb.debian.org/mirrors.tencent.com/' /etc/apt/sources.list

# Add any tools that are needed beyond Python 3.9
# NEW: Add bash-completion so that Press TAB can complete the command
RUN apt-get update && \
    apt-get install -y sudo vim git zip tree curl wget jq bash-completion && \
    apt-get autoremove -y && \
    apt-get clean -y


# Create a user for development
ARG USERNAME=devops
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user with passwordless sudo privileges
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && usermod -aG sudo $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Added libraries for PostgreSQL
RUN apt-get install -y gcc libpq-dev

# Set up the Python development environment
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip wheel && \
    pip install -r requirements.txt

# # For Feiyang to speed up
# RUN python -m pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --upgrade pip wheel && \
#     pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

ENV PORT 8080
EXPOSE $PORT

# Enable color terminal for docker exec bash
ENV TERM=xterm-256color

# Become a regular user
USER $USERNAME

FROM ros:humble

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-opencv \
    python3-cv-bridge \
    ros-humble-cv-bridge \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-navigation2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Set up workspace
WORKDIR /ros2_ws
COPY ros2_ws/src /ros2_ws/src

# Build the workspace
RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install

# Source workspace on container start
RUN echo '. /opt/ros/humble/setup.sh' >> /root/.bashrc && \
    echo '. /ros2_ws/install/setup.sh' >> /root/.bashrc

CMD ["bash"]

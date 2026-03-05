# Start with the ARM-compatible ROS 2 Humble base
FROM ros:humble-ros-base

# Install build tools, Nano for your scripts, and the GUI tools for RViz
RUN apt-get update && apt-get install -y \
    git \
    nano \
    python3-colcon-common-extensions \
    ros-humble-desktop \
    && rm -rf /var/lib/apt/lists/*

# Set up the ROS 2 workspace directory
WORKDIR /root/ros2_ws
RUN mkdir -p src

# Clone the official SLAMTEC LiDAR drivers
RUN cd src && git clone https://github.com/Slamtec/sllidar_ros2.git

# Build the LiDAR package (requires sourcing the ROS 2 core first)
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build --symlink-install"

# Automatically source ROS 2 and the built workspace every time a terminal opens
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
RUN echo "source /root/ros2_ws/install/setup.bash" >> /root/.bashrc

# Set the default action to open a bash shell
CMD ["bash"]
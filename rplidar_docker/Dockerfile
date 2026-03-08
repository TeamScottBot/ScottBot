FROM ros:humble-ros-base

RUN apt-get update && apt-get install -y \
    git \
    nano \
    python3-colcon-common-extensions \
    ros-humble-desktop \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir REVHubInterface

COPY . /ScottBot

WORKDIR /root/ros2_ws
RUN mkdir -p src

RUN cd src && git clone https://github.com/Slamtec/sllidar_ros2.git

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build --symlink-install"

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
RUN echo "source /root/ros2_ws/install/setup.bash" >> /root/.bashrc

CMD ["bash"]

---
title: Chapter 2 - ROS 2 Nodes, Topics, and Services
description: Understanding ROS 2 communication patterns for humanoid robotics
---

# Chapter 2: ROS 2 Nodes, Topics, and Services

## Learning Objectives

By the end of this chapter, you should be able to:
- Explain the difference between nodes, topics, and services in ROS 2
- Describe message passing in humanoid systems using specific examples like perception → motion
- Understand how distributed robotic behaviors emerge from these components
- Apply these concepts to humanoid robot architectures

## Introduction

The architecture of ROS 2 is built around three fundamental communication patterns: nodes as computational units, topics for asynchronous data flow, and services for synchronous interactions. These patterns enable the distributed nature of robotic systems and are particularly important in humanoid robotics where multiple sensors, controllers, and processing units must coordinate seamlessly.

Understanding these communication patterns is essential for developing effective humanoid robotic systems, as they determine how information flows through the robot's "nervous system" and how different components interact to achieve complex behaviors.

## Nodes as Computational Units

In ROS 2, a node is the fundamental unit of computation that performs specific functions within the robotic system. Each node typically represents a single process or thread that executes a particular algorithm or manages a specific device (Macenski, S., et al. (2022). ROS 2: Transforming the Robot Operating System for real-time and safety-critical applications. *IEEE Robotics & Automation Magazine*, 29(2), 26-35.).

For humanoid robots, nodes might include:
- **Sensor drivers**: Camera, LIDAR, IMU, force/torque sensors
- **Control algorithms**: Walking controllers, arm controllers, balance systems
- **Perception modules**: Object detection, person tracking, SLAM systems
- **Planning modules**: Path planning, motion planning, task planning
- **Behavior managers**: State machines, decision-making systems

Nodes in ROS 2 are designed to be lightweight and focused on specific tasks. This modularity allows for better maintainability, testing, and reusability of robotic software components. Each node can be developed, debugged, and optimized independently before integration into the larger system.

### Node Lifecycle

ROS 2 introduces explicit lifecycle management, allowing nodes to transition through different states (unconfigured, inactive, active, finalized) to enable more controlled system startup and shutdown (Mason, A., et al. (2021). Lifecycle management in ROS 2. *Proceedings of the International Conference on Simulation, Modeling, and Programming for Autonomous Robots*, 1-8.).

This lifecycle management is particularly important in humanoid robotics where:
- Safety systems must be initialized before motion control
- Sensors must be calibrated before perception systems can operate
- Multiple subsystems need to be brought up in a specific order
- Graceful shutdown procedures are essential for safety

## Topics for Asynchronous Data Flow

Topics enable asynchronous communication between nodes using a publish-subscribe pattern. This pattern is ideal for continuous data streams such as sensor readings, where the publisher doesn't need to know who is listening, and subscribers don't need to know where data originates (Quigley, M., et al. (2009). ROS: an open-source robot operating system. *ICRA Workshop on Open Source Software*, 3, 5.).

### Sensor-Actuator Communication

In humanoid robotics, topics are extensively used for sensor-actuator communication:

**Perception Pipeline Example**:
- Camera nodes publish image data to `/camera/image_raw`
- Image processing nodes subscribe to images and publish object detections to `/object_detections`
- Planning nodes subscribe to detections and publish motion commands to `/motion_commands`
- Controller nodes subscribe to commands and execute them on the physical robot

This asynchronous pattern allows each component to operate at its natural frequency without blocking other components. For example, cameras might publish at 30 Hz while IMUs publish at 1000 Hz, and both can be processed by the same perception system.

### Quality of Service (QoS) Settings

ROS 2's QoS settings allow fine-tuning of topic communication behavior:
- **Reliability**: Choose between best-effort (fast, may lose messages) and reliable (slower, all messages delivered)
- **Durability**: Decide whether late-joining subscribers receive past messages
- **Deadline**: Set maximum time for message delivery
- **History**: Control how many messages are stored

For humanoid robotics applications, these settings are crucial:
- Sensor data might use best-effort reliability with small history for real-time performance
- Critical safety messages might use reliable durability to ensure delivery
- Debugging information might use volatile durability to minimize memory usage

## Services for Synchronous Interactions

Services provide request-response communication patterns where a client sends a request and waits for a response. This synchronous pattern is appropriate for operations that have a clear beginning and end, and where the caller needs to wait for completion (Santos, J., et al. (2020). Distributed robotics systems using ROS 2: Architecture and applications. *Journal of Intelligent & Robotic Systems*, 99(3), 729-745.).

### Common Service Patterns in Humanoid Robotics

**Calibration Services**:
- Service: `/calibrate_sensors`
- Request: List of sensors to calibrate
- Response: Success/failure status and calibration parameters

**Navigation Services**:
- Service: `/navigate_to_pose`
- Request: Target pose (x, y, theta)
- Response: Navigation result (success, failure, timeout)

**Action Execution Services**:
- Service: `/execute_action`
- Request: Action name and parameters
- Response: Execution result and any returned data

Services are particularly useful when an operation must complete before the calling component can proceed. However, they should be used judiciously in real-time systems where blocking calls could affect performance.

## Message Passing in Humanoid Systems

The real power of ROS 2's communication patterns emerges when they are combined to create complex humanoid behaviors. Let's examine how perception information flows to motion execution in a typical humanoid robot:

### Perception to Motion Example

1. **Sensory Input**: Multiple sensors publish data to topics:
   - `/camera/rgb/image_raw` - RGB camera images
   - `/camera/depth/image_raw` - Depth camera data
   - `/imu/data` - Inertial measurement unit readings
   - `/joint_states` - Current joint positions and velocities

2. **Perception Processing**: Perception nodes subscribe to sensor data and publish processed information:
   - Object detection node: Subscribes to camera data, publishes object poses to `/detected_objects`
   - SLAM node: Subscribes to multiple sensors, publishes map to `/map` and pose to `/amcl_pose`
   - State estimation: Subscribes to IMU and joint states, publishes center of mass and balance state to `/balance_state`

3. **Planning and Control**: Planning nodes subscribe to perception data and publish control commands:
   - Path planner: Subscribes to map and goal, publishes path to `/global_plan`
   - Motion planner: Subscribes to path and current state, publishes motion commands to `/motion_commands`
   - Walking controller: Subscribes to motion commands and balance state, publishes joint trajectories to `/joint_trajectory`

4. **Actuation**: Controller nodes execute commands on the physical robot:
   - Joint trajectory controller: Subscribes to joint trajectories and commands physical actuators

This distributed approach allows each component to be developed and optimized independently while maintaining system-wide coordination through standardized message interfaces.

## Architectural Patterns for Humanoid Systems

Several architectural patterns emerge when designing humanoid robotics systems with ROS 2:

### Hierarchical Control Pattern
- High-level planners publish abstract goals
- Mid-level controllers translate goals to motion commands
- Low-level controllers execute precise actuator commands
- Each level operates at appropriate time scales and abstraction levels

### Sensor Fusion Pattern
- Multiple sensor nodes publish to different topics
- Fusion nodes subscribe to multiple sensor streams
- Combined state estimates are published for use by other components
- Redundancy improves robustness and accuracy

### Behavior-Based Pattern
- Multiple behavior nodes publish competing action proposals
- Arbitration nodes select appropriate actions based on context
- This enables reactive behaviors that can override planned actions when necessary

## Summary

ROS 2's communication patterns of nodes, topics, and services provide the foundation for distributed humanoid robotic systems. Nodes enable modular development of computational units, topics facilitate asynchronous data flow for continuous processes like sensing and perception, and services provide synchronous interactions for discrete operations.

The combination of these patterns enables complex humanoid behaviors to emerge from the interaction of specialized components. Quality of Service settings allow fine-tuning of communication behavior to meet specific application requirements, while the distributed architecture supports the modularity essential for developing complex humanoid systems.

Understanding these communication patterns is fundamental to designing effective humanoid robotic systems that can integrate perception, planning, control, and interaction capabilities in a coordinated manner.

## References

Macenski, S., et al. (2022). ROS 2: Transforming the Robot Operating System for real-time and safety-critical applications. *IEEE Robotics & Automation Magazine*, 29(2), 26-35.

Mason, A., et al. (2021). Lifecycle management in ROS 2. *Proceedings of the International Conference on Simulation, Modeling, and Programming for Autonomous Robots*, 1-8.

Quigley, M., et al. (2009). ROS: an open-source robot operating system. *ICRA Workshop on Open Source Software*, 3, 5.

Santos, J., et al. (2020). Distributed robotics systems using ROS 2: Architecture and applications. *Journal of Intelligent & Robotic Systems*, 99(3), 729-745.
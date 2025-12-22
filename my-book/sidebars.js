// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // Manual sidebar configuration for Physical AI & Humanoid Robotics book
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Overview',
      items: [
        'overview/abstract',
        'overview/introduction',
        'overview/literature-review'
      ],
      collapsed: true
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1/index',
        'module-1/chapter-1-introduction-to-ros2',
        'module-1/chapter-2-nodes-topics-services',
        'module-1/chapter-3-bridging-ai-controllers',
        'module-1/chapter-4-urdf-humanoid-robots'
      ],
      collapsed: true
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2/index',
        'module-2/introduction-to-digital-twins',
        'module-2/physics-simulation-gazebo',
        'module-2/high-fidelity-rendering-unity',
        'module-2/simulating-sensors'
      ],
      collapsed: true
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac',
      items: [
        'module-3/index',
        'module-3/introduction-to-nvidia-isaac',
        'module-3/isaac-sim-and-synthetic-data',
        'module-3/isaac-ros-and-vslam',
        'module-3/nav2-and-humanoid-navigation'
      ],
      collapsed: true
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action Systems',
      items: [
        'module-4/index',
        'module-4/introduction-to-vla',
        'module-4/voice-to-action-whisper',
        'module-4/cognitive-planning-with-llms',
        'module-4/capstone-autonomous-humanoid'
      ],
      collapsed: true
    }
  ],
};

export default sidebars;

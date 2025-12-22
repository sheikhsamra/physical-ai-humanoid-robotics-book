import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Physical AI Foundations',
    image: require('@site/static/img/robot.png').default,
    description: (
      <>
        An in-depth exploration of Physical Artificial Intelligence, focusing on
        embodied cognition, perception–action loops, and real-world interaction
        between intelligent agents and their physical environments.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics Architectures',
    image: require('@site/static/img/ai.png').default,
    description: (
      <>
        A comprehensive study of humanoid robot design, including kinematic
        structures, sensor fusion, control systems, locomotion, and manipulation
        architectures grounded in peer-reviewed research.
      </>
    ),
  },
  {
    title: 'RAG & Agent-Based Robotics Systems',
    image: require('@site/static/img/robot2.png').default,
    description: (
      <>
        Integration of Retrieval-Augmented Generation (RAG) and autonomous
        agents to enable explainable, verifiable, and reproducible intelligence
        in AI-native robotic systems.
      </>
    ),
  },
];

function Feature({image, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img
          src={image}
          className={styles.featureImage}
          alt={title}
        />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

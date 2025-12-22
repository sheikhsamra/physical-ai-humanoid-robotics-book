import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        {/* Naya wrapper div jo text aur image ko handle karega */}
        <div className={styles.heroContent}>
          
          {/* Left Side: Text Content */}
          <div className={styles.heroText}>
            <Heading as="h1" className="hero__title">
              {siteConfig.title}
            </Heading>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttons}>
  {/* Pehla Button */}
  <Link
    className="button button--secondary button--lg"
    to="/docs/overview/introduction">
    Get Started →
  </Link>

  {/* Dusra Button (Example: Documentation ya Github) */}
  <Link
    className="button button--outline button--secondary button--lg"
    to="/docs/overview/abstract">
    Learn More
  </Link>
</div>
          </div>

          {/* Right Side: Image */}
          <div className={styles.heroImage}>
            <img 
              src="img/hero.png" // Yahan apni image ka path likhein (static/img folder me rakhein)
              alt="Hero Banner" 
              className={styles.bannerImg}
            />
          </div>

        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}

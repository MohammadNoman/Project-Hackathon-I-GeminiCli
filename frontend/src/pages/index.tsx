import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

// Using global custom.css classes for hero styling
function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero', 'hero-banner')}>
      <div className="container">
        <Heading as="h1" className="hero-title">
          Master Physical AI & <br /> Humanoid Robotics
        </Heading>
        <p className="hero-subtitle">
          The world's first adaptive, AI-powered textbook.
          Learn robotics with a platform that understands your background and speaks your language.
        </p>
        <div className={styles.buttons} style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Reading Now 🚀
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/signup">
            Create Free Account
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Learn Physical AI and Humanoid Robotics with our adaptive AI textbook.">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}

import React, { useState } from 'react';
import styles from './styles.module.css';
import { useAuth } from '../../contexts/AuthContext';
import { personalizationService } from '../../services/personalization';
import Link from '@docusaurus/Link';

interface Props {
    children: string; // The original text to personalize
}

const PersonalizedContent: React.FC<Props> = ({ children }) => {
    const { isAuthenticated, user } = useAuth();
    const [personalizedText, setPersonalizedText] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handlePersonalize = async () => {
        setIsLoading(true);
        setError('');
        try {
            const data = await personalizationService.personalizeText(children);
            setPersonalizedText(data.personalized_text);
        } catch (err: any) {
            setError("Failed to personalize content. Please try again.");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    if (!isAuthenticated) {
        return (
            <div className={styles.container}>
                <div className={styles.original}>{children}</div>
                <div className={styles.loginPrompt}>
                    <Link to="/login">Log in</Link> to see this content personalized for your background.
                </div>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h4 className={styles.title}>
                    {personalizedText ? `Personalized for ${user?.name || 'You'}` : 'Content'}
                </h4>
                {!personalizedText && (
                    <button
                        className={styles.button}
                        onClick={handlePersonalize}
                        disabled={isLoading}
                    >
                        {isLoading ? (
                            <>
                                <span className={styles.spinner}>✨</span> Personalizing...
                            </>
                        ) : (
                            <>
                                <span>✨</span> Personalize for Me
                            </>
                        )}
                    </button>
                )}
            </div>

            {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}

            <div className={personalizedText ? styles.content : styles.original}>
                {personalizedText || children}
            </div>

            {personalizedText && (
                <div style={{ marginTop: '0.5rem', textAlign: 'right' }}>
                    <button
                        className=""
                        style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', fontSize: '0.8rem' }}
                        onClick={() => setPersonalizedText(null)}
                    >
                        Show Original
                    </button>
                </div>
            )}
        </div>
    );
};

export default PersonalizedContent;

import React, { useState } from 'react';
import styles from './styles.module.css';
import { useAuth } from '../../contexts/AuthContext';
import { localizationService } from '../../services/localization';
import Link from '@docusaurus/Link';

interface Props {
    children: string; // The original text to translate
}

const LocalizedContent: React.FC<Props> = ({ children }) => {
    const { isAuthenticated } = useAuth();
    const [translatedText, setTranslatedText] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [language, setLanguage] = useState('Urdu');
    const [error, setError] = useState('');

    const handleTranslate = async () => {
        setIsLoading(true);
        setError('');
        try {
            const data = await localizationService.translateText(children, language);
            setTranslatedText(data.translated_text);
        } catch (err: any) {
            setError("Failed to translate content. Please try again.");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    if (!isAuthenticated) {
        return (
            <div className={styles.container}>
                <div className={styles.original}>{children}</div>
            </div>
        );
    }

    const isRTL = language === 'Urdu' || language === 'Arabic' || language === 'Farsi';

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h4 className={styles.title}>
                    {translatedText ? `Translated to ${language}` : 'Multilingual View'}
                </h4>

                <div className={styles.controls}>
                    {!translatedText && (
                        <select
                            className={styles.select}
                            value={language}
                            onChange={(e) => setLanguage(e.target.value)}
                        >
                            <option value="Urdu">Urdu</option>
                            <option value="Spanish">Spanish</option>
                            <option value="French">French</option>
                            <option value="German">German</option>
                            <option value="Chinese">Chinese</option>
                        </select>
                    )}

                    {!translatedText && (
                        <button
                            className={styles.button}
                            onClick={handleTranslate}
                            disabled={isLoading}
                        >
                            {isLoading ? 'Translating...' : 'Translate'}
                        </button>
                    )}
                </div>
            </div>

            {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}

            <div className={`${translatedText ? styles.content : styles.original} ${translatedText && isRTL ? styles.rtl : ''}`}>
                {translatedText || children}
            </div>

            {translatedText && (
                <div style={{ marginTop: '0.5rem', textAlign: 'right' }}>
                    <button
                        className=""
                        style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', fontSize: '0.8rem' }}
                        onClick={() => setTranslatedText(null)}
                    >
                        Show Original
                    </button>
                </div>
            )}
        </div>
    );
};

export default LocalizedContent;

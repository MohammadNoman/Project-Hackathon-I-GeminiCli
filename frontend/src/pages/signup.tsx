import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useHistory } from '@docusaurus/router';
import { useAuth } from '../contexts/AuthContext';
import styles from '../components/Auth/styles.module.css';

export default function Signup() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        software_background: '',
        hardware_background: '',
        language_preference: 'python' // default
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { signup } = useAuth();
    const history = useHistory();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({
            ...formData,
            [e.target.id]: e.target.value
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await signup(formData);
            // Redirect to login or auto-login (for now redirect to login for clarity)
            history.push('/login');
        } catch (err: any) {
            setError(err.message || 'Failed to create account');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Layout title="Sign Up" description="Create your account">
            <div className={styles.authContainer}>
                <div className={styles.authCard}>
                    <h1 className={styles.title}>Create Account</h1>

                    {error && <div className={styles.error}>{error}</div>}

                    <form onSubmit={handleSubmit}>
                        <div className="row">
                            <div className="col col--6">
                                <div className={styles.formGroup}>
                                    <label className={styles.label} htmlFor="name">Full Name</label>
                                    <input
                                        id="name"
                                        type="text"
                                        className={styles.input}
                                        value={formData.name}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                            </div>
                            <div className="col col--6">
                                <div className={styles.formGroup}>
                                    <label className={styles.label} htmlFor="email">Email</label>
                                    <input
                                        id="email"
                                        type="email"
                                        className={styles.input}
                                        value={formData.email}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                            </div>
                        </div>

                        <div className={styles.formGroup}>
                            <label className={styles.label} htmlFor="password">Password</label>
                            <input
                                id="password"
                                type="password"
                                className={styles.input}
                                value={formData.password}
                                onChange={handleChange}
                                required
                                minLength={8}
                            />
                        </div>

                        <div className={styles.formGroup}>
                            <label className={styles.label} htmlFor="software_background">Software Background</label>
                            <input
                                id="software_background"
                                type="text"
                                className={styles.input}
                                value={formData.software_background}
                                onChange={handleChange}
                                placeholder="e.g. Python, JS, C++"
                            />
                        </div>

                        <div className={styles.formGroup}>
                            <label className={styles.label} htmlFor="language_preference">Preferred Language</label>
                            <select
                                id="language_preference"
                                className={styles.input}
                                value={formData.language_preference}
                                onChange={handleChange}
                            >
                                <option value="python">Python</option>
                                <option value="cpp">C++</option>
                                <option value="javascript">JavaScript</option>
                                <option value="urdu">Urdu (Translated)</option>
                            </select>
                        </div>

                        <button type="submit" className={styles.button} disabled={isLoading}>
                            {isLoading ? 'Creating Account...' : 'Sign Up'}
                        </button>
                    </form>

                    <div className={styles.linkText}>
                        Already have an account? <Link to="/login" className={styles.link}>Sign in</Link>
                    </div>
                </div>
            </div>
        </Layout>
    );
}

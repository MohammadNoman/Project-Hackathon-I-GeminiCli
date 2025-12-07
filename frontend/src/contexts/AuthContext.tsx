import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { authService, User } from '../services/auth';

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    signup: (data: any) => Promise<void>;
    logout: () => void;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check for existing session
        const storedUser = authService.getCurrentUser();
        if (storedUser) {
            setUser(storedUser);
        }
        setLoading(false);
    }, []);

    const login = async (email: string, password: string) => {
        const data = await authService.login(email, password);
        localStorage.setItem('token', data.access_token);
        // In a real app we might fetch the user profile here using the token
        // For now we'll store a basic user object or fetch it from a /me endpoint
        // Let's assume we can derive or fetch user info. For simplicity in this hackathon,
        // we might need a /users/me endpoint, but I'll skip that for a sec and mock the user object set
        // or better, let's implement the /me endpoint or similar in next steps.
        // For now, setting a placeholder or the email.

        const userObj = { id: 'temp', email: email };
        localStorage.setItem('user', JSON.stringify(userObj));
        setUser(userObj as User);
    };

    const signup = async (data: any) => {
        await authService.signup(data);
        // Auto login after signup? Or require login. Let's require login for security/simplicity.
    };

    const logout = () => {
        authService.logout();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, signup, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

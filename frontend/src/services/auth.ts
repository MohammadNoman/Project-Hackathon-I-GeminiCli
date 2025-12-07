import { config } from '../config';

const API_BASE_URL = config.apiBaseUrl;

export interface User {
    id: string;
    email: string;
    name?: string;
    software_background?: string;
    hardware_background?: string;
    language_preference?: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export const authService = {
    async signup(userData: any): Promise<User> {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Signup failed');
        }
        return response.json();
    },

    async login(email: string, password: string): Promise<AuthResponse> {
        const formData = new URLSearchParams();
        formData.append('username', email); // OAuth2PasswordRequestForm expects 'username', request expects form-urlencoded
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }
        return response.json();
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },

    getCurrentUser(): User | null {
        const userStr = localStorage.getItem('user');
        if (userStr) return JSON.parse(userStr);
        return null;
    },

    getToken(): string | null {
        return localStorage.getItem('token');
    }
};

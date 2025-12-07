import { authService } from './auth';
import { config } from '../config';

export interface PersonalizeResponse {
    personalized_text: string;
    original_text: string;
}

export const personalizationService = {
    async personalizeText(text: string): Promise<PersonalizeResponse> {
        const token = authService.getToken();
        if (!token) {
            throw new Error("User must be logged in to personalize content.");
        }

        const response = await fetch(`${config.apiBaseUrl}/personalize/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Personalization failed');
        }
        return response.json();
    }
};

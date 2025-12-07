import { authService } from './auth';
import { config } from '../config';

export interface TranslateResponse {
    translated_text: string;
    original_text: string;
    language: string;
}

export const localizationService = {
    async translateText(text: string, targetLanguage: string = 'Urdu'): Promise<TranslateResponse> {
        const token = authService.getToken();
        if (!token) {
            throw new Error("User must be logged in to translate content.");
        }

        const response = await fetch(`${config.apiBaseUrl}/translate/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text,
                target_language: targetLanguage
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Translation failed');
        }
        return response.json();
    }
};

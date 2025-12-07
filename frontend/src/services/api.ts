
export interface ChatResponse {
    response: string;
    source_chunks: string[];
}

import { config } from '../config';

// TODO: Make this configurable via environment variables
const API_BASE_URL = config.apiBaseUrl;

export const sendMessageToRAG = async (query: string, conversationId?: string): Promise<ChatResponse> => {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query,
                conversation_id: conversationId,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || errorData.message || 'Failed to fetch response from AI');
        }

        return await response.json();
    } catch (error) {
        console.error('Error querying RAG API:', error);
        throw error;
    }
};

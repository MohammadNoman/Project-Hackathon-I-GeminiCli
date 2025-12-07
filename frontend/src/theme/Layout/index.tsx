import React from 'react';
import Layout from '@theme-original/Layout';
import Chatbot from '@site/src/components/Chatbot';
import { AuthProvider } from '../../contexts/AuthContext';

export default function LayoutWrapper(props) {
    return (
        <AuthProvider>
            <Layout {...props} />
            <Chatbot />
        </AuthProvider>
    );
}

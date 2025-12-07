
// Configuration for the Frontend
// This helps manage environment-specific settings

const isProduction = process.env.NODE_ENV === 'production';

// TODO: REPLACE THIS ULR with your actual Render Backend URL after your first deployment!
// Example: "https://my-backend-service.onrender.com"
const PROD_BACKEND_URL = "https://project-hackathon-i-geminicli.onrender.com";

export const config = {
    // If we are in production build, use the Prod URL. Otherwise use localhost.
    // You can also override this by setting REACT_APP_API_URL if your build setup supports it.
    apiBaseUrl: isProduction ? PROD_BACKEND_URL : "http://localhost:8000",
};

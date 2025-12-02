// frontend/tests/integration/test_deployment_access.test.js
import axios from 'axios';

describe('Docusaurus Deployment Access Test', () => {
  it('should verify the deployed site is accessible and displays content', async () => {
    const deployedUrl = 'https://MohammadNoman.github.io/Project-Hackathon-I-GeminiCli/';
    
    // Check if the deployed URL returns a 200 status code
    const response = await axios.get(deployedUrl);
    expect(response.status).toBe(200);
    
    // Check if the response text contains the title of the textbook
    const text = response.data; // Axios puts the response data in .data
    expect(text).toContain('Physical AI & Humanoid Robotics Textbook');
  });
});

// frontend/tests/integration/test_build.test.js
const { execSync } = require('child_process');

describe('Docusaurus Build Integration Test', () => {
  it('should build successfully', () => {
    try {
      // Run the Docusaurus build command
      execSync('npm run build', { cwd: './', stdio: 'inherit' });
      // If the command completes without throwing an error, the build was successful
      expect(true).toBe(true);
    } catch (error) {
      // If an error is thrown, the build failed
      fail(`Docusaurus build failed: ${error.message}`);
    }
  }, 10 * 60 * 1000); // Set a timeout for 10 minutes (600,000 ms)
});

module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\.jsx?$': 'babel-jest',
    '^.+\.tsx?$': 'babel-jest',
  },
  moduleNameMapper: {
    '\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  setupFilesAfterEnv: [],
  testMatch: [
    '<rootDir>/tests/**/*.test.{js,jsx,ts,tsx}',
  ],
};
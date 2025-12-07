import React from 'react';
import renderer from 'react-test-renderer';
import Chatbot from './index';

describe('Chatbot', () => {
  it('renders correctly', () => {
    const tree = renderer
      .create(<Chatbot />)
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
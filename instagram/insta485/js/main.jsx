import React from 'react';
import ReactDOM from 'react-dom';
import Feed from './feed';

ReactDOM.render(
  // Insert the post component into the DOM
  <Feed url="/api/v1/p/" />,
  document.getElementById('reactEntry'),
);

import React, { useEffect, useState } from 'react';
import { stub } from '../data/client.js';

const App = () => {
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page-reload
    console.log('submitting');

    let call = stub.QueryES({ query: 'batman' });
    call.on('data', function (res) {
      console.log('Result', res);
    });
    call.on('end', function () {
      console.log('end');
    });
    call.on('error', function (e) {
      console.log(e);
    });
    call.on('status', function (status) {
      console.log(status);
    });
  };

  return (
    <div>
      <h1>Google has got nothing on us!</h1>
      <form onSubmit={handleSubmit}>
        <input type='text' id='query' name='query' />
        <input type='submit' value='Submit' />
      </form>
    </div>
  );
};

export default App;

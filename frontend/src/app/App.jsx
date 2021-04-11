import React, { useEffect, useState } from 'react';
import { search } from '../data/client.js';
import { Profile } from '../pages/Profile.jsx';

const App = () => {
  const [results, setResults] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page-reload
    let queryString = e.target[0].value;
    search(queryString, function (v) {
      setResults((prev) => [...prev, v]);
    });
  };

  return (
    <div>
      <h1>Google has got nothing on us!</h1>
      <form onSubmit={(e) => handleSubmit(e)}>
        <input type='text' id='query' name='query' />
        <input type='submit' value='Submit' />
      </form>
      <ul>
        {results?.map((obj, i) => {
          return (
            <div key={i}>
              {obj.id} {obj.score}
              <ul>
                {Object.entries(obj.dataMap)?.map((entry) => {
                  return (
                    <li>
                      {entry[0]}: {entry[1]}
                    </li>
                  );
                })}
              </ul>
              <img src={`http://covers.openlibrary.org/b/ISBN/${obj.dataMap['ISBN']}-M.jpg`} />
            </div>
          );
        })}
      </ul>
      <Profile />
    </div>
  );
};

export default App;

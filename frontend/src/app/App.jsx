import React, { useEffect, useState } from 'react';
import { search, getUserData, setUserData } from '../data/client.js';

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
      <button
        onClick={() =>
          setUserData({
            name: 'Simon',
            languages: ['German', 'French', 'Japanese', 'Norwegian'],
            topics: ['Romance', 'Short', 'Adventure', 'Mystery'],
            age: 10,
            sex: 'F',
          })
        }
      >
        Set USER
      </button>
      <button onClick={() => getUserData(1)}>Get USER</button>
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
    </div>
  );
};

export default App;

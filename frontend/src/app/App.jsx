import React, { useEffect, useState } from 'react';
import { search, setReadBook, setRat, setReadBookeBook, setRateBook } from '../data/client.js';

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
          setReadBook({
            userID: 1,
            documentID: '3TJ9EF93',
            is_read: true,
          })
        }
      >
        Set USER
      </button>
      <button
        onClick={() =>
          setRateBook({
            userID: 1,
            documentID: '3TJ9EF93',
            rating: 33,
          })
        }
      >
        Rate Book
      </button>
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

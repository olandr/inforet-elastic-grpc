import React, { useEffect, useState } from 'react';
import { search } from '../data/client.js';
import { Profile } from '../pages/Profile.jsx';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';

const App = () => {
  const [queryString, setQueryString] = useState('');
  const [results, setResults] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page-reload
    if (queryString !== '') {
      search(queryString, function (v) {
        setResults((prev) => [...prev, v]);
      });
    }
  };

  return (
    <div style={{ display: 'flex', margin: '0 32px', justifyContent: 'space-between' }}>
      <div>
        <h1>Google has got nothing on us!</h1>
        <form onSubmit={(e) => handleSubmit(e)} style={{ display: 'flex' }}>
          <TextField
            id='query'
            label='Search...'
            onChange={(e) => setQueryString(e.target.value)}
            style={{ width: '100%', paddingRight: '8px' }}
          ></TextField>
          <Button
            type='submit'
            variant={'contained'}
            value='Submit'
            style={{ color: '#FFF', backgroundColor: '#0F9D58' }}
          >
            Search
          </Button>
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
      </div>

      <Profile />
    </div>
  );
};

export default App;

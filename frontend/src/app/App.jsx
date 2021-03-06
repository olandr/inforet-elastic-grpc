import React, { useEffect, useState } from 'react';
import { search } from '../data/client.js';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import { SearchResult } from '../components/SearchResult.jsx';
import { Users } from '../components/Users.jsx';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

const example_record = {
  Authors: 'J.K. Rowling',
  'Count of text reviews': '12',
  CountsOfReview: '12',
  Description:
    "A fabulous opportunity to own all seven Harry Potter titles - Harry Potter and the Philosopher's Stone, Harry Potter and the Chamber of Secrets, Harry Potter and the Prisoner of Azkaban, Harry Potter and the Goblet of Fire, Harry Potter and the Order of the Phoenix, Harry Potter and the Half-Blood Prince and Harry Potter and the Deathly Hallows- in a fantastic boxed set.",
  ISBN: '0747593698',
  Id: '988373',
  Language: 'en-GB',
  Name: 'Complete Harry Potter Boxed Set',
  PublishDay: '10',
  PublishMonth: '1',
  PublishYear: '2007',
  Publisher: 'Bloomsbury Publishing',
  Rating: '4.74',
  RatingDist1: '1:1549',
  RatingDist2: '2:1634',
  RatingDist3: '3:8190',
  RatingDist4: '4:35392',
  RatingDist5: '5:197903',
  RatingDistTotal: 'total:244668',
  pagesNumber: '3421',
};

const App = () => {
  const [queryString, setQueryString] = useState('');
  const [results, setResults] = useState([]);
  const [customQuery, setCustomQuery] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page-reload
    setResults([]);
    if (queryString !== '') {
      search(currentUser.id, queryString, customQuery, function (v) {
        setResults(v);
      });
    }
  };

  return (
    <div style={{ display: 'flex', margin: '0 32px', justifyContent: 'space-between' }}>
      <div style={{ width: '70%' }}>
        <h1>Google has got nothing on us!</h1>
        <p>
          Use custom query: {customQuery ? 'Yes' : 'No'}
          <button onClick={() => setCustomQuery((v) => !v)}>Toggle Query Type</button>
        </p>
        <form onSubmit={(e) => handleSubmit(e)} style={{ display: 'flex' }}>
          <TextField
            id='query'
            label='Search...'
            onChange={(e) => {
              setResults([]);
              setQueryString(e.target.value);
            }}
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
                <SearchResult
                  currentUser={currentUser.id}
                  id={obj.id}
                  data={obj.dataMap}
                  score={obj.score}
                  is_read={obj.isRead}
                  rating={obj.rating}
                  pos={i}
                />
              </div>
            );
          })}
        </ul>
      </div>
      <Card style={{ width: '25%' }}>
        <CardContent>
          <h2 style={{ margin: 0 }}>
            Current user: {currentUser?.name} ({currentUser?.id})
          </h2>
          <Users setCurrentUser={(name) => setCurrentUser(name)} />
        </CardContent>
      </Card>
    </div>
  );
};

export default App;

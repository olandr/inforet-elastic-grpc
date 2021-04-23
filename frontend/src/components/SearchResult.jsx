import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Rating from '@material-ui/lab/Rating';
import { setRateBook, setReadBook } from '../data/client';

const useStyles = makeStyles((theme) => ({
  root: {
    margin: '8px',
  },
  read: {
    backgroundColor: 'lightblue',
    opacity: '80%',
  },
}));

export const SearchResult = (props) => {
  const classes = useStyles();
  const [rating, setRating] = useState(null);

  const handleRateBook = () => {
    let usageData = {
      userID: props.currentUser,
      documentID: props.data['Id'],
      rating: rating,
    };
    setRateBook(usageData);
  };

  const handleReadBook = () => {
    let usageData = {
      userID: props.currentUser,
      documentID: props.data['Id'],
      is_read: true,
    };
    setReadBook(usageData);
  };

  return (
    <Card className={`${classes.root} ${props.read ? classes.read : ''}`}>
      <CardContent style={{ display: 'flex', justifyContent: 'space-between' }}>
        <div style={{ width: '50%' }}>
          <div style={{ display: 'flex' }}>
            <h3 style={{ margin: '0' }}>{props.data['Name']}</h3>
            <p style={{ margin: '0 16px' }}>by {props.data['Authors']}</p>
          </div>

          <div>
            <h4 style={{ margin: '0' }}>Info</h4>
            <p>Score: {props.score.toFixed(2)}</p>
            <p>Language: {props.data['Language'] ? props.data['Language'] : 'unknown'}</p>
          </div>

          <div>{props.data['Description']}</div>
        </div>
      </CardContent>
      <CardActions>
        <Button size='small' onClick={() => handleReadBook()}>
          Read
        </Button>
        <Rating name={props.data['Id']} value={rating} onChange={(_, r) => handleRateBook()} />
      </CardActions>
    </Card>
  );
};
// FIXME: removing this temporarily to keep under any potential quota limits
//<img src={`http://covers.openlibrary.org/b/ISBN/${props.data['ISBN']}-M.jpg`} />

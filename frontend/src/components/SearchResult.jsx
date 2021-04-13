import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Rating from '@material-ui/lab/Rating';

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

  return (
    <Card className={`${classes.root} ${props.read ? classes.read : ''}`}>
      <CardContent style={{ display: 'flex', justifyContent: 'space-between' }}>
        <div style={{ width: '50%' }}>
          <div style={{ display: 'flex' }}>
            <h3 style={{ margin: '0' }}>{props.data['Name']}</h3>
            <p style={{ margin: '0 16px' }}>by {props.data['Authors']}</p>
          </div>
          <div>{props.data['Description']}</div>
        </div>
        <img src={`http://covers.openlibrary.org/b/ISBN/${props.data['ISBN']}-M.jpg`} />
      </CardContent>
      <CardActions>
        <Button size='small'>Read</Button>
        <Rating name={props.data['Id']} value={rating} onChange={(_, r) => setRating(r)} />
      </CardActions>
    </Card>
  );
};

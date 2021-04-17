import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

const useStyles = makeStyles((theme) => ({
  root: {
    margin: '8px',
  },
}));

export const Users = (props) => {
  const classes = useStyles();
  const [newUser, setNewUser] = useState(null);
  const uv = ['olandr', 'lembeye', 'bosch', 'lindstrand'];

  return (
    <>
      <div>
        <List>
          {uv.map((e, i) => (
            <User key={i} data={e} handleClick={() => props.setCurrentUser(e)} />
          ))}
        </List>
        <Button
          variant='outlined'
          style={{ color: '#FFF', backgroundColor: '#4285F4' }}
          onClick={() => setNewUser(true)}
        >
          Create new user{' '}
        </Button>
        {newUser && <UserForm />}
      </div>
    </>
  );
};

const User = (props) => {
  return (
    <ListItem button onClick={props.handleClick}>
      <ListItemText>{props.data}</ListItemText>
    </ListItem>
  );
};

const UserForm = () => {
  const [name, setName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page-reload
    if (name !== '') {
      console.log('new user:', name);
    }
  };

  return (
    <>
      <form onSubmit={(e) => handleSubmit(e)} style={{ display: 'flex' }}>
        <TextField
          id='name'
          label='Name'
          onChange={(e) => setName(e.target.value)}
          style={{ width: '100%', paddingRight: '8px' }}
        ></TextField>
        <Button
          type='submit'
          variant={'contained'}
          value='Submit'
          style={{ color: '#FFF', backgroundColor: '#4285F4' }}
        >
          Save
        </Button>
      </form>
    </>
  );
};

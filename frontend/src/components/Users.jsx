import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import { createUser, autoCreateUser } from '../data/client.js';

const useStyles = makeStyles((theme) => ({
  root: {
    margin: '8px',
  },
}));

export const Users = (props) => {
  const classes = useStyles();
  const [newUser, setNewUser] = useState(null);
  const [users, setUsers] = useState([]);

  const handleAutoSignup = () => {
    setUsers([]);
    autoCreateUser(function (v) {
      setUsers((prev) => [...prev, v]);
    });
  };

  const handleNewUser = (id, name) => {
    let user = {
      id: id,
      name: name,
    };
    setUsers((prev) => [...prev, user]);
  };

  return (
    <>
      <div>
        <List>
          {users.map((e, i) => (
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

        <Button variant='outlined' style={{ color: '#FFF', backgroundColor: '#DB4437' }} onClick={handleAutoSignup}>
          Auto create users{' '}
        </Button>
        {newUser && <UserForm addToList={(name, id) => handleNewUser(name, id)} />}
      </div>
    </>
  );
};

const User = (props) => {
  return (
    <ListItem button onClick={props.handleClick}>
      <ListItemText>{props.data.name}</ListItemText>
    </ListItem>
  );
};

const UserForm = (props) => {
  const [name, setName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page-reload
    if (name !== '') {
      console.log('new user:', name);
      createUser(
        {
          name: name,
        },
        (id, n) => props.addToList(id, n)
      );
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

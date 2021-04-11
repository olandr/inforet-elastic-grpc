import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';

const valid_languages = [
  'Swedish',
  'English',
  'German',
  'Spanish',
  'French',
  'Chinese',
  'Japanese',
  'Korean',
  'Hindi',
  'Danish',
  'Norwegian',
];

const valid_topics = [
  'Documentary',
  'Thriller',
  'Comedy',
  'Romance',
  'Adventure',
  'Mystery',
  'Short',
  'Crime',
  'Magic',
  'Teen',
];

const useStyles = makeStyles((theme) => ({
  root: {
    minWidth: 200,
    padding: '4px',
  },
  small: {
    minWidth: 200,
  },
}));

export const Profile = () => {
  const classes = useStyles();
  const [name, setName] = useState('');
  const [languages, setLanguages] = useState([]);
  const [topics, setTopics] = useState([]);
  const [age, setAge] = useState(0);
  const [sex, setSex] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(name, languages, topics, age, sex);
  };

  return (
    <div id='profile-box' style={{ width: '600px' }}>
      <form id='profile-settings' onSubmit={handleSubmit}>
        <Button
          type='submit'
          value='Submit'
          variant={'contained'}
          style={{ color: '#FFF', backgroundColor: '#4285F4' }}
        >
          Save
        </Button>
        <div style={{ width: '100%', backgroundColor: '#E6E6E6' }}>
          <TextField
            id='name'
            label='Name'
            onChange={(e) => setName(e.target.value)}
            style={{ width: '200px' }}
          ></TextField>
          <TextField
            id='age'
            label='Age'
            onChange={(e) => setAge(e.target.value)}
            style={{ width: '100px' }}
          ></TextField>
          <FormControl style={{ width: '100px' }}>
            <InputLabel id='sex'>Sex</InputLabel>
            <Select labelId='sex' name='sex' value={sex} onChange={(e) => setSex(e.target.value)}>
              <MenuItem value='M'>Male</MenuItem>
              <MenuItem value='F'>Female</MenuItem>
              <MenuItem value='O'>Other</MenuItem>
            </Select>
          </FormControl>
        </div>
        <div style={{ width: '100%', backgroundColor: '#FAFAFA' }}>
          <FormControl className={classes.root} style={{ color: '#000' }}>
            <FormLabel id='languages'>Languages</FormLabel>
            {valid_languages.map((e, i) => (
              <FormControlLabel
                key={i}
                control={
                  <Checkbox
                    color={'default'}
                    name={e.toLocaleLowerCase()}
                    onChange={() => setLanguages((p) => [...p, e])}
                  />
                }
                label={e}
              />
            ))}
          </FormControl>
          <FormControl className={classes.root} style={{ color: '#000' }}>
            <FormLabel id='topics'>Topics</FormLabel>
            {valid_topics.map((e, i) => (
              <FormControlLabel
                key={i}
                control={
                  <Checkbox
                    color={'default'}
                    name={e.toLocaleLowerCase()}
                    onChange={() => setTopics((p) => [...p, e])}
                  />
                }
                label={e}
              />
            ))}
          </FormControl>
        </div>
      </form>
    </div>
  );
};

import React, { useEffect, useState } from 'react';
import './profile.scss';
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
  formControl: {
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
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
    <div id='profile-box'>
      <form id='profile-settings' onSubmit={handleSubmit}>
        <Button type='submit' value='Submit'>
          Save
        </Button>
        <TextField id='name' label='Name' onChange={(e) => setName(e.target.value)}></TextField>
        <TextField id='age' label='Age' onChange={(e) => setAge(e.target.value)}></TextField>
        <FormControl className={classes.formControl}>
          <InputLabel id='sex'>Sex</InputLabel>
          <Select labelId='sex' name='sex' value={sex} onChange={(e) => setSex(e.target.value)}>
            <MenuItem value='M'>Male</MenuItem>
            <MenuItem value='F'>Female</MenuItem>
            <MenuItem value='O'>Other</MenuItem>
          </Select>
        </FormControl>
        <FormControl className={classes.formControl}>
          <FormLabel id='languages'>Languages</FormLabel>
          {valid_languages.map((e, i) => (
            <FormControlLabel
              key={i}
              control={<Checkbox name={e.toLocaleLowerCase()} onChange={() => setLanguages((p) => [...p, e])} />}
              label={e}
            />
          ))}
        </FormControl>
        <FormControl className={classes.formControl}>
          <FormLabel id='topics'>Topics</FormLabel>
          {valid_topics.map((e, i) => (
            <FormControlLabel
              key={i}
              control={<Checkbox name={e.toLocaleLowerCase()} onChange={() => setTopics((p) => [...p, e])} />}
              label={e}
            />
          ))}
        </FormControl>
      </form>
    </div>
  );
};

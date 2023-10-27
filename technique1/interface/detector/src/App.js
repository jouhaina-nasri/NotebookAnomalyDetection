import React, { useState } from 'react';
import axios from 'axios';
import { Button, LinearProgress, Typography, Paper, Container, Dialog, DialogTitle, DialogContent, DialogActions } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',  // Centre les éléments horizontalement
  },
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
  }
}));

const App = () => {
  const classes = useStyles();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onFileChange = (e) => {
    setFiles(e.target.files);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      setError('Aucun fichier sélectionné.');
      return;
    }
    setLoading(true);
    const formData = new FormData();
    
    for (let i = 0; i < files.length; i++) {
      formData.append('notebook_files', files[i]);
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob' // important
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'results.csv');
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      setError('Une erreur s’est produite pendant l’analyse.');
    } finally {
      setLoading(false);
    }
  };
  const handleClose = () => {
    setError(null);
  };
  return (
    <Container component="main" maxWidth="xs" className={classes.root}>
      <CssBaseline />
      <Paper elevation={3} className={classes.paper}>
        <Typography variant="h4">Choisissez les fichiers Jupyter Notebook à analyser</Typography>
        <form onSubmit={onSubmit}>
          <input type="file" multiple onChange={onFileChange} accept=".ipynb" />
          <Button type="submit" variant="contained" color="primary">
            Analyser
          </Button>
        </form>
        {loading && <LinearProgress />}
      <Dialog open={!!error} onClose={handleClose}>
        <DialogTitle>Erreur</DialogTitle>
        <DialogContent>
          <Typography variant="body1">{error}</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Quitter
          </Button>
        </DialogActions>
      </Dialog>
      </Paper>
    </Container>
  );
};

export default App;

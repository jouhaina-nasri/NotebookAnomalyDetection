import React, { useState } from 'react';
import axios from 'axios';
import {
  Alert,
  Box,
  Button,
  Chip,
  Container,
  LinearProgress,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import { parseReport } from './csv';

export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';

export default function App() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [report, setReport] = useState(null);

  const onFileChange = (e) => {
    setFiles(Array.from(e.target.files));
    setReport(null);
    setError(null);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      setError('Aucun fichier sélectionné.');
      return;
    }
    const formData = new FormData();
    files.forEach((file) => formData.append('notebook_files', file));

    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/analyze`, formData, { responseType: 'text' });
      setReport({ csv: response.data, ...parseReport(response.data) });
    } catch (err) {
      setError("Une erreur s'est produite pendant l'analyse.");
    } finally {
      setLoading(false);
    }
  };

  const download = () => {
    const url = URL.createObjectURL(new Blob([report.csv], { type: 'text/csv' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'results.csv';
    link.click();
    URL.revokeObjectURL(url);
  };

  const smellyRows = report ? report.rows.filter((row) => row.smells.length > 0) : [];

  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Notebook Smell Detector
        </Typography>
        <Typography color="text.secondary" sx={{ mb: 3 }}>
          Choisissez les fichiers Jupyter Notebook à analyser.
        </Typography>

        <Box component="form" onSubmit={onSubmit}>
          <Stack direction="row" spacing={2} alignItems="center">
            <Button variant="outlined" component="label">
              Choisir des fichiers
              <input
                hidden
                type="file"
                multiple
                accept=".ipynb"
                aria-label="notebooks"
                onChange={onFileChange}
              />
            </Button>
            <Typography variant="body2" color="text.secondary">
              {files.length === 0 ? 'Aucun fichier' : files.map((f) => f.name).join(', ')}
            </Typography>
          </Stack>
          <Button type="submit" variant="contained" sx={{ mt: 3 }} disabled={loading}>
            Analyser
          </Button>
        </Box>

        {loading && <LinearProgress sx={{ mt: 3 }} />}
        {error && (
          <Alert severity="error" sx={{ mt: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {report && (
          <Box sx={{ mt: 4 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
              <Typography variant="h6">
                {smellyRows.length} cellule(s) avec des smells sur {report.rows.length} analysée(s)
              </Typography>
              <Button onClick={download}>Télécharger le CSV</Button>
            </Stack>
            {smellyRows.length > 0 && (
              <Table size="small" sx={{ mt: 2 }}>
                <TableHead>
                  <TableRow>
                    <TableCell>Notebook</TableCell>
                    <TableCell>Cellule</TableCell>
                    <TableCell>Smells</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {smellyRows.map((row) => (
                    <TableRow key={`${row.file}-${row.cell}`}>
                      <TableCell>{row.file}</TableCell>
                      <TableCell>{row.cell}</TableCell>
                      <TableCell>
                        <Stack direction="row" spacing={1}>
                          {row.smells.map((smell) => (
                            <Chip key={smell} label={smell} size="small" color="warning" />
                          ))}
                        </Stack>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </Box>
        )}
      </Paper>
    </Container>
  );
}

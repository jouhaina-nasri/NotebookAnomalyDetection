import React from 'react';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import { afterEach, describe, expect, it, vi } from 'vitest';
import App, { API_URL } from './App';
import { parseReport } from './csv';

vi.mock('axios');

const CSV = [
  'File,Cell,Long Cell,Long Element Chain,Complex Container Comprehension,Long Expression,Complex IF-Conditional',
  'train.ipynb,1,0,0,0,0,0',
  'train.ipynb,4,1,0,0,1,0',
  '"a, b.ipynb",2,0,1,0,0,0',
].join('\n');

describe('parseReport', () => {
  it('maps each row to the smells flagged with 1', () => {
    const { smells, rows } = parseReport(CSV);
    expect(smells).toHaveLength(5);
    expect(rows[0]).toEqual({ file: 'train.ipynb', cell: 1, smells: [] });
    expect(rows[1].smells).toEqual(['Long Cell', 'Long Expression']);
    expect(rows[2]).toEqual({ file: 'a, b.ipynb', cell: 2, smells: ['Long Element Chain'] });
  });
});

describe('App', () => {
  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it('shows an error when no file is selected', async () => {
    render(<App />);
    await userEvent.click(screen.getByRole('button', { name: 'Analyser' }));
    expect(screen.getByText('Aucun fichier sélectionné.')).toBeInTheDocument();
    expect(axios.post).not.toHaveBeenCalled();
  });

  it('uploads notebooks and lists the smelly cells', async () => {
    axios.post.mockResolvedValue({ data: CSV });
    render(<App />);

    const file = new File(['{}'], 'train.ipynb', { type: 'application/json' });
    await userEvent.upload(screen.getByLabelText('notebooks'), file);
    await userEvent.click(screen.getByRole('button', { name: 'Analyser' }));

    expect(axios.post).toHaveBeenCalledWith(`${API_URL}/analyze`, expect.any(FormData), expect.anything());
    expect(await screen.findByText(/2 cellule\(s\) avec des smells sur 3/)).toBeInTheDocument();
    expect(screen.getByText('Long Expression')).toBeInTheDocument();
  });

  it('reports API failures', async () => {
    axios.post.mockRejectedValue(new Error('network'));
    render(<App />);
    await userEvent.upload(screen.getByLabelText('notebooks'), new File(['{}'], 'x.ipynb'));
    await userEvent.click(screen.getByRole('button', { name: 'Analyser' }));
    expect(await screen.findByText(/erreur/)).toBeInTheDocument();
  });
});

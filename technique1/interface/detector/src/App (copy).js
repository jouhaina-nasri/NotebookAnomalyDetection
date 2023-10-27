import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [files, setFiles] = useState([]);

  const onFileChange = (e) => {
    setFiles(e.target.files);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    
    for (let i = 0; i < files.length; i++) {
      formData.append('notebook_files', files[i]);
    }

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
  };

  return (
    <div>
      <h1>Choisissez les fichiers Jupyter Notebook à analyser</h1>
      <form onSubmit={onSubmit}>
        <input type="file" multiple onChange={onFileChange} />
        <button type="submit">Analyser</button>
      </form>
    </div>
  );
};

export default App;


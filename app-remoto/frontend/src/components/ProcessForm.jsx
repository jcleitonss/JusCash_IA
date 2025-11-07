import { useState } from 'react';
import { TextField, Button, Box, Typography, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const ProcessForm = ({ onSubmit, loading }) => {
  const [jsonInput, setJsonInput] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    try {
      const processo = JSON.parse(jsonInput);
      onSubmit(processo);
    } catch (err) {
      setError('JSON inválido. Verifique a formatação.');
    }
  };

  const exampleJson = `{
  "numeroProcesso": "0001234-56.2023.4.05.8100",
  "classe": "Cumprimento de Sentença",
  "orgaoJulgador": "19ª VARA FEDERAL",
  "esfera": "Federal",
  "documentos": [...],
  "movimentos": [...]
}`;

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Typography variant="h6" gutterBottom>
        Dados do Processo (JSON)
      </Typography>
      
      <TextField
        fullWidth
        multiline
        rows={12}
        value={jsonInput}
        onChange={(e) => setJsonInput(e.target.value)}
        placeholder={exampleJson}
        error={!!error}
        helperText={error}
        disabled={loading}
        sx={{ mb: 2 }}
      />

      <Button
        type="submit"
        variant="contained"
        size="large"
        fullWidth
        disabled={loading || !jsonInput}
        endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
      >
        {loading ? 'Verificando...' : 'Verificar Processo'}
      </Button>
    </Box>
  );
};

export default ProcessForm;

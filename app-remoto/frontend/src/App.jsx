import { useState } from 'react';
import { Container, Paper, Typography, Box, Alert, Grid, IconButton, Fade, Chip } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import CloseIcon from '@mui/icons-material/Close';
import CloudIcon from '@mui/icons-material/Cloud';
import ProcessForm from './components/ProcessForm';
import ResultCard from './components/ResultCard';
import { verificarProcesso } from './services/api';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2cbd62',
      light: '#5cd88a',
      dark: '#1fa04d',
    },
    secondary: {
      main: '#1976d2',
    },
    background: {
      default: '#f5f7fa',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  },
  shape: {
    borderRadius: 12,
  },
});

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleVerificar = async (processo) => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await verificarProcesso(processo);
      setResult(data);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Erro ao verificar processo. Verifique a conexão com a API.';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleClearResult = () => {
    setResult(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%)',
          py: 4,
        }}
      >
        <Container maxWidth="xl">
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Typography 
              variant="h3" 
              fontWeight="bold"
              sx={{ 
                color: '#2cbd62',
                mb: 1,
                textShadow: '2px 2px 4px rgba(0,0,0,0.1)'
              }}
            >
              🏛️ JUSCRASH
            </Typography>
            <Typography 
              variant="h6" 
              color="text.secondary"
              sx={{ fontWeight: 400, mb: 1 }}
            >
              Verificador Inteligente de Processos Judiciais
            </Typography>
            <Chip 
              icon={<CloudIcon />} 
              label="AWS Serverless" 
              color="primary" 
              size="small"
              variant="outlined"
            />
          </Box>

          {error && (
            <Fade in={!!error}>
              <Alert 
                severity="error" 
                sx={{ mb: 3, maxWidth: 'lg', mx: 'auto' }} 
                onClose={() => setError('')}
              >
                {error}
              </Alert>
            </Fade>
          )}

          <Grid container spacing={3}>
            <Grid item xs={12} md={result ? 6 : 12}>
              <Paper 
                elevation={2} 
                sx={{ 
                  p: 3,
                  height: '100%',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    elevation: 4,
                  }
                }}
              >
                <ProcessForm onSubmit={handleVerificar} loading={loading} />
              </Paper>
            </Grid>

            {result && (
              <Grid item xs={12} md={6}>
                <Fade in={!!result}>
                  <Paper 
                    elevation={2} 
                    sx={{ 
                      p: 3,
                      height: '100%',
                      position: 'relative',
                      transition: 'all 0.3s ease',
                    }}
                  >
                    <IconButton
                      onClick={handleClearResult}
                      sx={{
                        position: 'absolute',
                        top: 8,
                        right: 8,
                        zIndex: 1,
                      }}
                      size="small"
                    >
                      <CloseIcon />
                    </IconButton>
                    <ResultCard result={result} />
                  </Paper>
                </Fade>
              </Grid>
            )}
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;

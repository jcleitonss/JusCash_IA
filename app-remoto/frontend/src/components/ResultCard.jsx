import { Box, Typography, Divider, Zoom } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import WarningIcon from '@mui/icons-material/Warning';
import PolicyBadge from './PolicyBadge';

const ResultCard = ({ result }) => {
  const getDecisionConfig = (decision) => {
    const configs = {
      approved: {
        color: '#2cbd62',
        bgColor: '#e8f5e9',
        icon: <CheckCircleIcon sx={{ fontSize: 60 }} />,
        label: 'APROVADO',
      },
      rejected: {
        color: '#f44336',
        bgColor: '#ffebee',
        icon: <CancelIcon sx={{ fontSize: 60 }} />,
        label: 'REJEITADO',
      },
      incomplete: {
        color: '#ff9800',
        bgColor: '#fff3e0',
        icon: <WarningIcon sx={{ fontSize: 60 }} />,
        label: 'INCOMPLETO',
      },
    };
    return configs[decision] || configs.incomplete;
  };

  const config = getDecisionConfig(result.decision);

  return (
    <Box>
      <Zoom in={true} style={{ transitionDelay: '100ms' }}>
        <Box
          sx={{
            textAlign: 'center',
            py: 3,
            px: 2,
            borderRadius: 3,
            backgroundColor: config.bgColor,
            mb: 3,
          }}
        >
          <Box sx={{ color: config.color, mb: 1 }}>
            {config.icon}
          </Box>
          <Typography 
            variant="h5" 
            fontWeight="bold"
            sx={{ color: config.color }}
          >
            {config.label}
          </Typography>
        </Box>
      </Zoom>

      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" fontWeight="bold" color="text.secondary" gutterBottom>
          JUSTIFICATIVA
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <Typography variant="body1" sx={{ lineHeight: 1.7 }}>
          {result.rationale}
        </Typography>
      </Box>

      <Box>
        <Typography variant="subtitle2" fontWeight="bold" color="text.secondary" gutterBottom>
          POLÍTICAS CITADAS
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {(result.citacoes || []).map((policy, index) => (
            <PolicyBadge key={index} policyId={policy} />
          ))}
        </Box>
      </Box>
    </Box>
  );
};

export default ResultCard;

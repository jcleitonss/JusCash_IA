import { Chip } from '@mui/material';

const PolicyBadge = ({ policyId }) => {
  return (
    <Chip 
      label={policyId} 
      size="small" 
      color="primary" 
      variant="outlined"
      sx={{ m: 0.5 }}
    />
  );
};

export default PolicyBadge;

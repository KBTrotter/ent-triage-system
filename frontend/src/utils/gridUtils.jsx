import React from 'react';
import { Chip, Box } from '@mui/material';
import dayjs from 'dayjs';
import { URGENCY_PRIORITY, URGENCY_LABELS, URGENCY_COLORS } from '../constants/consts';

export const UrgencyCellRenderer = (params) => {
  if (!params.value) return null

  const label = URGENCY_LABELS[params.value];
  const color = URGENCY_COLORS[params.value];

  return (
    <Chip
      label={label}
      size="small"
      sx={{
        backgroundColor: color,
        color: 'white',
        fontWeight: 'bold',
        fontSize: '0.75rem',
      }}
    />
  );
};

export const dateTimeFormatter = (params) => {
  if (!params.value) return '-';
  return dayjs(params.value).format('h:mm A, MM/DD/YYYY');
};

export const urgencyComparator = (a, b) => {
  return URGENCY_PRIORITY[a] - URGENCY_PRIORITY[b];
};
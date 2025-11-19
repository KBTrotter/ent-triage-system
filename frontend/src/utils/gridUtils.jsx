import React from 'react';
import { Chip, IconButton } from '@mui/material';
import { Edit } from "@mui/icons-material";
import dayjs from 'dayjs';
import { URGENCY_PRIORITY, URGENCY_LABELS, URGENCY_COLORS } from '../utils/consts';

export const UrgencyCellRenderer = (params) => {
  if (!params.value) return null

  const label = URGENCY_LABELS[params.value];
  const color = URGENCY_COLORS[params.value];

  return (
    <Chip
      label={label}
      size="medium"
      sx={{
        backgroundColor: color,
        color: 'white',
        fontWeight: 'bold',
        fontSize: '0.75rem',
      }}
    />
  );
};

export const EditButtonCellRenderer = (params) => {
  const handleEdit = () => {
    // open modal here.... and things....
    console.log('Edit clicked for:', params.data);
  };

  return (
    <IconButton
      onClick={handleEdit}
      size="medium"
    >
      <Edit />
    </IconButton>
  );
};

export const ageValueGetter = (dob) => {
  if (!dob) return null;
  return dayjs().diff(dayjs(dob), 'year');
}

export const dateTimeFormatter = (params) => {
  if (!params.value) return '-';
  return dayjs(params.value).format('h:mm A, MM/DD/YYYY');
};

export const urgencyComparator = (a, b) => {
  return URGENCY_PRIORITY[a] - URGENCY_PRIORITY[b];
};
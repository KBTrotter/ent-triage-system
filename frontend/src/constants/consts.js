import { red, green, amber } from '@mui/material/colors';

// this should reflect how these enums are stored in db
export const URGENCY_VALUES = {
  ROUTINE: 'routine',
  SEMI_URGENT: 'semi_urgent',
  URGENT: 'urgent',
};

// this should reflect how these enums are stored in db
export const STATUS_VALUES = {
  PENDING: 'pending',
  RESOLVED: 'resolved',
};

export const STATUS_LABELS = {
  [STATUS_VALUES.PENDING]: 'Pending',
  [STATUS_VALUES.RESOLVED]: 'Resolved',
};

export const URGENCY_LABELS = {
  [URGENCY_VALUES.ROUTINE]: 'Routine',
  [URGENCY_VALUES.SEMI_URGENT]: 'Semi-Urgent',
  [URGENCY_VALUES.URGENT]: 'Urgent',
};

export const URGENCY_COLORS = {
  [URGENCY_VALUES.ROUTINE]: green[800],
  [URGENCY_VALUES.SEMI_URGENT]: amber[800],
  [URGENCY_VALUES.URGENT]: red[800],
};

export const URGENCY_PRIORITY = {
  [URGENCY_VALUES.URGENT]: 1,
  [URGENCY_VALUES.SEMI_URGENT]: 2,
  [URGENCY_VALUES.ROUTINE]: 3,
};
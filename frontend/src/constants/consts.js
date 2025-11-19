// this should reflect how these enums are stored in db
export const URGENCY_VALUES = {
  ROUTINE: 'routine',
  SEMI_URGENT: 'semi_urgent',
  URGENT: 'urgent',
};

export const URGENCY_LABELS = {
  [URGENCY_VALUES.ROUTINE]: 'Routine',
  [URGENCY_VALUES.SEMI_URGENT]: 'Semi-Urgent',
  [URGENCY_VALUES.URGENT]: 'Urgent',
};

export const URGENCY_COLORS = {
  [URGENCY_VALUES.ROUTINE]: '#4CAF50',
  [URGENCY_VALUES.SEMI_URGENT]: '#FF9800',
  [URGENCY_VALUES.URGENT]: '#F44336',
};

export const URGENCY_PRIORITY = {
  [URGENCY_VALUES.URGENT]: 1,
  [URGENCY_VALUES.SEMI_URGENT]: 2,
  [URGENCY_VALUES.ROUTINE]: 3,
};
import React from "react";
import { Chip, IconButton } from "@mui/material";
import { Edit } from "@mui/icons-material";
import dayjs from "dayjs";
import {
  URGENCY_PRIORITY,
  URGENCY_LABELS,
  URGENCY_COLORS,
} from "../utils/consts";
import CaseDetailsDialog from "../components/caseDetails/CaseDetailsDialog";

export const UrgencyCellRenderer = (params) => {
  if (!params.value) return null;

  const label = URGENCY_LABELS[params.value];
  const color = URGENCY_COLORS[params.value];

  return (
    <Chip
      label={label}
      size="medium"
      sx={{
        backgroundColor: color,
        color: "white",
        fontWeight: "bold",
        fontSize: "0.75rem",
      }}
    />
  );
};

export const EditButtonCellRenderer = (params) => {
  const [open, setOpen] = React.useState(false);
  const [caseData, setCaseData] = React.useState(null);
  const handleOpen = () => {
    setCaseData(params.data);
    setOpen(true);
  };
  const handleClose = () => setOpen(false);
  const handleSave = (updatedData) => {
    console.log("Saved data:", updatedData);
    handleClose();
  };

  return (
    <>
      <IconButton onClick={handleOpen} size="medium">
        <Edit />
      </IconButton>
      <CaseDetailsDialog
        open={open}
        onClose={handleClose}
        caseData={caseData}
        onSave={handleSave}
      />
    </>
  );
};

export const ageValueGetter = (dob) => {
  if (!dob) return null;
  return dayjs().diff(dayjs(dob), "year");
};

export const dateTimeFormatter = (params) => {
  if (!params.value) return "-";
  return dayjs(params.value).format("h:mm A, MM/DD/YYYY");
};

export const urgencyComparator = (a, b) => {
  return URGENCY_PRIORITY[a] - URGENCY_PRIORITY[b];
};

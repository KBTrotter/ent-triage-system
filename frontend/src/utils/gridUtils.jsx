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
import EditUserDialog from "../components/admin/EditUserDialog";
import { useTriageCases } from "../context/TriageCaseContext";
import { showToast } from "../utils/toast";

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

export const EditCaseButtonCellRenderer = (params) => {
  const [open, setOpen] = React.useState(false);
  const [saving, setSaving] = React.useState(false);
  
  const { updateCase, resolveCase } = useTriageCases();
  const caseData = params.data;

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

// utils/cellRenderers.jsx
const handleSave = async (updatedData) => {
  setSaving(true);
  
  try {
    if (updatedData.status === "resolved") {
      await resolveCase(caseData.case_id, updatedData.resolutionReason);
      showToast("Case resolved successfully!", "success");
    } else {
      await updateCase(caseData.case_id, updatedData);
      showToast("Case updated successfully!", "success");
    }

    handleClose();
  } catch (error) {
    console.error("Failed to update case:", error);
    showToast(error.message || "Failed to update case. Please try again.", "error");
  } finally {
    setSaving(false);
  }
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
        saving={saving}
      />
    </>
  );
};

export const EditUserButtonCellRenderer = (params) => {
  const [open, setOpen] = React.useState(false);
  const userData = params.data;
  
  const handleOpen = () => {
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
      <EditUserDialog
        open={open}
        onClose={handleClose}
        userData={userData}
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
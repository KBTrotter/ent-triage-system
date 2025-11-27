import React, { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  Typography,
} from "@mui/material";
import RenderTextField from "../fields/RenderTextField";
import RenderSelectField from "../fields/RenderSelectField";

const USER_ROLE_OPTIONS = [
  { value: "Physician", label: "Physician" },
  { value: "Staff", label: "Staff" },
  { value: "Admin", label: "Admin" },
];

export default function EditUserDialog({ open, onClose, userData, onSave }) {
  const [editMode, setEditMode] = useState(false);

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
      first_name: userData?.first_name || "",
      last_name: userData?.last_name || "",
      email: userData?.email || "",
      role: userData?.role || "",
    },
    validationSchema: Yup.object({
      first_name: Yup.string().required("First name is required"),
      last_name: Yup.string().required("Last name is required"),
      email: Yup.string()
        .email("Invalid email address")
        .required("Email is required"),
      role: Yup.string().required("Role is required"),
    }),
    onSubmit: (values) => {
      onSave(values);
      setEditMode(false);
    },
  });

  const handleClose = () => {
    setEditMode(false);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>User Details</DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid size={6}>
            <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
              First Name
            </Typography>
            <RenderTextField
              editMode={editMode}
              formik={formik}
              fieldName="first_name"
            />
          </Grid>
          <Grid size={6}>
            <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
              Last Name
            </Typography>
            <RenderTextField
              editMode={editMode}
              formik={formik}
              fieldName="last_name"
            />
          </Grid>
          <Grid size={12}>
            <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
              Email
            </Typography>
            <RenderTextField
              editMode={editMode}
              formik={formik}
              fieldName="email"
              type="email"
            />
          </Grid>
          <Grid size={12}>
            <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
              Role
            </Typography>
            <RenderSelectField
              editMode={editMode}
              formik={formik}
              fieldName="role"
              options={USER_ROLE_OPTIONS}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        {editMode ? (
          <>
            <Button onClick={() => setEditMode(false)}>Cancel</Button>
            <Button onClick={formik.handleSubmit} variant="contained">
              Save
            </Button>
          </>
        ) : (
          <>
            <Button onClick={() => setEditMode(true)} variant="contained">
              Edit
            </Button>
            <Button onClick={handleClose}>Close</Button>
          </>
        )}
      </DialogActions>
    </Dialog>
  );
}
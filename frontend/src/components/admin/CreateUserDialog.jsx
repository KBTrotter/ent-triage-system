import React from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
} from "@mui/material";
import RenderTextField from "../fields/RenderTextField";
import RenderSelectField from "../fields/RenderSelectField";

const USER_ROLE_OPTIONS = [
  { value: "physician", label: "Physician" },
  { value: "staff", label: "Staff" },
  { value: "admin", label: "Admin" },
];

export default function CreateUserDialog({ open, onClose, onSave }) {
  const formik = useFormik({
    initialValues: {
      firstName: "",
      lastName: "",
      email: "",
      role: "",
    },
    validationSchema: Yup.object({
      firstName: Yup.string().required("First name is required"),
      lastName: Yup.string().required("Last name is required"),
      email: Yup.string()
        .email("Invalid email address")
        .required("Email is required"),
      role: Yup.string().required("Role is required"),
    }),
    onSubmit: (values) => {
      onSave(values);
      formik.resetForm();
    },
  });

  const handleClose = () => {
    formik.resetForm();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Create New User</DialogTitle>
      <DialogContent>
        <Box mt={2} display="flex" flexDirection="column" gap={2}>
          <RenderTextField
            editMode={true}
            formik={formik}
            fieldName="firstName"
            label="First Name"
          />
          <RenderTextField
            editMode={true}
            formik={formik}
            fieldName="lastName"
            label="Last Name"
          />
          <RenderTextField
            editMode={true}
            formik={formik}
            fieldName="email"
            label="Email"
            type="email"
          />
          <RenderSelectField
            editMode={true}
            formik={formik}
            fieldName="role"
            label="Role"
            options={USER_ROLE_OPTIONS}
          />
          <Typography variant="caption" color="textSecondary" sx={{ mt: 1 }}>
            An invitation email with login credentials will be sent to the user.
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={formik.handleSubmit} variant="contained">
          Create User
        </Button>
      </DialogActions>
    </Dialog>
  );
}

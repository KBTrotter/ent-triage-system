import React, { useEffect, useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { useAuth } from "../../context/AuthContext";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Grid,
  Typography,
} from "@mui/material";
import RenderTextField from "../fields/RenderTextField";
import RenderSelectField from "../fields/RenderSelectField";
import ResolveCaseDialog from "./ResolveCaseDialog";
import {
  URGENCY_VALUES,
  URGENCY_LABELS,
  RETURNING_PATIENT_OPTIONS,
} from "../../utils/consts";

export default function CaseDetailsDialog({ open, onClose, caseData, onSave }) {
  const [formData, setFormData] = useState({});
  const [editMode, setEditMode] = useState(false);
  const [resolveMode, setResolveMode] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    if (caseData) {
      setFormData(caseData);
    }
  }, [caseData]);

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
      patientFirstName: formData.first_name || "",
      patientLastName: formData.last_name || "",
      patientDOB: formData.dob || "",
      patientContact: formData.contactInfo || "",
      returningPatient: formData.returningPatient ?? false,
      caseUrgency: formData.urgencyLevel || "",
      patientInsurance: formData.insuranceInfo || "Not Provided",
      aiSummary: formData.aiSummary || "",
      overrideSummary: formData.overrideSummary || "",
      clinicNotes: formData.clinicianSummary || "",
      caseResolutionReason: formData.resolutionReason || "",
      resolvedBy: formData.resolvedBy || "",
    },
    validationSchema: Yup.object({
      patientFirstName: Yup.string().required("Name is required"),
      patientLastName: Yup.string().required("Name is required"),
      patientDOB: Yup.string().required("DOB is required"),
      patientContact: Yup.string(),
      patientInsurance: Yup.string(),
      overrideSummary: Yup.string(),
      clinicNotes: Yup.string(),
      caseUrgency: Yup.string().required("Case urgency is required"),
      caseResolutionReason: Yup.string().when("status", {
        is: "resolved",
        then: (schema) => schema.required("Resolution reason is required"),
      }),
      resolvedBy: Yup.string().when("status", {
        is: "resolved",
        then: (schema) => schema.required("Resolved by is required"),
      }),
    }),
    onSubmit: (values) => {
      onSave(values);
      setEditMode(false);
    },
  });

  const handleOpenResolve = () => {
    formik.setFieldValue("resolvedBy", user?.username || "");
    setResolveMode(true);
  };

  // Fields: Patient Name, DOB, Contact Info, Insurance Info, AiSummary, Override Summary, Clinician Notes
  // Dropdowns: Urgency Level, Returning Patient (Yes/No)

  return (
    <>
      <Dialog
        open={open}
        onClose={(_, reason) => {
          if (reason === "backdropClick") return;
          onClose();
        }}
        maxWidth="lg"
        fullWidth>
        <DialogTitle>Case Details</DialogTitle>
        <DialogContent>
          <Grid container spacing={4}>
            <Grid>
              {/* Left side content */}
              <Typography variant="h8">Patient Information</Typography>
              <Box mt={2} display="flex" flexDirection="column" gap={2}>
                <RenderTextField
                  editMode={editMode}
                  formik={formik}
                  fieldName="patientFirstName"
                  label="First Name"
                />
                <RenderTextField
                  editMode={editMode}
                  formik={formik}
                  fieldName="patientLastName"
                  label="Last Name"
                />
                <RenderTextField
                  editMode={editMode}
                  formik={formik}
                  fieldName="patientDOB"
                  label="Date of Birth"
                  type="date"
                />
                <RenderTextField
                  editMode={editMode}
                  formik={formik}
                  fieldName="patientContact"
                  label="Contact Information"
                />
                <RenderTextField
                  editMode={editMode}
                  formik={formik}
                  fieldName="patientInsurance"
                  label="Insurance Info"
                />
                <RenderSelectField
                  editMode={editMode}
                  formik={formik}
                  fieldName="returningPatient"
                  label="Returning Patient"
                  options={RETURNING_PATIENT_OPTIONS}
                />
              </Box>
            </Grid>
            <Box
              sx={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                gap: 2,
              }}>
              {/* Right side content */}
              <Typography variant="h8">Case Information</Typography>
              <Box>
                <Box mb={2}>
                  <RenderSelectField
                    editMode={editMode}
                    formik={formik}
                    fieldName="caseUrgency"
                    label="Case Urgency"
                    options={Object.values(URGENCY_VALUES).map((v) => ({
                      value: v,
                      label: URGENCY_LABELS[v],
                    }))}
                    renderChip
                  />
                </Box>
                <Typography variant="subtitle2" color="textSecondary">
                  AI Summary
                </Typography>
                <Typography variant="body2">
                  {formik.values.aiSummary || "---"}
                </Typography>
              </Box>
              {editMode || formik.values.overrideSummary ? (
                <RenderTextField
                  editMode={editMode}
                  formik={formik}
                  fieldName="overrideSummary"
                  label="Override Summary"
                />
              ) : (
                <Button onClick={() => setEditMode(true)}>
                  Override Summary
                </Button>
              )}
              <Typography variant="h8">Case Notes</Typography>
              <RenderTextField
                editMode={editMode}
                formik={formik}
                fieldName="clinicNotes"
                label="Clinician Notes"
              />

              {caseData?.status === "resolved" && (
                <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                  <Typography variant="h8">Resolution Information</Typography>
                  <RenderTextField
                    editMode={false}
                    formik={formik}
                    fieldName="caseResolutionReason"
                    label="Resolution Reason"
                  />
                  <RenderTextField
                    editMode={false}
                    formik={formik}
                    fieldName="resolvedBy"
                    label="Resolved By"
                  />{" "}
                </Box>
              )}
            </Box>
          </Grid>
        </DialogContent>
        <DialogActions>
          {editMode ? (
            <>
              <Button onClick={formik.handleSubmit} variant="contained">
                Save
              </Button>
              <Button
                onClick={() => {
                  formik.resetForm();
                  setEditMode(false);
                }}>
                Cancel
              </Button>
            </>
          ) : (
            <>
              <Button onClick={() => setEditMode(true)} variant="contained">
                Edit
              </Button>
              {formData?.status !== "resolved" && (
                <Button onClick={handleOpenResolve}>Resolve</Button>
              )}
              <Button onClick={onClose}>Close</Button>
            </>
          )}
        </DialogActions>
      </Dialog>
      <ResolveCaseDialog
        open={resolveMode}
        onClose={() => setResolveMode(false)}
        initialResolvedBy={user?.username || ""}
        onResolve={(data) => {
          onSave({
            ...caseData,
            resolutionReason: data.resolutionReason,
            resolvedBy: data.resolvedBy,
            status: "resolved",
          });
          setResolveMode(false);
        }}
      />
    </>
  );
}
